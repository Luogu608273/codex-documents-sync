from pathlib import Path
from collections import Counter
import random
import subprocess
import time
import json

OUT = Path(r'C:\Users\605\Documents\Output\debug-four-20261029')
WORK = Path(__file__).parent
rng = random.Random(20261029)
report = {}

def run(p, data, expected):
    inp = OUT / (p + '-max.in')
    inp.write_text(data)
    start = time.perf_counter()
    with inp.open() as f:
        r = subprocess.run([str(OUT / (p + '.exe'))], stdin=f,
                           capture_output=True, timeout=30)
    elapsed = time.perf_counter() - start
    assert r.returncode == 0, (p, r.returncode, r.stderr)
    assert r.stdout.decode().split() == expected.split(), p
    report[p] = round(elapsed, 3)
    print(p, 'max-size passed', round(elapsed, 3), 'seconds', flush=True)

n, l = 30000, 200
chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_@'
tails = [''.join(chars[(i >> (6*j)) & 63] for j in range(4)) for i in range(n)]
ans = 0
for j in range(4):
    counts = Counter(s[:j] + s[j+1:] for s in tails)
    ans += sum(c*(c-1)//2 for c in counts.values())
run('P4503', f'{n} {l} 64\n' + ''.join('a'*196 + s + '\n' for s in tails), str(ans))

n = 18
edges = [(u,v) for u in range(n) for v in range(n) if u != v]
run('P4802', f'{n} {len(edges)}\n' + ''.join(f'{u} {v} 10000\n' for u,v in edges), '170000')

n, q, mod = 200000, 200000, 1000000007
m = (10**18//n-1)*n+1
qs = [(rng.randint(1, 10**18), rng.randint(0, 10**18)) for _ in range(q)]
ans = []
for s, k in qs:
    if not k:
        ans.append(str(s % mod))
    else:
        first = 1 + (s+m-1)//n*n
        ans.append(str((first + (k-1)*(m//n)*n) % mod))
run('P11267', f'{n} {m} {q}\n' + '1'+'0'*(n-1)+'\n' +
    ''.join(f'{s} {k}\n' for s,k in qs), '\n'.join(ans))

m = 5000000
run('P10526', f'1 {m}\n' + 'a'*1000000 + '\n' + 'TE'*(m//2) + '\n', '1 '*(m//2))

(WORK / 'stress-results.json').write_text(json.dumps(report, indent=2))
print(report)
