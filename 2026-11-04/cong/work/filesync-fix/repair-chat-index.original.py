#!/usr/bin/env python3
"""Rebuild chat indexes using isolated native replay; never start a model turn."""
import argparse
import contextlib
import ctypes
import ctypes.util
import datetime
import hashlib
import json
import os
from pathlib import Path
import queue
import re
import shutil
import sqlite3
import subprocess
import threading
import time
import tempfile


def read_names(root):
    path = root / 'session_index.jsonl'
    if not path.exists():
        return {}
    rows = [json.loads(s) for s in path.read_text(encoding='utf-8-sig').splitlines() if s.strip()]
    names = {}
    for row in sorted(rows, key=lambda x: str(x.get('updated_at', ''))):
        title = row.get('thread_name')
        tid = row.get('id', '')
        if re.fullmatch(r'[0-9a-fA-F-]{36}', tid) and isinstance(title, str) and title.strip():
            names[tid] = title
    return names


def connect_readonly(path):
    return sqlite3.connect(path.resolve().as_uri() + '?mode=ro', uri=True, timeout=10)


def state_database(root):
    paths = list(root.glob('state_*.sqlite'))
    paths.sort(key=lambda p: int(re.search(r'state_(\d+)', p.name)[1]), reverse=True)
    for path in paths:
        with contextlib.closing(connect_readonly(path)) as db:
            if db.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='threads'").fetchone():
                return path
    return None


def session_hashes(root):
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest()
            for folder in ('sessions', 'archived_sessions')
            for p in (root / folder).rglob('*')
            if p.is_file() and (p.name.endswith('.jsonl') or p.name.endswith('.jsonl.zst'))}


def backup(root, destination):
    destination.mkdir(parents=True)
    for path in list(root.glob('state_*.sqlite')) + list(root.glob('thread_history_*.sqlite')) + [root / 'sqlite' / 'codex-dev.db']:
        if not path.exists():
            continue
        target = destination / path.relative_to(root)
        target.parent.mkdir(parents=True, exist_ok=True)
        src = connect_readonly(path)
        dst = sqlite3.connect(str(target))
        try:
            src.backup(dst, pages=256, sleep=0.05)
        finally:
            src.close()
            dst.close()
    path = root / 'session_index.jsonl'
    if path.exists():
        shutil.copy2(str(path), str(destination / path.name))


