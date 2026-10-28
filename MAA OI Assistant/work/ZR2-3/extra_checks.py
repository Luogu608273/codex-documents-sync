from validate import ROOT, R, run, bracket_brute, checkbatch
import json,time
cs=[]
for k in range(500):
    q=R.randint(1,100)
    a=[]; ops=[]; ans=[]
    for i in range(q):
        t=R.randint(1,3); x=R.randint(-10**7,10**7); y=R.randint(-10**7,10**7)
        if t==1: a=[y,x]+a
        if t==2: a=[x]+a+[y]
        if t==3: a=a+[x,y]
        ops.append(f'{t} {x} {y}\n'); ans.append(bracket_brute(a))
    cs.append((str(q)+'\n'+''.join(ops),'\n'.join(map(str,ans))))
for kind in ['std','partial']: checkbatch('brackets',cs,500,kind)
run('brackets','partial','1\n2000\n'+'2 10000000 10000000\n'*2000,'\n'.join(str(i*10**7) for i in range(1,2001)))
run('brackets','partial','1\n2\n1 10 100\n2 1 100000\n','100\n101',file=True)
passed=[]; skipped=[]
for f in sorted((ROOT/'official_C').glob('*.in')):
    data=f.read_text(); z=list(map(int,data.split())); n,A,B=z[:3]
    if len(z)!=3+3*n or n>150 or A>150 or B>150 or max(z[3::3])>150:
        skipped.append(f.name); continue
    ans=f.with_suffix('.ans').read_text()
    run('greedy','std',data,ans)
    passed.append(f.name)
result={'brackets_extra_cases':500,'brackets_extra_answers':sum(x[0].count('\n')-1 for x in cs),'brackets_partial_q2000':True,'greedy_official_cases_passed':passed,'greedy_official_cases_skipped_outside_pdf_constraints':skipped}
(ROOT/'extra_validation.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
print({k:(len(v) if isinstance(v,list) else v) for k,v in result.items()})
