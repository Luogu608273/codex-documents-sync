import itertools
import random
import subprocess
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
rng = random.Random(20261010)
cases = []
expected = []

def add_case(n, intervals):
    ok = any(
        all(sum(x[l - 1:r]) == 2 for l, r in intervals)
        for x in itertools.product((0, 1), repeat=n)
    )
    cases.append((n, intervals))
    expected.append('Yes' if ok else 'No')

for n in range(2, 6):
    intervals = [(l, r) for l in range(1, n + 1) for r in range(l + 1, n + 1)]
    for mask in range(1, 1 << len(intervals)):
        add_case(n, [p for i, p in enumerate(intervals) if mask >> i & 1])

for _ in range(1000):
    n = rng.randint(2, 9)
    intervals = [(l, r) for l in range(1, n + 1) for r in range(l + 1, n + 1)]
    rng.shuffle(intervals)
    chosen = intervals[:rng.randint(1, len(intervals))]
    if rng.randrange(2):
        chosen = chosen + chosen[:rng.randint(1, len(chosen))]
    add_case(n, chosen)

data = [str(len(cases))]
for n, intervals in cases:
    data.append(f'{n} {len(intervals)}')
    data.extend(f'{l} {r}' for l, r in intervals)
target = sys.argv[1] if len(sys.argv) > 1 else 'interval_sum_two_debug.exe'
result = subprocess.run([str(root / target)],
    input='\n'.join(data) + '\n', capture_output=True, text=True, timeout=20, check=True)
actual = result.stdout.split()
for i, ((n, intervals), want, got) in enumerate(zip(cases, expected, actual)):
    if want != got:
        (root / 'interval_sum_two_first_failure.in').write_text(
            '1\n' + f'{n} {len(intervals)}\n' + ''.join(f'{l} {r}\n' for l, r in intervals),
            encoding='utf-8')
        raise SystemExit(f'MISMATCH case={i} seed=20261010 expected={want} actual={got}')
assert len(actual) == len(expected), (len(actual), len(expected), result.stderr)
print(f'PASS {len(cases)} cases; exhaustive n<=5 plus 1000 random cases; seed=20261010')