class AppServer:
    def __init__(self, executable, root):
        if not (root / '.filesync-isolated-home').is_file():
            raise RuntimeError('恢复引擎只能在带隔离标记的临时副本中运行。')
        # Only disposable homes are passed here. Never load live config/auth/MCP servers.
        env = {k: v for k, v in os.environ.items() if not k.startswith('CODEX_')
               and k not in ('OPENAI_API_KEY', 'OPENAI_ACCESS_TOKEN', 'CHATGPT_ACCESS_TOKEN')}
        env['CODEX_HOME'] = str(root)
        self.process = subprocess.Popen([str(executable), 'app-server'], cwd=str(root), env=env,
                                        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.queue = queue.Queue()
        self.sequence = 0
        self.error_tail = []

        def receive():
            for line in self.process.stdout:
                try:
                    self.queue.put(json.loads(line))
                except ValueError:
                    pass

        def drain():
            for line in self.process.stderr:
                self.error_tail.append(line.decode('utf-8', 'replace')[:300])
                self.error_tail = self.error_tail[-5:]

        threading.Thread(target=receive, daemon=True).start()
        threading.Thread(target=drain, daemon=True).start()

    def initialize(self):
        self.call('initialize', {'clientInfo': {'name': 'filesync_chat_restore', 'version': '6.0.0'},
                                'capabilities': {'experimentalApi': True}})
        self.process.stdin.write(b'{"method":"initialized","params":{}}\n')
        self.process.stdin.flush()

    def call(self, method, params):
        if method not in ('initialize', 'thread/list', 'thread/read', 'thread/resume',
                          'thread/unarchive', 'thread/unsubscribe', 'thread/turns/list'):
            raise ValueError('Recovery RPC method is not allowed')
        self.sequence += 1
        seq = self.sequence
        data = {'id': seq, 'method': method, 'params': params}
        self.process.stdin.write((json.dumps(data, ensure_ascii=False) + '\n').encode('utf-8'))
        self.process.stdin.flush()
        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if self.process.poll() is not None and self.queue.empty():
                raise RuntimeError('Codex app-server 已提前退出；请检查客户端安装和 config.toml。')
            try:
                reply = self.queue.get(timeout=0.25)
            except queue.Empty:
                continue
            if reply.get('id') == seq:
                if 'error' in reply:
                    raise RuntimeError(method + ': RPC ' + str(reply['error'].get('code', 'error')))
                return reply.get('result', {})
        raise TimeoutError(method + ' 超时')

    def close(self):
        try:
            self.process.stdin.close()
        except OSError:
            pass
        try:
            self.process.wait(timeout=5)
        except subprocess.TimeoutExpired:
            self.process.terminate()
            self.process.wait(timeout=5)


def find_codex(explicit=None):
    if explicit:
        candidates = [Path(explicit)]
    else:
        base = Path(os.environ.get('LOCALAPPDATA', '')) / 'OpenAI' / 'Codex' / 'bin'
        candidates = sorted(base.glob('*/codex.exe'), key=lambda p: p.stat().st_mtime, reverse=True)
        found = shutil.which('codex.exe') or shutil.which('codex')
        if found:
            candidates.append(Path(found))
    for path in candidates:
        try:
            result = subprocess.run([str(path), '--version'], stdout=subprocess.PIPE,
                                    stderr=subprocess.PIPE, timeout=8)
            if result.returncode == 0 and b'codex' in result.stdout.lower():
                return path
        except (OSError, subprocess.TimeoutExpired):
            pass
    raise RuntimeError('未找到可运行的 Codex 引擎。请先安装并启动一次 Codex，或指定 --codex-exe。')


def indexed_ids(root):
    path = state_database(root)
    if path is None:
        return set()
    with contextlib.closing(connect_readonly(path)) as db:
        return {row[0] for row in db.execute('SELECT id FROM threads')}


def apply_names(root, names):
    path = state_database(root)
    if path is None:
        raise RuntimeError('Codex 未生成聊天索引；原文件保留，请检查客户端版本。')
    with sqlite3.connect(str(path), timeout=10) as db:
        columns = {row[1] for row in db.execute('PRAGMA table_info(threads)')}
        fields = [name for name in ('title', 'name') if name in columns]
        if not fields:
            raise RuntimeError('当前聊天数据库结构不支持标题恢复，未写入标题。')
        assignment = ', '.join(field + '=?' for field in fields)
        for tid, title in names.items():
            db.execute('UPDATE threads SET ' + assignment + ' WHERE id=?', [title] * len(fields) + [tid])
        for tid, title in db.execute('SELECT id,' + fields[0] + ' FROM threads'):
            if tid in names and title != names[tid]:
                raise RuntimeError('聊天标题校验失败，事务已回滚。')
    with contextlib.closing(connect_readonly(path)) as db:
        if db.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
            raise RuntimeError('聊天数据库完整性检查失败，请保留备份。')
    cache = root / 'sqlite' / 'codex-dev.db'
    cache_count = 0
    if cache.exists():
        with sqlite3.connect(str(cache), timeout=10) as db:
            tables = {row[0] for row in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            if 'local_thread_catalog' in tables:
                # Only the local host; remote catalogs can belong to other installations.
                rows = list(db.execute('SELECT host_id,thread_id,display_title FROM local_thread_catalog'))
                for host, tid, old_title in rows:
                    if host == 'local' and tid in names and old_title != names[tid]:
                        db.execute('UPDATE local_thread_catalog SET display_title=? WHERE host_id=? AND thread_id=?',
                                   (names[tid], host, tid))
                        cache_count += 1
                if cache_count and 'local_thread_catalog_metadata' in tables:
                    db.execute('UPDATE local_thread_catalog_metadata SET catalog_revision=catalog_revision+1 WHERE id=1')
    return cache_count


def plain_path(value):
    value = str(value)
    return Path(value[4:] if value.startswith('\\\\?\\') else value)


def database(root, pattern):
    paths = sorted(root.glob(pattern), key=lambda p: int(re.search(r'_(\d+)\.sqlite$', p.name)[1]), reverse=True)
    return paths[0] if paths else None


def db_rows(path, table, tid=None):
    with contextlib.closing(connect_readonly(path)) as db:
        db.row_factory = sqlite3.Row
        if tid is None:
            rows = db.execute('SELECT * FROM ' + table).fetchall()
        else:
            rows = db.execute('SELECT * FROM ' + table + ' WHERE thread_id=?', (tid,)).fetchall()
        return [dict(row) for row in rows]


def copy_database(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    with contextlib.closing(connect_readonly(source)) as src, contextlib.closing(sqlite3.connect(str(target))) as dst:
        src.backup(dst, pages=256, sleep=0.01)


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def raw_paths(root):
    return sorted(p for folder in ('sessions', 'archived_sessions')
                  for p in (root / folder).rglob('*')
                  if p.is_file() and (p.name.endswith('.jsonl') or p.name.endswith('.jsonl.zst')))


def relative_rollout(value, root, files):
    path = plain_path(value)
    try:
        relative = str(path.relative_to(root))
        if relative in files:
            return relative
    except ValueError:
        pass
    # A copied database can still contain the previous machine's absolute path.
    candidates = [name for name in files if Path(name).name in (path.name, path.name + '.zst')]
    if len(candidates) != 1:
        raise RuntimeError('无法唯一匹配聊天原始文件；停止恢复，未猜测会话路径。')
    return candidates[0]


def bind_rollouts(home, original_root, hashes):
    path = state_database(home)
    with contextlib.closing(sqlite3.connect(str(path))) as db:
        for tid, rollout in db.execute('SELECT id,rollout_path FROM threads').fetchall():
            relative = relative_rollout(rollout, original_root, hashes)
            db.execute('UPDATE threads SET rollout_path=? WHERE id=?', (str(home / relative), tid))
        db.commit()


def snapshot(root, home, verify):
    state = state_database(root)
    if state is None:
        raise RuntimeError('请先启动一次 Codex，让客户端创建本机数据库后再恢复。')
    home.mkdir(); verify.mkdir()
    for destination in (home, verify):
        (destination / '.filesync-isolated-home').touch()
    for p in [state] + list(root.glob('thread_history_*.sqlite')):
        copy_database(p, home / p.name)
        copy_database(home / p.name, verify / p.name)
    hashes = {}
    for p in raw_paths(root):
        relative = str(p.relative_to(root)); data = p.read_bytes()
        hashes[relative] = hashlib.sha256(data).hexdigest()
        for destination in (home, verify):
            target = destination / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    if not hashes:
        raise RuntimeError('没有找到聊天原始文件，请先下载聊天记录。')
    for destination in (home, verify):
        bind_rollouts(destination, root, hashes)
    return hashes


def native_history(api, tid, message_sink=None):
    cursor = None; seen = set(); turns = []; items = []
    while True:
        params = {'threadId': tid, 'limit': 100, 'sortDirection': 'asc', 'itemsView': 'full'}
        if cursor:
            params['cursor'] = cursor
        result = api.call('thread/turns/list', params)
        for turn in result.get('data', []):
            turns.append(turn['id'])
            for item in turn.get('items', []):
                items.append([turn['id'], item])
                if message_sink is not None and item.get('type') in ('userMessage', 'agentMessage'):
                    message_sink[(turn['id'], item['id'])] = normalized_message(item, native=True)
        cursor = result.get('nextCursor')
        if not cursor:
            break
        if cursor in seen:
            raise RuntimeError('聊天正文分页游标重复，停止恢复。')
        seen.add(cursor)
    encoded = json.dumps([turns, items], sort_keys=True, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    return {'turns': len(turns), 'items': len(items),
            'users': sum(item['type'] == 'userMessage' for _, item in items),
            'agents': sum(item['type'] == 'agentMessage' for _, item in items),
            'digest': hashlib.sha256(encoded).hexdigest()}


def scan_metadata(api):
    for archived in (False, True):
        cursor = None; seen = set()
        while True:
            params = {'limit': 100, 'archived': archived, 'sourceKinds': ['vscode', 'cli'],
                      'modelProviders': [], 'useStateDbOnly': False}
            if cursor:
                params['cursor'] = cursor
            result = api.call('thread/list', params)
            cursor = result.get('nextCursor')
            if not cursor:
                break
            if cursor in seen:
                raise RuntimeError('会话列表分页游标重复。')
            seen.add(cursor)


def prepare(root, executable, home, verify, hashes, raw_history):
    api = AppServer(executable, home)
    try:
        api.initialize(); scan_metadata(api)
        metadata = db_rows(state_database(home), 'threads')
        for row in metadata:
            row['rollout_path'] = relative_rollout(row['rollout_path'], home, hashes)
    finally:
        api.close()
    # Every history_base ancestor must be projected explicitly. A normal resume
    # can silently return just the last fragment when ancestor caches are absent.
    remaining = set()
    for row in metadata:
        remaining.update(raw_history.chain(row['rollout_path']))
    replayed = set(); total = len(remaining)
    while remaining:
        batch = []; logical_ids = set()
        for relative in sorted(remaining):
            parent = raw_history.parent(relative)
            logical = raw_history.headers[relative]['id']
            if parent and parent not in replayed:
                continue
            if logical not in logical_ids:
                batch.append(relative); logical_ids.add(logical)
        if not batch:
            raise RuntimeError('历史片段依赖无法排序，未修改本机。')
        # Changing the selected head is restricted to this disposable database.
        with contextlib.closing(sqlite3.connect(str(state_database(home)))) as db:
            for relative in batch:
                node = raw_history.headers[relative]; path = home / relative
                if 'archived_sessions' in Path(relative).parts:
                    active = home / 'sessions' / path.name
                    active.parent.mkdir(parents=True, exist_ok=True)
                    shutil.move(str(path), str(active)); path = active
                changed = db.execute('UPDATE threads SET rollout_path=?,archived=0,archived_at=NULL WHERE id=?',
                                     (str(path), node['id'])).rowcount
                if changed != 1:
                    raise RuntimeError('历史片段缺少本机元数据，停止恢复。')
            db.commit()
        api = AppServer(executable, home)
        try:
            api.initialize()
            for relative in batch:
                logical = raw_history.headers[relative]['id']
                result = api.call('thread/resume', {'threadId': logical, 'excludeTurns': True,
                                  'cwd': str(home), 'approvalPolicy': 'never', 'sandbox': 'read-only'})
                if result.get('thread', {}).get('id') != logical:
                    raise RuntimeError('原生恢复返回了不同的会话 ID。')
                replayed.add(relative); remaining.remove(relative)
        finally:
            api.close()
        print('已按依赖顺序读取 %d/%d 个历史片段。' % (len(replayed), total), flush=True)
    history = database(home, 'thread_history_*.sqlite')
    target_history = database(verify, 'thread_history_*.sqlite')
    if history is None:
        raise RuntimeError('当前引擎未能在隔离副本中生成正文数据库，未修改本机。')
    if target_history is None:
        target_history = verify / history.name
        empty_history(history, target_history)
    all_ids = sorted({raw_history.file_id(name) for name in replayed})
    add_missing_metadata(state_database(verify), metadata, verify)
    replace_history(target_history, history, all_ids)
    expected = {}; checked_messages = 0
    api = AppServer(executable, verify)
    try:
        api.initialize()
        for row in metadata:
            actual = {}
            result = native_history(api, row['id'], actual)
            wanted = raw_history.messages(row['rollout_path'])
            missing = set(wanted) - set(actual)
            extra = set(actual) - set(wanted)
            changed = sum(actual[key] != wanted[key] for key in set(actual) & set(wanted))
            if missing or extra or changed:
                raise RuntimeError('正文与原始历史不一致（缺少 %d 条、多出 %d 条、正文不同 %d 条），未修改本机。'
                                   % (len(missing), len(extra), changed))
            expected[row['id']] = result
            checked_messages += len(wanted)
    finally:
        api.close()
    return metadata, expected, [], history, checked_messages


def table_columns(db, table):
    names = [r[1] for r in db.execute('PRAGMA table_info(' + table + ')')]
    if not names or any(not re.fullmatch(r'[A-Za-z_][A-Za-z_0-9]*', s) for s in names):
        raise RuntimeError('正文数据库结构不受支持。')
    return names


def add_missing_metadata(path, metadata, root):
    # Preserve every existing local row, including archive flags, projects and pins.
    with contextlib.closing(sqlite3.connect(str(path), timeout=10)) as db:
        columns = table_columns(db, 'threads')
        if any(set(row) != set(columns) for row in metadata):
            raise RuntimeError('会话元数据版本不一致，停止回填。')
        sql = 'INSERT OR IGNORE INTO threads(' + ','.join(columns) + ') VALUES(' + ','.join('?' for _ in columns) + ')'
        for row in metadata:
            values = dict(row)
            values['rollout_path'] = str(root / row['rollout_path'])
            db.execute(sql, [values[col] for col in columns])
        db.commit()


def replace_history(target, recovered, ids, guard=None):
    """One transaction; never copy the disposable home's replay cursors."""
    tables = ('thread_turns', 'thread_items')
    source_rows = {table: db_rows(recovered, table) for table in tables}
    with contextlib.closing(sqlite3.connect(str(target), timeout=10)) as dst, \
            contextlib.closing(connect_readonly(recovered)) as src:
        for table in tables:
            if table_columns(dst, table) != table_columns(src, table):
                raise RuntimeError('正文数据库版本不一致，未写入。')
        dst.execute('BEGIN IMMEDIATE')
        try:
            if guard:
                guard()
            selected = set(ids)
            for table in tables:
                columns = table_columns(dst, table)
                for tid in ids:
                    dst.execute('DELETE FROM ' + table + ' WHERE thread_id=?', (tid,))
                sql = 'INSERT INTO ' + table + '(' + ','.join(columns) + ') VALUES(' + ','.join('?' for _ in columns) + ')'
                dst.executemany(sql, [[row[col] for col in columns] for row in source_rows[table]
                                      if row['thread_id'] in selected])
            for tid in ids:
                dst.execute('DELETE FROM thread_history_projection_state WHERE thread_id=?', (tid,))
            if dst.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
                raise RuntimeError('正文数据库校验失败，已回滚。')
            if guard:
                guard()
            dst.commit()
        except BaseException:
            dst.rollback()
            raise


def empty_history(source, target):
    """Keep the engine's schema/migrations, with no projected data or cursors."""
    if target.exists():
        raise RuntimeError('正文数据库已存在，停止首次建库以避免覆盖。')
    copy_database(source, target)
    with contextlib.closing(sqlite3.connect(str(target), timeout=10)) as db:
        with db:
            for table in ('thread_items', 'thread_turns', 'thread_history_projection_state'):
                db.execute('DELETE FROM ' + table)
            if db.execute('PRAGMA quick_check').fetchone()[0] != 'ok':
                raise RuntimeError('首次正文数据库结构校验失败。')


def publish_history(root, recovered, ids, destination, guard):
    """Publish a validated new database atomically, without replacing any file."""
    if database(root, 'thread_history_*.sqlite') is not None:
        raise RuntimeError('首次恢复期间正文数据库已由其他程序创建，未覆盖。')
    staging = destination / ('new-' + recovered.name)
    empty_history(recovered, staging)
    replace_history(staging, recovered, ids, guard)
    guard()
    target = root / recovered.name
    # The backup directory is on the same volume. link is atomic and exclusive;
    # removing the staging name prevents future app writes affecting the backup.
    os.link(str(staging), str(target))
    staging.unlink()
    return target


def zstd_bytes(path, header_only=False):
    """Decode with Git's native zstd DLL, not MSYS's DLL."""
    candidates = []
    git = shutil.which('git')
    if git:
        base = Path(git).resolve().parent.parent
        candidates += [base / d / 'bin' / 'libzstd.dll' for d in ('ucrt64', 'mingw64')]
    for base in (Path(os.environ.get('ProgramFiles', 'C:/Program Files')) / 'Git',):
        candidates += [base / d / 'bin' / 'libzstd.dll' for d in ('ucrt64', 'mingw64')]
    library = next((str(p) for p in candidates if p.exists()), None)
    if not library and os.name != 'nt':
        library = ctypes.util.find_library('zstd')
    if not library:
        raise RuntimeError('无法读取压缩记录的历史引用，请安装新版 Git 或更新客户端。')
    z = ctypes.CDLL(library)
    class Input(ctypes.Structure):
        _fields_ = [('src', ctypes.c_void_p), ('size', ctypes.c_size_t), ('pos', ctypes.c_size_t)]
    class Output(ctypes.Structure):
        _fields_ = [('dst', ctypes.c_void_p), ('size', ctypes.c_size_t), ('pos', ctypes.c_size_t)]
    z.ZSTD_createDStream.restype = ctypes.c_void_p
    z.ZSTD_initDStream.argtypes = [ctypes.c_void_p]
    z.ZSTD_initDStream.restype = ctypes.c_size_t
    z.ZSTD_decompressStream.argtypes = [ctypes.c_void_p, ctypes.POINTER(Output), ctypes.POINTER(Input)]
    z.ZSTD_decompressStream.restype = ctypes.c_size_t
    z.ZSTD_isError.argtypes = [ctypes.c_size_t]
    z.ZSTD_isError.restype = ctypes.c_uint
    z.ZSTD_freeDStream.argtypes = [ctypes.c_void_p]
    data = path.read_bytes(); input_buffer = ctypes.create_string_buffer(data)
    source = Input(ctypes.cast(input_buffer, ctypes.c_void_p), len(data), 0)
    stream = z.ZSTD_createDStream(); z.ZSTD_initDStream(stream); result = bytearray(); code = 1
    try:
        limit = 1024 * 1024 if header_only else 256 * 1024 * 1024
        while source.pos < source.size or code:
            buffer = ctypes.create_string_buffer(131072)
            output = Output(ctypes.cast(buffer, ctypes.c_void_p), len(buffer), 0)
            before = source.pos
            code = z.ZSTD_decompressStream(stream, ctypes.byref(output), ctypes.byref(source))
            if z.ZSTD_isError(code) or (source.pos == before and not output.pos):
                raise RuntimeError('压缩记录头无法解析。')
            result.extend(buffer.raw[:output.pos])
            if len(result) > limit:
                raise RuntimeError('解压后的聊天片段过大，停止恢复。')
            if header_only and b'\n' in result:
                return bytes(result.split(b'\n', 1)[0])
        return bytes(result)
    finally:
        z.ZSTD_freeDStream(stream)


def zstd_header(path):
    return zstd_bytes(path, header_only=True)


def normalized_message(item, native=False):
    kind = item['type']
    if kind in ('UserMessage', 'userMessage'):
        # Optional null fields were omitted by some older writers.
        def clean(value):
            if isinstance(value, dict):
                result = {k: clean(v) for k, v in value.items() if v is not None}
                if result.get('type') == 'local_image':
                    result['type'] = 'localImage'
                return result
            if isinstance(value, list):
                return [clean(v) for v in value]
            return value
        return {'kind': 'user', 'content': clean(item['content'])}
    if native:
        text = item['text']
    else:
        text = ''.join(part.get('text', '') if isinstance(part, dict) else str(part)
                       for part in item['content'])
    return {'kind': 'agent', 'text': text}


class RawHistory:
    """Independent message oracle from exact ancestor byte ranges, not SQLite."""
    def __init__(self, home, hashes):
        self.home = home; self.headers = {}; self.by_id = {}; self.memo = {}; self.data = {}
        for relative in hashes:
            path = home / relative
            fid = self.file_id(relative)
            if fid in self.by_id:
                raise RuntimeError('历史片段标识重复。')
            self.by_id[fid] = relative
            if path.name.endswith('.zst'):
                first = zstd_header(path)
            else:
                with path.open('rb') as handle:
                    first = handle.readline(1024 * 1024)
            row = json.loads(first)
            if row.get('type') != 'session_meta':
                raise RuntimeError('历史片段缺少元数据。')
            self.headers[relative] = row['payload']

    @staticmethod
    def file_id(relative):
        matches = re.findall(r'[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}', Path(relative).name)
        if not matches:
            raise RuntimeError('历史片段文件名不含标识。')
        return matches[-1].lower()

    def parent(self, relative):
        base = self.headers[relative].get('history_base') or {}
        if not base:
            return None
        parent = self.by_id.get(base['thread_id'].lower())
        if parent is None:
            raise RuntimeError('聊天历史引用的原始片段缺失。')
        return parent

    def chain(self, relative):
        result = set()
        while relative:
            if relative in result:
                raise RuntimeError('聊天历史引用存在循环。')
            result.add(relative); relative = self.parent(relative)
        return result

    def messages(self, relative, limit=None):
        key = (relative, limit)
        if key in self.memo:
            return self.memo[key]
        if relative not in self.data:
            path = self.home / relative
            self.data[relative] = zstd_bytes(path) if path.name.endswith('.zst') else path.read_bytes()
        data = self.data[relative]
        if limit is not None and (not 0 <= limit <= len(data) or (limit and data[limit - 1:limit] != b'\n')):
            raise RuntimeError('聊天历史的字节边界无效。')
        if limit == 0:
            return {}
        base = self.headers[relative].get('history_base') or {}
        parent = self.parent(relative)
        items = dict(self.messages(parent, base['end_byte_offset'])) if parent else {}
        content = data if limit is None else data[:limit]
        for line in content.splitlines():
            if not line.strip():
                continue
            row = json.loads(line); payload = row.get('payload', {})
            if row.get('type') == 'event_msg' and payload.get('type') == 'item_completed':
                item = payload['item']
                if item.get('type') in ('UserMessage', 'AgentMessage'):
                    items[(payload['turn_id'], item['id'])] = normalized_message(item)
        self.memo[key] = items
        return items


def dependencies(home, hashes):
    by_file_id = {}; bases = {}
    for relative in hashes:
        path = home / relative
        ids = re.findall(r'[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}', path.name)
        if not ids or ids[-1] in by_file_id:
            raise RuntimeError('聊天片段标识重复或缺失，未猜测历史引用。')
        by_file_id[ids[-1]] = relative
        if path.name.endswith('.zst'):
            first = zstd_header(path)
        else:
            with path.open('rb') as handle:
                first = handle.readline(1024 * 1024)
        obj = json.loads(first)
        if obj.get('type') != 'session_meta':
            raise RuntimeError('聊天片段缺少 session_meta。')
        bases[relative] = (obj.get('payload', {}).get('history_base') or {}).get('thread_id')
    def chain(relative):
        result = set()
        while relative:
            if relative in result:
                raise RuntimeError('聊天历史引用存在循环。')
            result.add(relative)
            parent = bases.get(relative)
            if parent and parent not in by_file_id:
                raise RuntimeError('聊天历史引用缺少原始片段。')
            relative = by_file_id.get(parent)
        return result
    return chain


def messages(path, tid):
    return {(r['turn_id'], r['item_id']): json.loads(r['item_json'])
            for r in db_rows(path, 'thread_items', tid)
            if r['item_type'] in ('userMessage', 'agentMessage')}


def item_contents(path, tid):
    return {(r['turn_id'], r['item_id']): json.loads(r['item_json'])
            for r in db_rows(path, 'thread_items', tid)}


def require_offline(root):
    if os.name == 'nt':
        live_root = Path(os.environ.get('CODEX_HOME') or str(Path.home() / '.codex')).resolve()
        if root == live_root:
            result = subprocess.run(['powershell.exe', '-NoProfile', '-Command',
                                     '[bool](Get-Process -Name codex -ErrorAction SilentlyContinue)'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=10)
            if result.returncode != 0 or result.stdout.decode('utf-8', 'replace').strip().lower() != 'false':
                raise RuntimeError('修复正文索引前请退出 Codex；在线备份及 --check-only 检查仍可使用。')


def recover(root, executable, check_only=False):
    root = Path(root).resolve()
    if not check_only:
        require_offline(root)
    live_history = database(root, 'thread_history_*.sqlite')
    history_was_missing = live_history is None
    temp = Path(tempfile.mkdtemp(prefix='filesync-chat-rebuild-'))
    report = {'format': 6, 'check_only': check_only, 'history_database_missing': history_was_missing}
    try:
        home = temp / 'native'; verify = temp / 'verify'
        hashes = snapshot(root, home, verify)
        # Read dependencies from immutable copies BEFORE native resume appends settings.
        chain = dependencies(verify, hashes)
        raw_history = RawHistory(verify, hashes)
        metadata, expected, failures, recovered, checked_messages = prepare(root, executable, home, verify, hashes, raw_history)
        report.update(session_files=len(hashes), native_threads=len(expected),
                      native_turns=sum(v['turns'] for v in expected.values()),
                      native_users=sum(v['users'] for v in expected.values()),
                      native_agents=sum(v['agents'] for v in expected.values()),
                      native_errors=len(failures), native_empty=sum(v['turns'] == 0 for v in expected.values()),
                      raw_messages_verified=checked_messages)
        candidates = []; skipped = []; all_dependencies = set(); repair_ids = set()
        current = {r['id']: r for r in db_rows(state_database(root), 'threads')}
        def unchanged(names):
            return all((root / name).is_file() and file_hash(root / name) == hashes[name] for name in names)
        for row in metadata:
            tid = row['id']
            if tid not in expected or not expected[tid]['turns']:
                continue
            deps = chain(row['rollout_path'])
            cache_ids = {re.findall(r'[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}', Path(name).name)[-1]
                         for name in deps}
            if not unchanged(deps):
                skipped.append({'id': tid, 'reason': 'raw_files_changed'}); continue
            if tid in current and relative_rollout(current[tid]['rollout_path'], root, hashes) != row['rollout_path']:
                skipped.append({'id': tid, 'reason': 'selected_rollout_changed'}); continue
            conflicting = False; different = tid not in current
            for cache_id in cache_ids:
                old = messages(live_history, cache_id) if live_history else {}
                new = messages(recovered, cache_id)
                if any(key not in new or new[key] != value for key, value in old.items()):
                    conflicting = True
                old_items = item_contents(live_history, cache_id) if live_history else {}
                different = different or old_items != item_contents(recovered, cache_id)
            if conflicting:
                skipped.append({'id': tid, 'reason': 'existing_message_conflict'}); continue
            if not different:
                continue
            candidates.append(tid); all_dependencies.update(deps); repair_ids.update(cache_ids)
        report.update(repairable_threads=len(candidates), repairable_segments=len(repair_ids), skipped_threads=len(skipped))
        if check_only:
            return report
        destination = root / '.filesync-chat-backups' / datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        backup(root, destination)
        (destination / 'session-file-hashes.json').write_text(json.dumps(hashes, indent=2), encoding='utf-8')
        def guard():
            require_offline(root)
            if live_history is None and database(root, 'thread_history_*.sqlite') is not None:
                raise RuntimeError('恢复期间正文数据库已由其他程序创建，未覆盖。')
            if not unchanged(all_dependencies):
                raise RuntimeError('恢复期间聊天原文发生变化，事务已回滚；请稍后重试。')
            live_rows = {r['id']: r for r in db_rows(state_database(root), 'threads')}
            source_rows = {r['id']: r for r in metadata}
            for tid in candidates:
                if tid in live_rows and relative_rollout(live_rows[tid]['rollout_path'], root, hashes) != source_rows[tid]['rollout_path']:
                    raise RuntimeError('恢复期间会话切换了历史片段，事务已回滚。')
            for cache_id in repair_ids:
                old = messages(live_history, cache_id) if live_history else {}
                new = messages(recovered, cache_id)
                if any(key not in new or new[key] != value for key, value in old.items()):
                    raise RuntimeError('恢复期间本机正文索引发生变化，事务已回滚。')
        if live_history is None:
            live_history = publish_history(root, recovered, sorted(repair_ids), destination, guard)
        else:
            replace_history(live_history, recovered, sorted(repair_ids), guard)
        for cache_id in repair_ids:
            if item_contents(live_history, cache_id) != item_contents(recovered, cache_id):
                raise RuntimeError('恢复后正文校验失败，请保留备份：' + str(destination))
        guard()
        add_missing_metadata(state_database(root), [r for r in metadata if r['id'] in candidates], root)
        # Original titles are restored separately; the live raw logs are never written.
        cache_count = apply_names(root, read_names(root))
        report.update(repaired_threads=len(candidates), cache_titles_updated=cache_count, backup=str(destination),
                      raw_files_written=0, failures=failures, skipped=skipped)
        (destination / 'report.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
        return report
    finally:
        # Windows may release app-server handles only after this Python exits.
        for _ in range(5):
            try:
                shutil.rmtree(str(temp)); break
            except OSError:
                time.sleep(0.2)
        if temp.exists():
            print('临时副本稍后可删除：' + str(temp), flush=True)


def restore(root, executable, check_only=False):
    report = recover(root, executable, check_only)
    safe = {k: v for k, v in report.items() if k not in ('failures', 'skipped')}
    print(json.dumps(safe, ensure_ascii=False), flush=True)
    if check_only:
        print('隔离验证完成，未修改本机索引。')
    elif report['native_errors'] or report['skipped_threads']:
        print('已恢复通过验证的正文；部分会话暂未处理，请查看 report.json。原文未覆盖。')
    else:
        print('正文索引和原始标题已恢复。请重新打开会话刷新显示；原文和归档状态保持不变。')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    parser.add_argument('--codex-exe')
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args()
    restore(args.root, find_codex(args.codex_exe), args.check_only)


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('恢复停止：' + str(error))
        raise SystemExit(1)
