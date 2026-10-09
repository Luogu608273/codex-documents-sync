from pathlib import Path
import subprocess,time,json,random
root=Path(__file__).resolve().parents[1];tmp=root/'work'/'tests'
report=json.loads((root/'work'/'test_report.json').read_text())
def run(stem,name,data):
    (tmp/(name+'.in')).write_text(data,encoding='utf-8');start=time.perf_counter()
    p=subprocess.run([str(tmp/(stem+'.exe'))],cwd=tmp,capture_output=True,timeout=30)
    assert p.returncode==0,(stem,p.stderr)
    return (tmp/(name+'.out')).read_text().split(),time.perf_counter()-start
for a,L,R,expected in [([-500000000,500000000],1,500000000,2),([0,1,2,3,4],2,500000000,5),([0],500000000,500000000,1),([0,5,10],5,5,1)]:
    data=f'{len(a)} {L} {R}\n'+' '.join(map(str,a))+'\n'
    for stem in ['U1708_code','U1708_partial_40','U1708_partial_20']:
        actual,_=run(stem,'watch',data);assert actual==[str(expected)],(data,actual)
        report['comparisons'][stem]+=1
n=150000;k=20;data=f'{n} {k}\n'+''.join(f'{i//2} {i}\n' for i in range(2,n+1))+' '.join(str(i%k+1) for i in range(n))+'\n'+' '.join(str(1000000000-i) for i in range(k))+'\n'
a,t=run('U1710_code','sect',data);b,_=run('U1710_partial_66','sect',data);assert a==b
report['large_case_seconds']['sect_binary_tree_n150000']=t
m=49999;K=100003;W=2*K
ps=[(0,0),(W,0)]
for j in range(m):
    ps.append((j+W,(j+1)*K))
    if j+1<m:ps.append((j+1+W,(j+1)*K))
ps.append((m-1,m*K))
for j in range(m-1,-1,-1):
    ps.append((j,j*K))
    if j:ps.append((j-1,j*K))
assert ps[-1]==ps[0];ps.pop()
# y must remain within the statement's bound: use K=10007 instead.
ps=[(x,y//K*10007) for x,y in ps];K=10007
# Shift right boundary to preserve width 2K after changing K.
ps=[(x-W+2*K if x>=W else x,y) for x,y in ps]
data=f'{len(ps)} {K}\n'+''.join(f'{x} {y}\n' for x,y in ps)
a,t=run('U1711_code','tile',data);expected=str(2*K+m-1);assert a==[expected],(a,expected)
report['large_case_seconds']['tile_199996_vertices_many_phases']=t
print('Boundary and extra large cases passed.',report['large_case_seconds'],flush=True)
(root/'work'/'test_report.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
