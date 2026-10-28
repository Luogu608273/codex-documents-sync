from pathlib import Path
import subprocess, random, itertools, json, time, collections, sys
ROOT=Path(__file__).resolve().parents[2]
TASK=Path(__file__).resolve().parent
CXX='C:/TDM-GCC-64/bin/g++.exe'
random.seed(20261021)
P=998244353
EXE={}
LOG=[]

def compile_all():
    files=list((ROOT/'outputs/N17').rglob('*.cpp'))+list((ROOT/'outputs/S17').rglob('*.cpp'))
    for f in files:
        key=(f.parents[1].name,f.parent.name,f.stem)
        for local in [True,False]:
            out=TASK/('bin/'+'_'.join(key)+('_local' if local else '')+'.exe')
            out.parent.mkdir(exist_ok=True)
            cmd=[CXX,str(f),'-std=c++17','-O2','-Wall','-Wextra','-o',str(out)]
            if local: cmd.append('-DLOCAL')
            r=subprocess.run(cmd,capture_output=True,text=True)
            if r.returncode or r.stderr: raise RuntimeError(str(f)+'\n'+r.stderr)
            EXE[key+(local,)]=out
    print('Compiled 32 variants without warnings.',flush=True)

def run(group,name,inp,typ='std',local=True,timeout=15):
    exe=EXE[group,name,typ,local]
    if local:
        r=subprocess.run([str(exe)],input=inp,text=True,capture_output=True,timeout=timeout)
        out=r.stdout
    else:
        d=TASK/'io'/group/name/typ
        d.mkdir(parents=True,exist_ok=True)
        stem=name.split('_',1)[1]
        (d/(stem+'.in')).write_text(inp,encoding='ascii')
        r=subprocess.run([str(exe)],cwd=d,text=True,capture_output=True,timeout=timeout)
        out=(d/(stem+'.out')).read_text()
    if r.returncode: raise RuntimeError(f'{group}/{name}/{typ} exit {r.returncode}: {r.stderr}')
    return out.split()

def check(group,name,inp,expected,partial=True,fileio=False):
    expected=list(map(str,expected))
    for typ in ['std','partial'] if partial else ['std']:
        for local in [True,False] if fileio else [True]:
            got=run(group,name,inp,typ,local)
            if got!=expected:
                d=TASK/'failure';d.mkdir(exist_ok=True)
                (d/'input.txt').write_text(inp)
                (d/'expected.txt').write_text(' '.join(expected))
                (d/'actual.txt').write_text(' '.join(got))
                raise AssertionError((group,name,typ,local,got[:30],expected[:30]))

def sam():
    for t in range(100):
        n=random.randint(1,15);s=''.join(random.choices('abc',k=n));qs=[];ans=[]
        for l in range(n):
            for r in range(l,n):
                qs.append((l+1,r+1));c=collections.Counter(s[i:j] for i in range(l,r+1) for j in range(i+1,r+2));ans.append(max(c.values()))
        inp=f'{n} {len(qs)}\n{s}\n'+''.join(f'{l} {r}\n' for l,r in qs)
        check('S17','A_sam',inp,ans,fileio=t==0)
    LOG.append('sam: 100 strings, all intervals versus literal substring enumeration; file IO passed.')

def lis():
    cases=[]
    for n in range(1,7): cases.extend(itertools.permutations(range(1,n+1)))
    cases+= [random.sample(range(1,31),30) for _ in range(60)]
    for t,a in enumerate(cases):
        ans=[]
        for x in range(1,len(a)+1):
            b=[y for y in a if y<=x];f=[]
            for i,y in enumerate(b): f.append(1+max([f[j] for j in range(i) if b[j]<y],default=0))
            ans.append(max(f))
        check('S17','B_lis',f'{len(a)}\n'+ ' '.join(map(str,a))+'\n',ans,fileio=t==0)
    LOG.append(f'lis: {len(cases)} permutations, rebuilding each filtered sequence and quadratic LIS; file IO passed.')

