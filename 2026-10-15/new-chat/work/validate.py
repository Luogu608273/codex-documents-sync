from check import partitions, exact
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import subprocess, random, time

def make_perm(a):
    p=[]
    for x in a:
        start=len(p)+1
        p += list(range(start+1,start+x)) + [start]
    return p

def expected(a,k):
    boss = sum(x==k+1 for x in a)
    if boss:
        if any(x>k+1 for x in a) or (k>1 and boss>1):
            return False
        need=sum(x for x in a if 1<x<=k) + a.count(1)%(k+1)
        return 1<=need<=k
    if any(x>k for x in a):
        return False
    # Independently enumerate the first move, then check the safe-state condition.
    for mask in range(1,1<<len(a)):
        if sum(x for i,x in enumerate(a) if mask>>i&1)>k:
            continue
        left=sorted((x-1 for i,x in enumerate(a) if not(mask>>i&1)),reverse=True)
        if sum(left[:k])<=k:
            return True
    return False

def full_brute(a,k):
    n=sum(a)
    allmask=(1<<n)-1
    cycles=[]
    start=0
    for x in a:
        cycles.append(((1<<x)-1)<<start)
        start+=x
    @lru_cache(None)
    def dfs(red,blue,turn):
        if any(red&c and blue&c for c in cycles):
            return False
        white=allmask^(red|blue)
        if not white:
            return True
        good = (turn==1)
        sub=white
        while sub:
            if sub.bit_count()<=k:
                for color in range(2):
                    result=dfs(red|sub if color==0 else red,blue|sub if color==1 else blue,turn^1)
                    if result==(turn==0):
                        return result
            sub=(sub-1)&white
        return good
    return dfs(0,0,0)

if __name__=='__main__':
    cases=[]
    full_count=0
    for n in range(2,13):
        for a in partitions(n):
            for k in range(1,n+1):
                want=exact(a,k)
                assert expected(a,k)==want,(a,k,'formula')
                if n<=7:
                    assert full_brute(a,k)==want,(a,k,'full game')
                    full_count+=1
                cases.append((a,k,want))
    random.Random(20261015).shuffle(cases)
    data=[str(len(cases))]
    for a,k,want in cases:
        data += [f'{sum(a)} {k}', ' '.join(map(str,make_perm(a)))]
    run=subprocess.run(['work/fixed.exe'],input='\n'.join(data)+'\n',text=True,capture_output=True,check=True)
    lines=run.stdout.splitlines()
    assert len(lines)==len(cases)
    for (a,k,want),got in zip(cases,lines):
        assert got==('Alice' if want else 'Bob'),(a,k,want,got)
    print('PASS full coloring minimax:',full_count)
    print('PASS reduced minimax, independent subset check, compiled fixed C++:',len(cases))
    ex='2\n7 2\n1 2 4 3 6 7 5\n8 4\n2 1 4 5 6 7 8 3\n'
    for exe in ['original','fixed']:
        p=subprocess.run([f'work/{exe}.exe'],input=ex,text=True,capture_output=True,check=True)
        print(exe,'counterexamples:',p.stdout.splitlines())
    # Stress total n and k, including a long chain in the original DSU.
    stress=[]
    n=200000
    stress.append((n,20,list(range(1,n+1)),'Alice'))
    stress.append((n,20,[n]+list(range(1,n)),'Bob'))
    for n,k,p,want in stress:
        data=f'1\n{n} {k}\n'+ ' '.join(map(str,p))+'\n'
        begin=time.perf_counter()
        run=subprocess.run(['work/fixed.exe'],input=data,text=True,capture_output=True,check=True)
        assert run.stdout.strip()==want
        print('PASS max n',want,'seconds',round(time.perf_counter()-begin,3))
