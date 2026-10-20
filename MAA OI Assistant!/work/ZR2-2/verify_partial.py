import ctypes
import itertools
import json
import random
import subprocess
import time
from pathlib import Path
import verify

ROOT = Path(__file__).resolve().parent
RNG = random.Random(2026102002)
REPORT = []


class Counters(ctypes.Structure):
    _fields_ = [('cb', ctypes.c_ulong), ('faults', ctypes.c_ulong)] + [(x, ctypes.c_size_t) for x in ['peak', 'working', 'p1', 'p2', 'p3', 'p4', 'page', 'pagepeak']]


def run(name, data, expected=None, mode='local', oracle=True):
    t = time.perf_counter()
    if mode == 'file':
        d = ROOT / f'partial-file-{name}'
        d.mkdir(exist_ok=True)
        (d / f'{name}.in').write_text(data, encoding='ascii')
        p = subprocess.run([str(ROOT/f'{name}-partial-file.exe')], cwd=d, capture_output=True, timeout=30)
        out = (d/f'{name}.out').read_text(encoding='ascii')
        assert not p.stdout
    else:
        p = subprocess.run([str(ROOT/f'{name}-partial-local.exe')], input=data.encode(), capture_output=True, timeout=30)
        out = p.stdout.decode()
    assert p.returncode == 0, (name,p.returncode,p.stderr)
    if expected is not None and out.split() != str(expected).split():
        (ROOT/f'{name}-partial-first-failure.in').write_text(data,encoding='ascii')
        (ROOT/f'{name}-partial-first-failure.json').write_text(json.dumps(dict(seed=2026102002,expected=str(expected),actual=out)),encoding='utf-8')
        raise AssertionError((name,str(expected)[:400],out[:400]))
    if oracle:
        std,_ = verify.run(name,data)
        if name == 'bracket':
            assert list(map(len,out.splitlines())) == list(map(len,std.splitlines()))
        else:
            assert out.split() == std.split(),name
    return out,time.perf_counter()-t


