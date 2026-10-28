import collections
import itertools
import pathlib
import random
import string
import subprocess

root = pathlib.Path(__file__).resolve().parent
cases = [('abc', 'abc', 0), ('BBC', 'ABC', -1), ('abc', 'bbc', 1),
         ('ABCD', 'BACD', 3), ('abc', 'baa', 3), ('abc', 'bca', 4)]
letters = string.ascii_uppercase + string.ascii_lowercase
cases += [(letters, 'BADD' + letters[4:], 4),
          (letters, 'BAA' + letters[3:], 3),
          (letters, 'BA' + letters[2:], -1), (letters, letters, 0)]
random.seed(9013)
for length in range(1, 6):
    sources = list(itertools.product(range(4), repeat=length))
    random.shuffle(sources)
    for source in sources[:10]:
        dist = {source: 0}
        q = collections.deque([source])
        while q:
            u = q.popleft()
            for a in set(u):
                for b in range(5):
                    if a == b:
                        continue
                    v = tuple(b if c == a else c for c in u)
                    if v not in dist:
                        dist[v] = dist[u] + 1
                        q.append(v)
        for _ in range(10):
            target = tuple(random.randrange(4) for _ in range(length))
            s = ''.join('ABCD'[x] for x in source)
            t = ''.join('ABCD'[x] for x in target)
            cases.append((s, t, dist.get(target, -1)))
for start in range(0, len(cases), 10):
    batch = cases[start:start + 10]
    data = str(len(batch)) + '\n' + ''.join(s + '\n' + t + '\n' for s, t, _ in batch)
    run = subprocess.run([str(root / 'p9013_debug.exe')], input=data, text=True,
                         capture_output=True, check=True)
    actual = list(map(int, run.stdout.split()))
    expected = [ans for _, _, ans in batch]
    if actual != expected:
        (root / 'p9013_first_mismatch.in').write_text(data)
        raise AssertionError((start, batch, actual, expected, 'seed=9013'))
print('PASS:', len(cases), 'cases; BFS alphabet=5; seed=9013')
