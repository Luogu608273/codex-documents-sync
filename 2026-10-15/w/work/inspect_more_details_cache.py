import json
import struct
from datetime import datetime, timezone, timedelta
from pathlib import Path

ROOT = Path(r'C:\Users\605\AppData\Roaming\Codex\web\Codex\Default\Local Storage\leveldb')
TARGETS = {'4290238484', '473637331'}


def varint(b, i):
    n = shift = 0
    while True:
        v = b[i]
        i += 1
        n |= (v & 127) << shift
        if v < 128:
            return n, i
        shift += 7


def unsnappy(b):
    expected, i = varint(b, 0)
    out = bytearray()
    while i < len(b):
        tag = b[i]
        i += 1
        kind = tag & 3
        if kind == 0:
            n = tag >> 2
            if n >= 60:
                width = n - 59
                n = int.from_bytes(b[i:i + width], 'little')
                i += width
            n += 1
            out.extend(b[i:i + n])
            i += n
        else:
            if kind == 1:
                n = 4 + ((tag >> 2) & 7)
                offset = ((tag & 224) << 3) | b[i]
                i += 1
            else:
                n = 1 + (tag >> 2)
                width = 2 if kind == 2 else 4
                offset = int.from_bytes(b[i:i + width], 'little')
                i += width
            assert 0 < offset <= len(out)
            for _ in range(n):
                out.append(out[-offset])
    assert len(out) == expected
    return bytes(out)


def entries(b):
    end = len(b) - 4 - 4 * struct.unpack_from('<I', b, len(b) - 4)[0]
    key = b''
    i = 0
    while i < end:
        shared, i = varint(b, i)
        size, i = varint(b, i)
        value_size, i = varint(b, i)
        key = key[:shared] + b[i:i + size]
        i += size
        value = b[i:i + value_size]
        i += value_size
        yield key, value


def table(b):
    assert b[-8:] == bytes.fromhex('57fb808b247547db')
    _, i = varint(b, len(b) - 48)
    _, i = varint(b, i)
    index_offset, i = varint(b, i)
    index_size, _ = varint(b, i)

    def block(offset, size):
        data = b[offset:offset + size]
        kind = b[offset + size]
        assert kind in (0, 1)
        return unsnappy(data) if kind else data

    for _, handle in entries(block(index_offset, index_size)):
        offset, i = varint(handle, 0)
        size, _ = varint(handle, i)
        yield from entries(block(offset, size))


def find_flags(x, path=''):
    if isinstance(x, str) and x.lstrip().startswith(('{', '[')):
        try:
            find_flags(json.loads(x), path + '/json')
        except ValueError:
            pass
    elif isinstance(x, dict):
        for k, v in x.items():
            if k in TARGETS:
                allowed = {a: v[a] for a in ('value', 'rule_id', 'name') if a in v} if isinstance(v, dict) else v
                print('GATE', k, json.dumps(allowed), 'section', path.rsplit('/', 1)[-1])
            else:
                find_flags(v, path + '/' + k)
    elif isinstance(x, list):
        for v in x:
            find_flags(v, path)


latest = {}
for p in ROOT.glob('*.ldb'):
    try:
        for key, value in table(p.read_bytes()):
            if b'statsig' not in key.lower():
                continue
            tag = int.from_bytes(key[-8:], 'little')
            seq, kind = tag >> 8, tag & 255
            user_key = key[:-8]
            if user_key not in latest or seq > latest[user_key][0]:
                latest[user_key] = (seq, kind, value, p.name)
    except Exception as exc:
        print('READ_ERROR', p.name, type(exc).__name__, str(exc))
print('STATSIG_CACHE_KEYS', len(latest))
for seq, kind, value, source in latest.values():
    if kind != 1 or not value:
        continue
    try:
        text = value[1:].decode('utf-16-le' if value[0] == 0 else 'utf-8')
        obj = json.loads(text)
    except (ValueError, UnicodeError):
        continue
    print('CACHE_RECORD', source, 'sequence', seq)
    if isinstance(obj, dict):
        print('SCHEMA', [(k, type(v).__name__, len(v) if isinstance(v, (str, dict, list)) else None) for k, v in obj.items()][:12])
        if isinstance(obj.get('data'), str):
            data = obj['data']
            print('DATA_START', repr(data[:45]), 'HAS_TARGET', any(k in data for k in TARGETS))
            try:
                parsed = json.loads(data)
                if isinstance(parsed, dict):
                    print('DATA_SCHEMA', [(k, type(v).__name__, len(v) if isinstance(v, (str, dict, list)) else None) for k, v in parsed.items()][:16])
                    print('HASH_USED', parsed.get('hash_used'))
                    if isinstance(obj.get('receivedAt'), (int, float)):
                        stamp = obj['receivedAt']
                        if stamp > 100000000000:
                            stamp /= 1000
                        print('CACHE_RECEIVED_AT', datetime.fromtimestamp(stamp, timezone(timedelta(hours=8))).isoformat())
                    gates = parsed.get('feature_gates', {})
                    for target in sorted(TARGETS):
                        hashed = 0
                        for c in target:
                            hashed = (31 * hashed + ord(c)) & 0xffffffff
                        gate = gates.get(target, gates.get(str(hashed)))
                        print('LOOKUP_GATE', target, 'PRESENT', gate is not None,
                              'VALUE', gate.get('value', gate.get('v')) if isinstance(gate, dict) else None)
            except ValueError:
                pass
    find_flags(obj)
