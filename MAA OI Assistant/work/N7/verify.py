from pathlib import Path
import subprocess,random,itertools,time,json,math,sys
W=Path(__file__).resolve().parent
O=W.parents[1]/'outputs'/'N7'
R=random.Random(16701669)
report={'seed':16701669,'compiler':'TDM-GCC 10.3.0','flags':'-std=c++17 -O2 -Wall -Wextra','tests':[]}
def run(num,mode,data,timeout=30):
    t=time.perf_counter()
    r=subprocess.run([str(W/f'U{num}_{mode}.exe')],input=data,text=True,capture_output=True,timeout=timeout)
    if r.returncode: raise RuntimeError((num,mode,r.returncode,r.stderr))
    return r.stdout.split(),time.perf_counter()-t

def check(num,mode,data,expected,label):
    a,t=run(num,mode,data)
    b=str(expected).split() if isinstance(expected,str) else list(map(str,expected))
    if a!=b:
        p=W/f'FAIL_U{num}_{label}'
        p.with_suffix('.in').write_text(data,encoding='utf-8')
        p.with_suffix('.expected').write_text(' '.join(b))
        p.with_suffix('.actual').write_text(' '.join(a))
        raise AssertionError((num,mode,label,p))
    return t

def note(name,**kw):
    report['tests'].append(dict(name=name,**kw));print(name,kw,flush=True)

# T1: an unrelated exhaustive set-partition program.
cases=list(itertools.product(range(1,5),repeat=2))
data=str(len(cases))+'\n'+''.join(f'{n} {m}\n' for n,m in cases)
expected,t=run(1667,'partial',data)
check(1667,'std',data,expected,'all_small_partitions')
note('U1667 全部 n,m<=4 与无序集合划分穷举一致',cases=len(cases),partial_seconds=round(t,3))
# Integer factorial formula at moderate sizes, computed using exact integer divisions.
cases=[];expected=[]
for _ in range(250):
    n=R.randrange(1,22);m=R.randrange(1,22);k=(n+1)//2;h=(m+1)//2;s=k*h;z=n*m-s
    a=math.factorial(s)*math.factorial(z)//(math.factorial(h)**k*math.factorial(m-h)**k*math.factorial(m)**(n-k)*math.factorial(k)*math.factorial(n-k))
    cases.append((n,m));expected.extend((z+1,a%998244353))
data=f'{len(cases)}\n'+''.join(f'{n} {m}\n' for n,m in cases)
check(1667,'std',data,expected,'integer_formula');note('U1667 大整数精确计数公式交叉验证',cases=len(cases))

# T2: de Bruijn sequence contains every word of length eight.
def debruijn(k,n):
    a=[0]*(k*n);seq=[]
    def db(t,p):
        if t>n:
            if n%p==0:seq.extend(a[1:p+1])
        else:
            a[t]=a[t-p];db(t+1,p)
            for j in range(a[t-p]+1,k):a[t]=j;db(t+1,t)
    db(1,1);return [x+1 for x in seq+seq[:n-1]]

def direct(a,l,r):
    best=0
    for i in range(l,r):
        c=[0]*3
        for j in range(i,r):
            c[a[j]-1]+=1
            if c[0]!=c[1] and c[0]!=c[2] and c[1]!=c[2]:best=max(best,j-i+1)
    return best

def three(a,queries,expect=None,partial=False,label='three'):
    data=f'0 {len(a)} {len(queries)}\n'+' '.join(map(str,a))+'\n'+''.join(f'{l+1} {r}\n' for l,r in queries)
    if expect is None:expect=[direct(a,l,r) for l,r in queries]
    check(1668,'std',data,expect,label)
    if partial:check(1668,'partial',data,expect,label)

