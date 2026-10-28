import itertools
import pathlib
import subprocess

root = pathlib.Path(__file__).resolve().parent
cases = [(n, a) for n in range(4, 17) for a in itertools.combinations(range(1, n), n // 2)]
p = subprocess.Popen([str(root / 'arc233_a_debug.exe')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
def send(s):
    p.stdin.write(str(s) + '\n')
    p.stdin.flush()
send(len(cases))
for n, a in cases:
    send(n)
    q = 0
    while True:
        line = p.stdout.readline().split()
        assert len(line) == 2, (n, a, line)
        op, x = line[0], int(line[1])
        if op == '?':
            q += 1
            assert 1 <= x < n and q <= 3 * n // 4, (n, a, q, x)
            send('Yes' if x in a else 'No')
        else:
            assert op == '!', (n, a, line)
            f = [n + 1] * (n + 1)
            f[0] = 0
            for v in a:
                for j in range(n, v - 1, -1):
                    f[j] = min(f[j], f[j - v] + 1)
            want = f[n] if f[n] <= n else -1
            assert x == want, (n, a, x, want)
            break
p.stdin.close()
assert p.wait(timeout=5) == 0
print('PASS:', len(cases), 'sets; answer, query range, query limit and Yes/No protocol checked')
p = subprocess.Popen([str(root / 'arc233_a_debug.exe')], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True, bufsize=1)
p.stdin.write('1\n4\n')
p.stdin.flush()
assert p.stdout.readline().strip() == '? 1'
p.stdin.write('-1\n')
p.stdin.flush()
assert p.wait(timeout=5) == 0
assert p.stdout.read() == ''
print('PASS: immediate exit after -1')