def wolf():
    cases=[];ans=[]
    for n in range(2,11):
        for t in range(80):
            s=''.join(random.choices('LR',k=n))
            b=[random.randrange(n+1) for _ in range(n)]
            if t%2==0:
                mask=random.choice([x for x in range(1<<n) if not x&(x<<1)])
                for i in range(n):
                    if not mask>>i&1: b[i]=sum(mask>>j&1 for j in (range(i) if s[i]=='L' else range(i+1,n)))
            cnt=0
            for mask in range(1<<n):
                if mask&(mask<<1):continue
                if all(mask>>i&1 or b[i]==sum(mask>>j&1 for j in (range(i) if s[i]=='L' else range(i+1,n))) for i in range(n)):cnt+=1
            cases.append(f'{n}\n{s}\n'+ ' '.join(map(str,b))+'\n');ans.append(cnt)
    inp=str(len(cases))+'\n'+''.join(cases)
    check('S17','C_wolf',inp,ans,fileio=True)
    LOG.append(f'wolf: {len(cases)} cases versus all nonadjacent wolf masks; multi-case reset and file IO passed.')

def knapsack(w,n):
    f=[0]*(n+1);f[0]=1
    for j,v in enumerate(w):
        for x in range(1<<j,n+1):f[x]=(f[x]+v*f[x-(1<<j)])%P
    return f

def power():
    for t in range(12):
        w=[random.randrange(1,P) for _ in range(30)] if t<10 else [1 if t==10 else P-1]*30
        f=knapsack(w,65535)
        qs=list(range(1,1024))+[32767,32768,32769,65534,65535]+random.sample(range(1,65536),1000)
        inp=' '.join(map(str,w))+'\n'+str(len(qs))+'\n'+'\n'.join(map(str,qs))+'\n'
        check('S17','D_power',inp,[f[x] for x in qs],fileio=t==0)
        high=[1<<j for j in range(16,30)]+[(1<<30)-1,(1<<29)-1]+[random.randrange(1,1<<30) for _ in range(10)]
        inp=' '.join(map(str,w))+'\n'+str(len(high))+'\n'+'\n'.join(map(str,high))+'\n'
        check('S17','D_power',inp,[coef(w,x) for x in high],partial=False)
    LOG.append('power: 12 weight sets including 1 and P-1; 24,336 queries versus weighted complete knapsack; file IO passed.')
    LOG.append('power: 312 high-bit queries versus independent rational generating-function parity extraction (Bostan-Mori), including 2^30-1.')

def coef(w,n):
    num=[1];factors=[]
    for t in range(30):
        factors.append(w[t]);poly=[1]
        for a in factors:
            out=[0]*(len(poly)+1)
            for i,x in enumerate(poly):out[i]=(out[i]+x)%P;out[i+1]=(out[i+1]+x*a)%P
            poly=out
        out=[0]*(len(poly)+len(num)-1)
        for i,x in enumerate(num):
            for j,y in enumerate(poly):out[i+j]=(out[i+j]+x*y)%P
        num=out[(n&1)::2];n>>=1;factors=[x*x%P for x in factors]
    return num[0] if num else 0

