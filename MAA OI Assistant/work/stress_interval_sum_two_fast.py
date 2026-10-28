import json
import random
import subprocess
import sys
import time
from pathlib import Path

root = Path(__file__).resolve().parent
folder = root / 'interval_sum_two_caps_bench'
rng = random.Random(19260817)
results = []
target = sys.argv[1] if len(sys.argv) > 1 else 'interval_sum_two_fast.exe'
for case in range(28):
    n = 500000
    density = (0.9, 0.7, 0.5, 0.3, 0.1, 0.01, 0.0001)[case % 7]
    ones = [i for i in range(n) if rng.random() < density]
    intervals = []
    for _ in range(500000):
        k = rng.randrange(len(ones) - 1)
        l = rng.randint(ones[k - 1] + 1 if k else 0, ones[k])
        r = rng.randint(ones[k + 1], ones[k + 2] - 1 if k + 2 < len(ones) else n - 1)
        intervals.append((l + 1, r + 1))
    if case // 7 == 1:
        intervals.sort()
    elif case // 7 == 2:
        intervals.sort(reverse=True)
    elif case // 7 == 3:
        intervals.sort(key=lambda p: (p[1], -p[0]))
    data = '1\n' + f'{n} {len(intervals)}\n' + ''.join(f'{l} {r}\n' for l, r in intervals)
    start = time.perf_counter()
    p = subprocess.run([str(root / target)], input=data, capture_output=True, text=True, timeout=10)
    row = dict(case=case, density=density, order=case // 7, answer=p.stdout.strip(), seconds=round(time.perf_counter() - start, 3), stats=p.stderr.strip())
    results.append(row)
    print(json.dumps(row), flush=True)
    (folder / (Path(target).stem + '_stress_report.json')).write_text(json.dumps(results, indent=2), encoding='utf-8')
    if p.stdout.strip() != 'Yes' or p.returncode:
        (folder / 'first_fast_false_no.in').write_text(data, encoding='utf-8')
        raise SystemExit('FAIL; seed=19260817; retained input')
print('PASS 28 maximum-size known-satisfiable instances')
