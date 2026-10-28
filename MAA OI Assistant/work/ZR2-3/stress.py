from validate import ROOT, R, run
import time,json
records=[]
def test(name,kind,data,ans,label):
    t=time.perf_counter()
    out=run(name,kind,data,ans,timeout=120)
    records.append({'problem':name,'program':kind,'case':label,'seconds':round(time.perf_counter()-t,3),'output_tokens':len(out.split()),'expected_checked':ans is not None})
    print(records[-1],flush=True)
test('color','std','20\n'+('100000\n'+'A'*100000+'\n')*20,'3\n'*20,'20 * N=100000, all A')
test('color','partial','20\n'+('1000\n'+'A'*1000+'\n')*20,'3\n'*20,'20 * N=1000, quadratic worst case')
test('greedy','std','150 150 150\n'+('1 1000000000 1000000000\n')*150,300000000000,'maximum score, A=B=150')
a=[(R.randint(1,10),R.randint(1,10**9),R.randint(1,10**9)) for _ in range(150)]
data='150 149 150\n'+''.join(f'{c} {u} {v}\n' for c,u,v in a)
test('greedy','std',data,None,'dense reachable states, A=149 B=150')
test('brackets','std','1\n400000\n'+('3 10000000 10000000\n')*400000,'\n'.join(str(i*10000000) for i in range(1,400001)),'400000 right insertions, maximum sum')
ops=''.join(f'{R.randint(1,3)} -10000000 -10000000\n' for _ in range(400000))
test('brackets','std','1\n400000\n'+ops,'\n'.join(str(-i*10000000) for i in range(1,400001)),'400000 mixed insertions, negative equal values')
n=500000
k=(n//2+1)//2
test('noise','std','3\n'+(str(n)+'\n'+'1 -1 '*(n//2)+'\n')*3,(str(k*(n+1)-2*k*k)+'\n')*3,'T=3 N=500000 alternating signs, repeated LCP worst case')
test('noise','std','1\n500000\n'+'1 '*500000+'\n',0,'N=500000, no valid interval')
a=[R.choice([-1,1])*R.randint(1,n) for _ in range(n)]
test('noise','std','1\n'+str(n)+'\n'+' '.join(map(str,a))+'\n',None,'N=500000 random full alphabet, performance only')
test('noise','partial','1\n2000\n'+'1 -1 '*1000+'\n',500500,'N=2000 alternating signs')
(ROOT/'stress.json').write_text(json.dumps(records,indent=2,ensure_ascii=False),encoding='utf-8')
