import itertools
import json
import pathlib
import random
import subprocess
import time
from functools import lru_cache

D = pathlib.Path(__file__).resolve().parent
P = 998244353
R = random.Random(20261018)
stats = {}

def run(name, data, expected, timeout=8):
    r = subprocess.run([str(D / (name + '.exe'))], input=data, text=True,
                       capture_output=True, timeout=timeout)
    got = [int(x) for x in r.stdout.split()]
    if r.returncode or got != expected:
        (D / 'first_failure.in').write_text(data, encoding='utf-8')
        (D / 'first_failure.json').write_text(json.dumps(
            dict(program=name, expected=expected, actual=got, stderr=r.stderr,
                 seed=20261018), ensure_ascii=False, indent=2), encoding='utf-8')
        raise AssertionError((name, data, expected, got, r.stderr))
    stats[name] = stats.get(name, 0) + 1

def check(name, data, expected):
    for kind in ('std', 'partial'):
        run(name + '_' + kind, data, expected)

def counter():
    check('counter', '2 10\n0 1\n5 0\n', [3])
    check('counter', '1 10\n4 3\n', [7])
    for _ in range(170):
        n, b = R.randint(1, 12), R.randint(1, 120)
        t = sorted(R.sample(range(300), n))
        v = [R.randrange(140) for _ in range(n)]
        if R.randrange(2):
            k, z = R.randint(1, 120), R.randrange(120)
            v = [(z + a) % k for a in t]
        ans = sum(all(0 <= v[i] < k and (v[i] - t[i] - v[0] + t[0]) % k == 0
                      for i in range(n)) for k in range(1, b + 1))
        check('counter', f'{n} {b}\n' + ''.join(f'{a} {z}\n' for a,z in zip(t,v)), [ans])
    for data, ans in [('1 1000000000000\n1000000000000 1000000000000\n',0),
                      ('2 1000000000000\n0 0\n1000000000000 1000000000000\n',0),
                      ('2 1000000000000\n0 0\n1000000000000 0\n',169)]:
        run('counter_std', data, [ans])

def outputs(s):
    n = len(s)
    @lru_cache(None)
    def dfs(i):
        if i == n: return {'': 0}
        d = {s[i] + t: c for t,c in dfs(i+1).items()}
        for a in range(1, n-i+1):
            for b in range(n-i-a+1):
                x = s[i+a:i+a+b] + s[i:i+a][::-1]
                for t,c in dfs(i+a+b).items():
                    k = x+t
                    d[k] = min(d.get(k, 100), c+1)
        return d
    return dfs(0)

def buffer():
    check('buffer', '4\nabcd\ncdba\n', [1])
    check('buffer', '3\naba\naba\n', [0])
    for _ in range(150):
        n = R.randint(1, 8)
        s = ''.join(R.choice('abc') for _ in range(n))
        d = outputs(s)
        if R.randrange(2): t = R.choice(list(d))
        else: t = ''.join(R.choice('abc') for _ in range(n))
        check('buffer', f'{n}\n{s}\n{t}\n', [d.get(t, -1)])
    # Exhaust all binary pairs through length 4, including repeated letters.
    for n in range(1, 5):
        ss = [''.join(x) for x in itertools.product('ab', repeat=n)]
        for s in ss:
            d = outputs(s)
            for t in ss: check('buffer', f'{n}\n{s}\n{t}\n', [d.get(t,-1)])

def alphabet():
    check('alphabet', '4\naa\nab\nba\nbb\n', [748683267,748683265,748683265,748683267])
    check('alphabet', '3\na\nab\nz\n', [748683265,748683265,1])
    for _ in range(100):
        k = R.randint(1, 5)
        words = set()
        n = R.randint(1, min(12, sum(k**j for j in range(1,5))))
        while len(words) < n:
            words.add(''.join(R.choice('abcde'[:k]) for _ in range(R.randint(1,4))))
        words = sorted(words)
        ranks = [[] for _ in words]
        chars = sorted(set(''.join(words)))
        for a in itertools.permutations(chars):
            rk = {c:i for i,c in enumerate(a)}
            order = sorted(range(n), key=lambda i:tuple(rk[c] for c in words[i]))
            for r,i in enumerate(order,1): ranks[i].append(r)
        t = len(ranks[0]); inv = pow(t,P-2,P)
        ans = [(sum(r*r for r in rs)*inv - (sum(rs)*inv % P)**2) % P for rs in ranks]
        check('alphabet', str(n)+'\n'+'\n'.join(words)+'\n', ans)
    # More than six actual letters, to exercise the partial's pairwise branch.
    words = ['abcd', 'abcde', 'bcfa', 'ghac', 'adgh', 'hafg']
    n = len(words); f=[0]*n; g=[0]*n; t=0
    for a in itertools.permutations('abcdefgh'):
        rk = {c:i for i,c in enumerate(a)}
        for r,i in enumerate(sorted(range(n),key=lambda i:tuple(rk[c] for c in words[i])),1):
            f[i]+=r; g[i]+=r*r
        t+=1
    inv=pow(t,P-2,P)
    check('alphabet', str(n)+'\n'+'\n'.join(words)+'\n',
          [(g[i]*inv-(f[i]*inv%P)**2)%P for i in range(n)])

