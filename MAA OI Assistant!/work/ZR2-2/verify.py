import itertools
import json
import random
import subprocess
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RNG = random.Random(20261020)
REPORT = []


def run(name, data, expected=None, mode='local', timeout=30):
    exe = ROOT / f'{name}-{mode}.exe'
    t = time.perf_counter()
    if mode == 'file':
        d = ROOT / f'file-{name}'
        d.mkdir(exist_ok=True)
        (d / f'{name}.in').write_text(data, encoding='ascii')
        p = subprocess.run([str(exe)], cwd=d, capture_output=True, timeout=timeout)
        out = (d / f'{name}.out').read_text(encoding='ascii')
        assert not p.stdout
    else:
        p = subprocess.run([str(exe)], input=data.encode(), capture_output=True, timeout=timeout)
        out = p.stdout.decode()
    assert p.returncode == 0, (name, p.returncode, p.stderr)
    if expected is not None and out.split() != str(expected).split():
        (ROOT / f'{name}-first-failure.in').write_text(data, encoding='ascii')
        (ROOT / f'{name}-first-failure.json').write_text(json.dumps({'seed': 20261020, 'expected': str(expected), 'actual': out}), encoding='utf-8')
        raise AssertionError((name, str(expected)[:500], out[:500]))
    return out, time.perf_counter() - t


def bracket_check(strings, out):
    rows = out.splitlines()
    assert len(rows) == len(strings)
    for text, row in zip(strings, rows):
        depth = 0
        digits = []
        for c in row:
            if c == '(':
                depth += 1
            elif c == ')':
                depth -= 1
                assert depth >= 0
            else:
                assert c.isdigit() and depth == int(c)
                digits.append(c)
        assert depth == 0 and len(digits) == len(text)
        assert sum(x != y for x, y in zip(text, digits)) <= 1
        a = [0] + list(map(int, text)) + [0]
        best = sum(abs(x-y) for x, y in zip(a, a[1:]))
        for i in range(1, len(a)-1):
            old = a[i]
            for v in range(10):
                a[i] = v
                best = min(best, sum(abs(x-y) for x, y in zip(a, a[1:])))
            a[i] = old
        assert len(row) == len(text) + best, (text, row, best)


def test_bracket():
    ss = ['0000', '101', '99099', '9', '221']
    for mode in ['local', 'file']:
        out, _ = run('bracket', str(len(ss))+'\n'+'\n'.join(ss)+'\n', mode=mode)
        bracket_check(ss, out)
    ss = [''.join(t) for n in range(1, 7) for t in itertools.product('0123', repeat=n)]
    ss += [''.join(RNG.choices('0123456789', k=RNG.randint(1, 35))) for _ in range(3000)]
    # Split batches to obey the statement's T <= 10000.
    out, elapsed = run('bracket', str(len(ss))+'\n'+'\n'.join(ss)+'\n')
    bracket_check(ss, out)
    REPORT.append({'problem': 'bracket', 'cases': len(ss), 'seconds': elapsed})
    print('bracket passed', len(ss), flush=True)


def poly_answer(terms, p, x, y, s):
    z = (x % p, s)
    seen = {}
    seq = []
    while z not in seen:
        seen[z] = len(seq)
        seq.append(z)
        v, t = z
        z = (sum(a * pow(v, b, p) for a, b in terms[t]) % p, t ^ 1)
    if y < len(seq):
        return seq[y][0]
    l = seen[z]
    return seq[l + (y-l) % (len(seq)-l)][0]


def test_poly():
    sample = '2 1 8 17\n1 1\n1 0\n2 1\n3 1 0\n3 1 1\n3 2 0\n3 2 1\n3 3 0\n3 3 1\n0 4 0\n0 4 1\n'
    for mode in ['local', 'file']:
        run('poly', sample, '4 6 8 7 9 14 6 3', mode)
    cases = 0
    for t in range(160):
        p = RNG.randint(2, 80)
        terms = [[(RNG.choice([0, 1, p, 10**9, RNG.randint(0, 10**9)]), RNG.choice([0, 1, 2, 10**9, RNG.randint(0, 10**9)])) for _ in range(RNG.randint(1, 10))] for _ in range(2)]
        qs = [(RNG.choice([0, 1, p-1, p, 10**9, RNG.randint(0, 10**9)]), RNG.choice([1, 2, 3, 10**9, RNG.randint(1, 10**9)]), RNG.randrange(2)) for _ in range(100)]
        data = f'{len(terms[0])} {len(terms[1])} {len(qs)} {p}\n'
        data += ''.join(f'{a} {b}\n' for ts in terms for a, b in ts)
        data += ''.join(f'{x} {y} {s}\n' for x, y, s in qs)
        ans = '\n'.join(str(poly_answer(terms, p, *q)) for q in qs)
        run('poly', data, ans)
        cases += len(qs)
    REPORT.append({'problem': 'poly', 'instances': 160, 'queries': cases})
    print('poly passed', cases, flush=True)


def transform_answer(a, b, c):
    m = len(b)
    dp = [0] * m
    for x in a:
        costs = [None] * m
        t = 0
        while costs[x] is None:
            costs[x] = t
            t += c[x]
            x = b[x]
        ndp = [10**30] * m
        mn = 10**30
        for v in range(m):
            mn = min(mn, dp[v])
            if costs[v] is not None:
                ndp[v] = max(mn, costs[v])
        dp = ndp
    ans = min(dp)
    return -1 if ans == 10**30 else ans


