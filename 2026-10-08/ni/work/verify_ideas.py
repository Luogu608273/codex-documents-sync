import random
from itertools import combinations

def watch(a,L,R):
    blocks=[]
    for i,x in enumerate(a):
        if i==0 or x-a[i-1]>=L: blocks.append([i,i])
        else: blocks[-1][1]=i
    dp=[]; p=0
    for l,r in blocks:
        while p<len(a) and a[p]<a[l]-R: p+=1
        best=0 if p==0 else 10**9
        for j,(u,v) in enumerate(blocks[:len(dp)]):
            if a[v]>=a[p-1]-R: best=min(best,dp[j])
        dp.append(best+r-l+1)
    return min(dp[j] for j,(l,r) in enumerate(blocks) if a[r]>=a[-1]-R)

def watch_b(a,L,R):
    best=len(a)
    for s in range(1,1<<len(a)):
        if s.bit_count()>=best: continue
        if all((s>>i&1) or L<=min(abs(x-y) for j,y in enumerate(a) if s>>j&1)<=R for i,x in enumerate(a)):
            best=s.bit_count()
    return best

def merge_b(a,k):
    n=len(a); lo=[0]*(1<<n); hi=lo[:]
    for s in range(1,1<<n):
        if s&(s-1)==0: lo[s]=hi[s]=a[s.bit_length()-1]; continue
        lo[s]=10**20; hi[s]=-10**20; t=(s-1)&s
        while t:
            u=s^t
            if u and t<u:
                lo[s]=min(lo[s],k-hi[t]-hi[u]); hi[s]=max(hi[s],k-lo[t]-lo[u])
            t=(t-1)&s
    return hi[-1]

def merge(a,k):
    a=sorted(a,reverse=True); n=len(a); r=(2-n)%3
    total=sum(a); pre=0; ans=-10**20
    for p in range(n+1):
        if p: pre+=a[p-1]
        if p%3==r: ans=max(ans,2*pre-total+(n+1-2*p)//3*k)
    return ans

def tile_b(cells,K):
    ans=0; M=max(x for x,y in cells)+1
    for t in range(1,M+1):
        rem={(x,y) for x,y in cells if x<t}
        while rem:
            x,y=min(rem)
            square={(x+i,y+j) for i in range(K) for j in range(K)}
            if not square<=rem: break
            rem-=square
        if not rem: ans=t
    return ans

def tile(cells,K):
    M=max(x for x,y in cells)+1; H=max(y for x,y in cells)+1
    phases=[-1]*H; ans=0
    for x in range(M+1):
        ps=set(phases)-{-1}
        if len(ps)==1:
            p=next(iter(ps)); ans=max(ans,x-(x-p)%K)
        elif not ps: ans=x
        old={(y) for y in range(H) if phases[y]>=0}
        new={y for y in range(H) if (x,y) in cells}
        if any(phases[y]!=x%K for y in old-new): return ans
        for y in old-new: phases[y]=-1
        for y in new-old: phases[y]=x%K
        i=0
        while i<H:
            j=i+1
            while j<H and phases[j]==phases[i]: j+=1
            if phases[i]>=0 and (j-i)%K: return ans
            i=j
    return ans

random.seed(1708)
for z in range(1000):
    n=random.randint(1,10); a=sorted(random.sample(range(-20,30),n)); L=random.randint(1,12); R=random.randint(L,20)
    assert watch(a,L,R)==watch_b(a,L,R),(a,L,R)
for z in range(500):
    n=random.randint(2,8); a=[random.randint(1,20) for _ in range(n)]; k=random.randint(1,50)
    assert merge(a,k)==merge_b(a,k),(a,k)
for z in range(15000):
    M=random.randint(1,10); H=random.randint(1,10)
    cells={(x,y) for x in range(M) for y in range(H) if random.random()<.65}
    if not cells: continue
    K=random.randint(1,4)
    assert tile(cells,K)==tile_b(cells,K),(cells,K,tile(cells,K),tile_b(cells,K))
print('Passed: watch 1000, merge 500, tile 15000 randomized comparisons.')