def median():
    cases=list(itertools.product(range(1,4),repeat=4))+[tuple(random.choices(range(1,7),k=random.choice([2,6,8,10]))) for _ in range(400)]
    for t,a in enumerate(cases):
        n=len(a);possible=set()
        def dfs(l,med):
            if l==n:return True
            for r in range(l+1,n+1,2):
                x=sorted(a[l:r])[(r-l)//2]
                if med is None or x==med:
                    if dfs(r,x):return True
            return False
        ans='Yes' if dfs(0,None) else 'No'
        check('N17','A_median',str(n)+'\n'+' '.join(map(str,a))+'\n',[ans],fileio=t==0)
    LOG.append(f'median: {len(cases)} arrays versus all odd-length partitions, without assuming two blocks; file IO passed.')

def capacity(a):
    # Exact BFS: main track on the left, siding stack, last emitted value.
    # Siding pops return to the right end of the remaining main track.
    n=len(a)
    def possible(cap):
        start=(tuple(a),(),10**9);seen={start};q=collections.deque([start])
        while q:
            left,st,last=q.popleft()
            if not left and not st:return True
            cand=[]
            if left:
                if left[-1]<=last:cand.append((left[:-1],st,left[-1]))
                if len(st)<cap:cand.append((left[:-1],st+(left[-1],),last))
            if st:cand.append((left+(st[-1],),st[:-1],last))
            for key in cand:
                if key not in seen:seen.add(key);q.append(key)
        return False
    return next(x for x in range(n) if possible(x))

def tramcar():
    for t in range(160):
        n=random.randint(1,6);a=[random.randrange(4) for _ in range(n)];k=random.randint(0,4)
        zs=[i for i,x in enumerate(a) if x==0]
        best=n
        def dfs(j,left):
            nonlocal best
            if j==len(zs):
                c=capacity(a)
                formula=max((sum(y<x for y in a[i+1:]) for i,x in enumerate(a)),default=0)
                assert c==formula,('capacity formula',a,c,formula)
                best=min(best,c);return
            for x in range(left+1):a[zs[j]]=x;dfs(j+1,left-x)
            a[zs[j]]=0
        orig=a[:];dfs(0,k)
        inp=f'{n} {k}\n'+' '.join(map(str,orig))+'\n'
        check('N17','B_tramcar',inp,[best],partial=k==0,fileio=t==0 and k==0)
    check('N17','B_tramcar','4 0\n5 0 4 0\n',[3],fileio=True)
    for inp,ans in [('4 14\n5 0 4 0\n',1),('4 8\n5 0 4 0\n',2),('4 123456789\n40 30 20 10\n',3)]:check('N17','B_tramcar',inp,[ans],False)
    LOG.append('tramcar: 160 tiny cases, all affordable fillings and exact siding-state search; original 3 samples and K=0 file IO passed.')

def signature(n,edges):
    g=[[] for _ in range(n)]
    for x,y in edges:g[x].append(y);g[y].append(x)
    d=[999]*(n*2);d[0]=0;q=collections.deque([0])
    while q:
        v=q.popleft();x,p=divmod(v,2)
        for y in g[x]:
            z=y*2+(p^1)
            if d[z]==999:d[z]=d[v]+1;q.append(z)
    return tuple(d)

def connected():
    cases=[];ans=[]
    for n in range(2,6):
        es=list(itertools.combinations_with_replacement(range(n),2));best={};selected=[]
        for mask in range(1<<len(es)):
            c=mask.bit_count()
            if c<n-1:continue
            edges=[e for i,e in enumerate(es) if mask>>i&1];sig=signature(n,edges)
            if any(sig[2*i]==sig[2*i+1]==999 for i in range(n)):continue
            best[sig]=min(best.get(sig,999),c)
            selected.append((edges,sig))
        random.shuffle(selected)
        for edges,sig in selected[:min(120,len(selected))]:
            cases.append(f'{n} {len(edges)}\n'+''.join(f'{x+1} {y+1}\n' for x,y in edges));ans.append(best[sig])
    check('N17','C_connected',str(len(cases))+'\n'+''.join(cases),ans,fileio=True)
    LOG.append(f'connected: {len(cases)} inputs; oracle enumerates ALL graphs with loops on up to 5 labeled vertices, not just edge deletions; file IO passed.')

def crystal():
    cases=0
    for t in range(200):
        k=random.randint(1,4);n=random.randint(1,11);a=[''.join(random.choices('01',k=k)) for _ in range(k)];s=''.join(random.choices('abcd'[:k],k=n))
        seen={s};q=[s]
        for z in q:
            for i in range(1,len(z)):
                if a[ord(z[i-1])-97][ord(z[i])-97]=='1':
                    v=z[:i]+z[i+1:]
                    if v not in seen:seen.add(v);q.append(v)
        inp=f'{k} {n}\n'+'\n'.join(a)+'\n'+s+'\n'
        check('N17','D_crystal',inp,[min(seen)],fileio=t==0);cases+=1
    for s,ans in [('abacaba','aac'),('bcacb','bacb')]:check('N17','D_crystal',f'3 {len(s)}\n010\n001\n100\n{s}\n',[ans])
    LOG.append(f'crystal: {cases} cases versus BFS over all legal deletion sequences; original samples and file IO passed.')

if __name__=='__main__':
    compile_all()
    for fn in [sam,lis,wolf,power,median,tramcar,connected,crystal]:
        t=time.perf_counter();fn();print(fn.__name__,round(time.perf_counter()-t,3),'s PASS',flush=True)
        (TASK/'verification.json').write_text(json.dumps(LOG,ensure_ascii=False,indent=2),encoding='utf-8')
