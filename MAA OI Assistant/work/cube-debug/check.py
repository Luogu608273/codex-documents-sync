from pathlib import Path
import subprocess
import random
import itertools
import time

root = Path(__file__).resolve().parent
samples = Path(r'C:\Users\605\Downloads\contest_2224\cube')
exe = str(root / 'brute.exe')

def run(data, timeout=10):
    start = time.perf_counter()
    p = subprocess.run([exe], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, timeout=timeout)
    return int(p.stdout), time.perf_counter() - start

for i in [1, 2, 3, 4, 5, 7]:
    path = samples / f'ex_cube{i}.in'
    try:
        ans, elapsed = run(path.read_bytes())
        expected = int(path.with_suffix('.out').read_text())
        print(path.name, 'PASS' if ans == expected else ('FAIL', ans, expected), f'{elapsed:.3f}s', flush=True)
    except subprocess.TimeoutExpired:
        print(path.name, 'TIMEOUT 10s', flush=True)

def brute(a, b, c, removed):
    unvisited = set(itertools.product(range(a), range(b), range(c))) - removed
    ans = 0
    while unvisited:
        ans += 1
        q = [unvisited.pop()]
        for x, y, z in q:
            for u, v, w in [(x-1,y,z),(x+1,y,z),(x,y-1,z),(x,y+1,z),(x,y,z-1),(x,y,z+1)]:
                if (u,v,w) in unvisited:
                    unvisited.remove((u,v,w))
                    q.append((u,v,w))
    return ans

seed = 20261027
rng = random.Random(seed)
for i in range(1000):
    a, b, c = [rng.randint(1, 7) for _ in range(3)]
    cells = list(itertools.product(range(a), range(b), range(c)))
    removed = set(rng.sample(cells, rng.randrange(len(cells))))
    data = (f'{a} {b} {c} {len(removed)}\n' + ''.join(f'{x} {y} {z}\n' for x,y,z in removed)).encode()
    ans, _ = run(data)
    expected = brute(a, b, c, removed)
    if ans != expected:
        (root / 'first_mismatch.in').write_bytes(data)
        print('FAIL', seed, i, ans, expected, flush=True)
        raise SystemExit(1)
print('Random PASS: 1000, seed:', seed)
print('Source bytes:', (root / 'brute.cpp').stat().st_size)
