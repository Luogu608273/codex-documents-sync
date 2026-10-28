import random
import subprocess
import time
from pathlib import Path

base = Path(__file__).resolve().parent
exe = base / 'combo_complete.exe'
seed = 2202
rng = random.Random(seed)

def brute(patterns, text):
    return sum(all(s in text[l:r] for s in patterns)
               for l in range(len(text)) for r in range(l + 1, len(text) + 1))

cases = [
    (['ab', 'ba'], 'abab'),
    (['b', 'b'], 'bbb'),
    (['b', 'b', 'ab'], 'abab'),
    (['a', 'aa', 'aaa'], 'aaaaa'),
    (['ab', 'bc', 'cd'], 'abcdabcd'),
    (['a', 'b', 'c', 'd'], 'aaa'),
    (['a'], 'aaaa'),
    (['abcd', 'bca', 'da'], 'abcdabcada'),
]
for _ in range(12000):
    patterns = []
    for _ in range(rng.randint(1, 8)):
        if patterns and rng.randrange(5) == 0:
            patterns.append(rng.choice(patterns))
        else:
            patterns.append(''.join(rng.choice('abcd') for _ in range(rng.randint(1, 6))))
    text = ''.join(rng.choice('abcd') for _ in range(rng.randint(1, 18)))
    cases.append((patterns, text))

data = [str(len(cases))]
expected = []
for patterns, text in cases:
    assert all(set(s) <= set('abcd') for s in [*patterns, text])
    data.extend([str(len(patterns)), *patterns, text])
    expected.append(brute(patterns, text))
run = subprocess.run([str(exe)], input='\n'.join(data) + '\n', text=True,
                     capture_output=True, check=True)
actual = list(map(int, run.stdout.split()))
if len(actual) != len(expected):
    raise AssertionError((len(actual), len(expected), run.stderr))
for i, (a, b) in enumerate(zip(actual, expected)):
    if a != b:
        patterns, text = cases[i]
        failure = base / 'combo_complete_first_failure.in'
        failure.write_text('\n'.join(['1', str(len(patterns)), *patterns, text]) + '\n')
        raise AssertionError((seed, i, cases[i], a, b, str(failure)))
print(f'PASS brute cases={len(cases)} seed={seed}')

length = 1999998
data = f'2\n1\n{"a" * length}\n{"a" * length}\n1\nb\nbb\n'
start = time.perf_counter()
run = subprocess.run([str(exe)], input=data, text=True, capture_output=True, check=True)
assert list(map(int, run.stdout.split())) == [1, 3], run.stdout
print(f'PASS deep fail tree and reset nodes={length} local_seconds={time.perf_counter() - start:.3f}')

length = 2000000
run = subprocess.run([str(exe)], input=f'1\n1\na\n{"a" * length}\n',
                     text=True, capture_output=True, check=True)
assert int(run.stdout) == length * (length + 1) // 2, run.stdout
print(f'PASS 64-bit answer={run.stdout.strip()}')
