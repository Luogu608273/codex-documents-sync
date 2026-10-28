from pathlib import Path
import json
import random
import statistics
import subprocess
import time

p = Path(__file__).resolve().parent
baseline = p.parent / 'p11234-debug-20261023/fixed.exe'
optimized = p / 'optimized.exe'
rng = random.Random(112342023)

def timed(exe, data):
    start = time.perf_counter()
    r = subprocess.run([str(exe)], input=data, capture_output=True, timeout=40)
    elapsed = time.perf_counter() - start
    if r.returncode:
        raise RuntimeError((str(exe), r.returncode, r.stderr.decode(errors='replace')))
    return elapsed, r.stdout

def make_random():
    n = m = 100000
    parts = [f'{n} {m}', ' '.join(str(rng.randrange(32)) for _ in range(n)),
             ' '.join(str(rng.randrange(1, n + 1)) for _ in range(m))]
    for r in range(1, 18):
        parts.append(''.join(str(rng.randrange(2)) for _ in range(1 << (17 - r))))
    parts.append('256')
    parts.extend(' '.join(str(rng.randrange(32)) for _ in range(4)) for _ in range(256))
    data = ('\n'.join(parts) + '\n').encode()
    (p / 'random_max.in').write_bytes(data)
    return data

cases = [('zero', (p.parent / 'p11234-debug-20261023/max.in').read_bytes()),
         ('random', make_random())]
report = []
for name, data in cases:
    times = [[], []]
    reference = None
    for repeat in range(3):
        order = [0, 1] if repeat % 2 == 0 else [1, 0]
        for which in order:
            elapsed, output = timed([baseline, optimized][which], data)
            times[which].append(elapsed)
            if reference is None:
                reference = output
            if output != reference:
                raise AssertionError(f'output mismatch case={name} repeat={repeat} variant={which}')
    old, new = map(statistics.median, times)
    row = dict(case=name, baseline_seconds=old, optimized_seconds=new,
               reduction_percent=100 * (1 - new / old), raw_seconds=times)
    report.append(row)
    print(json.dumps(row), flush=True)
(p / 'benchmark.json').write_text(json.dumps(report, indent=2), encoding='utf-8')
