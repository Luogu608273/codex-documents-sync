#!/usr/bin/env python3
"""Portable, selective Codex preferences. No authentication or live DB in Git."""
import argparse
import contextlib
import copy
import datetime
import hashlib
import importlib.util
import json
import ntpath
import os
from pathlib import Path
import re
import sqlite3
import tempfile
import uuid

spec = importlib.util.spec_from_file_location('chat_repair', Path(__file__).with_name('repair-chat-index.py'))
repair = importlib.util.module_from_spec(spec)
spec.loader.exec_module(repair)

SNAPSHOT = '.filesync-preferences.json'
CONFIG_KEYS = ('model', 'model_provider', 'model_reasoning_effort', 'model_verbosity',
               'service_tier', 'sandbox_mode', 'approval_policy', 'personality')
ATOM_KEYS = ('composer-permission-mode-visibility', 'composer-model-picker-selection-mode-v1',
             'chatgpt-work-model-picker-selection-mode-v1', 'composer-recent-model-configurations-v1',
             'flat-project-sidebar-preferences-v1')
HOST_ATOMS = ('agent-mode-by-host-id', 'preferred-non-full-access-agent-mode-by-host-id')
THREAD_COLUMNS = ('project_id', 'is_pinned', 'thread_section_id', 'section_position', 'section_entered_at_ms')
IDENTIFIER = re.compile(r'^[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}$')


def encode(data):
    return (json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + '\n').encode('utf-8')


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_bytes(path):
    return path.read_bytes() if path.exists() else b''


def read_json(path):
    raw = read_bytes(path)
    return json.loads(raw.decode('utf-8-sig')) if raw else {}


def atomic_write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, name = tempfile.mkstemp(prefix='.filesync-', dir=str(path.parent))
    try:
        with os.fdopen(fd, 'wb') as stream:
            stream.write(data)
        os.replace(name, str(path))
    finally:
        if os.path.exists(name):
            os.unlink(name)


def norm(path):
    value = str(path)
    if value.startswith('\\\\?\\'):
        value = value[4:]
    return ntpath.normcase(ntpath.normpath(value))


def portable(path, home):
    path = str(path)
    plain = path[4:] if path.startswith('\\\\?\\') else path
    if norm(plain) == norm(home):
        return '@USERPROFILE@'
    if norm(plain).startswith(norm(home).rstrip('\\') + '\\'):
        return '@USERPROFILE@/' + plain[len(str(home).rstrip('\\/')) + 1:].replace('\\', '/')
    return plain


def expand(path, home):
    if path == '@USERPROFILE@':
        return str(home)
    if path.startswith('@USERPROFILE@/'):
        suffix = path[len('@USERPROFILE@/'):]
        if any(x in ('', '.', '..') for x in suffix.split('/')) or ':' in suffix or '\\' in suffix:
            raise RuntimeError('偏好快照的项目路径无效。')
        return ntpath.join(str(home), *suffix.split('/')) if os.name == 'nt' else str(home / suffix)
    return path


def rows(db, table):
    db.row_factory = sqlite3.Row
    return [dict(row) for row in db.execute('SELECT * FROM ' + table)]


def selected_config(raw):
    result = {}
    for line in raw.decode('utf-8-sig').splitlines():
        if line.lstrip().startswith('['):
            break
        match = re.fullmatch(r'\s*([a-z_]+)\s*=\s*("(?:[^"\\\r\n]|\\.)*"|\'[^\'\r\n]*\')\s*(?:#.*)?', line)
        if match and match[1] in CONFIG_KEYS:
            value = json.loads(match[2]) if match[2].startswith('"') else match[2][1:-1]
            result[match[1]] = value
    return result


def patch_config(raw, settings):
    lines = raw.decode('utf-8-sig').splitlines(keepends=True)
    first_section = next((i for i, line in enumerate(lines) if line.lstrip().startswith('[')), len(lines))
    prefix = []; remaining = dict(settings)
    for line in lines[:first_section]:
        match = re.match(r'^\s*([a-z_]+)\s*=', line)
        if match and match[1] in settings:
            if match[1] in remaining:
                prefix.append(match[1] + ' = ' + json.dumps(remaining.pop(match[1]), ensure_ascii=False) + '\n')
        else:
            prefix.append(line)
    if prefix and not prefix[-1].endswith(('\n', '\r')):
        prefix[-1] += '\n'
    prefix += [key + ' = ' + json.dumps(value, ensure_ascii=False) + '\n' for key, value in sorted(remaining.items())]
    return (''.join(prefix + lines[first_section:])).encode('utf-8')


