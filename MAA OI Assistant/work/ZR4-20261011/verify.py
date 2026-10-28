from pathlib import Path
import subprocess, random, itertools, json, time

ROOT = Path(__file__).resolve().parents[2]
WORK = Path(__file__).resolve().parent
OUT = ROOT / 'outputs' / 'ZR4'
GPP = r'C:/TDM-GCC-64/bin/g++.exe'
rng = random.Random(20261011)
log = {}

def run(name, inp, local=True):
    exe = WORK / (name + ('' if local else '_file') + '.exe')
    if local:
        p = subprocess.run([str(exe)], input=inp, text=True, capture_output=True, check=True)
        return p.stdout.split()
    folder = WORK / ('io_' + name)
    folder.mkdir(exist_ok=True)
    (folder / (name + '.in')).write_text(inp, encoding='utf-8')
    subprocess.run([str(exe)], cwd=folder, check=True)
    return (folder / (name + '.out')).read_text().split()

for name in ('seq', 'xor', 'combo', 'game'):
    for local in (True, False):
        cmd = [GPP, '-std=c++17', '-O2', '-Wall', '-Wextra']
        if local: cmd += ['-DLOCAL']
        cmd += [str(OUT/name/'code.cpp'), '-o', str(WORK/(name+('' if local else '_file')+'.exe'))]
        subprocess.run(cmd, check=True)

samples = {
    'seq': [('3 1\n2 4 0\n1 1\n2 0 3\n', ['26']),
            ('3 2\n2 4 0\n1 1\n2 0 3\n', ['25']),
            ('3 2\n1 1\n2 0 2\n1 3\n', ['19'])],
    'xor': [('4\n3 3\n3 5 6\n2 0\n0 0\n1 3\n7\n4 4\n1 2 4 8\n', ['14','0','14','16']),
            ('2\n8 7\n4 23 33 52 54 57 85 101\n10 7\n17 30 33 61 64 92 93 99 112 124\n', ['232','254']),
            ('3\n1 0\n0\n3 20\n524288 524289 786432\n2 20\n1048574 1048575\n', ['0','1572864','2097150'])],
    'combo': [('1\n2\nab\nba\nabab\n', ['3'])],
    'game': [('6\n1 1 4 5 1 4\n5\n2 1 4\n2 2 6\n2 3 6\n1 5 7\n2 3 6\n', ['Bob','Alice','Bob','Alice'])]
}
for name, cases in samples.items():
    for inp, expected in cases:
        for local in (True, False):
            assert run(name, inp, local) == expected, (name, inp)
log['samples'] = 'All 8 printed sample cases pass in stdin/stdout and official file IO modes.'

for case in range(400):
    n = rng.randrange(2, 8)
    a = [[rng.randrange(7) for _ in range(rng.randrange(1, 5))] for _ in range(n)]
    vals = []
    for p in itertools.permutations(range(n)):
        seq = [x for i in p for x in a[i]]
        vals.append(sum((i+1)*x for i,x in enumerate(seq)))
    vals.sort(reverse=True)
    for k in (1,2):
        inp = f'{n} {k}\n' + ''.join(f'{len(s)} '+ ' '.join(map(str,s))+'\n' for s in a)
        got = int(run('seq',inp)[0])
        if got != vals[k-1]:
            (WORK/'first_seq_failure.in').write_text(inp)
            raise AssertionError((case,k,got,vals[k-1]))
log['seq'] = '800 random queries checked against full permutation enumeration, seed 20261011.'

cases=[]; expect=[]
for case in range(7000):
    alph = 'abcd'[:rng.randrange(1,5)]
    n = rng.randrange(1,9)
    pats = [''.join(rng.choice(alph) for _ in range(rng.randrange(1,8))) for _ in range(n)]
    if case % 3 == 0 and n > 1: pats[-1] = pats[0]
    if case % 5 == 0 and n > 1: pats[0] = pats[-1][:rng.randrange(1,len(pats[-1])+1)]
    t = ''.join(rng.choice(alph) for _ in range(rng.randrange(1,25)))
    expected = sum(all(s in t[l:r] for s in pats) for l in range(len(t)) for r in range(l+1,len(t)+1))
    cases.append(str(n)+'\n'+'\n'.join(pats)+'\n'+t+'\n')
    expect.append(expected)
inp = str(len(cases))+'\n'+''.join(cases)
got = list(map(int,run('combo',inp)))
if got != expect:
    j=next(i for i,(x,y) in enumerate(zip(got,expect)) if x!=y)
    (WORK/'first_combo_failure.in').write_text('1\n'+cases[j])
    raise AssertionError((j,got[j],expect[j]))
log['combo'] = '7000 random cases checked by enumerating all text intervals, seed 20261011.'

for name in ('game','xor'):
    p=subprocess.run([str(WORK/('check_'+name+'.exe'))],capture_output=True,text=True,check=True)
    log[name]=p.stdout.strip()

# Large legal cases; local wall-clock time is not an official judge verdict.
bench={}
def benchrun(name, inp):
    path=WORK/(name+'_large.in')
    path.write_text(inp,encoding='utf-8')
    with path.open() as f:
        start=time.perf_counter()
        p=subprocess.run([str(WORK/(name+'.exe'))],stdin=f,stdout=subprocess.DEVNULL,check=True)
        bench[name]=round(time.perf_counter()-start,3)

benchrun('seq','200000 2\n'+('5 1000000 1000000 1000000 1000000 1000000\n'*200000))
benchrun('xor','1\n1000000 20\n'+' '.join(str(rng.randrange(1<<20)) for _ in range(1000000))+'\n')
patterns=[''.join(p) for p in itertools.product('abcd',repeat=9)]
text=''.join(rng.choice('abcd') for _ in range(2000000))
# 4^9 * 9 exceeds the pattern budget; take 200000 distinct patterns (1.8M chars).
patterns=patterns[:200000]
benchrun('combo','1\n200000\n'+'\n'.join(patterns)+'\n'+text+'\n')
arr=[str(rng.randrange(1,1000000001)) for _ in range(1000000)]
ops=[]
for j in range(1000000):
    if j % 3 == 0:
        ops.append(f'1 {rng.randrange(1,1000001)} {rng.randrange(1,1000000001)}\n')
    else:
        l=rng.randrange(1,1000001);r=rng.randrange(1,1000001)
        if l>r:l,r=r,l
        ops.append(f'2 {l} {r}\n')
benchrun('game','1000000\n'+' '.join(arr)+'\n1000000\n'+''.join(ops))
log['large_case_seconds']=bench
(WORK/'verification.json').write_text(json.dumps(log,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(log,ensure_ascii=False,indent=2))