def test_transform():
    sample = '3\n2 3\n3 1\n2 3 3\n2 5 7\n2 3\n3 1\n1 2 3\n1 1 1\n2 3\n3 1\n2 3 1\n100 2 3\n'
    for mode in ['local', 'file']:
        run('transform', sample, '7 -1 3', mode)
    cases = []
    for m in range(1, 4):
        for b in itertools.product(range(m), repeat=m):
            for a in itertools.product(range(m), repeat=3):
                cases.append((a, b, [1 + (i*7) % 5 for i in range(m)]))
    for _ in range(9000):
        n, m = RNG.randint(1, 12), RNG.randint(1, 12)
        a = [RNG.randrange(m) for _ in range(n)]
        b = [RNG.randrange(m) for _ in range(m)]
        c = [RNG.choice([1, 10**9, RNG.randint(1, 100)]) for _ in range(m)]
        cases.append((a, b, c))
    data = [str(len(cases))]
    ans = []
    for a, b, c in cases:
        data += [f'{len(a)} {len(b)}', ' '.join(str(x+1) for x in a), ' '.join(str(x+1) for x in b), ' '.join(map(str, c))]
        ans.append(str(transform_answer(a, b, c)))
    _, elapsed = run('transform', '\n'.join(data)+'\n', '\n'.join(ans))
    REPORT.append({'problem': 'transform', 'cases': len(cases), 'seconds': elapsed})
    print('transform passed', len(cases), flush=True)


def relation(a, b):
    return 3 if a == b else 1 if a > b else 2 if b > a else 4


def test_set():
    samples = [
        ('4 8 3\n1 1 4 10\n1 1 2 20\n3 1 2\n3 1 3\n1 3 3 30\n3 1 3\n2 1 2 20\n3 1 2\n', '3 1 4 3'),
        ('3 9 2\n1 1 3 5\n1 1 1 7\n1 2 2 8\n3 1 2\n3 1 3\n2 1 1 7\n3 1 2\n2 2 2 8\n3 1 2\n', '4 1 2 3'),
        ('2 6 3\n1 1 2 1\n1 1 1 2\n1 1 1 3\n1 1 1 4\n3 1 2\n3 2 1\n', '1 2'),
        ('2 6 3\n1 1 2 1000000000000\n1 1 1 999999999999\n1 1 1 999999999998\n3 1 2\n2 1 1 999999999998\n3 1 2\n', '1 1'),
    ]
    for data, ans in samples:
        for mode in ['local', 'file']:
            run('set', data, ans, mode)
    cases = queries = 0
    for k in [1, 2, 3, 7, 15, 30]:
        for _ in range(10):
            n = RNG.randint(2, 30)
            sets = [set() for _ in range(n)]
            vals = [1, 10**12] + RNG.sample(range(2, 10**12), 78)
            ops, ans = [], []
            for j in range(1200):
                if RNG.random() < .48:
                    u, v = RNG.randrange(n), RNG.randrange(n)
                    if abs(len(sets[u])-len(sets[v])) <= k:
                        ops.append(f'3 {u+1} {v+1}')
                        ans.append(str(relation(sets[u], sets[v])))
                        continue
                x = RNG.choice(vals)
                l = r = RNG.randrange(n)
                old = x in sets[l]
                while l and (x in sets[l-1]) == old and RNG.random() < .7:
                    l -= 1
                while r+1 < n and (x in sets[r+1]) == old and RNG.random() < .7:
                    r += 1
                for i in range(l, r+1):
                    if old:
                        sets[i].remove(x)
                    else:
                        sets[i].add(x)
                ops.append(f'{2 if old else 1} {l+1} {r+1} {x}')
            run('set', f'{n} {len(ops)} {k}\n'+'\n'.join(ops)+'\n', '\n'.join(ans))
            queries += len(ans)
            cases += 1
    # Every possible allowed size difference, with and without containment.
    ops, ans = [], []
    ss = [set(), set()]
    for d in range(31):
        for i in range(2):
            for x in sorted(ss[i]):
                ops.append(f'2 {i+1} {i+1} {x}')
            ss[i].clear()
        for j in range(100):
            ops.append(f'1 1 2 {10**12-j}')
            for t in ss:
                t.add(10**12-j)
        for j in range(d):
            ops.append(f'1 1 1 {j+1}')
            ss[0].add(j+1)
        for u,v in [(0,1),(1,0),(0,0)]:
            ops.append(f'3 {u+1} {v+1}')
            ans.append(str(relation(ss[u],ss[v])))
        ops += ['1 1 1 777777777777', '1 2 2 888888888888']
        ss[0].add(777777777777)
        ss[1].add(888888888888)
        ops.append('3 1 2')
        ans.append('4')
    run('set', f'2 {len(ops)} 30\n'+'\n'.join(ops)+'\n', '\n'.join(ans))
    REPORT.append({'problem': 'set', 'random_instances': cases, 'random_queries': queries, 'targeted_queries': len(ans)})
    print('set passed', cases, queries, flush=True)


if __name__ == '__main__':
    for fn in [test_bracket, test_poly, test_transform, test_set]:
        fn()
        (ROOT / 'validation.json').write_text(json.dumps(REPORT, ensure_ascii=False, indent=2), encoding='utf-8')
    print('ALL PASSED', flush=True)