def capture(root, home=None):
    home = Path(home or Path.home())
    state_path = repair.state_database(root)
    if not state_path:
        raise RuntimeError('请先启动一次 Codex 创建本机状态数据库。')
    global_path = root / '.codex-global-state.json'
    before = read_bytes(global_path)
    state = json.loads(before.decode('utf-8-sig')) if before else {}
    config_raw = read_bytes(root / 'config.toml')
    # All related tables come from one SQLite read transaction, including during online export.
    with contextlib.closing(repair.connect_readonly(state_path)) as db:
        db.execute('BEGIN')
        projects = rows(db, 'projects'); roots = rows(db, 'project_roots')
        sections = rows(db, 'thread_sections'); threads = rows(db, 'threads')
    if before != read_bytes(global_path) or config_raw != read_bytes(root / 'config.toml'):
        raise RuntimeError('导出期间偏好正在写入，请稍后重试。')
    local = state.get('local-projects', {})
    mapping = {}
    for host, links in state.get('app-server-project-id-by-legacy-project-id-by-host', {}).items():
        if host.startswith('local:') and norm(host[6:]) == norm(root):
            mapping.update(links)
    result = {'format': 1, 'projects': [], 'sections': [], 'threads': {}, 'atoms': {},
              'local_permission_selection': None, 'config': selected_config(config_raw), 'project_order': []}
    for project in projects:
        pid = project['id']
        paths = [portable(x['path'], home) for x in sorted(roots, key=lambda x: x['position']) if x['project_id'] == pid]
        legacy = [key for key, value in mapping.items() if value == pid and key in local]
        if not legacy:
            legacy = [key for key, value in local.items()
                      if sorted(norm(portable(p, home)) for p in value.get('rootPaths', [])) == sorted(map(norm, paths))]
        if len(legacy) > 1:
            raise RuntimeError('项目路径对应多个旧项目，未导出歧义映射。')
        legacy_id = legacy[0] if legacy else pid
        mapping[legacy_id] = pid
        result['projects'].append({'id': pid, 'legacy_id': legacy_id, 'name': project['name'],
                                   'roots': paths, 'position': project['position']})
    known_projects = {p['id'] for p in result['projects']}
    pinned = set(state.get('pinned-thread-ids', []))
    assignments = state.get('thread-project-assignments', {})
    for row in threads:
        tid = row['id']
        if not IDENTIFIER.fullmatch(tid):
            continue
        item = {key: row[key] for key in THREAD_COLUMNS}
        assignment = assignments.get(tid, {})
        if not item['project_id'] and assignment.get('projectKind') == 'local':
            item['project_id'] = mapping.get(assignment.get('projectId'))
        if item['project_id'] and item['project_id'] not in known_projects:
            raise RuntimeError('聊天引用了缺失的本机项目，未导出不完整快照。')
        item['is_pinned'] = bool(item['is_pinned'] or tid in pinned)
        result['threads'][tid] = item
    result['sections'] = [{k: x[k] for k in ('id', 'name', 'appearance')} for x in sections]
    atoms = state.get('electron-persisted-atom-state', {})
    for key in ATOM_KEYS:
        if key in atoms:
            value = atoms[key]
            if key == 'composer-recent-model-configurations-v1':
                value = [{k: x[k] for k in ('model', 'reasoningEffort', 'serviceTier') if k in x}
                         for x in value[:3]]
            if key == 'flat-project-sidebar-preferences-v1':
                value = {k: v for k, v in value.items() if k in ('chatSortMode', 'projectSortMode', 'mode', 'initialized')}
            result['atoms'][key] = value
    for key in HOST_ATOMS:
        if 'local' in atoms.get(key, {}):
            result['atoms'][key] = {'local': atoms[key]['local']}
    selection = atoms.get('permission-selection-by-host-id:local')
    if selection and selection.get('kind') == 'agent-mode':
        result['local_permission_selection'] = {k: selection[k] for k in ('kind', 'agentMode')}
    result['project_order'] = [mapping.get(pid, pid) for pid in state.get('project-order', [])
                               if mapping.get(pid, pid) in known_projects]
    result['projects'].sort(key=lambda x: x['id'])
    result['sections'].sort(key=lambda x: x['id'])
    return result


