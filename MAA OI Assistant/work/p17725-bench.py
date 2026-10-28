from pathlib import Path
import json
import random
import subprocess
import time

root = Path(__file__).resolve().parent.parent
w = root / 'work'
s = (root / 'outputs' / 'P17725' / 'std.cpp').read_text(encoding='utf-8')
s = s.replace('printf("%d\\n", g -', 'fprintf(stderr, "nodes=%d\\n", tot);\n    printf("%d\\n", g -')
(w / 'p17725-instrument.cpp').write_text(s, encoding='utf-8')
subprocess.run(['C:/TDM-GCC-64/bin/g++.exe', str(w / 'p17725-instrument.cpp'), '-o', str(w / 'p17725-instrument.exe'), '-std=c++17', '-O2', '-Wall', '-Wextra'], check=True)
rng = random.Random(177252026)
n = 1000000
p = w / 'p17725-scale.in'
with p.open('w', encoding='ascii') as f:
    f.write('0 5\n')
    for kind in range(5):
        f.write(str(n) + '\n')
        if kind == 0:
            a = [0] * n
        elif kind == 1:
            a = list(range(n))
        elif kind == 2:
            a = list(range(n, 0, -1))
        elif kind == 3:
            a = [rng.randrange(1 << 30) for _ in range(n)]
        else:
            a = [rng.randrange(16) for _ in range(n)]
        f.write(' '.join(map(str, a)) + '\n')
with p.open('r', encoding='ascii') as f:
    start = time.perf_counter()
    r = subprocess.run([str(w / 'p17725-instrument.exe')], stdin=f, text=True, capture_output=True, check=True)
    elapsed = time.perf_counter() - start
print(json.dumps({'n': n, 'total_n': 5*n, 'seconds': round(elapsed, 3), 'answers': r.stdout.split(), 'nodes': r.stderr.splitlines()}))
