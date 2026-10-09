from pathlib import Path
import subprocess, random, time, json, runpy
from collections import defaultdict

root=Path(__file__).resolve().parents[1]; out=root/'outputs'; tmp=root/'work'/'tests'; tmp.mkdir(parents=True,exist_ok=True)
gxx=r'C:\TDM-GCC-64\bin\g++.EXE'
bins={}
for src in out.glob('*.cpp'):
    exe=tmp/(src.stem+'.exe')
    p=subprocess.run([gxx,'-std=c++17','-O2','-pipe',str(src),'-o',str(exe)],capture_output=True,text=True)
    if p.returncode: raise RuntimeError(src.name+'\n'+p.stderr)
    bins[src.stem]=exe
print('Compiled',len(bins),'C++17 programs.',flush=True)
model=runpy.run_path(str(root/'work'/'verify_ideas.py'))
counts=defaultdict(int); timing={}
def run(stem, name, data):
    (tmp/(name+'.in')).write_text(data,encoding='utf-8')
    target=tmp/(name+'.out')
    if target.exists():target.unlink()
    start=time.perf_counter()
    p=subprocess.run([str(bins[stem])],cwd=tmp,capture_output=True,timeout=30)
    elapsed=time.perf_counter()-start
    if p.returncode:raise RuntimeError((stem,p.returncode,p.stderr))
    return target.read_text().split(),elapsed
def check(stem,name,data,expected):
    actual,_=run(stem,name,data)
    assert actual==list(map(str,expected)),(stem,data,actual,expected)
    counts[stem]+=1

samples=[('U1708','watch','3 2 5\n0 3 10\n',[2]),('U1709','merge','2 3\n1 10\n5 10 20\n',[-6,-1,9]),('U1710','sect','4 2\n1 2\n2 3\n3 4\n1 2 1 2\n8 5\n',[5]),('U1711','tile','4 2\n0 0\n5 0\n5 4\n0 4\n',[4])]
for prefix,name,data,exp in samples:
    for stem in bins:
        if stem.startswith(prefix):check(stem,name,data,exp)
random.seed(1709)
for _ in range(200):
    n=random.randint(1,11);a=sorted(random.sample(range(-30,40),n));L=random.randint(1,15);R=random.randint(L,30)
    data=f'{n} {L} {R}\n'+ ' '.join(map(str,a))+'\n';exp=[model['watch_b'](a,L,R)]
    for stem in bins:
        if stem.startswith('U1708'):check(stem,'watch',data,exp)
print('Watch random comparisons passed.',flush=True)
for _ in range(100):
    n=random.randint(2,8);q=10;a=[random.randint(1,30) for _ in range(n)];ks=[random.randint(1,90) for _ in range(q)]
    data=f'{n} {q}\n'+' '.join(map(str,a))+'\n'+' '.join(map(str,ks))+'\n';exp=[model['merge_b'](a,k) for k in ks]
    for stem in bins:
        if stem.startswith('U1709'):check(stem,'merge',data,exp)
print('Merge random comparisons passed.',flush=True)

def sect_b(n,k,edges,c,w):
    tr=[[] for _ in range(n)]
    for u,v in edges:tr[u].append(v);tr[v].append(u)
    deps=[]
    for t in range(k):
        nodes=[i for i in range(n) if c[i]==t];par=[-1]*n;par[nodes[0]]=nodes[0];order=[nodes[0]]
        for u in order:
            for v in tr[u]:
                if par[v]<0:par[v]=u;order.append(v)
        mask=1<<t
        for v in nodes:
            while v!=nodes[0]:mask|=1<<c[v];v=par[v]
        deps.append(mask)
    ans=sum(w)
    for s in range(1,1<<k):
        if all(not(s>>t&1) or deps[t]&s==deps[t] for t in range(k)):
            ans=min(ans,sum(w[t] for t in range(k) if s>>t&1)-max(w[t] for t in range(k) if s>>t&1))
    return ans
for _ in range(200):
    k=random.randint(1,7);n=random.randint(2*k,3*k+4);c=list(range(k))*2+[random.randrange(k) for _ in range(n-2*k)];random.shuffle(c)
    edges=[(i,random.randrange(i)) for i in range(1,n)];w=[random.randint(1,100) for _ in range(k)]
    data=f'{n} {k}\n'+''.join(f'{u+1} {v+1}\n' for u,v in edges)+' '.join(str(t+1) for t in c)+'\n'+' '.join(map(str,w))+'\n'
    exp=[sect_b(n,k,edges,c,w)]
    for stem in bins:
        if stem.startswith('U1710'):check(stem,'sect',data,exp)