def validate(data):
    expected = {'format', 'projects', 'sections', 'threads', 'atoms', 'config', 'local_permission_selection', 'project_order'}
    if not isinstance(data, dict) or set(data) != expected or data['format'] != 1:
        raise RuntimeError('偏好快照格式不支持。')
    if set(data['config']) - set(CONFIG_KEYS) or set(data['atoms']) - set(ATOM_KEYS + HOST_ATOMS):
        raise RuntimeError('偏好快照包含未允许的设置。')
    if any(not isinstance(v, str) or any(c in v for c in '\r\n\x00') for v in data['config'].values()):
        raise RuntimeError('模型/权限配置值无效。')
    def identifier(value):
        if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
            raise RuntimeError('偏好快照含无效标识。')
    pids = set(); legacy = set(); sids = set()
    for p in data['projects']:
        if set(p) != {'id', 'legacy_id', 'name', 'roots', 'position'}:
            raise RuntimeError('项目字段不支持。')
        identifier(p['id']); identifier(p['legacy_id'])
        if p['id'] in pids or p['legacy_id'] in legacy or not isinstance(p['name'], str) or not isinstance(p['position'], int):
            raise RuntimeError('项目快照不完整或重复。')
        pids.add(p['id']); legacy.add(p['legacy_id'])
        if not isinstance(p['roots'], list) or any(not isinstance(x, str) or '\x00' in x for x in p['roots']):
            raise RuntimeError('项目路径格式错误。')
    for section in data['sections']:
        if set(section) != {'id', 'name', 'appearance'}:
            raise RuntimeError('分组字段不支持。')
        identifier(section['id'])
        if section['id'] in sids or not isinstance(section['name'], str) or section['appearance'] is not None and not isinstance(section['appearance'], str):
            raise RuntimeError('聊天分组无效。')
        sids.add(section['id'])
    for tid, row in data['threads'].items():
        identifier(tid)
        if set(row) != set(THREAD_COLUMNS) or row['project_id'] is not None and row['project_id'] not in pids or row['thread_section_id'] is not None and row['thread_section_id'] not in sids:
            raise RuntimeError('聊天项目或分组引用无效。')
        if type(row['is_pinned']) is not bool:
            raise RuntimeError('置顶值必须为布尔值。')
        if any(row[k] is not None and not isinstance(row[k], (int, float)) for k in ('section_position', 'section_entered_at_ms')):
            raise RuntimeError('分组顺序无效。')
    if any(pid not in pids for pid in data['project_order']):
        raise RuntimeError('项目排序引用无效。')
    for key, value in data['atoms'].items():
        if key in HOST_ATOMS and (not isinstance(value, dict) or set(value) != {'local'} or not isinstance(value['local'], str)):
            raise RuntimeError('只允许本机权限偏好。')
        elif key == 'composer-permission-mode-visibility' and type(value) is not bool:
            raise RuntimeError('完全访问开关格式无效。')
        elif key.endswith('selection-mode-v1') and value is not None and not isinstance(value, str):
            raise RuntimeError('模型选择偏好无效。')
        elif key == 'composer-recent-model-configurations-v1':
            if not isinstance(value, list) or len(value) > 3 or any(not isinstance(x, dict) or set(x) - {'model', 'reasoningEffort', 'serviceTier'} or any(v is not None and not isinstance(v, str) for v in x.values()) for x in value):
                raise RuntimeError('最近模型配置无效。')
        elif key == 'flat-project-sidebar-preferences-v1' and (not isinstance(value, dict) or set(value) - {'chatSortMode', 'projectSortMode', 'mode', 'initialized'}):
            raise RuntimeError('侧栏偏好无效。')
    permission = data['local_permission_selection']
    if permission is not None and (not isinstance(permission, dict) or set(permission) != {'kind', 'agentMode'} or permission['kind'] != 'agent-mode' or not isinstance(permission['agentMode'], str)):
        raise RuntimeError('权限偏好格式无效。')
    return data


