import collections
import heapq
import itertools
import json
import pathlib
import random
import subprocess
import time

ROOT = pathlib.Path(__file__).resolve().parent
SEED = 222527
rng = random.Random(SEED)
report = {'seed': SEED, 'samples': [], 'random': {}}

def run(name, data, timeout=8):
    start = time.perf_counter()
    p = subprocess.run([str(ROOT / (name + '.exe'))], input=data.encode(),
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=timeout)
    assert p.returncode == 0, (name, p.returncode, p.stderr.decode(errors='replace'))
    return p.stdout.decode(), time.perf_counter() - start

def fail(name, data, output, expected):
    (ROOT / 'first_failure.in').write_text(data, encoding='utf-8')
    (ROOT / 'first_failure.json').write_text(json.dumps({'name': name, 'output': output,
        'expected': expected, 'seed': SEED}, ensure_ascii=False, indent=2), encoding='utf-8')
    raise AssertionError((name, output[:500], str(expected)[:500]))

def check_a(data, output):
    it = iter(map(int, data.split()))
    n, m = next(it), next(it)
    a = [[next(it) for _ in range(m)] for _ in range(n)]
    s = sum(map(sum, a))
    out = list(map(int, output.split()))
    if s % n:
        return out == [-1]
    target = s // n
    best = sum(max(0, sum(row) - target) for row in a)
    if len(out) != 1 + 3 * best or out[0] != best:
        return False
    for i in range(best):
        u, v, j = (z - 1 for z in out[1 + i * 3:4 + i * 3])
        if not (0 <= u < n and 0 <= v < n and u != v and 0 <= j < m):
            return False
        a[u][j], a[v][j] = a[v][j], a[u][j]
    return all(sum(row) == target for row in a)

def rects_ok(a, b):
    x1, y1, x2, y2 = a
    u1, v1, u2, v2 = b
    return (max(x1, u1) >= min(x2, u2) or max(y1, v1) >= min(y2, v2)
            or (x1 <= u1 and y1 <= v1 and x2 >= u2 and y2 >= v2)
            or (u1 <= x1 and v1 <= y1 and u2 >= x2 and v2 >= y2))

def parse_d(data):
    it = iter(map(int, data.split()))
    n = next(it)
    return n, [(next(it), next(it)) for _ in range(n)], [(next(it), next(it)) for _ in range(n)]

def check_d(data, output, expected=None):
    n, a, b = parse_d(data)
    out = output.split()
    if not out or out[0] not in ('Yes', 'No'):
        return False
    if out[0] == 'No':
        return len(out) == 1 and (expected is None or expected.split()[0] == 'No')
    if expected is not None and expected.split()[0] != 'Yes':
        return False
    p = list(map(int, out[1:]))
    if sorted(p) != list(range(1, n + 1)):
        return False
    rects = []
    for (x, y), j in zip(a, p):
        u, v = b[j - 1]
        if x >= u or y >= v:
            return False
        rects.append((x, y, u, v))
    if n <= 1000:
        return all(rects_ok(rects[i], rects[j]) for i in range(n) for j in range(i))
    # Public large samples supply the canonical (unique) matching.
    return expected is not None and p == list(map(int, expected.split()[1:]))

def road_brute(n, heights, edges, x):
    adj = [[] for _ in range(n)]
    for u, v, t in edges:
        adj[u].append((v, t))
        adj[v].append((u, t))
    dis = {(0, x): 0}
    q = [(0, 0, x)]
    while q:
        d, u, h = heapq.heappop(q)
        if dis[u, h] != d:
            continue
        if u == n - 1 and h == heights[u]:
            return d
        moves = []
        if h:
            moves.append((u, h - 1, 1))
        if h < heights[u]:
            moves.append((u, h + 1, 1))
        for v, t in adj[u]:
            if 0 <= h - t <= heights[v]:
                moves.append((v, h - t, t))
        for v, z, w in moves:
            if d + w < dis.get((v, z), 10**30):
                dis[v, z] = d + w
                heapq.heappush(q, (d + w, v, z))
    return -1

def moment_brute(n, edges, k):
    adj = [[] for _ in range(n)]
    for i, (u, v) in enumerate(edges):
        adj[u].append((v, i))
        adj[v].append((u, i))
    paths = set()
    for rt in range(n):
        st = [(rt, -1, ())]
        while st:
            u, fa, p = st.pop()
            if len(p) == k:
                paths.add(tuple(sorted(p)))
                continue
            for v, e in adj[u]:
                if v != fa:
                    st.append((v, u, p + (e,)))
    if not paths:
        return n - 1
    ends = [[] for _ in range(n - 1)]
    for p in paths:
        ends[max(p)].append(p)
    col = [0] * (n - 1)
    best = 1
    def dfs(i, count):
        nonlocal best
        if count + n - 1 - i <= best:
            return
        if i == n - 1:
            best = max(best, count)
            return
        for c in range(count + 1):
            col[i] = c
            if any(len({col[j] for j in p}) == k for p in ends[i]):
                continue
            dfs(i + 1, max(count, c + 1))
    col[0] = 0
    dfs(1, 1)
    return best

