from pathlib import Path
import subprocess
import time

root = Path(__file__).resolve().parent
samples = Path(r'C:\Users\605\Downloads\1028\大样例')
for inp in sorted((samples / 'seq').glob('*.in')):
    (root / 'seq.in').write_bytes(inp.read_bytes())
    subprocess.run([str(root / 'seq_user.exe')], cwd=str(root), check=True)
    assert (root / 'seq.out').read_bytes().split() == inp.with_suffix('.ans').read_bytes().split()
    print(inp.name, 'PASS', flush=True)

(root / 'poly.in').write_text('5 3\n2 4 1 5 8\n')
subprocess.run([str(root / 'poly.exe')], cwd=str(root), check=True)
assert list(map(int, (root / 'poly.out').read_text().split())) == [-1, -1, -1, 5, 8]
print('poly statement sample PASS', flush=True)
for inp in sorted((samples / 'poly').glob('*.in')):
    with inp.open() as f:
        n, k = map(int, f.readline().split())
    if n * k > 10000000:
        print(inp.name, 'SKIP n*k=%d' % (n * k), flush=True)
        continue
    (root / 'poly.in').write_bytes(inp.read_bytes())
    begin = time.perf_counter()
    subprocess.run([str(root / 'poly.exe')], cwd=str(root), check=True)
    elapsed = time.perf_counter() - begin
    assert (root / 'poly.out').read_bytes().split() == inp.with_suffix('.out').read_bytes().split()
    print(inp.name, 'PASS seconds=%.3f' % elapsed, flush=True)
