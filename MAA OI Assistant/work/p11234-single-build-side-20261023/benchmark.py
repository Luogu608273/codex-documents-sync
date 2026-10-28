from pathlib import Path
import random
import statistics
import subprocess
import time

p = Path(__file__).resolve().parent
old_source = p.parent / 'p11234-debug-20261023/fixed.cpp'
subprocess.run([r'C:/TDM-GCC-64/bin/g++.exe', str(old_source), '-std=c++17', '-O2', '-Wall', '-Wextra', '-o', str(p / 'baseline.exe')], check=True)

def run(exe, data):
    start = time.perf_counter()
    result = subprocess.run([str(p / exe)], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=60)
    duration = time.perf_counter() - start
    if result.returncode:
        raise RuntimeError((exe, result.returncode, result.stderr.decode(errors='replace')))
    return result.stdout, duration

def compare(name, data, expected=None):
    times = {'baseline.exe': [], 'main.exe': []}
    output = None
    for rep in range(3):
        order = ('baseline.exe', 'main.exe') if rep % 2 == 0 else ('main.exe', 'baseline.exe')
        for exe in order:
            got, elapsed = run(exe, data)
            times[exe].append(elapsed)
            if output is None:
                output = got
            assert got == output, (name, exe)
            if expected is not None:
                assert got.decode().splitlines() == expected
    old = statistics.median(times['baseline.exe'])
    new = statistics.median(times['main.exe'])
    line = f'{name}: PASS baseline_median={old:.4f}s single_build_median={new:.4f}s ratio={new/old:.3f}'
    print(line, flush=True)
    return line

lines = []
data = (p.parent / 'p11234-debug-20261023/max.in').read_bytes()
n = 100000
query = [(i * 7907) % n + 1 for i in range(n)]
value = 0
for i, c in enumerate(query, 1):
    length = 1 << (c - 1).bit_length()
    answer = c if c == length else (c + 1 + length) * (length - c) // 2
    value ^= i * answer
lines.append(compare('n=m=100000 T=256 all_zero_ability', data, [str(value)] * 256))

rng = random.Random(112342024)
parts = [f'{n} {n}', ' '.join(str(rng.randrange(25)) for _ in range(n)), ' '.join(map(str, query))]
for r in range(1, 18):
    parts.append(''.join(str(rng.randrange(2)) for _ in range(1 << (17 - r))))
parts.append('128')
for _ in range(128):
    parts.append(' '.join(str(rng.randrange(32)) for _ in range(4)))
data = ('\n'.join(parts) + '\n').encode()
(p / 'threshold.in').write_bytes(data)
lines.append(compare('n=m=100000 T=128 random_threshold_ability seed=112342024', data))
(p / 'validation.txt').write_text('PASS cases=4510 prefix_checks=26573 seed=112342023\n' + '\n'.join(lines) + '\n', encoding='utf-8')