def d_brute(a, b):
    n = len(a)
    cand = [[j for j in range(n) if a[i][0] < b[j][0] and a[i][1] < b[j][1]] for i in range(n)]
    order = sorted(range(n), key=lambda i: len(cand[i]))
    rects = []
    def dfs(t, mask):
        if t == n:
            return True
        i = order[t]
        for j in cand[i]:
            if mask >> j & 1:
                continue
            r = a[i] + b[j]
            if all(rects_ok(r, s) for s in rects):
                rects.append(r)
                if dfs(t + 1, mask | 1 << j):
                    return True
                rects.pop()
        return False
    return dfs(0, 0)

def samples():
    for pid, name in [(3721, 'utopia'), (3722, 'road'), (3723, 'moment'), (3724, 'passerby')]:
        for path in sorted((ROOT / ('sample-' + str(pid))).glob('*.in')):
            data = path.read_text()
            expected = path.with_suffix('.out').read_text()
            output, elapsed = run(name + '_std', data)
            ok = (check_a(data, output) if name == 'utopia' else
                  check_d(data, output, expected) if name == 'passerby' else
                  output.split() == expected.split())
            if not ok:
                fail(name + '_sample_' + path.stem, data, output, expected)
            report['samples'].append({'name': path.stem, 'seconds': round(elapsed, 4)})
        print(name, '公开样例通过', flush=True)

def random_a():
    for case in range(400):
        n, m = rng.randint(1, 12), rng.randint(1, 12)
        a = [[rng.randrange(2) for _ in range(m)] for _ in range(n)]
        data = f'{n} {m}\n' + '\n'.join(' '.join(map(str, row)) for row in a) + '\n'
        for ver in ('std', 'partial'):
            output, _ = run('utopia_' + ver, data)
            if not check_a(data, output):
                fail('utopia_' + ver, data, output, 'legal optimal construction')
    report['random']['utopia'] = 400
    print('utopia 随机构造 400 组通过', flush=True)

def random_b():
    for case in range(600):
        n = rng.randint(2, 9)
        h = [rng.randint(1, 10) for _ in range(n)]
        if case % 5 == 0:
            h = [h[0]] * n
        x = 0 if case % 4 == 0 else rng.randint(0, h[0])
        m = rng.randint(1, n * (n - 1))
        edges = []
        for _ in range(m):
            u, v = rng.sample(range(n), 2)
            edges.append((u, v, rng.randint(1, 14)))
        data = f'{n} {m} {x}\n' + ' '.join(map(str, h)) + '\n' + ''.join(f'{u+1} {v+1} {t}\n' for u, v, t in edges)
        expected = road_brute(n, h, edges, x)
        for ver in ('std', 'partial'):
            output, _ = run('road_' + ver, data)
            if output.split() != [str(expected)]:
                fail('road_' + ver, data, output, expected)
    report['random']['road'] = 600
    print('road 分层图暴力 600 组通过', flush=True)

def random_c():
    for case in range(300):
        n = rng.randint(2, 10)
        edges = [(i, rng.randrange(i)) for i in range(1, n)]
        if case % 5 == 0:
            edges = [(i, i-1) for i in range(1, n)]
        if case % 5 == 1:
            edges = [(i, 0) for i in range(1, n)]
        rng.shuffle(edges)
        k = rng.randint(2, n)
        data = f'{n} {k}\n' + ''.join(f'{u+1} {v+1}\n' for u, v in edges)
        expected = moment_brute(n, edges, k)
        for ver in ('std', 'partial'):
            output, _ = run('moment_' + ver, data)
            if output.split() != [str(expected)]:
                fail('moment_' + ver, data, output, expected)
    for case in range(40):
        n = rng.randint(30, 100)
        k = rng.randint(2, min(30, n))
        data = f'{n} {k}\n' + ''.join(f'{i+1} {rng.randrange(i)+1}\n' for i in range(1, n))
        output, _ = run('moment_std', data)
        other, _ = run('moment_partial', data)
        if output.split() != other.split():
            fail('moment_medium', data, output, other)
    report['random']['moment_brute'] = 300
    report['random']['moment_partial_compare'] = 40
    print('moment 任意颜色分割暴力 300 组、中型 DP 40 组通过', flush=True)

def random_d():
    grid = list(itertools.product(range(3), repeat=2))
    count = 0
    for n in (2, 3, 4):
        for a in itertools.combinations(grid, n):
            left = set(a)
            for b in itertools.combinations([p for p in grid if p not in left], n):
                expected = d_brute(a, b)
                data = str(n) + '\n' + ''.join(f'{x} {y}\n' for x, y in a + b)
                output, _ = run('passerby_std', data)
                if (output.split()[0] == 'Yes') != expected or not check_d(data, output):
                    fail('passerby_exhaustive', data, output, expected)
                count += 1
    for case in range(500):
        n = rng.randint(1, 7)
        points = rng.sample(list(itertools.product(range(-3, 5), repeat=2)), 2*n)
        a, b = points[:n], points[n:]
        expected = d_brute(a, b)
        data = str(n) + '\n' + ''.join(f'{x} {y}\n' for x, y in a + b)
        for ver in ('std', 'partial'):
            output, _ = run('passerby_' + ver, data)
            if (output.split()[0] == 'Yes') != expected or not check_d(data, output):
                fail('passerby_' + ver, data, output, expected)
    report['random']['passerby_grid_exhaustive'] = count
    report['random']['passerby_brute'] = 500
    print('passerby 网格穷举', count, '组、随机暴力 500 组通过', flush=True)

if __name__ == '__main__':
    samples()
    random_a()
    random_b()
    random_c()
    random_d()
    (ROOT / 'validation.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('ALL PASS', flush=True)
