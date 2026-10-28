from pathlib import Path
import subprocess
import itertools
import random
import time

root = Path(__file__).resolve().parent
samples = Path(r'C:\Users\605\Downloads\contest_2224\persona')

def run(name, data):
    start = time.perf_counter()
    p = subprocess.run([str(root / (name + '.exe'))], input=data, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    return p.stdout.decode().split(), time.perf_counter() - start

def pack(cases):
    lines = [str(len(cases))]
    for n, rules in cases:
        lines.append(f'{n} {len(rules)}')
        for c, ds in rules:
            lines.append(f'{c} {len(ds)}' + ''.join(' ' + str(d) for d in ds))
    return ('\n'.join(lines) + '\n').encode()

def brute(n, rules):
    f = [set() for _ in range(n + 1)]
    changed = True
    while changed:
        changed = False
        for c, ds in rules:
            s = {0}
            for d in ds:
                t = {1} if isinstance(d, str) else f[d]
                s = {x ^ y for x in s for y in t}
            old = len(f[c])
            f[c] |= s
            changed |= len(f[c]) != old
    return 'YES' if 1 in f[1] else 'NO'

for path in sorted(samples.glob('*.in')):
    ans, elapsed = run('fixed', path.read_bytes())
    expected = path.with_suffix('.out').read_text().split()
    print(path.name, 'PASS' if ans == expected else ('FAIL', ans, expected), f'{elapsed:.3f}s')

hack = (root / 'hack.in').read_bytes()
print('First 5 original:', run('original', hack)[0])
print('First 5 fixed:', run('fixed', hack)[0])

targeted = [
    (1, []),
    (1, [(1, ('a', 'a')), (1, (1, 'a'))]),
    (1, [(1, (1, 'a')), (1, ('a', 'a'))]),
    (1, [(1, (1, 1)), (1, ('a',))]),
    (2, [(2, ('a',)), (2, (2, 2, 2, 'a', 'a')), (1, ('a', 'a'))]),
]
print('Targeted expected:', [brute(*case) for case in targeted])
print('Targeted original:', run('original', pack(targeted))[0])
print('Targeted fixed:', run('fixed', pack(targeted))[0])
(root / 'targeted.in').write_bytes(pack(targeted))

cases = []
options = [(1, ds) for k in range(4) for ds in itertools.product((1, 'a', 'b'), repeat=k)]
for m in range(4):
    for rules in itertools.combinations_with_replacement(options, m):
        cases.append((1, list(rules)))
seed = 20261027
rng = random.Random(seed)
for _ in range(30000):
    n = rng.randrange(1, 7)
    symbols = list(range(1, n + 1)) + ['a', 'b']
    rules = [(rng.randrange(1, n + 1), tuple(rng.choice(symbols) for _ in range(rng.randrange(7)))) for _ in range(rng.randrange(13))]
    cases.append((n, rules))

for offset in range(0, len(cases), 1000):
    group = cases[offset:offset + 1000]
    ans = run('fixed', pack(group))[0]
    expected = [brute(*case) for case in group]
    if ans != expected:
        i = next(i for i, (a, b) in enumerate(zip(ans, expected)) if a != b)
        (root / 'first_mismatch.in').write_bytes(pack([group[i]]))
        print('FAIL', seed, offset + i, ans[i], expected[i])
        raise SystemExit(1)
print('Exhaustive/random PASS:', len(cases), 'seed:', seed)
