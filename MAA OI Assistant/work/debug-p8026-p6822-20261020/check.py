import ctypes
import random
import subprocess
import time
from pathlib import Path

root = Path(__file__).resolve().parent
rng = random.Random(20261020)
for case in range(60):
    n = rng.randint(2, 14)
    k = rng.choice([1, 2, 3, 5, 200])
    q = rng.randint(30, 160)
    fa = [list(range(n + 1)) for _ in range(k)]
    def find(i, x):
        while fa[i][x] != x:
            x = fa[i][x]
        return x
    ops, expected = [], []
    for _ in range(q):
        u, v, i = rng.randint(1, n), rng.randint(1, n), rng.randrange(k)
        ops.append((u, v, i + 1))
        fa[i][find(i, u)] = find(i, v)
        groups = {}
        for x in range(1, n + 1):
            key = tuple(find(j, x) for j in range(k))
            groups[key] = groups.get(key, 0) + 1
        expected.append(sum(s * s for s in groups.values()))
    data = '{} {} {}\n'.format(k, n, q) + ''.join('{} {} {}\n'.format(*op) for op in ops)
    p = subprocess.run([str(root / 'p8026.exe')], input=data.encode(), stdout=subprocess.PIPE, timeout=10)
    actual = list(map(int, p.stdout.split()))
    if p.returncode or actual != expected:
        (root / 'p8026-first-failure.in').write_text(data)
        raise RuntimeError(('p8026 mismatch', case, p.returncode, actual, expected))
print('P8026: 60 random cases passed, seed=20261020', flush=True)
for name in ['p6822-wa.in', 'p6822-isolated.in']:
    p = subprocess.run([str(root / 'p6822.exe')], input=(root / name).read_bytes(), stdout=subprocess.PIPE, timeout=10)
    print(name, 'exit=', p.returncode, 'stdout=', p.stdout.decode(), flush=True)

n, k = 5000, 200
merges = []
step = 1
while step < n:
    for l in range(1, n + 1, step * 2):
        if l + step <= n:
            merges.append((l, l + step))
    step *= 2
assert len(merges) == n - 1
path = root / 'p8026-balanced-max.in'
with path.open('w') as f:
    f.write('{} {} {}\n'.format(k, n, k * len(merges)))
    for i in range(1, k + 1):
        for u, v in merges:
            f.write('{} {} {}\n'.format(u, v, i))

class Counters(ctypes.Structure):
    _fields_ = [('cb', ctypes.c_ulong), ('PageFaultCount', ctypes.c_ulong)] + [(s, ctypes.c_size_t) for s in ['PeakWorkingSetSize', 'WorkingSetSize', 'QuotaPeakPagedPoolUsage', 'QuotaPagedPoolUsage', 'QuotaPeakNonPagedPoolUsage', 'QuotaNonPagedPoolUsage', 'PagefileUsage', 'PeakPagefileUsage']]
get_info = ctypes.WinDLL('psapi').GetProcessMemoryInfo
get_info.argtypes = [ctypes.c_void_p, ctypes.POINTER(Counters), ctypes.c_ulong]
peak = 0
t = time.perf_counter()
with path.open('rb') as f:
    p = subprocess.Popen([str(root / 'p8026.exe')], stdin=f, stdout=subprocess.DEVNULL)
    while p.poll() is None:
        c = Counters()
        c.cb = ctypes.sizeof(c)
        if get_info(int(p._handle), ctypes.byref(c), c.cb):
            peak = max(peak, c.PeakWorkingSetSize)
        if time.perf_counter() - t > 90:
            p.kill()
            raise RuntimeError('benchmark timeout')
        time.sleep(0.05)
print('P8026 max balanced: exit={}, seconds={:.3f}, local Windows peak working set={:.1f} MiB'.format(p.returncode, time.perf_counter() - t, peak / 2**20), flush=True)
