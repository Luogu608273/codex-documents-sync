import json, random, subprocess, time, ctypes
from pathlib import Path
ROOT=Path(__file__).resolve().parent
R=random.Random(20261013)
report=json.loads((ROOT/'verification.json').read_text(encoding='utf-8'))

def test(problem,label,data,want=None,name='std'):
    start=time.perf_counter()
    p=subprocess.run([str(ROOT/problem/(name+'.exe'))],input=data,text=True,capture_output=True,timeout=60)
    elapsed=time.perf_counter()-start
    if p.returncode or (want is not None and p.stdout.split()!=list(map(str,want))):
        (ROOT/'first_failure.in').write_text(data,encoding='utf-8')
        raise AssertionError((problem,label,p.returncode,p.stdout[:100],want))
    row={'problem':problem,'program':name,'case':label,'seconds':round(elapsed,3),'input_bytes':len(data)}
    report['stress'].append(row)
    print(json.dumps(row,ensure_ascii=False),flush=True)

n=m=1000000
data=f'{n} {m}\n'+'1 '*n+'\n'+'1 1 1\n'*m
test('nlp','n=m=1000000_duplicate_rules_full_merge',data,[1,1])
data=f'{n} {m}\n'+'1 '*n+'\n'+''.join(f'{i} {i} 1\n' for i in range(m,0,-1))
test('nlp','n=m=1000000_distinct_reverse_rules_full_merge',data,[1,1])
del data

def singleton(n,m,kind):
    # n*m <= 2000000, all sets have one element.
    s=['1',f'{n} {m}',('1 '*m+'\n')*n]
    for i in range(n):
        if kind=='same': row=[1]*m
        elif kind=='distinct': row=[i+1]*m
        elif kind=='last_pair': row=[min(i+1,n-1)]*m
        elif kind=='alternating': row=[i+1 if j%2==0 else 1 for j in range(m)]
        s.append(' '.join(map(str,row)))
    return '\n'.join(s)+'\n'

for kind in ['same','distinct','last_pair','alternating']:
    n,m=1000,2000
    if kind in ['same','last_pair']: want=[0]
    elif kind=='distinct': want=[m*(m-1)//2]
    else: want=[sum(max(0,r-3 if r%2==0 else r-2) for r in range(1,m+1))]
    test('card',f'n=1000_m=2000_{kind}',singleton(n,m,kind),want)
for kind in ['same','distinct','alternating']:
    n,m=2,200000
    want=[0] if kind=='same' else [m*(m-1)//2] if kind=='distinct' else [sum(max(0,r-3 if r%2==0 else r-2) for r in range(1,m+1))]
    test('card',f'n=2_m=200000_{kind}',singleton(n,m,kind),want)
test('card','n=1_m=200000',singleton(1,200000,'same'),[200000*200001//2])
n,m=200,1000
test('card','partial_n=200_m=1000_distinct',singleton(n,m,'distinct'),[m*(m-1)//2],name='partial_scalar')
test('game','T=100000_max_boundary','100000\n'+'1 1000000\n'*100000,['0.50000']*100000)
report['memory_bound']={'card_word_count_n1000':sum(16-((i+1)//64) for i in range(999)),
    'card_two_matrices_bytes_n1000_m2000':2*2000*8*sum(16-((i+1)//64) for i in range(999))}
(ROOT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
