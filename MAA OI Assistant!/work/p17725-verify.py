import itertools
import json
from pathlib import Path
import random
import subprocess
import time

root = Path(__file__).resolve().parent.parent
work = root / 'work'
sample = json.loads((work / 'p17725-page.json').read_text(encoding='utf-8'))['data']['problem']['samples'][0]
exe = str(work / 'p17725-std.exe')
r = subprocess.run([exe], input=sample[0], text=True, capture_output=True, check=True)
assert r.stdout.split() == sample[1].split(), r.stdout

seed = 177252026
rng = random.Random(seed)
cases = []
for n in range(1, 9):
    cases.extend(itertools.product(range(4), repeat=n))
for z in range(12000):
    n = rng.randint(1, 35)
    w = rng.choice([2, 4, 8, 16, 32, 64])
    a = [rng.randrange(w) for _ in range(n)]
    if z % 5 == 0:
        a[-1] = 0
    cases.append(a)

start = time.perf_counter()
for l in range(0, len(cases), 100):
    batch = cases[l:l + 100]
    inp = '0 %d\n' % len(batch) + ''.join(str(len(a)) + '\n' + ' '.join(map(str, a)) + '\n' for a in batch)
    x = subprocess.run([exe], input=inp, text=True, capture_output=True, check=True).stdout.split()
    y = subprocess.run([str(work / 'p17725-brute.exe')], input=inp, text=True, capture_output=True, check=True).stdout.split()
    if x != y:
        (work / 'p17725-first-failure.in').write_text(inp, encoding='ascii')
        for a, p, q in zip(batch, x, y):
            if p != q:
                raise AssertionError((seed, a, p, q))
result = {'sample': 'passed', 'seed': seed, 'exhaustive': sum(4 ** n for n in range(1, 9)), 'random': 12000, 'seconds': round(time.perf_counter() - start, 3)}
(root / 'outputs' / 'P17725' / 'validation.json').write_text(json.dumps(result, indent=2), encoding='utf-8')
print(json.dumps(result))
