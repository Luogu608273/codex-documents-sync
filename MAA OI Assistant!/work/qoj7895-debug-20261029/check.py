import itertools
import pathlib
import random
import subprocess

P = 998244353
OUT = pathlib.Path('C:/Users/605/Documents/Output/qoj7895-debug-20261029')
SRC = pathlib.Path(__file__).parent

def dense(n, k, edges):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u - 1].append(v - 1)
        g[v - 1].append(u - 1)
    def dfs(u, fa):
        a = [0] * (k + 2)
        a[1] = 1
        for v in g[u]:
            if v == fa:
                continue
            b = dfs(v, u)
            c = [0] * (k + 2)
            for i in range(1, k + 2):
                c[i] = (c[i] + a[i] * (b[k] + b[k + 1])) % P
                for j in range(1, k + 2 - i):
                    c[i + j] = (c[i + j] + a[i] * b[j]) % P
            a = c
        return a
    a = dfs(0, -1)
    return (a[k] + a[k + 1]) % P

def brute(n, k, edges):
    ans = 0
    for mask in range(1 << (n - 1)):
        fa = list(range(n))
        def find(x):
            while fa[x] != x:
                x = fa[x]
            return x
        for i, (u, v) in enumerate(edges):
            if mask >> i & 1:
                fa[find(u - 1)] = find(v - 1)
        sizes = [0] * n
        for u in range(n):
            sizes[find(u)] += 1
        if all(s == 0 or s == k or s == k + 1 for s in sizes):
            ans += 1
    return ans % P

def encode(cases):
    a = [str(len(cases))]
    for n, k, edges in cases:
        a.append(f'{n} {k}')
        a.extend(f'{u} {v}' for u, v in edges)
    return '\n'.join(a) + '\n'

def run(name, cases):
    p = subprocess.run([str(OUT / (name + '.exe'))], input=encode(cases), text=True, capture_output=True, timeout=25)
    if p.returncode:
        raise RuntimeError((name, p.returncode, p.stderr))
    return list(map(int, p.stdout.split()))

rng = random.Random(789520261029)
cases = []
expected = []
small = 0
for n in range(2, 13):
    trees = [[(i - 1, i) for i in range(2, n + 1)], [(1, i) for i in range(2, n + 1)]]
    trees += [[(rng.randrange(1, i), i) for i in range(2, n + 1)] for _ in range(12)]
    for edges in trees:
        for k in range(1, n + 1):
            c = (n, k, edges)
            b, d = brute(*c), dense(*c)
            assert b == d, (c, b, d)
            cases.append(c)
            expected.append(b)
            small += 1
print('Brute-force verified reference on', small, 'cases', flush=True)
for n in range(20, 91):
    edges = [(i - 1, i) for i in range(2, n + 1)]
    for k in [1, 2, 3, 4, 5, n // 2, n]:
        c = (n, k, edges)
        cases.append(c)
        expected.append(dense(*c))
for _ in range(650):
    n = rng.randrange(13, 140)
    edges = [(rng.randrange(1, i), i) for i in range(2, n + 1)]
    rng.shuffle(edges)
    k = rng.choice([1, 2, 3, rng.randrange(1, n + 1)])
    c = (n, k, edges)
    cases.append(c)
    expected.append(dense(*c))
for _ in range(80):
    n = rng.randrange(40, 130)
    mid = n // 2
    edges = [(i - 1, i) for i in range(2, mid + 1)] + [(1, mid + 1)] + [(i - 1, i) for i in range(mid + 2, n + 1)]
    rng.shuffle(edges)
    c = (n, rng.choice([1, 2, 3]), edges)
    cases.append(c)
    expected.append(dense(*c))
for name in ['original', 'fixed']:
    result = run(name, cases)
    assert len(result) == len(cases), (name, len(result), len(cases))
    failures = [i for i, (a, b) in enumerate(zip(result, expected)) if a != b]
    print(name, ':', len(cases) - len(failures), '/', len(cases), 'passed', flush=True)
    if failures:
        idx = failures[0]
        c = cases[idx]
        (OUT / ('first-' + name + '.in')).write_text(encode([c]), encoding='ascii')
        print('First mismatch:', 'n,k=', c[:2], 'expected=', expected[idx], 'actual=', result[idx], 'seed=789520261029', flush=True)
    if name == 'fixed':
        assert not failures

paths = []
for n in range(2, 65):
    for left in range(1, n - 1):
        order = list(range(2, left + 2)) + [1] + list(range(left + 2, n + 1))
        edges = list(zip(order, order[1:]))
        paths.append((n, 1, edges))
actual = run('original', paths)
for c, value in zip(paths, actual):
    correct = dense(*c)
    if value != correct:
        (OUT / 'path-counterexample.in').write_text(encode([c]), encoding='ascii')
        print('Deterministic path mismatch: n,k=', c[:2], 'expected=', correct, 'actual=', value, flush=True)
        print('Path edges:', c[2], flush=True)
        break

from math import comb
n = 100000
stress = [
    (n, 1, [(1, i) for i in range(2, n + 1)]),
    (n, 1, [(i - 1, i) for i in range(2, n + 1)]),
    (n, 316, [(i - 1, i) for i in range(2, n + 1)]),
]
fib0, fib1 = 0, 1
for _ in range(n + 1):
    fib0, fib1 = fib1, (fib0 + fib1) % P
want = [n, fib0, sum(comb(c, n - 316 * c) for c in range(n // 317, n // 316 + 1) if 0 <= n - 316 * c <= c) % P]
got = run('fixed', stress)
assert got == want, (got, want)
print('Maximum-size stress: star k=1; path k=1; path k=316: PASS', got, flush=True)
