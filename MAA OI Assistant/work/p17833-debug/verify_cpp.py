import itertools
import json
from pathlib import Path
import random
import subprocess
import time
from check import brute


def main():
    cases = []
    for n in range(1, 9):
        for gaps in itertools.product(range(1, 4), repeat=n - 1):
            x = [0]
            for g in gaps:
                x.append(x[-1] + g)
            for d in range(1, 8):
                cases.append((x, d))
    rng = random.Random(17833)
    for _ in range(10000):
        n = rng.randint(1, 18)
        x = sorted(rng.sample(range(-100, 101), n))
        cases.append((x, rng.randint(1, 80)))
    cases.extend([
        ([-10**18, 10**18], 2 * 10**18),
        ([-10**18, 0, 10**18], 10**18),
        ([-10**18 + 4 * 10**17 * i for i in range(6)], 8 * 10**17),
        ([-10**18 + (2 * 10**18 // 7) * i for i in [0, 1, 2, 4, 6, 7]], 3 * (2 * 10**18 // 7)),
    ])
    out = Path(r'C:\Users\605\Documents\Output\p17833-debug')
    text = ['0 {}'.format(len(cases))]
    expected = []
    for x, d in cases:
        text.extend(['{} {}'.format(len(x), d), ' '.join(map(str, x))])
        expected.append(len(brute(x, d)))
    data = '\n'.join(text) + '\n'
    (out / 'batch.in').write_text(data)
    p = subprocess.run([str(out / 'fixed.exe')], input=data, capture_output=True, text=True, check=True)
    actual = list(map(int, p.stdout.split()))
    assert actual == expected, next((i, cases[i], actual[i], expected[i]) for i in range(len(cases)) if actual[i] != expected[i])
    n = 1999999
    data = '0 2\n{} 2\n{}\n1 1\n0\n'.format(n, ' '.join(map(str, range(n))))
    (out / 'large.in').write_text(data)
    start = time.perf_counter()
    p = subprocess.run([str(out / 'fixed.exe')], input=data, capture_output=True, text=True, check=True)
    elapsed = time.perf_counter() - start
    assert list(map(int, p.stdout.split())) == [n - 3, 0], p.stdout
    result = dict(cpp_cases=len(cases), seed=17833, large_n=n, total_large_n=n+1, large_seconds=elapsed, status='PASS')
    Path(__file__).with_name('cpp-verification.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result))


if __name__ == '__main__':
    main()