a=debruijn(3,8);queries=[(l,l+d) for l in range(len(a)) for d in range(1,min(8,len(a)-l)+1)]
three(a,queries,label='debruijn');note('U1668 含全部 3^8 个八位三色串的序列，穷举所有长度<=8询问',n=len(a),queries=len(queries))
num=0
for typ in range(32):
    n=R.randrange(20,180)
    if typ==0:a=[1]*n
    elif typ==1:a=[i%3+1 for i in range(n)]
    elif typ==2:a=[i%2+1 for i in range(n)]
    elif typ==3:a=[1]*(n//2)+[2]*(n-n//2)
    else:a=[R.randrange(1,4) for _ in range(n)]
    f=[[0]*(n+1) for _ in range(n+1)]
    for l in range(n-1,-1,-1):
        c=[0]*3
        for r in range(l+1,n+1):
            c[a[r-1]-1]+=1;f[l][r]=max(f[l+1][r],f[l][r-1])
            if len(set(c))==3:f[l][r]=r-l
    queries=[(l,r) for l in range(n) for r in range(l+1,n+1)]
    three(a,queries,[f[l][r] for l,r in queries],True,f'arr_{typ}')
    num+=len(queries)
note('U1668 随机及全同色/三周期/双色/分段数组所有区间，与二次DP一致',arrays=32,queries=num)

# T3: for every query explicitly try each p and apply all functions in forward order.
n=45;ops=[];a=[R.randrange(30) for _ in range(n)];b=[R.randrange(60) for _ in range(n)];aa=a[:];bb=b[:];expected=[]
for _ in range(18000):
    op=R.choices([1,2,3],[2,2,6])[0]
    if op<3:
        i=R.randrange(n);v=R.choice([0,10**9 if op==1 else 10**15,R.randrange(100)])
        (aa if op==1 else bb)[i]=v;ops.append(f'{op} {i+1} {v}')
    else:
        l=R.randrange(n);r=R.randrange(l,n);x=R.choice([0,10**15,R.randrange(150)])
        best=x
        for p in range(l,r+1):
            v=x
            for i in range(p,r+1):v=min(v+aa[i],bb[i])
            best=max(best,v)
        expected.append(best);ops.append(f'3 {l+1} {r+1} {x}')
data=f'0 {n} {len(ops)}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n'+'\n'.join(ops)+'\n'
for mode in ['std','partial']:check(1669,mode,data,expected,'forward_brute')
note('U1669 随机修改询问，与逐起点正向函数复合暴力一致',operations=len(ops),queries=len(expected))
# Exhaustive small arrays, no modifications, limits and zeros.
num=0
for _ in range(35):
    n=R.randrange(1,9);a=[R.choice([0,1,2,10**9]) for i in range(n)];b=[R.choice([0,1,2,10**15]) for i in range(n)]
    ops=[];expected=[]
    for l in range(n):
        for r in range(l,n):
            for x in [0,1,2,3,10**15]:
                best=x
                for p in range(l,r+1):
                    y=x
                    for i in range(p,r+1):y=min(y+a[i],b[i])
                    best=max(best,y)
                ops.append(f'3 {l+1} {r+1} {x}');expected.append(best)
    data=f'0 {n} {len(ops)}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,b))+'\n'+'\n'.join(ops)+'\n'
    for mode in ['std','partial']:check(1669,mode,data,expected,f'limits_{_}')
    num+=len(ops)
note('U1669 零值/上界及全部区间边界测试',arrays=35,queries=num)

# T4: all connected simple graphs n<=5; partial uses Prufer trees and enumerates edge subsets.
def connected(n,es):
    adj=[[] for _ in range(n)]
    for u,v in es:adj[u].append(v);adj[v].append(u)
    vis={0};st=[0]
    while st:
        for v in adj[st.pop()]:
            if v not in vis:vis.add(v);st.append(v)
    return len(vis)==n

def graph_case(n,es,label):
    data=f'{n} {len(es)}\n'+''.join(f'{u+1} {v+1}\n' for u,v in es)
    exp,_=run(1670,'partial',data)
    check(1670,'std',data,exp,label)
num=0
for n in range(3,6):
    edges=list(itertools.combinations(range(n),2))
    for s in range(1<<len(edges)):
        es=[e for i,e in enumerate(edges) if s>>i&1]
        if connected(n,es):graph_case(n,es,f'all_{n}_{s}');num+=1
note('U1670 所有 3~5 点简单连通图，与 Prüfer/边子集穷举一致',graphs=num)
for i in range(100):
    n=6;es=[(u,v) for u,v in itertools.combinations(range(n),2) if R.random()<R.uniform(.15,.99)]
    while not connected(n,es):
        es=[(u,v) for u,v in itertools.combinations(range(n),2) if R.random()<.6]
    graph_case(n,es,f'random6_{i}')
note('U1670 六点随机连通图，与 Prüfer/边子集穷举一致',graphs=100)
# Any input tree: only one connected spanning edge subgraph and one spanning tree.
for n in [6,12,18]:
    for typ in ['path','star','random']:
        es=[(i-1,i) if typ=='path' else (0,i) if typ=='star' else (R.randrange(i),i) for i in range(1,n)]
        data=f'{n} {len(es)}\n'+''.join(f'{u+1} {v+1}\n' for u,v in es)
        check(1670,'std',data,[1],f'tree_{n}_{typ}')
note('U1670 树图恒为1（链/星/随机树）',cases=9)
report['status']='PASS'
(W/'verification_core.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print('CORE PASS',flush=True)
