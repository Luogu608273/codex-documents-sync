from collections import deque

def brackets(m, s='', bal=0):
    if not m:
        if bal == 0:
            yield s
        return
    if m > bal:
        yield from brackets(m-1, s+'(', bal+1)
    if bal:
        yield from brackets(m-1, s+')', bal-1)

def blocks(s):
    c, cnt = [], 0
    for x in s:
        if x == '(':
            cnt += 1
        else:
            c.append(cnt)
            cnt = 0
    return c

def score(s):
    return max(map(len, s.split(')')))

def brute(s):
    seen = {s}
    layer = {s}
    best = score(s)
    ans = [best]
    for _ in range(len(s)//2):
        nex = set()
        for x in layer:
            for i in range(len(x)-1):
                if x[i:i+2] == '()':
                    y = '('+x[:i]+x[i+2:]+')'
                    if y not in seen:
                        nex.add(y)
        seen.update(nex)
        layer = nex
        if nex:
            best = max(best, max(map(score, nex)))
        ans.append(best)
    return ans

def original(s, k, c=None):
    a = blocks(s)
    if c is None:
        c = [0]*(len(s)+1)
    c[:len(a)] = a
    m = len(a)
    ans = z = 0
    for i in range(k+1):
        z += c[i]
        ans = max(ans, min(m, z+k-i))
    z = 0
    j = 1
    for i in range(1, m+1):
        z += c[i]-1
        while j < i and (c[j] < 0 or i-j > k):
            z -= c[j]
            j += 1
        ans = max(ans, z+1)
    return ans

def fixed(s, k):
    c = blocks(s)
    m = len(c)
    ans = z = 0
    for i in range(min(k+1, m)):
        z += c[i]
        ans = max(ans, min(m, z+k-i))
    p = [0]
    for x in c:
        p.append(p[-1]+x-1)
    q = deque([0])
    for i in range(1, m+1):
        while q[0] < i-k-1:
            q.popleft()
        ans = max(ans, p[i]-p[q[0]]+1)
        while q and p[q[-1]] >= p[i]:
            q.pop()
        q.append(i)
    return ans

def obvious_patch(s, k):
    c = blocks(s)
    m = len(c)
    ans = z = 0
    for i in range(min(k+1, m)):
        z += c[i]
        ans = max(ans, min(m, z+k-i))
    z = j = 0
    for i in range(m):
        z += c[i]-1
        while j < i and (c[j] == 0 or i-j > k):
            z -= c[j]-1
            j += 1
        ans = max(ans, z+1)
    return ans

if __name__ == '__main__':
    count = 0
    first = {}
    for m in range(1, 9):
        for s in brackets(2*m):
            truth = brute(s)
            for k, expect in enumerate(truth):
                count += 1
                assert fixed(s, k) == expect, (s, k, expect, fixed(s, k))
                for name, fn in [('original', original), ('obvious_patch', obvious_patch)]:
                    got = fn(s, k)
                    if got != expect and name not in first:
                        first[name] = (s, k, got, expect, blocks(s))
                        print(name, first[name], flush=True)
        print('m', m, 'checks', count, flush=True)
    print('PASS', count)