def tree_data(a, edges, queries):
    return f'{len(a)} {len(queries)}\n'+' '.join(map(str,a))+'\n'+''.join(
        f'{u+1} {v+1}\n' for u,v in edges)+''.join(f'{u+1} {x}\n' for u,x in queries)

def tree_oracle(a, edges, queries, brute=True):
    n=len(a); adj=[[] for _ in a]
    for u,v in edges: adj[u].append(v); adj[v].append(u)
    par=[-1]*n; order=[0]; par[0]=0
    for u in order:
        for v in adj[u]:
            if v!=par[u]: par[v]=u; order.append(v)
    sub=[1<<i for i in range(n)]
    for v in order[:0:-1]: sub[par[v]]|=sub[v]
    if brute:
        connected=[]
        for mask in range(1,1<<n):
            u=(mask&-mask).bit_length()-1; seen=1<<u; stack=[u]
            for u in stack:
                for v in adj[u]:
                    if mask>>v&1 and not seen>>v&1: seen|=1<<v; stack.append(v)
            if seen==mask: connected.append((mask,sum(a[i] for i in range(n) if mask>>i&1)))
        ans=[]
        for u,x in queries:
            best=-10**30; c=0
            for mask,s in connected:
                if not mask>>u&1: continue
                val=s+x*(mask&sub[u]).bit_count()
                if val>best: best=val; c=1
                elif val==best: c+=1
            ans.append(c%P)
        return ans
    # Independent full DP, root at the queried u, changing only original subtree u.
    ans=[]
    for root,x in queries:
        pa=[-1]*n; oo=[root]; pa[root]=root
        for u in oo:
            for v in adj[u]:
                if v!=pa[u]: pa[v]=u; oo.append(v)
        f=[0]*n; g=[1]*n
        for u in oo[::-1]:
            f[u]=a[u]+(x if sub[root]>>u&1 else 0)
            for v in adj[u]:
                if v==pa[u]:continue
                f[u]+=max(0,f[v])
                if f[v]>=0:g[u]=g[u]*(g[v]+(f[v]==0))%P
        ans.append(g[root])
    return ans

def subsidy():
    check('subsidy','3 4\n1 -2 0\n1 2\n1 3\n1 0\n1 1\n2 2\n3 -1\n',[2,1,2,1])
    check('subsidy','3 3\n0 -1 1\n1 2\n2 3\n1 0\n2 1\n3 -1\n',[2,2,1])
    for case in range(170):
        n=R.randint(1,12)
        a=[R.randint(-5,5) for _ in range(n)]
        if case%10==0:a=[0]*n
        edges=[(R.randrange(v),v) for v in range(1,n)]
        if case%7==0: edges=[(v-1,v) for v in range(1,n)]
        if case%7==1: edges=[(0,v) for v in range(1,n)]
        queries=[(u,x) for u in range(n) for x in range(-6,7)]
        R.shuffle(queries)
        check('subsidy',tree_data(a,edges,queries),tree_oracle(a,edges,queries))
    for case in range(30):
        n=R.randint(30,180)
        a=[R.randint(-10**9,10**9) for _ in range(n)] if case%2 else [R.randint(-4,4) for _ in range(n)]
        edges=[(R.randrange(v),v) for v in range(1,n)]
        queries=[(R.randrange(n),R.choice([-10**9,10**9,R.randint(-10,10)])) for _ in range(100)]
        check('subsidy',tree_data(a,edges,queries),tree_oracle(a,edges,queries,False))
    # Construct an all-zero subtree with exactly P-1 rooted connected sets.
    edges=[]; root=0; nn=1
    for bit in bin(P-1)[3:]:
        edges.append((root,nn)); nn+=1
        if bit=='1': edges.append((root,nn)); root=nn; nn+=1
    edges.append((root,nn)); root=nn; nn+=1
    mp={root:0}; mp.update({v:i+1 for i,v in enumerate(v for v in range(nn) if v!=root)})
    edges=[(mp[u],mp[v]) for u,v in edges]
    a=[0]*nn; queries=[(u,x) for u in range(nn) for x in (-1,0,1)]
    check('subsidy',tree_data(a,edges,queries),tree_oracle(a,edges,queries,False))

if __name__=='__main__':
    begin=time.perf_counter()
    for fun in (counter,buffer,alphabet,subsidy):
        fun();print(fun.__name__,'OK',flush=True)
    result=dict(seed=20261018,case_counts=stats,elapsed_seconds=round(time.perf_counter()-begin,3))
    (D/'verification.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
    print(json.dumps(result),flush=True)
