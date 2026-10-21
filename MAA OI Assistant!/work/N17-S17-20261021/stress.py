import verify as v
from pathlib import Path
import subprocess, time, random, json, ctypes
T=v.TASK
for f in (T/'bin').glob('*_local.exe'):
    group,letter,name,typ,_=f.stem.split('_')
    v.EXE[group,letter+'_'+name,typ,True]=f
REPORT=[]

class PMC(ctypes.Structure):
    _fields_=[('cb',ctypes.c_ulong),('PageFaultCount',ctypes.c_ulong),('PeakWorkingSetSize',ctypes.c_size_t),('WorkingSetSize',ctypes.c_size_t),('QuotaPeakPagedPoolUsage',ctypes.c_size_t),('QuotaPagedPoolUsage',ctypes.c_size_t),('QuotaPeakNonPagedPoolUsage',ctypes.c_size_t),('QuotaNonPagedPoolUsage',ctypes.c_size_t),('PagefileUsage',ctypes.c_size_t),('PeakPagefileUsage',ctypes.c_size_t)]

def timed(group,name,inp,expected=None,label='',typ='std'):
    start=time.perf_counter()
    p=subprocess.Popen([str(v.EXE[group,name,typ,True])],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=p.communicate(inp.encode(),timeout=60)
    dt=time.perf_counter()-start
    pm=PMC();pm.cb=ctypes.sizeof(pm)
    ok=ctypes.windll.psapi.GetProcessMemoryInfo(ctypes.c_void_p(int(p._handle)),ctypes.byref(pm),pm.cb)
    if p.returncode:raise RuntimeError((group,name,p.returncode,err))
    got=out.decode().split()
    if expected is not None:
        expected=list(map(str,expected))
        if got!=expected:raise AssertionError((group,name,label,got[:20],expected[:20]))
    item=dict(group=group,problem=name,variant=typ,label=label,seconds=round(dt,3),peak_working_set_MiB=round(pm.PeakWorkingSetSize/2**20,1) if ok else None,output_tokens=len(got),expected_checked=expected is not None)
    REPORT.append(item);print(item,flush=True)
    (T/'stress.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2),encoding='utf-8')
    return got

def official():
    random.seed(712021)
    for group,letter,name in [('N17','B','B_tramcar'),('N17','C','C_connected')]:
        f=T/'reference'/group/(letter+'.cpp');out=T/'bin'/('ref_'+name+'.exe')
        text=f.read_text(encoding='utf-8-sig');text=text.replace('freopen("tramcar.in","r",stdin);','').replace('freopen("tramcar.out","w",stdout);','').replace('freopen("connected.in","r",stdin);','').replace('freopen("connected.out","w",stdout);','')
        # Accommodate reference whitespace exactly via regex.
        import re
        text=re.sub(r'freopen\([^;]+;', '', text)
        tmp=T/'reference'/group/(letter+'_local.cpp');tmp.write_text(text,encoding='utf-8')
        r=subprocess.run([v.CXX,str(tmp),'-std=c++17','-O2','-w','-o',str(out)],capture_output=True,text=True)
        if r.returncode:raise RuntimeError(r.stderr)
        for t in range(40):
            if letter=='B':
                n=random.randint(10,1500);a=[random.randrange(10000) if random.random()<.65 else 0 for _ in range(n)];inp=f'{n} {random.randrange(10**7)}\n'+' '.join(map(str,a))+'\n'
            else:
                cases=[]
                for _ in range(30):
                    n=random.randrange(6,100);es={(i,random.randrange(i)) for i in range(1,n)}
                    for j in range(random.randrange(2*n)):es.add(tuple(sorted((random.randrange(n),random.randrange(n)))))
                    cases.append(f'{n} {len(es)}\n'+''.join(f'{x+1} {y+1}\n' for x,y in es))
                inp=str(len(cases))+'\n'+''.join(cases)
            r=subprocess.run([str(out)],input=inp,capture_output=True,text=True,timeout=15)
            assert r.returncode==0
            v.check(group,name,inp,r.stdout.split(),partial=False)
        REPORT.append(dict(group=group,problem=name,label='official reference differential',cases=40 if letter=='B' else 1200))
        print(name,'official differential PASS',flush=True)

def samples():
    v.check('S17','A_sam','6 3\nbanana\n1 6\n2 5\n3 3\n',[3,2,1])
    v.check('S17','A_sam','4 2\nabab\n1 4\n1 2\n',[2,1])
    v.check('S17','B_lis','3\n3 1 2\n',[1,2,2])
    v.check('S17','B_lis','5\n2 5 3 1 4\n',[1,1,2,3,3])
    v.check('S17','C_wolf','3\n3\nRLL\n1 0 0\n3\nRRR\n2 0 1\n5\nRRLRR\n1 2 1 1 0\n',[1,0,1])
    v.check('S17','C_wolf','1\n5\nLRLLR\n0 1 1 1 0\n',[6])
    w='2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97 101 103 107 109 113\n'
    v.check('S17','D_power',w+'4\n1\n2\n3\n4\n',[2,7,14,42])
    v.check('S17','D_power',w+'6\n5\n6\n7\n15\n16\n32768\n',[84,210,420,165060,345218,900837553])
    for a,ans in [([1,1,1,1],'Yes'),([1,2,3,3,2,1],'Yes'),([1,2,1,3,2,3],'No')]:v.check('N17','A_median',str(len(a))+'\n'+' '.join(map(str,a))+'\n',[ans])
    v.check('N17','C_connected','2\n5 5\n1 2\n2 3\n2 5\n1 4\n4 5\n5 5\n1 2\n2 3\n3 4\n4 5\n1 5\n',[4,5])
    REPORT.append(dict(label='samples',result='S17 all samples; N17 median all, tramcar all, crystal all, connected sample 1 checked.'))

def large():
    n=10**6;q=10**6
    timed('S17','A_sam',f'{n} {q}\n'+'a'*n+'\n'+('1 1000000\n'*q),[n]*q,'n=q=1e6, identical characters')
    timed('S17','B_lis',str(n)+'\n'+' '.join(map(str,range(n,0,-1)))+'\n',[1]*n,'n=1e6, decreasing')
    timed('S17','B_lis',str(n)+'\n'+' '.join(map(str,range(1,n+1)))+'\n',range(1,n+1),'n=1e6, increasing')
    n=500000
    # Every even position is L with b=i/2; odds are R with b=(n-i)/2, forcing a structured candidate.
    random.seed(818)
    d=''.join(random.choices('LR',k=n));b=[i//2 if c=='L' else (n-i)//2 for i,c in enumerate(d,1)]
    inp=f'1\n{n}\n{d}\n'+' '.join(map(str,b))+'\n'
    timed('S17','C_wolf',inp,label='sum n=5e5, alternating wolf assignment with mixed directions')
    # Maximize valid, dispersed event labels in the segment tree.
    b=[random.randrange(n//4) for _ in range(n)]
    timed('S17','C_wolf',f'1\n{n}\n'+('LR'*(n//2))+'\n'+' '.join(map(str,b))+'\n',label='n=5e5, O(n) distinct-q events')
    n=5000
    timed('S17','C_wolf',f'1\n{n}\n'+('L'*n)+'\n'+('0 '*n)+'\n',label='partial n=5000',typ='partial')
    q=10**6
    timed('S17','D_power',' '.join(['1']*30)+f'\n{q}\n'+('1073741823\n'*q),[v.coef([1]*30,(1<<30)-1)]*q,'q=1e6, max n, all weights=1')
    n=200000
    timed('N17','A_median',str(n)+'\n'+' '.join(map(str,range(1,n+1)))+'\n',['No'],'n=2e5, strictly increasing')
    n=300000
    timed('N17','B_tramcar',f'{n} 0\n'+' '.join(map(str,range(n,0,-1)))+'\n',[n-1],'n=3e5, K=0, decreasing')
    timed('N17','B_tramcar',f'{n} 1000000000000\n'+('1000000 0 '*(n//2))+'\n',[0],'n=3e5, 1.5e5 empty cars, sufficient K')
    n=100000
    inp=f'1\n{n} {n-1}\n'+''.join(f'{i} {i+1}\n' for i in range(1,n))
    timed('N17','C_connected',inp,[n-1],'n=1e5, path')
    inp=f'1\n{n} {n}\n'+''.join(f'{i} {i+1}\n' for i in range(1,n))+f'{n} {n}\n'
    timed('N17','C_connected',inp,[n],'n=1e5, path and far-end self-loop')
    n=500000
    timed('N17','D_crystal',f'1 {n}\n0\n'+'a'*n+'\n',['a'*n],'n=5e5, no deletions')
    timed('N17','D_crystal',f'1 {n}\n1\n'+'a'*n+'\n',['a'],'n=5e5, all deletable')
    s=('abacaba'*((n+6)//7))[:n]
    timed('N17','D_crystal',f'3 {n}\n010\n001\n100\n'+s+'\n',label='n=5e5, periodic string, cyclic deletion rules')
    # Partial boundary cases, checked against standard.
    for group,name,inp in [('S17','B_lis','5000\n'+' '.join(map(str,range(5000,0,-1)))+'\n'),('N17','A_median','2000\n'+' '.join(map(str,range(1,2001)))+'\n'),('N17','B_tramcar','5000 0\n'+' '.join(map(str,range(5000,0,-1)))+'\n'),('N17','D_crystal','3 500\n010\n001\n100\n'+('abacaba'*72)[:500]+'\n')]:
        expected=v.run(group,name,inp)
        timed(group,name,inp,expected,'partial supported upper boundary',typ='partial')

if __name__=='__main__':
    samples();official();large()
    (T/'stress.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2),encoding='utf-8')
