from pathlib import Path
import subprocess
import time
import random

root = Path(__file__).resolve().parent
source = Path(r'C:\Users\605\Downloads\1028\大样例')
exe = root / 'other_checks.exe'
for mode in ['seq', 'poly', 'name']:
    for inp in sorted((source / mode).glob('*.in')):
        expected = inp.with_suffix('.ans')
        if not expected.exists():
            expected = inp.with_suffix('.out')
        output = root / (inp.stem + '.actual')
        begin = time.perf_counter()
        with inp.open('rb') as fin, output.open('wb') as fout:
            subprocess.run([str(exe), mode], stdin=fin, stdout=fout, check=True)
        elapsed = time.perf_counter() - begin
        got, want = output.read_bytes().split(), expected.read_bytes().split()
        assert got == want, (mode, inp.name, 'sample mismatch')
        print(mode, inp.name, 'PASS', 'seconds=%.3f' % elapsed, flush=True)

# Original weight executable; independent recurrence on the set of possible
# current-item weights. This test does not use the submitted alternating sums.
def reference(b, H):
    low, high, ans = 0, H, 0
    for x in b:
        low, high = max(0, x - high), min(H, x - low)
        if low > high:
            ans += 1
            low, high = 0, H
    return ans

random.seed(20261028)
n, H = 200000, 1000000000
cases = [
    ('alternating_extremes', [0 if i % 2 else 2 * H for i in range(n - 1)]),
    ('all_zero', [0] * (n - 1)),
    ('all_maximum', [2 * H] * (n - 1)),
    ('all_H', [H] * (n - 1)),
    ('random_large', [random.randrange(2 * H + 1) for _ in range(n - 1)]),
]
for label, b in cases:
    (root / 'weight.in').write_text('%d %d\n%s\n' % (n, H, ' '.join(map(str, b))))
    subprocess.run([str(root / 'weight.exe')], cwd=str(root), check=True)
    got = int((root / 'weight.out').read_text())
    want = reference(b, H)
    assert got == want, (label, got, want)
    print('weight', label, 'PASS', got, flush=True)

# Bounds n=1 and n=2; exhaust all edge values for small H and both extremes
# for H=1e9, using the exact submitted executable.
for n, H, b in [(1, 1, []), (1, 10**9, [])] + [
    (2, H, [x]) for H in [1, 2, 10**9] for x in sorted(set([0, 1, H, 2 * H - 1, 2 * H]))
]:
    (root / 'weight.in').write_text('%d %d\n%s\n' % (n, H, ' '.join(map(str, b))))
    subprocess.run([str(root / 'weight.exe')], cwd=str(root), check=True)
    assert int((root / 'weight.out').read_text()) == 0
print('weight n=1/n=2 boundaries PASS', flush=True)
