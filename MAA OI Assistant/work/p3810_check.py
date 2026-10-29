import random
import subprocess
from pathlib import Path

root = Path(__file__).resolve().parent
rng = random.Random(3810)
exe = root / 'p3810_original.exe'

def run(a):
    data = f'{len(a)} 4\n' + ''.join('%d %d %d\n' % p for p in a)
    got = list(map(int, subprocess.check_output([str(exe)], input=data.encode()).split()))
    want = [0] * len(a)
    for p in a:
        v = sum(all(q[j] <= p[j] for j in range(3)) for q in a) - 1
        want[v] += 1
    return data, got, want

for case in range(2000):
    n = rng.randint(17, 60)
    a = [tuple(rng.randint(1, 4) for _ in range(3)) for _ in range(n)]
    if case % 2 == 0:
        a = [(1, 1, 1)] * (n // 2) + a[n // 2:]
    data, got, want = run(a)
    if got != want:
        (root / 'p3810_first_failure.in').write_text(data)
        (root / 'p3810_first_failure.txt').write_text(f'seed=3810 case={case}\ngot={got}\nwant={want}\n')
        changed = True
        while changed:
            changed = False
            for i in range(len(a)):
                b = a[:i] + a[i+1:]
                if b and run(b)[1] != run(b)[2]:
                    a = b
                    changed = True
                    break
        data, got, want = run(a)
        (root / 'p3810_small_failure.in').write_text(data)
        print(data, 'got=', got, '\nwant=', want)
        break
else:
    print('No failure found')
