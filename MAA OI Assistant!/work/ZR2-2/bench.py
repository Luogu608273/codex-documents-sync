import ctypes
import json
import random
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RNG = random.Random(20261020)
REPORT = []


class Counters(ctypes.Structure):
    _fields_ = [('cb', ctypes.c_ulong), ('faults', ctypes.c_ulong)] + [(x, ctypes.c_size_t) for x in ['peak', 'working', 'p1', 'p2', 'p3', 'p4', 'page', 'pagepeak']]


def execute(name, tag, generate, check):
    src = ROOT / f'{tag}.in'
    dst = ROOT / f'{tag}.out'
    generate(src)
    t = time.perf_counter()
    with src.open('rb') as f, dst.open('wb') as g:
        p = subprocess.Popen([str(ROOT / f'{name}-local.exe')], stdin=f, stdout=g, stderr=subprocess.PIPE)
        _, err = p.communicate(timeout=90)
        elapsed = time.perf_counter()-t
        info = Counters()
        info.cb = ctypes.sizeof(info)
        fn = ctypes.windll.psapi.GetProcessMemoryInfo
        fn.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong]
        ok = fn(int(p._handle), ctypes.byref(info), ctypes.sizeof(info))
    assert p.returncode == 0, (name, p.returncode, err)
    check(dst)
    row = dict(problem=name, tag=tag, seconds=round(elapsed, 4), peak_working_set_mib=round(info.peak/2**20, 2) if ok else None, input_bytes=src.stat().st_size, output_bytes=dst.stat().st_size)
    REPORT.append(row)
    (ROOT / 'benchmark.json').write_text(json.dumps(REPORT, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(row), flush=True)


def bracket_generate(path):
    path.write_text('1\n'+'90'*1000000+'\n', encoding='ascii')


def bracket_check(path):
    text = path.read_text().rstrip('\n')
    assert len(text) == 20000000-18
    depth = cnt = changes = 0
    for ch in text:
        if ch == '(':
            depth += 1
        elif ch == ')':
            depth -= 1
            assert depth >= 0
        else:
            assert depth == int(ch)
            changes += ch != ('9' if cnt % 2 == 0 else '0')
            cnt += 1
    assert depth == 0 and cnt == 2000000 and changes <= 1


def poly_generate(path):
    p = 100000
    with path.open('w', encoding='ascii', newline='\n') as f:
        f.write(f'10 10 300000 {p}\n')
        for s in range(2):
            for j in range(4):
                a, b = 12345+j*1234, 10**9-j*12345
                f.write(f'{a} {b}\n{p-a} {b}\n')
            f.write(f'{s+1} 1\n1 0\n')
        for i in range(300000):
            f.write(f'{(i*1234567)%(10**9+1)} {10**9-(i%2)} {(i//2)%2}\n')


def poly_check(path):
    p = 100000
    rows = path.read_text().split()
    assert len(rows) == 300000
    for i, row in enumerate(rows):
        x, y, s = (i*1234567)%(10**9+1), 10**9-i%2, (i//2)%2
        a = pow(2, y//2, p)
        ans = (a*x + (3 if s == 0 else 2)*(a-1)) % p
        if y % 2:
            ans = ((s+1)*ans+1) % p
        assert int(row) == ans, (i, row, ans)


def transform_generate(path, kind):
    n = m = 1000000
    with path.open('w', encoding='ascii', newline='\n') as f:
        f.write(f'1\n{n} {m}\n')
        f.write('1 '*(n-2)+f'{m} 1\n')
        if kind == 'chain':
            f.write(' '.join(map(str, range(2,m+1)))+f' {m}\n')
        elif kind == 'cycle':
            f.write(' '.join(map(str, range(2,m+1)))+' 1\n')
        else:
            f.write((str(m)+' ')*m+'\n')
        f.write('1000000000 '*m+'\n')


def set_generate(path, n, m, k):
    q = (m-k)//2
    with path.open('w', encoding='ascii', newline='\n') as f:
        f.write(f'{n} {m} {k}\n')
        for i in range(k):
            f.write(f'1 1 1 {10**12-i}\n')
        for i in range(q):
            l = RNG.randint(2, n-1)
            r = RNG.randint(l, n-1)
            f.write(f'1 {l} {r} {i+1}\n')
            f.write(f'3 {1 if i%2==0 else n} {n if i%2==0 else 1}\n')


def set_check(path, m, k):
    rows = path.read_text().split()
    assert len(rows) == (m-k)//2
    for i, row in enumerate(rows):
        assert row == ('1' if i%2 == 0 else '2'), (i, row)


if __name__ == '__main__':
    execute('bracket', 'bracket-max', bracket_generate, bracket_check)
    execute('poly', 'poly-max', poly_generate, poly_check)
    for kind in ['chain', 'cycle', 'star']:
        expected = (1000000-1)*10**9 if kind == 'chain' else 10**9
        execute('transform', f'transform-max-{kind}', lambda p: transform_generate(p, kind), lambda p: (_ for _ in ()).throw(AssertionError(p.read_text())) if int(p.read_text()) != expected else None)
    execute('set', 'set-max-k30', lambda p: set_generate(p, 200000, 200000, 30), lambda p: set_check(p, 200000, 30))
    execute('set', 'set-max-k2', lambda p: set_generate(p, 2000000, 2000000, 2), lambda p: set_check(p, 2000000, 2))
    print('ALL MAXIMUM CASES PASSED', flush=True)