def save(row):
    REPORT.append(row)
    (ROOT/'partial-validation.json').write_text(json.dumps(REPORT,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(row,ensure_ascii=False),flush=True)


def samples():
    ss=['0000','101','99099','9','221']
    data='5\n'+'\n'.join(ss)+'\n'
    for mode in ['local','file']:
        out,_=run('bracket',data,mode=mode)
        verify.bracket_check(ss,out)
    data='2 1 8 17\n1 1\n1 0\n2 1\n3 1 0\n3 1 1\n3 2 0\n3 2 1\n3 3 0\n3 3 1\n0 4 0\n0 4 1\n'
    for mode in ['local','file']:
        run('poly',data,'4 6 8 7 9 14 6 3',mode)
    data='3\n2 3\n3 1\n2 3 3\n2 5 7\n2 3\n3 1\n1 2 3\n1 1 1\n2 3\n3 1\n2 3 1\n100 2 3\n'
    for mode in ['local','file']:
        run('transform',data,'7 -1 3',mode)
    for data,ans in [
        ('4 8 3\n1 1 4 10\n1 1 2 20\n3 1 2\n3 1 3\n1 3 3 30\n3 1 3\n2 1 2 20\n3 1 2\n','3 1 4 3'),
        ('3 9 2\n1 1 3 5\n1 1 1 7\n1 2 2 8\n3 1 2\n3 1 3\n2 1 1 7\n3 1 2\n2 2 2 8\n3 1 2\n','4 1 2 3'),
        ('2 6 3\n1 1 2 1\n1 1 1 2\n1 1 1 3\n1 1 1 4\n3 1 2\n3 2 1\n','1 2'),
        ('2 6 3\n1 1 2 1000000000000\n1 1 1 999999999999\n1 1 1 999999999998\n3 1 2\n2 1 1 999999999998\n3 1 2\n','1 1')]:
        for mode in ['local','file']:
            run('set',data,ans,mode)
    save(dict(test='PDF samples',both_io_modes=True,result='passed'))


def bracket():
    strings=[''.join(t) for n in range(1,7) for t in itertools.product('0123',repeat=n)]
    strings += [''.join(RNG.choices('0123456789',k=RNG.randint(1,40))) for _ in range(1000)]
    groups=[]
    batch=[]
    total=0
    for s in strings:
        if total+len(s)>1000:
            groups.append(batch)
            batch=[]
            total=0
        batch.append(s)
        total+=len(s)
    if batch:
        groups.append(batch)
    for batch in groups:
        assert sum(map(len,batch))<=1000
        data=str(len(batch))+'\n'+'\n'.join(batch)+'\n'
        out,_=run('bracket',data)
        verify.bracket_check(batch,out)
    save(dict(test='bracket exhaustive and random',cases=len(strings),groups=len(groups),sum_length_per_group_at_most=1000,result='passed'))


def poly():
    count=0
    for _ in range(100):
        p=RNG.randint(2,1000)
        terms=[[(RNG.randint(0,10**9),RNG.choice([0,1,2,10**9,RNG.randint(0,10**9)])) for _ in range(RNG.randint(1,10))] for s in range(2)]
        qs=[(RNG.choice([0,p,10**9,RNG.randint(0,10**9)]),RNG.choice([1,2,3,1000,RNG.randint(1,1000)]),RNG.randrange(2)) for _ in range(100)]
        data=f'{len(terms[0])} {len(terms[1])} {len(qs)} {p}\n'
        data+=''.join(f'{a} {b}\n' for ts in terms for a,b in ts)
        data+=''.join(f'{x} {y} {s}\n' for x,y,s in qs)
        ans='\n'.join(str(verify.poly_answer(terms,p,*q)) for q in qs)
        run('poly',data,ans)
        count+=len(qs)
    save(dict(test='poly random',instances=100,queries=count,p_q_y_at_most=1000,result='passed'))


def transform():
    cases=[]
    for m in range(1,4):
        for b in itertools.product(range(m),repeat=m):
            for a in itertools.product(range(m),repeat=3):
                cases.append((a,b,[i*2+1 for i in range(m)]))
    for _ in range(3000):
        n,m=RNG.randint(1,15),RNG.randint(1,15)
        cases.append(([RNG.randrange(m) for _ in range(n)],[RNG.randrange(m) for _ in range(m)],[RNG.choice([1,10**9,RNG.randint(1,1000)]) for _ in range(m)]))
    groups=[]
    batch=[]
    sn=sm=0
    for case in cases:
        a,b,c=case
        if sn+len(a)>2000 or sm+len(b)>2000:
            groups.append(batch)
            batch=[]
            sn=sm=0
        batch.append(case)
        sn+=len(a)
        sm+=len(b)
    if batch:
        groups.append(batch)
    for batch in groups:
        assert sum(len(c[0]) for c in batch)<=2000 and sum(len(c[1]) for c in batch)<=2000
        data=[str(len(batch))]
        ans=[]
        for a,b,c in batch:
            data.extend([f'{len(a)} {len(b)}',' '.join(str(x+1) for x in a),' '.join(str(x+1) for x in b),' '.join(map(str,c))])
            ans.append(str(verify.transform_answer(a,b,c)))
        run('transform','\n'.join(data)+'\n','\n'.join(ans))
    save(dict(test='transform exhaustive and random',cases=len(cases),groups=len(groups),sum_n_and_sum_m_per_group_at_most=2000,result='passed'))


def sets():
    queries=0
    for k in [1,2,7,30]:
        for _ in range(10):
            n=RNG.randint(2,50)
            ss=[set() for _ in range(n)]
            vals=[1,10**12]+RNG.sample(range(2,10**12),98)
            ops=[]
            ans=[]
            for j in range(1500):
                if RNG.random()<.5:
                    u,v=RNG.randrange(n),RNG.randrange(n)
                    if abs(len(ss[u])-len(ss[v]))<=k:
                        ops.append(f'3 {u+1} {v+1}')
                        ans.append(str(verify.relation(ss[u],ss[v])))
                        continue
                x=RNG.choice(vals)
                l=r=RNG.randrange(n)
                old=x in ss[l]
                while l and (x in ss[l-1])==old and RNG.random()<.75:
                    l-=1
                while r+1<n and (x in ss[r+1])==old and RNG.random()<.75:
                    r+=1
                for i in range(l,r+1):
                    if old:
                        ss[i].remove(x)
                    else:
                        ss[i].add(x)
                ops.append(f'{2 if old else 1} {l+1} {r+1} {x}')
            run('set',f'{n} {len(ops)} {k}\n'+'\n'.join(ops)+'\n','\n'.join(ans))
            queries+=len(ans)
    save(dict(test='set legal random operations',instances=40,queries=queries,n_m_at_most=2000,result='passed'))


def maximum(name,data,expected=None,bracket_string=None,tag=''):
    src=ROOT/f'partial-max-{name}{tag}.in'
    dst=ROOT/f'partial-max-{name}{tag}.out'
    src.write_text(data,encoding='ascii')
    with src.open('rb') as f,dst.open('wb') as g:
        t=time.perf_counter()
        p=subprocess.Popen([str(ROOT/f'{name}-partial-local.exe')],stdin=f,stdout=g,stderr=subprocess.PIPE)
        _,err=p.communicate(timeout=30)
        elapsed=time.perf_counter()-t
        info=Counters()
        info.cb=ctypes.sizeof(info)
        fn=ctypes.windll.psapi.GetProcessMemoryInfo
        fn.argtypes=[ctypes.c_void_p,ctypes.c_void_p,ctypes.c_ulong]
        ok=fn(int(p._handle),ctypes.byref(info),ctypes.sizeof(info))
    assert p.returncode==0,(name,p.returncode,err)
    out=dst.read_text()
    if bracket_string:
        verify.bracket_check([bracket_string],out)
    else:
        assert out.split()==str(expected).split(),(name,out[:200])
    # Cross-check numerical results with the independently structured full solution.
    if name!='bracket':
        std,_=verify.run(name,data)
        assert std.split()==out.split()
    save(dict(test=name+' maximum supported '+tag,seconds=round(elapsed,4),peak_working_set_mib=round(info.peak/2**20,2) if ok else None,result='passed'))


def maxima():
    text='90'*500
    maximum('bracket','1\n'+text+'\n',bracket_string=text)
    p=1000
    data='10 10 1000 1000\n'
    for s in range(2):
        for j in range(4):
            a,b=123+j*17,10**9-j*12345
            data+=f'{a} {b}\n{p-a} {b}\n'
        data+=f'{s+1} 1\n1 0\n'
    ans=[]
    z=pow(2,500,p)
    for i in range(1000):
        x=i*1000000
        s=i%2
        data+=f'{x} 1000 {s}\n'
        ans.append(str((z*x+(3 if s==0 else 2)*(z-1))%p))
    maximum('poly',data,'\n'.join(ans))
    n=m=2000
    data=f'1\n{n} {m}\n'+'1 '*(n-2)+f'{m} 1\n'
    data+=' '.join(map(str,range(2,m+1)))+f' {m}\n'+'1000000000 '*m+'\n'
    maximum('transform',data,str((m-1)*10**9))
    data='2000 2000 30\n'+''.join(f'1 1 2000 {i+1}\n' for i in range(1000))+''.join(f'3 {i%2000+1} {(i*17)%2000+1}\n' for i in range(1000))
    maximum('set',data,'3\n'*1000,tag='mixed')
    data='2000 2000 30\n'+''.join(f'1 1 2000 {i+1}\n' for i in range(2000))
    maximum('set',data,'',tag='storage')


if __name__=='__main__':
    for fn in [samples,bracket,poly,transform,sets,maxima]:
        fn()
    print('ALL PARTIAL CHECKS PASSED',flush=True)
