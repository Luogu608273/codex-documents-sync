from pathlib import Path
import random
import subprocess
import time

root = Path(__file__).resolve().parent
src = (root / 'original.cpp').read_text()
(root / 'fixed.cpp').write_text(src.replace('else st.insert(a[i]);', 'else st.insert(i);').replace('s += tp.mn;', 's += a[tp.mn];'))
for name in ['original', 'fixed']:
    p = subprocess.run(['C:/TDM-GCC-64/bin/g++.exe', '-std=c++17', '-O2', '-Wall', '-Wextra', str(root / (name + '.cpp')), '-o', str(root / (name + '.exe'))], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    print(name + ' compiled; ' + p.stderr.strip())

def run(name, data):
    p = subprocess.run([str(root / (name + '.exe'))], input=data, capture_output=True, text=True, timeout=30)
    assert p.returncode == 0, (p.returncode, p.stderr)
    return list(map(int, p.stdout.split()))

counter = '11 1\n1 2 4 8 16 32 64 128 256 401 1000\n2 1 11\n'
(root / 'counterexample.in').write_text(counter)
print('counterexample:', run('original', counter), run('fixed', counter), 'expected [913]')
sample = '3 7\n1 3 2\n2 1 1\n2 2 2\n2 1 3\n1 3 1\n2 1 3\n1 1 5\n2 1 3\n'
assert run('fixed', sample) == [2, 1, 7, 6, 2]

def brute(a):
    limit = 4096
    mask = (1 << (limit + 1)) - 1
    bits = 1
    for v in a:
        if v <= limit:
            bits = (bits | (bits << v)) & mask
    missing = (~bits) & mask
    assert missing != 0
    return (missing & -missing).bit_length() - 1

queries = 0
for seed in range(50):
    rng = random.Random(seed)
    n = rng.randint(11, 30)
    a = [1, 2, 4, 8, 16, 32, 64, 128, 256, 401, 1000] + [rng.randint(1, 20) for _ in range(n - 11)]
    lines = [f'{n} 500', ' '.join(map(str, a))]
    expected = []
    for k in range(500):
        if rng.random() < .4:
            x = rng.randrange(n)
            v = rng.choice([1, 2, 3, 399, 400, 401, 402, 1000, 200000, rng.randint(1, 32)])
            lines.append(f'1 {x+1} {v}')
            a[x] = v
        else:
            l = rng.randrange(n)
            r = rng.randrange(l, n)
            lines.append(f'2 {l+1} {r+1}')
            expected.append(brute(a[l:r+1]))
    data = '\n'.join(lines) + '\n'
    actual = run('fixed', data)
    if actual != expected:
        (root / f'failure-seed-{seed}.in').write_text(data)
        raise AssertionError((seed, actual, expected))
    queries += len(expected)
print('50 seeds, 25000 operations,', queries, 'subset-DP checked queries passed')

for label, a in [
    ('large-enumeration', [1] * 400 + [401] * 199599 + [200000]),
    ('long-long', [1 << i for i in range(18)] + [200000] * 199982),
]:
    data = f'{len(a)} 1\n' + ' '.join(map(str, a)) + f'\n2 1 {len(a)}\n'
    expected = sum(a) + 1
    start = time.monotonic()
    actual = run('fixed', data)
    assert actual == [expected], (label, actual, expected)
    print(label, actual, 'passed', round(time.monotonic() - start, 3), 'seconds including process startup')
