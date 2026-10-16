import random

rng = random.Random(20261012)
cases = []
for n in range(2, 6):
    intervals = [(l, r) for l in range(1, n + 1) for r in range(l + 1, n + 1)]
    for mask in range(1, 1 << len(intervals)):
        cases.append((n, [pair for j, pair in enumerate(intervals) if mask >> j & 1]))
for _ in range(5000):
    n = rng.randint(2, 25)
    intervals = [(l, r) for l in range(1, n + 1) for r in range(l + 1, n + 1)]
    rng.shuffle(intervals)
    cases.append((n, intervals[:rng.randint(1, len(intervals))]))

for case, (n, intervals) in enumerate(cases):
    a, b = [0] * (n + 1), [n + 1] * (n + 1)
    for l, r in intervals:
        a[r], b[r] = max(a[r], l), min(b[r], l)
    for r in range(1, n + 1):
        a[r] = max(a[r], a[r - 1])
    for r in range(n - 1, 0, -1):
        b[r] = min(b[r], b[r + 1])
    states = {(0, 0)}
    positions, left, right = [0], [0], [0]
    lo, hi, low_col, high_col = 0, -1, 0, -1
    for r in range(1, n + 1):
        new_rows = sorted({v for u, v in states if v >= a[r] and u < b[r]})
        states = {(u, v) for u, v in states if u >= a[r]} | {(v, r) for v in new_rows}
        while lo < len(positions) and positions[lo] < a[r - 1]:
            lo += 1
        while hi + 1 < len(positions) and positions[hi + 1] < b[r]:
            hi += 1
        while low_col < len(positions) and (positions[low_col] < a[r] or right[low_col] < lo):
            low_col += 1
        while high_col + 1 < len(positions) and left[high_col + 1] <= hi:
            high_col += 1
        compressed = positions[low_col:high_col + 1] if lo <= hi and low_col <= high_col else []
        assert compressed == new_rows, (case, r, intervals, compressed, new_rows)
        if new_rows:
            l, rr = positions.index(new_rows[0]), positions.index(new_rows[-1])
            assert new_rows == positions[l:rr + 1], (case, r, 'not contiguous')
            assert l >= left[-1] and rr >= right[-1], (case, r, 'not monotone')
            positions.append(r)
            left.append(l)
            right.append(rr)
    expected = bool(states)
    actual = positions[right[-1]] >= a[n]
    assert actual == expected, (case, intervals, actual, expected)
print(f'PASS {len(cases)} cases: interval structure, monotone endpoints, compressed transitions; seed=20261012')
