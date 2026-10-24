from pathlib import Path
import subprocess
import time

p = Path(__file__).resolve().parent
source = (p / 'fixed.cpp').read_text(encoding='utf-8')
compiler = r'C:/TDM-GCC-64/bin/g++.exe'

def compile_one(name, text):
    (p / (name + '.cpp')).write_text(text, encoding='utf-8')
    subprocess.run([compiler, str(p / (name + '.cpp')), '-std=c++17', '-O2', '-Wall', '-Wextra', '-o', str(p / (name + '.exe'))], check=True)

def run(name, data):
    r = subprocess.run([str(p / (name + '.exe'))], input=data, text=True, capture_output=True, timeout=40, cwd=str(p))
    if r.returncode:
        raise RuntimeError((name, r.returncode, r.stderr))
    return r.stdout.strip()

compile_one('bad_equal', source.replace('a[l] >= lim', 'a[l] > lim'))
compile_one('bad_xor', source.replace('cin >> b[i];', 'cin >> b[i], b[i] = min(b[i], k);'))
equal_case = '2 2\n1 0\n1 2\n0\n1\n0 0 0 0\n'
xor_case = '2 2\n2 0\n1 2\n0\n1\n0 2 0 0\n'
(p / 'equal.in').write_text(equal_case, encoding='utf-8')
(p / 'xor.in').write_text(xor_case, encoding='utf-8')
assert run('fixed', equal_case) == '3'
assert run('bad_equal', equal_case) == '1'
assert run('fixed', xor_case) == '5'
assert run('bad_xor', xor_case) == '3'
print('REGRESSION PASS equality fixed=3 bad=1; xor fixed=5 bad=3')

n = 100000
m = 100000
groups = 256
query = [(i * 7907) % n + 1 for i in range(m)]
want = 0
for i, c in enumerate(query, 1):
    length = 1 << (c - 1).bit_length()
    value = c if c == length else (c + 1 + length) * (length - c) // 2
    want ^= i * value
parts = [f'{n} {m}', ' '.join(['2147483647'] * n), ' '.join(map(str, query))]
for r in range(1, 18):
    parts.append('0' * (1 << (17 - r)))
parts += [str(groups)] + ['2147483647 2147483647 2147483647 2147483647'] * groups
data = '\n'.join(parts) + '\n'
(p / 'max.in').write_text(data, encoding='utf-8')
start = time.perf_counter()
got = run('fixed', data).splitlines()
elapsed = time.perf_counter() - start
assert got == [str(want)] * groups
print(f'MAX PASS n=m=100000 T=256 expected={want} elapsed_seconds={elapsed:.3f}')
