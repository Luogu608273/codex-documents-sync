from pathlib import Path
import heapq
import random
import subprocess

root = Path(__file__).resolve().parent
rng = random.Random(20261020)

def brute(n, edges):
    g = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        g[u].append((v, w))
        g[v].append((u, w))
    dis = {(1, 0): 0}
    pq = [(0, 1, 0)]
    while pq:
        d, u, last = heapq.heappop(pq)
        if dis[u, last] != d:
            continue
        for v, w in g[u]:
            nd = d + max(last, w)
            if nd < dis.get((v, w), 10**30):
                dis[v, w] = nd
                heapq.heappush(pq, (nd, v, w))
    return min(d + last for (u, last), d in dis.items() if u == n)

def check(n, edges, expected=None):
    data = '{} {}\n'.format(n, len(edges)) + ''.join('{} {} {}\n'.format(*e) for e in edges)
    if expected is None:
        expected = brute(n, edges)
    p = subprocess.run([str(root / 'p6822-fixed.exe')], input=data.encode(), stdout=subprocess.PIPE, timeout=15)
    if p.returncode or int(p.stdout) != expected:
        (root / 'p6822-fixed-first-failure.in').write_text(data)
        raise RuntimeError((p.returncode, p.stdout, expected))

check(4, [(1, 2, 1), (2, 3, 2), (2, 4, 3)], 7)
check(3, [(1, 3, 1)], 2)
check(1, [(1, 1, 7)], 0)
for case in range(200):
    n = rng.randint(2, 12)
    edges = []
    for u in range(2, n + 1):
        edges.append((u, rng.randrange(1, u), rng.choice([1, 2, 3, 10**6, rng.randint(1, 50)])))
    for _ in range(rng.randrange(25)):
        u, v = rng.sample(range(1, n + 1), 2)
        edges.append((u, v, rng.choice([1, 2, 3, 10**6, rng.randint(1, 50)])))
    check(n, edges)
print('200 random cases and 3 targeted cases passed; seed=20261020', flush=True)
n = 100000
edges = [(u, u + 1, 10**6) for u in range(1, n)]
while len(edges) < 200000:
    u = rng.randrange(1, n)
    edges.append((u, u + 1, 10**6))
check(n, edges, n * 10**6)
print('n=100000 m=200000 boundary passed; answer=100000000000', flush=True)