print('Sect subset-enumeration comparisons passed.',flush=True)

def polygon(cells):
    if not cells:return None
    dx=min(x for x,y in cells);dy=min(y for x,y in cells);cells={(x-dx,y-dy) for x,y in cells}
    edges=set()
    for x,y in cells:
        vs=[(x,y),(x+1,y),(x+1,y+1),(x,y+1)]
        for a,b in zip(vs,vs[1:]+vs[:1]):
            if (b,a) in edges:edges.remove((b,a))
            else:edges.add((a,b))
    adj={}
    for a,b in edges:
        if a in adj:return None
        adj[a]=b
    start=next(iter(adj));a=start;vs=[]
    while True:
        vs.append(a);a=adj[a]
        if a==start:break
    if len(vs)!=len(edges):return None
    ps=[]
    for i,b in enumerate(vs):
        a=vs[i-1];c=vs[(i+1)%len(vs)]
        if not(a[0]==b[0]==c[0] or a[1]==b[1]==c[1]):ps.append(b)
    if random.randrange(2):ps.reverse()
    return cells,ps
tested=0
for z in range(4000):
    K=random.randint(1,4)
    if z%3==0:
        cells={(x,y) for x in range(random.randint(1,12)) for y in range(random.randint(1,12)) if random.random()<.8}
    elif z%3==1:
        cells=set()
        for j in range(random.randint(1,5)):
            l=random.randint(0,6);r=l+K*random.randint(1,3)
            cells|={(x,y) for x in range(l,r) for y in range(j*K,(j+1)*K)}
    else:
        cells={(0,0)}
        for j in range(random.randint(1,50)):
            x,y=random.choice(tuple(cells));dx,dy=random.choice([(0,1),(0,-1),(1,0),(-1,0)]);cells.add((x+dx,y+dy))
    result=polygon(cells)
    if result is None:continue
    cells,ps=result;data=f'{len(ps)} {K}\n'+''.join(f'{x} {y}\n' for x,y in ps);exp=[model['tile_b'](cells,K)]
    for stem in bins:
        if stem.startswith('U1711'):check(stem,'tile',data,exp)
    tested+=1
    if tested==600:break
print('Tile polygon comparisons passed:',tested,flush=True)

# Adversarial tile phases: the previous cut lies before the most recent event.
cells={(x,y) for x in range(6) for y in range(4)}|{(x,y) for x in range(1,5) for y in range(4,8)}
cells,ps=polygon(cells);data=f'{len(ps)} 4\n'+''.join(f'{x} {y}\n' for x,y in ps)
for stem in bins:
    if stem.startswith('U1711'):check(stem,'tile',data,[0])

n=200000;data=f'{n} 1 1\n'+' '.join(str(i*10) for i in range(n))+'\n'
result,t=run('U1708_code','watch',data);assert result==[str(n)];timing['watch_n200000']=t
n=q=150000;data=f'{n} {q}\n'+' '.join(['1000000000']*n)+'\n'+' '.join(['1']*q)+'\n'
result,t=run('U1709_code','merge',data);assert len(result)==q and len(set(result))==1;timing['merge_nq150000']=t
n=150000;k=50000;data=f'{n} {k}\n'+''.join(f'{i} {i+1}\n' for i in range(1,n))+' '.join(str(i%k+1) for i in range(n))+'\n'+' '.join(['1000000000']*k)+'\n'
result,t=run('U1710_code','sect',data);assert result==[str((k-1)*1000000000)];timing['sect_chain_n150000']=t

# A 200000-vertex histogram polygon, every column is a union of aligned K-squares.
m=99999;K=3;heights=[3*(1+i%2) for i in range(m)];ps=[(0,0),(m*3,0),(m*3,heights[-1])]
for i in range(m-1,0,-1):ps.extend([(i*3,heights[i]),(i*3,heights[i-1])])
ps.append((0,heights[0]));data=f'{len(ps)} {K}\n'+''.join(f'{x} {y}\n' for x,y in ps)
result,t=run('U1711_code','tile',data);assert result==[str(m*3)];timing['tile_n200000']=t
print('Large cases passed:',timing,flush=True)
report={'compiled':len(bins),'comparisons':dict(counts),'large_case_seconds':timing,'judge_status':'Not submitted; local tests only.'}
(root/'work'/'test_report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
