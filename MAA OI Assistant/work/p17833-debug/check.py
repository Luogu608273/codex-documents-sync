from collections import deque
from itertools import product
import json
from pathlib import Path
import random


def brute(x, d):
    n = len(x)
    pairs = []
    for s in range(n):
        dis, cnt = [-1] * n, [0] * n
        dis[s], cnt[s] = 0, 1
        q = deque([s])
        while q:
            u = q.popleft()
            for v in range(n):
                if u == v or abs(x[u] - x[v]) > d:
                    continue
                if dis[v] == -1:
                    dis[v] = dis[u] + 1
                    q.append(v)
                if dis[v] == dis[u] + 1:
                    cnt[v] = min(3, cnt[v] + cnt[u])
        pairs.extend((s + 1, v + 1) for v in range(s + 1, n) if cnt[v] == 2)
    return pairs


def calc(x, d, weighted=False, guard=False):
    n = len(x)
    x = [0] + list(x)
    l, r, cl1, cr1, cl2, cr2 = ([0] * (n + 2) for _ in range(6))
    j = 1
    for i in range(1, n + 1):
        while j < i and x[j] + d < x[i]:
            j += 1
        l[i] = j
    j = n
    for i in range(n, 0, -1):
        while j > i and x[j] - d > x[i]:
            j -= 1
        r[i] = j
    cl2[n] = cr2[1] = 1
    for i in range(n - 1, 0, -1):
        cl2[i] = cl2[i + 1] + 1 if r[i] == r[i + 1] else 1
    for i in range(2, n + 1):
        cr2[i] = cr2[i - 1] + 1 if l[i] == l[i - 1] else 1
    for i in range(1, n + 1):
        if r[l[i]] == i and l[i] != i:
            cl1[i] = cl1[l[i]] + (min(cl2[l[i]], i - l[i]) if weighted else 1)
    for i in range(n, 0, -1):
        if l[r[i]] == i and r[i] != i:
            cr1[i] = cr1[r[i]] + (min(cr2[r[i]], r[i] - i) if weighted else 1)
    ans = 0
    details = []
    for i in range(1, n):
        a, b = i, i + 1
        if x[b] - x[a] > d:
            continue
        p, q = l[b], r[a]
        if p == a or q == b:
            continue
        if r[p] == b and l[q] == a:
            left = (cl1[p] if not guard or l[a] == p else 0) + min(cl2[p], a - p)
            right = (cr1[q] if not guard or r[b] == q else 0) + min(cr2[q], q - b)
            ans += left * right
            details.append((a, b, p, q, left, right))
    return ans, details


def main():
    first = {}
    cases = []
    for n in range(1, 9):
        for gaps in product(range(1, 4), repeat=n - 1):
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
    for x, d in cases:
        pairs = brute(x, d)
        expected = len(pairs)
        for key, weighted, guard in [('original', False, False), ('only_weighted', True, False), ('only_guard', False, True), ('fixed', True, True)]:
            result, details = calc(x, d, weighted, guard)
            if result != expected and key not in first:
                first[key] = dict(x=x, d=d, expected=expected, result=result, pairs=pairs, details=details)
                print(key, json.dumps(first[key]), flush=True)
            if key == 'fixed' and result != expected:
                raise AssertionError(first[key])
    out = Path(r'C:\Users\605\Documents\Output\p17833-debug')
    out.mkdir(parents=True, exist_ok=True)
    bad = first['original']
    (out / 'first-mismatch.in').write_text('0 2\n{} {}\n{}\n1 1\n0\n'.format(len(bad['x']), bad['d'], ' '.join(map(str, bad['x']))))
    Path(__file__).with_name('verification.json').write_text(json.dumps(dict(seed=17833, cases=len(cases), first=first), indent=2))
    print('PASS', len(cases), flush=True)


if __name__ == '__main__':
    main()
