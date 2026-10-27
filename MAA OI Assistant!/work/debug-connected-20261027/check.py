from collections import deque
from pathlib import Path
import random
import subprocess
import time

root = Path(__file__).resolve().parent
exe = root / 'main.exe'


def check(cases, name):
    data = [str(len(cases))]
    for n, edges, expected in cases:
        data.append(f'{n} {len(edges)}')
        data.extend(f'{u + 1} {v + 1}' for u, v in edges)
    start = time.perf_counter()
    result = subprocess.run([str(exe)], input='\n'.join(data) + '\n',
                            text=True, capture_output=True, timeout=30)
    if result.returncode:
        raise RuntimeError(result.stderr)
    output = list(map(int, result.stdout.split()))
    if len(output) != len(cases):
        raise AssertionError((name, len(output), len(cases)))
    for index, ((n, edges, expected), actual) in enumerate(zip(cases, output)):
        if actual != expected:
            failure = root / 'first-failure.in'
            failure.write_text('1\n' + f'{n} {len(edges)}\n' + ''.join(
                f'{u + 1} {v + 1}\n' for u, v in edges), encoding='utf-8')
            raise AssertionError((name, index, actual, expected, str(failure)))
    print(f'{name}: {len(cases)} cases passed ({time.perf_counter() - start:.3f}s)', flush=True)


check([
    (5, [(0, 1), (1, 2), (1, 4), (0, 3), (3, 4)], 4),
    (5, [(0, 1), (1, 2), (2, 3), (3, 4), (0, 4)], 5),
], 'samples')

# Enumerate all possible G and G' on at most five labeled vertices.
# The oracle groups them by all parity distances, taking the fewest edges.
all_cases = []
for n in range(2, 6):
    possible = [(u, v) for u in range(n) for v in range(u, n)]
    records = []
    best = {}
    for mask in range(1 << len(possible)):
        graph = [[] for _ in range(n)]
        edges = []
        for index, (u, v) in enumerate(possible):
            if mask >> index & 1:
                graph[u].append(v)
                graph[v].append(u)
                edges.append((u, v))
        dist = [-1] * (2 * n)
        dist[0] = 0
        q = deque([0])
        while q:
            state = q.popleft()
            u, p = divmod(state, 2)
            for v in graph[u]:
                target = 2 * v + (p ^ 1)
                if dist[target] == -1:
                    dist[target] = dist[state] + 1
                    q.append(target)
        if any(dist[2 * u] == dist[2 * u + 1] == -1 for u in range(n)):
            continue
        signature = tuple(dist)
        best[signature] = min(best.get(signature, len(possible)), len(edges))
        records.append((edges, signature))
    all_cases.extend((n, edges, best[signature]) for edges, signature in records)

random.Random(20261027).shuffle(all_cases)
batch, total = [], 0
for case in all_cases:
    if total + case[0] > 100000:
        check(batch, 'exhaustive-small-graphs')
        batch, total = [], 0
    batch.append(case)
    total += case[0]
if batch:
    check(batch, 'exhaustive-small-graphs')

n = 100000
edges = [(i, i + 1) for i in range(n - 1)] + [(n - 1, n - 1)]
check([(n, edges, n)], 'longest-class-chain')
edges = [(0, i) for i in range(1, n)] + [(0, 0)]
check([(n, edges, n)], 'largest-single-class')
check([(2, [(0, 1)] + ([(0, 0)] if i & 1 else []), 2 if i & 1 else 1)
       for i in range(50000)], 'maximum-test-count')