def baseline_path(root):
    # FileSync only supports a normal outer Git directory for portable metadata.
    folder = root / '.git'
    if not folder.is_dir() or folder.is_symlink():
        raise RuntimeError('偏好快照需要普通外层 .git 目录。')
    return folder / 'filesync-preferences-baseline.json'


def export(root, home=None):
    target = root / SNAPSHOT
    baseline = baseline_path(root)
    previous = read_bytes(target)
    current = encode(validate(capture(root, home)))
    if previous:
        validate(json.loads(previous.decode('utf-8-sig')))
        saved = read_json(baseline).get('sha256')
        if digest(previous) != saved and previous != current:
            raise RuntimeError('已下载的偏好快照尚未恢复。请退出 Codex 后选主菜单 11，避免新电脑空状态覆盖原备份。')
    if previous != current:
        atomic_write(target, current)
    atomic_write(baseline, encode({'sha256': digest(current)}))
    return {'snapshot_bytes': len(current), 'threads': len(json.loads(current)['threads'])}


def plan_restore(root, data, home=None):
    validate(data)
    home = Path(home or Path.home())
    current = capture(root, home)
    state = read_json(root / '.codex-global-state.json')
    pid_map = {}; legacy_map = {}; used_legacy = set(state.get('local-projects', {}))
    existing = current['projects']
    for p in data['projects']:
        roots = sorted(map(norm, p['roots']))
        matches = [x for x in existing if roots and sorted(map(norm, x['roots'])) == roots]
        if len(matches) > 1:
            raise RuntimeError('本机有重复路径的项目，无法自动匹配。')
        if matches:
            target = matches[0]
            pid_map[p['id']] = target['id']; legacy_map[p['id']] = target['legacy_id']
        else:
            collision = next((x for x in existing if x['id'] == p['id']), None)
            if collision:
                raise RuntimeError('项目 ID 已被其他本机路径使用，未覆盖。')
            pid_map[p['id']] = p['id']
            legacy_map[p['id']] = p['legacy_id'] if p['legacy_id'] not in used_legacy else str(uuid.uuid4())
        used_legacy.add(legacy_map[p['id']])
    missing = set(data['threads']) - set(current['threads'])
    if missing:
        raise RuntimeError('偏好快照中有 %d 个聊天尚未导入。请先下载并用主菜单 10 恢复聊天。' % len(missing))
    sid_map = {}
    for section in data['sections']:
        match = next((x for x in current['sections'] if x['id'] == section['id']), None)
        if match and match['name'] != section['name']:
            raise RuntimeError('聊天分组 ID 冲突，未覆盖。')
        sid_map[section['id']] = section['id']
    local = state.setdefault('local-projects', {})
    now = int(datetime.datetime.now().timestamp() * 1000)
    for p in data['projects']:
        lid = legacy_map[p['id']]
        entry = local.setdefault(lid, {'id': lid, 'createdAt': now, 'updatedAt': now})
        entry.update(name=p['name'], rootPaths=[expand(x, home) for x in p['roots']])
    host = 'local:' + str(root)
    mapping = state.setdefault('app-server-project-id-by-legacy-project-id-by-host', {}).setdefault(host, {})
    for pid in pid_map:
        mapping[legacy_map[pid]] = pid_map[pid]
    # Mark this host migrated; otherwise the app's legacy migration can undo restored SQL metadata.
    # Existing migration flags are preserved. Never copy another host's migration state.
    assignments = state.setdefault('thread-project-assignments', {})
    hosts = state.setdefault('thread-project-membership-host-ids', {})
    projectless = set(state.get('projectless-thread-ids', []))
    pinned = set(state.get('pinned-thread-ids', []))
    sql_threads = {}
    for tid, source in data['threads'].items():
        row = copy.deepcopy(source)
        pid = row['project_id']
        if pid:
            row['project_id'] = pid_map[pid]
            assignments[tid] = {'projectKind': 'local', 'projectId': legacy_map[pid]}
            hosts[tid] = 'local'; projectless.discard(tid)
        else:
            assignments.pop(tid, None); hosts.pop(tid, None); projectless.add(tid)
        if row['is_pinned']:
            pinned.add(tid)
        else:
            pinned.discard(tid)
        sql_threads[tid] = row
    state['projectless-thread-ids'] = sorted(projectless)
    state['pinned-thread-ids'] = sorted(pinned)
    order = [legacy_map[pid] for pid in data['project_order']]
    state['project-order'] = order + [pid for pid in state.get('project-order', []) if pid not in order]
    atoms = state.setdefault('electron-persisted-atom-state', {})
    for key, value in data['atoms'].items():
        if key in HOST_ATOMS:
            atoms.setdefault(key, {}).update(value)
        else:
            atoms[key] = copy.deepcopy(value)
    if data['local_permission_selection'] is not None:
        atoms['permission-selection-by-host-id:local'] = copy.deepcopy(data['local_permission_selection'])
    return {'state': state, 'pid_map': pid_map, 'threads': sql_threads,
            'config': patch_config(read_bytes(root / 'config.toml'), data['config']), 'data': data, 'home': home,
            'current': current, 'input_hashes': {name: digest(read_bytes(root / name))
                                              for name in ('.codex-global-state.json', 'config.toml')}}


