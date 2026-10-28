import itertools, json, random, subprocess, time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
R = random.Random(20261013)
report = {'seed': 20261013, 'checks': [], 'stress': []}

def run(problem, name, data, timeout=30):
    start = time.perf_counter()
    p = subprocess.run([str(ROOT / problem / (name + '.exe'))], input=data,
                       text=True, capture_output=True, timeout=timeout)
    if p.returncode:
        raise RuntimeError((problem, name, p.returncode, p.stderr))
    return p.stdout.split(), time.perf_counter() - start

def check(problem, name, data, expected):
    got, _ = run(problem, name, data)
    want = str(expected).split() if not isinstance(expected, list) else list(map(str, expected))
    if got != want:
        (ROOT / 'first_failure.in').write_text(data, encoding='utf-8')
        raise AssertionError((problem, name, got, want))

# Finite brute force searches a substantially larger rectangle than the inputs.
cases = [(a,b) for a in range(1,31) for b in range(1,31)]
expect = []
for a,b in cases:
    best = min((x*(x-1)+y*(y-1))/((x+y)*(x+y-1))
               for x in range(a,71) for y in range(b,71))
    expect.append(f'{best:.5f}')
data = str(len(cases))+'\n'+'\n'.join(f'{a} {b}' for a,b in cases)+'\n'
for name in ['std','partial_enumerate']:
    check('game', name, data, expect)
check('game','std','4\n2 3\n1 5\n10 11\n999999 1000000\n',
      ['0.40000','0.44444','0.47619','0.50000'])
report['checks'].append({'game_exhaustive_inputs':len(cases),'search_bound':70})

def nlp_brute(a,s):
    a = a[:]
    while True:
        found = False
        for x,y,z in s:
            for i in range(len(a)-1):
                if a[i] == x and a[i+1] == y:
                    a[i:i+2] = [z]
                    found = True
                    break
            if found: break
        if not found: return [len(a)] + a

nc = []
for n in range(1,7):
    for a in itertools.product([1,2],repeat=n):
        for s in [[(1,1,1)],[(1,1,2)],[(1,2,1)],[(1,2,2)],
                  [(2,1,1)],[(2,1,2)],[(2,2,1)],[(2,2,2)],
                  [(1,1,2),(2,2,1)],[(1,2,2),(1,2,1),(2,2,1)]]:
            # Token bounds are n+m; all above are legal except n=1,m=1, still max=2.
            nc.append((a,s))
for _ in range(500):
    n,m = R.randint(1,25),R.randint(1,25)
    a=[R.randint(1,min(n+m,5)) for i in range(n)]
    s=[tuple(R.randint(1,min(n+m,5)) for i in range(3)) for j in range(m)]
    nc.append((a,s))
for a,s in nc:
    data=f'{len(a)} {len(s)}\n'+' '.join(map(str,a))+'\n'
    data+=''.join(' '.join(map(str,t))+'\n' for t in s)
    want=nlp_brute(list(a),s)
    for name in ['std','partial_scan']: check('nlp',name,data,want)
for name in ['std','partial_scan']:
    check('nlp',name,'5 3\n3 3 2 2 2\n1 2 7\n3 3 1\n2 2 9\n',[2,7,9])
    check('nlp',name,'4 2\n1 1 1 1\n1 1 2\n2 2 3\n',[1,3])
report['checks'].append({'nlp_against_rule_first_brute':len(nc)})

def card_data(cases):
    s=[str(len(cases))]
    for a in cases:
        n,m=len(a),len(a[0]); s.append(f'{n} {m}')
        for row in a: s.append(' '.join(str(len(x)) for x in row))
        s.append(' '.join(str(x) for row in a for cell in row for x in sorted(cell)))
    return '\n'.join(s)+'\n'

def card_brute(a):
    n,m=len(a),len(a[0]); ans=0
    for l in range(m):
        for r in range(l,m):
            ok=True
            for bad in range(l,r+1):
                for x in range(n):
                    for y in range(x+1,n):
                        if all(a[x][j]&a[y][j] for j in range(l,r+1) if j!=bad):
                            ok=False
            ans+=ok
    return ans

cc=[]
sets=[{1},{2},{1,2}]
for m in range(1,4):
    for cells in itertools.product(sets,repeat=2*m):
        cc.append([list(cells[:m]),list(cells[m:])])
for _ in range(500):
    n,m=R.randint(1,7),R.randint(1,9)
    cc.append([[set(R.sample(range(1,8),R.randint(1,4))) for j in range(m)] for i in range(n)])
# Cross 64-bit boundaries and exercise a multiword final student row.
for n in [63,64,65,127,128,129]:
    for t in range(4):
        cc.append([[{i+1 if R.randrange(4) else 1} for j in range(5)] for i in range(n)])
for t in range(0,len(cc),10):
    batch=cc[t:t+10]
    want=[card_brute(a) for a in batch]
    data=card_data(batch)
    for name in ['std','partial_pairs','partial_scalar']: check('card',name,data,want)
check('card','std','2\n2 3\n1 1 1\n1 1 1\n1 3 4 2 3 5\n2 4\n1 1 1 1\n1 1 1 1\n1 2 4 6 1 3 5 6\n',[1,4])
report['checks'].append({'card_against_deleted_coordinate_brute':len(cc)})
print(json.dumps(report,ensure_ascii=False,indent=2),flush=True)
(ROOT/'verification.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
