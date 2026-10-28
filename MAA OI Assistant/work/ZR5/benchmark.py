import json, pathlib, random, subprocess, time
D=pathlib.Path(__file__).resolve().parent
P=998244353
R=random.Random(20261018)
results=[]
def bench(name, label, data, expected=None, timeout=30):
    path=D/(label+'.in');path.write_text(data,encoding='utf-8')
    begin=time.perf_counter()
    with path.open() as f:
        r=subprocess.run([str(D/(name+'.exe'))],stdin=f,capture_output=True,text=True,timeout=timeout)
    elapsed=round(time.perf_counter()-begin,3)
    if r.returncode:raise AssertionError((name,r.returncode,r.stderr))
    ans=list(map(int,r.stdout.split()))
    if expected is not None and ans!=expected:raise AssertionError((label,ans[:10],expected[:10]))
    x=dict(program=name,case=label,seconds=elapsed,input_bytes=len(data),output_lines=len(ans))
    results.append(x);print(json.dumps(x),flush=True)

bench('buffer_std','buffer6000equal','6000\n'+'a'*6000+'\n'+'a'*6000+'\n',[0])
s=''.join(R.choice('abcd') for _ in range(6000))
bench('buffer_std','buffer6000reverse','6000\n'+s+'\n'+s[::-1]+'\n',[1])
n=50000
words=[''.join(chr(97+(i//(26**j))%26) for j in range(4)) for i in range(n)]
bench('alphabet_std','alphabetL200000',str(n)+'\n'+'\n'.join(words)+'\n')
bench('alphabet_std','alphabetdeep','1\n'+'a'*200000+'\n',[0])
bench('counter_std','counter200000','200000 1000000000000\n'+''.join(f'{i*5000000} 0\n' for i in range(200000)))
for shape in ('chain','binary','star'):
    n=q=500000
    edges=''.join(f'{(i-1 if shape=="chain" else i//2 if shape=="binary" else 1)} {i}\n' for i in range(2,n+1))
    data=f'{n} {q}\n'+'0 '*n+'\n'+edges+''.join(f'{i+1} 0\n' for i in range(q))
    g=[1]*(n+1)
    for i in range(n,1,-1):
        p=i-1 if shape=='chain' else i//2 if shape=='binary' else 1
        g[p]=g[p]*(g[i]+1)%P
    up=[1]*(n+1)
    if shape=='chain':
        for i in range(2,n+1):up[i]=i
    elif shape=='star':
        z=(pow(2,n-2,P)+1)%P
        for i in range(2,n+1):up[i]=z
    else:
        for i in range(1,n+1):
            if i*2<=n:up[i*2]=(up[i]*(g[i*2+1]+1 if i*2+1<=n else 1)+1)%P
            if i*2+1<=n:up[i*2+1]=(up[i]*(g[i*2]+1)+1)%P
    expected=[g[i]*up[i]%P for i in range(1,n+1)]
    bench('subsidy_std','subsidy500000_'+shape,data,expected)
n=500000
edges=''.join(f'1 {i}\n' for i in range(2,n+1))
bench('subsidy_std','subsidy500000_heap',f'{n} 1\n-1000000000 '+'1 '*(n-1)+'\n'+edges+'1 2000\n',[1])
(D/'benchmark.json').write_text(json.dumps(results,indent=2),encoding='utf-8')