def apply_plan(root, plan, guard=None, refresh_snapshot=False):
    guard = guard or (lambda: repair.require_offline(root))
    guard()
    if capture(root, plan['home']) != plan['current'] or any(digest(read_bytes(root / name)) != sha for name, sha in plan['input_hashes'].items()):
        raise RuntimeError('生成恢复方案后本机状态已变化，请重试。')
    db_path = repair.state_database(root)
    updates = {root / '.codex-global-state.json': encode(plan['state']), root / 'config.toml': plan['config']}
    if refresh_snapshot:
        snapshot_bytes = encode(validate(plan['data']))
        updates[root / SNAPSHOT] = snapshot_bytes
        updates[baseline_path(root)] = encode({'sha256': digest(snapshot_bytes)})
    paths = list(updates)
    original = {p: read_bytes(p) for p in paths}
    present = {p: p.exists() for p in paths}
    backup = root / '.filesync-preferences-backups' / datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup.mkdir(parents=True)
    for path, raw in original.items():
        if present[path]:
            (backup / path.name).write_bytes(raw)
    with contextlib.closing(repair.connect_readonly(db_path)) as src, contextlib.closing(sqlite3.connect(str(backup / db_path.name))) as dst:
        src.backup(dst)
    # Back up the catalog too; it is a cache but project_id must agree for immediate display.
    catalog_path = root / 'sqlite' / 'codex-dev.db'
    if catalog_path.exists():
        with contextlib.closing(repair.connect_readonly(catalog_path)) as src, contextlib.closing(sqlite3.connect(str(backup / 'codex-dev.db'))) as dst:
            src.backup(dst)
    written = {}
    with contextlib.closing(sqlite3.connect(str(db_path), timeout=10)) as db:
        if catalog_path.exists():
            db.execute('ATTACH DATABASE ? AS catalog', (str(catalog_path),))
        db.execute('BEGIN IMMEDIATE')
        try:
            guard()
            if any(read_bytes(p) != original[p] for p in paths):
                raise RuntimeError('恢复前偏好发生变化，已停止。')
            if capture(root, plan['home']) != plan['current']:
                raise RuntimeError('恢复前项目或置顶状态发生变化，事务回滚。')
            now = int(datetime.datetime.now().timestamp() * 1000)
            for p in plan['data']['projects']:
                pid = plan['pid_map'][p['id']]
                db.execute('INSERT OR IGNORE INTO projects(id,name,metadata,position,created_at_ms,updated_at_ms) VALUES(?,?,?, ?,?,?)',
                           (pid, p['name'], '{}', p['position'], now, now))
                db.execute('UPDATE projects SET name=?, position=? WHERE id=?', (p['name'], p['position'], pid))
                db.execute('DELETE FROM project_roots WHERE project_id=?', (pid,))
                db.executemany('INSERT INTO project_roots(project_id,position,path) VALUES(?,?,?)',
                               [(pid, i, expand(path, plan['home'])) for i, path in enumerate(p['roots'])])
            for section in plan['data']['sections']:
                db.execute('INSERT INTO thread_sections(id,name,appearance) VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET name=excluded.name,appearance=excluded.appearance',
                           (section['id'], section['name'], section['appearance']))
            for tid, row in plan['threads'].items():
                count = db.execute('UPDATE threads SET ' + ','.join(k + '=?' for k in THREAD_COLUMNS) + ' WHERE id=?',
                                   tuple(row[k] for k in THREAD_COLUMNS) + (tid,)).rowcount
                if count != 1:
                    raise RuntimeError('恢复期间聊天索引消失，事务回滚。')
                if catalog_path.exists():
                    db.execute("UPDATE catalog.local_thread_catalog SET project_id=? WHERE thread_id=? AND host_id='local'", (row['project_id'], tid))
            guard()
            for path, raw in updates.items():
                if raw != original[path]:
                    atomic_write(path, raw); written[path] = raw
            guard()
            db.commit()
        except Exception:
            db.rollback()
            for path, raw in written.items():
                if read_bytes(path) != raw:
                    raise RuntimeError('恢复期间文件被其他程序改动，请从备份检查：' + str(backup))
                if present[path]:
                    atomic_write(path, original[path])
                else:
                    path.unlink()
            raise
    return {'backup': str(backup), 'projects': len(plan['pid_map']), 'threads': len(plan['threads']),
            'pinned': sum(x['is_pinned'] for x in plan['threads'].values())}


