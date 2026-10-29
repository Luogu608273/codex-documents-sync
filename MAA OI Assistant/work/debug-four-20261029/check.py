from pathlib import Path
import random
import string
import subprocess
import json
import time

OUT = Path(r'C:\Users\605\Documents\Output\debug-four-20261029')
WORK = Path(__file__).parent
SEED = 20261029
rng = random.Random(SEED)
stats = {}

def run(p, data, original=False, timeout=10):
    name = p + ('-original' if original else '')
    r = subprocess.run([str(OUT / (name + '.exe'))], input=data, text=True,
                       capture_output=True, timeout=timeout)
    if r.returncode:
        raise RuntimeError((name, r.returncode, r.stderr))
    return list(map(int, r.stdout.split()))

def check(p, data, expected):
    actual = run(p, data)
    if actual != expected:
        (OUT / (p + '-failure.in')).write_text(data)
        (WORK / (p + '-failure.json')).write_text(json.dumps({
            'seed': SEED, 'expected': expected, 'actual': actual}))
        raise AssertionError((p, expected[:20], actual[:20]))
    stats[p] = stats.get(p, 0) + 1

def repro(p, data, expected, name='repro'):
    (OUT / (p + '-' + name + '.in')).write_text(data)
    old = run(p, data, True)
    print(p, name, 'original:', old, 'expected:', expected, flush=True)
    check(p, data, expected)

alphabet = string.ascii_lowercase + string.ascii_uppercase + string.digits + '_@'
values = {c: i+1 for i, c in enumerate(alphabet)}
seen = {}
for it in range(300000):
    s = 'a' + ''.join(rng.choices(alphabet, k=9))
    h = 65
    for c in s[1:]:
        h = (h * 13331 + values[c]) % 1000000003
    if h in seen and seen[h] != s:
        a, b = seen[h], s
        break
    seen[h] = s
else:
    raise AssertionError('No collision found')
assert sum(x != y for x, y in zip(a, b)) > 1
repro('P4503', '2 10 64\n' + a + '\n' + b + '\n', [0], 'collision')
print('collision strings:', a, b, flush=True)
check('P4503', '4 3 64\nFax\nfax\nmax\nmac\n', [4])
for _ in range(100):
    l = rng.randint(2, 30)
    n = rng.randint(2, 100)
    strings = set()
    while len(strings) < n:
        if strings and rng.random() < .6:
            s = list(rng.choice(sorted(strings)))
            s[rng.randrange(l)] = rng.choice(alphabet)
            strings.add(''.join(s))
        else:
            strings.add(''.join(rng.choices(alphabet, k=l)))
    strings = sorted(strings)
    ans = sum(sum(x != y for x, y in zip(a, b)) == 1
              for i, a in enumerate(strings) for b in strings[:i])
    check('P4503', f'{n} {l} 64\n' + '\n'.join(strings) + '\n', [ans])

repro('P4802', '3 1\n0 2 5\n', [5])
check('P4802', '3 3\n0 2 5\n0 1 4\n1 2 3\n', [7])
for _ in range(150):
    n = rng.randint(2, 8)
    edges = {(u, v): rng.randint(1, 10000)
             for u in range(n) for v in range(n)
             if u != v and rng.random() < .35}
    edges[0, n-1] = rng.randint(1, 10000)
    ans = [0]
    def dfs(u, mask, dist):
        if u == n-1:
            ans[0] = max(ans[0], dist)
            return
        for v in range(n):
            if not (mask >> v & 1) and (u, v) in edges:
                dfs(v, mask | 1 << v, dist + edges[u, v])
    dfs(0, 1, 0)
    data = f'{n} {len(edges)}\n' + ''.join(f'{u} {v} {w}\n' for (u,v),w in edges.items())
    check('P4802', data, ans)

repro('P11267', '4 5 1\n1000\n2 1\n', [5])
repro('P11267', '8 9 1\n10000100\n3 1\n', [9], 'prefix')
check('P11267', '8 3 2\n10001011\n1 2\n4 3\n', [5, 10])

def kingdom(ss, m, s, k):
    n = len(ss)
    pos, step, seen = s, 0, {}
    while step < k:
        key = (pos-1) % n
        if key in seen:
            oldstep, oldpos = seen[key]
            loops = (k-step) // (step-oldstep)
            if loops:
                pos += loops * (pos-oldpos)
                step += loops * (step-oldstep)
                continue
        else:
            seen[key] = step, pos
        for d in range(min(m, n)):
            nxt = pos + m - d
            if ss[(nxt-1) % n] == '1':
                pos = nxt
                break
        else:
            pos += 1
        step += 1
    return pos % 1000000007

cases = set()
for n in range(1, 5):
    for mask in range(1 << n):
        ss = ''.join(str(mask >> i & 1) for i in range(n))
        for m in {1, n, n+1, 2*n, 2*n+1}:
            cases.add((ss, m))
for _ in range(100):
    n = rng.randint(1, 30)
    cases.add((''.join(rng.choices('01', k=n)),
               rng.choice([rng.randint(1, 100), rng.randint(1, 10**18)])))
queries = 0
for ss, m in sorted(cases):
    qs = [(s, k) for s in range(1, len(ss)+1) for k in [0, 1, 2, 13, 10**18]]
    qs += [(rng.randint(1, 10**18), rng.randint(0, 10**18)) for _ in range(10)]
    data = f'{len(ss)} {m} {len(qs)}\n{ss}\n' + ''.join(f'{s} {k}\n' for s,k in qs)
    check('P11267', data, [kingdom(ss, m, s, k) for s,k in qs])
    queries += len(qs)
print('P11267 queries:', queries, flush=True)

repro('P10526', '1 2\na\nTE\n', [1])

def terminal(words, keys):
    p, ans = '', []
    for c in keys:
        if c.islower():
            p += c
        elif c == 'B':
            p = p[:-1]
        elif c == 'T':
            matches = [w for w in words if w.startswith(p)]
            if matches:
                lo, hi = min(matches), max(matches)
                j = 0
                while j < min(len(lo), len(hi)) and lo[j] == hi[j]:
                    j += 1
                p = lo[:j]
        else:
            ans.append(words.index(p)+1 if p in words else -1)
            p = ''
    return ans

for words, keys in [(['ab','abc'], 'aTEaTBEabcxBBTE'),
                    (['abc','abd'], 'TTBBaTBEabTBE'),
                    (['a'], 'BBTabBBBBTEaBBBTE')]:
    data = f'{len(words)} {len(keys)}\n' + '\n'.join(words) + '\n' + keys + '\n'
    check('P10526', data, terminal(words, keys))
for _ in range(50):
    words = set()
    while len(words) < 20:
        words.add(''.join(rng.choices('abcd', k=rng.randint(1, 12))))
    words = sorted(words)
    keys = ''.join(rng.choices('abcdBTE', weights=[1,1,1,1,3,3,2], k=3000))
    data = f'{len(words)} {len(keys)}\n' + '\n'.join(words) + '\n' + keys + '\n'
    check('P10526', data, terminal(words, keys))

report = {'seed': SEED, 'passed_cases': stats, 'kingdom_queries': queries,
          'collision_strings': [a,b]}
(WORK / 'check-results.json').write_text(json.dumps(report, indent=2))
print(json.dumps(report, indent=2), flush=True)
