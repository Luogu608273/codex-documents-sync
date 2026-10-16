import json
import random
import subprocess
import time
from pathlib import Path

root = Path(__file__).resolve().parent
folder = root / 'interval_sum_two_caps_bench'
folder.mkdir(exist_ok=True)
rng = random.Random(20261010)
report = []

def run_case(name, n, intervals, expected):
    path = folder / (name + '.in')
    path.write_text('1\n' + f'{n} {len(intervals)}\n' + ''.join(f'{l} {r}\n' for l, r in intervals), encoding='utf-8')
    results = {}
    for target in ('interval_sum_two_original_caps.exe', 'interval_sum_two_fast.exe'):
        start = time.perf_counter()
        with path.open('r') as stream:
            try:
                p = subprocess.run([str(root / target)], stdin=stream, capture_output=True, text=True, timeout=20)
                results[target] = dict(answer=p.stdout.strip(), seconds=round(time.perf_counter() - start, 3), stats=p.stderr.strip(), exit=p.returncode)
            except subprocess.TimeoutExpired:
                results[target] = dict(answer='TIMEOUT', seconds=20)
    row = dict(name=name, n=n, m=len(intervals), expected=expected, results=results)
    report.append(row)
    print(json.dumps(row, ensure_ascii=False), flush=True)
    (folder / 'report.json').write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding='utf-8')

n = 500000
run_case('all_adjacent', n, [(i, i + 1) for i in range(1, n)], 'Yes')
run_case('long_negative_cycle', n, [(i, i + 1) for i in range(1, n)] + [(1, n)], 'No')

for density in (0.5, 0.02, 0.0002):
    ones = [i for i in range(n) if rng.random() < density]
    intervals = []
    for _ in range(500000):
        k = rng.randrange(len(ones) - 1)
        l = rng.randint(ones[k - 1] + 1 if k else 0, ones[k])
        r = rng.randint(ones[k + 1], ones[k + 2] - 1 if k + 2 < len(ones) else n - 1)
        intervals.append((l + 1, r + 1))
    run_case('known_yes_' + str(density), n, intervals, 'Yes')

run_case('nested_two_ones', n, [(rng.randint(1, n // 2), rng.randint(n // 2 + 1, n)) for _ in range(500000)], 'Yes')