def restore(root, check_only=False, home=None):
    path = root / SNAPSHOT
    if not path.exists():
        raise RuntimeError('没有偏好快照。请先在原电脑用新版 FileSync 上传，再在这里下载。')
    raw = read_bytes(path)
    data = validate(json.loads(raw.decode('utf-8-sig')))
    plan = plan_restore(root, data, home)
    if check_only:
        return {'check_only': True, 'projects': len(data['projects']), 'threads': len(data['threads'])}
    report = apply_plan(root, plan)
    atomic_write(baseline_path(root), encode({'sha256': digest(raw)}))
    return report


def infer_projects(root, check_only=False, home=None):
    # Recovery for older backups: cwd can suggest project membership, but never pins.
    incoming = read_bytes(root / SNAPSHOT)
    baseline_file = baseline_path(root)
    baseline_bytes = read_bytes(baseline_file)
    if incoming and read_json(baseline_file).get('sha256') != digest(incoming):
        raise RuntimeError('已下载的偏好快照尚未恢复，请先用主菜单 11；未按目录推断。')
    data = capture(root, home)
    changed = []
    with contextlib.closing(repair.connect_readonly(repair.state_database(root))) as db:
        cwd_rows = rows(db, 'threads')
    for thread in cwd_rows:
        tid = thread['id']
        if tid not in data['threads'] or data['threads'][tid]['project_id']:
            continue
        cwd = norm(portable(thread['cwd'], Path(home or Path.home())))
        matches = [(len(norm(path)), project['id']) for project in data['projects'] for path in project['roots']
                   if cwd == norm(path) or cwd.startswith(norm(path).rstrip('\\') + '\\')]
        if not matches:
            continue
        best = max(length for length, pid in matches)
        choices = {pid for length, pid in matches if length == best}
        if len(choices) != 1:
            continue
        data['threads'][tid]['project_id'] = choices.pop(); changed.append(tid)
    if check_only:
        return {'check_only': True, 'inferred_project_links': len(changed), 'pins_inferred': 0}
    # Reconcile known global assignments as well as inferred legacy memberships.
    plan = plan_restore(root, data, home)
    plan['input_hashes'][SNAPSHOT] = digest(incoming)
    plan['input_hashes']['.git/filesync-preferences-baseline.json'] = digest(baseline_bytes)
    # Publish the rebuilt associations together with the local snapshot and its
    # baseline. A subsequent menu-11 restore must not undo menu-12 recovery.
    report = apply_plan(root, plan, refresh_snapshot=True)
    report.update(inferred_project_links=len(changed), pins_inferred=0)
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', required=True)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--export', action='store_true')
    group.add_argument('--restore', action='store_true')
    group.add_argument('--infer-projects', action='store_true')
    parser.add_argument('--check-only', action='store_true')
    args = parser.parse_args(); root = Path(args.root).resolve()
    if args.export:
        if args.check_only:
            report = {'snapshot_bytes': len(encode(validate(capture(root)))), 'check_only': True}
        else:
            report = export(root)
    elif args.restore:
        report = restore(root, args.check_only)
    else:
        report = infer_projects(root, args.check_only)
    print(json.dumps(report, ensure_ascii=False))


if __name__ == '__main__':
    try:
        main()
    except Exception as error:
        print('偏好操作停止：' + str(error))
        raise SystemExit(1)
