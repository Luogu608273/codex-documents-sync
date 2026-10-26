import itertools
import pathlib
import random
import subprocess

root = pathlib.Path(__file__).resolve().parent
rng = random.Random(14363)

def brute(rules, a, b):
    ans = 0
    for x, y in rules:
        for p in range(len(a) - len(x) + 1):
            if a[p:p + len(x)] == x and a[:p] + y + a[p + len(x):] == b:
                ans += 1
    return ans

def check(rules, queries, name):
    data = f'{len(rules)} {len(queries)}\n'
    data += ''.join(a + ' ' + b + '\n' for a, b in rules + queries)
    expected = [brute(rules, a, b) for a, b in queries]
    result = subprocess.run([str(root / 'main.exe')], input=data, text=True,
                            capture_output=True, check=True)
    actual = list(map(int, result.stdout.split()))
    if actual != expected:
        (root / 'first_failure.in').write_text(data)
        (root / 'first_failure.expected').write_text('\n'.join(map(str, expected)))
        (root / 'first_failure.actual').write_text(result.stdout)
        raise AssertionError((name, 14363))
    return len(queries)

rules = []
for k in range(1, 4):
    words = [''.join(x) for x in itertools.product('ab', repeat=k)]
    rules += list(itertools.product(words, repeat=2))
rules += rules[:10]
words = [''.join(x) for k in range(1, 6)
         for x in itertools.product('ab', repeat=k)]
queries = [(a, b) for a in words for b in words if a != b]
total = check(rules, queries, 'exhaustive')

def word(k):
    return ''.join(rng.choice('abc') for _ in range(k))

for case in range(30):
    rules = []
    for _ in range(100):
        k = rng.randint(1, 12)
        rules.append((word(k), word(k)))
    rules += rules[:10]
    queries = []
    for _ in range(100):
        a, b = rng.choice(rules)
        left, right = word(rng.randrange(8)), word(rng.randrange(8))
        x, y = left + a + right, left + b + right
        if x != y:
            queries.append((x, y))
        x, y = word(rng.randint(1, 25)), word(rng.randint(1, 25))
        if x != y:
            queries.append((x, y))
    total += check(rules, queries, f'random {case}')

print(f'Passed {total} queries: exhaustive small alphabet + 30 random batches; seed=14363')
