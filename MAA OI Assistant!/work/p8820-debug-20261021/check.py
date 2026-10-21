import pathlib
import subprocess
import random
import collections
import heapq

root = pathlib.Path(__file__).resolve().parent
src = (root / 'original.cpp').read_text()
base = src.replace('freopen("transmit2.in", "r", stdin);', '')
start = base.replace('void dp1(int u, int v, Line & Li){', 'void dp1(int u, int v, Line & Li){\n\tu = fa[u];')
both = start.replace('mul(rc, vc[u].x, rc);', 'mul(vc[u].x, rc, rc);')
for name, code in [('original_stdin', base), ('fix_start', start), ('fix_both', both)]:
    (root / (name + '.cpp')).write_text(code)
    subprocess.run(['C:/TDM-GCC-64/bin/g++.exe', '-std=c++17', '-O2', '-Wall', '-Wextra', str(root / (name + '.cpp')), '-o', str(root / (name + '.exe'))], check=True)

def data(n, k, a, edges, qs):
    lines = ['%d %d %d' % (n, len(qs), k), ' '.join(map(str, a))]
    lines += ['%d %d' % e for e in edges + qs]
    return '\n'.join(lines) + '\n'

def run(name, inp):
    return list(map(int, subprocess.check_output([str(root / (name + '.exe'))], input=inp.encode()).split()))

def brute(n, k, a, edges, qs):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u-1].append(v-1)
        g[v-1].append(u-1)
    h = [[] for _ in range(n)]
    for s in range(n):
        d = [-1] * n
        d[s] = 0
        que = collections.deque([s])
        while que:
            u = que.popleft()
            for v in g[u]:
                if d[v] == -1:
                    d[v] = d[u] + 1
                    que.append(v)
        h[s] = [v for v in range(n) if 0 < d[v] <= k]
    ds = []
    for s in range(n):
        d = [10**30] * n
        d[s] = a[s]
        pq = [(d[s], s)]
        while pq:
            x, u = heapq.heappop(pq)
            if x != d[u]:
                continue
            for v in h[u]:
                y = x + a[v]
                if y < d[v]:
                    d[v] = y
                    heapq.heappush(pq, (y, v))
        ds.append(d)
    return [ds[u-1][v-1] for u,v in qs]

cases = [
    ('duplicate', data(2, 1, [1, 1], [(1,2)], [(1,2)])),
    ('offpath', data(6, 3, [1,100,100,100,1,1], [(1,2),(2,3),(3,4),(4,5),(3,6)], [(1,5)])),
]
for name, inp in cases:
    (root / (name + '.in')).write_text(inp)
    print(name, {v:run(v,inp) for v in ['original_stdin','fix_start','fix_both']}, flush=True)

rng = random.Random(8820)
for it in range(500):
    n = rng.randint(3, 12)
    k = 2
    a = [rng.randint(1,20) for _ in range(n)]
    edges = [(v, rng.randrange(1,v)) for v in range(2,n+1)]
    qs = [(u,v) for u in range(1,n+1) for v in range(u+1,n+1)]
    inp = data(n,k,a,edges,qs)
    want = brute(n,k,a,edges,qs)
    got = run('fix_start',inp)
    if got != want:
        idx = next(i for i in range(len(got)) if got[i] != want[i])
        inp = data(n,k,a,edges,[qs[idx]])
        (root / 'order.in').write_text(inp)
        print('order seed=8820 iteration=%d' % it, 'expected', want[idx], {v:run(v,inp) for v in ['original_stdin','fix_start','fix_both']}, '\n'+inp, flush=True)
        break

for k in [1, 2]:
    for it in range(150):
        n = rng.randint(2, 16)
        a = [rng.randint(1,100) for _ in range(n)]
        edges = [(v, rng.randrange(1,v)) for v in range(2,n+1)]
        qs = [(u,v) for u in range(1,n+1) for v in range(u+1,n+1)]
        inp = data(n,k,a,edges,qs)
        want = brute(n,k,a,edges,qs)
        got = run('fix_both',inp)
        if got != want:
            (root / 'unexpected.in').write_text(inp)
            raise AssertionError((k,it))
    print('fix_both k=%d: 150 random trees passed' % k, flush=True)
