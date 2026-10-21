from pathlib import Path
import subprocess, random, itertools, time, json
ROOT=Path(__file__).resolve().parent
R=random.Random(20261021)
report={'seed':20261021,'checks':[]}
def run(name,kind,data,expected=None,file=False,timeout=30):
    exe=ROOT/(name+'_'+kind+('_file' if file else '')+'.exe')
    if file:
        d=ROOT/'fileio'/name/kind
        d.mkdir(parents=True,exist_ok=True)
        (d/(name+'.in')).write_text(data,encoding='ascii')
        p=subprocess.run([str(exe)],cwd=d,capture_output=True,timeout=timeout)
        out=(d/(name+'.out')).read_text()
    else:
        p=subprocess.run([str(exe)],input=data,text=True,capture_output=True,timeout=timeout)
        out=p.stdout
    if p.returncode or (expected is not None and out.split()!=str(expected).split()):
        f=ROOT/(name+'_first_failure.in')
        if not f.exists():
            f.write_text(data)
            f.with_suffix('.json').write_text(json.dumps({'expected':str(expected),'actual':out,'returncode':p.returncode,'stderr':p.stderr},ensure_ascii=False))
        raise AssertionError((name,kind,str(expected)[:100],out[:100],p.returncode))
    return out
def checkbatch(name,cases,size,kind='std'):
    for k in range(0,len(cases),size):
        z=cases[k:k+size]
        run(name,kind,str(len(z))+'\n'+''.join(x[0] for x in z),'\n'.join(str(x[1]) for x in z))
def color_brute(s):
    masks={'U':0,'R':1,'Y':2,'B':4,'O':3,'P':5,'G':6,'A':7}
    ans=0
    for b in [1,2,4]:
        goal=sum((1<<i) for i,c in enumerate(s) if masks[c]&b)
        ops=[]
        for l in range(len(s)):
            for r in range(l,len(s)):
                z=((1<<(r-l+1))-1)<<l
                if z&goal==z: ops.append(z)
        f={0:0}
        for z in range(1<<len(s)):
            if z not in f: continue
            for op in ops:
                v=z|op
                f[v]=min(f.get(v,100),f[z]+1)
        ans+=f[goal]
    return ans
def greedy_brute(a,A,B):
    ans=0
    for p in itertools.permutations(a):
        x,y,z=A,B,0
        for c,u,v in p:
            if c<=x: x-=c; z+=u
            if c<=y: y-=c; z+=v
        ans=max(ans,z)
    return ans
def bracket_brute(a):
    f={0:0}
    for v in a:
        g={}
        for b,z in f.items():
            g[b+1]=max(g.get(b+1,-10**30),z+v)
            if b: g[b-1]=max(g.get(b-1,-10**30),z)
        f=g
    return f[0]
def noise_brute(a):
    return sum(all(a[l+i]==-a[l+m+i] for i in range(m)) for m in range(1,len(a)//2+1) for l in range(len(a)-2*m+1))
def main():
    samples={
        'color':('3\n9\nYYYBBBYYY\n6\nYYGGBB\n5\nROAOR\n','3\n2\n3'),
        'greedy':('2 6 8\n3 10 1\n5 8 10\n','21'),
        'brackets':('3\n4\n3 2 3\n3 4 5\n3 6 7\n3 -1 -1\n3\n1 10 100\n2 1 100000\n3 10000 1000\n1\n2 -1234567 7654321\n','2\n6\n12\n19\n100\n101\n100101\n-1234567'),
        'noise':('1\n9\n1 -3 2 -2 -1 3 -2 2 -2\n','4')}
    for name,(data,ans) in samples.items():
        for kind in ['std','partial']:
            run(name,kind,data,ans)
            run(name,kind,data,ans,file=True)
    report['checks'].append('all complete PDF samples, 8 LOCAL and 8 file-I/O programs')
    for data,ans in [('2 1 1\n1 5 1\n1 1 10\n','11'),('3 5 6\n4 1 100\n3 100 1\n2 10 10\n','220')]:
        for kind in ['std','partial']: run('greedy',kind,data,ans)
    cs=[]
    strings=[''.join(x) for n in range(1,4) for x in itertools.product('URYBOPGA',repeat=n)]
    strings+=[''.join(R.choices('URYBOPGA',k=R.randint(1,8))) for _ in range(400)]
    for s in strings: cs.append((str(len(s))+'\n'+s+'\n',color_brute(s)))
    for kind in ['std','partial']: checkbatch('color',cs,20,kind)
    report['checks'].append(f'color: {len(cs)} exhaustive/random independent interval-cover cases')
    print(report['checks'][-1],flush=True)
    for k in range(240):
        n=R.randint(1,7 if k<220 else 8)
        A,B=R.randint(1,15),R.randint(1,15)
        a=[(R.randint(1,15),R.randint(1,100),R.randint(1,100)) for _ in range(n)]
        data=f'{n} {A} {B}\n'+''.join(f'{c} {u} {v}\n' for c,u,v in a)
        ans=greedy_brute(a,A,B)
        for kind in ['std','partial']: run('greedy',kind,data,ans)
    for k in range(40):
        n,A=R.randint(9,150),R.randint(1,150)
        a=[(R.randint(1,150),R.randint(1,10**9),R.randint(1,10**9)) for _ in range(n)]
        f=[0]*(A+1)
        for c,u,v in a:
            for j in range(A,c-1,-1): f[j]=max(f[j],f[j-c]+u+v)
        data=f'{n} {A} {A}\n'+''.join(f'{c} {u} {v}\n' for c,u,v in a)
        for kind in ['std','partial']: run('greedy',kind,data,f[A])
    report['checks'].append('greedy: 240 permutation brute-force cases and 40 A=B knapsack cases')
    print(report['checks'][-1],flush=True)
    cs=[]
    for k in range(500):
        q=R.randint(1,50 if k<490 else 100)
        a=[]; ops=[]; ans=[]
        for i in range(q):
            t=R.randint(1,3)
            x,y=R.randint(-10,10),R.randint(-10,10)
            if k>=490: x*=10**6; y*=10**6
            if t==1: a=[y,x]+a
            if t==2: a=[x]+a+[y]
            if t==3: a=a+[x,y]
            ops.append(f'{t} {x} {y}\n')
            ans.append(bracket_brute(a))
        cs.append((str(q)+'\n'+''.join(ops),'\n'.join(map(str,ans))))
    for kind in ['std','partial']: checkbatch('brackets',cs,500,kind)
    report['checks'].append(f'brackets: 500 mixed-query cases ({sum(x[0].count(chr(10))-1 for x in cs)} answers) against balance DP')
    print(report['checks'][-1],flush=True)
    cs=[]
    arrays=[list(x) for n in range(1,10) for x in itertools.product([-1,1],repeat=n)]
    arrays += [[R.choice([-1,1])*R.randint(1,min(n,5)) for _ in range(n)] for n in [R.randint(1,50) for _ in range(600)]]
    arrays += [[1]*n for n in [2,3,17,50]]
    for a in arrays: cs.append((str(len(a))+'\n'+' '.join(map(str,a))+'\n',noise_brute(a)))
    for kind in ['std','partial']: checkbatch('noise',cs,3,kind)
    report['checks'].append(f'noise: {len(cs)} exhaustive/random cubic-brute cases')
    print(report['checks'][-1],flush=True)
    (ROOT/'validation.json').write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding='utf-8')
if __name__=='__main__': main()
