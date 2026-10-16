from functools import lru_cache
from itertools import product

def partitions(n, lo=1):
    if n == 0:
        yield ()
    for x in range(lo, n + 1):
        for tail in partitions(n-x, x):
            yield (x,) + tail

def orig(a, k, repeat=True):
    if min(a) > k:
        return False
    ls = sorted((x-1 for x in a if x>1), reverse=True)
    m = len(ls)
    b = [[False]* (k+1) for _ in range(k+1)]
    b[0][0] = True
    s = sum(ls[:k])
    ans = s <= k
    for i in range(1, min(k,m)+1):
        s = sum(ls[:k+i])
        if repeat:
            for w in ls[:k+i]:
                for l in range(k,w-1,-1):
                    b[i][l] |= b[i-1][l-w]
        else:
            b = [[False]*(k+1) for _ in range(k+1)]
            b[0][0] = True
            for w in ls[:k+i]:
                for c in range(i,0,-1):
                    for l in range(k,w-1,-1):
                        b[c][l] |= b[c-1][l-w]
        ans |= any(b[i][l] and s-l<=k for l in range(k-i+1))
        if ans:
            break
    if ans:
        cnt = sum(x for x in a if x != k+1)
        if k+1 in a and cnt>k and cnt%(k+1)==0:
            return False
    return ans

@lru_cache(None)
def exact(a, k, turn=0):
    if not a:
        return True
    if turn == 0:
        for mask in range(1,1<<len(a)):
            if sum(x for i,x in enumerate(a) if mask>>i&1) <= k:
                if exact(tuple(x for i,x in enumerate(a) if not(mask>>i&1)), k, 1):
                    return True
        return False
    for take in product(*(range(min(x,k)+1) for x in a)):
        used = sum(take)
        if not 1<=used<=k:
            continue
        forced = sum(x-y for x,y in zip(a,take) if 0<y<x)
        if forced>k:
            return False
        intact = tuple(x for x,y in zip(a,take) if y==0)
        if not intact and not forced:
            continue
        can = False
        for mask in range(1<<len(intact)):
            used2 = sum(x for i,x in enumerate(intact) if mask>>i&1)
            if 1<=forced+used2<=k:
                remain = tuple(x for i,x in enumerate(intact) if not(mask>>i&1))
                if exact(remain,k,1):
                    can=True
                    break
        if not can:
            return False
    return True

if __name__ == '__main__':
    first1=first2=None
    cases=0
    for n in range(2,13):
        for a in partitions(n):
            for k in range(1,min(5,n)+1):
                correct = exact(a,k)
                old = orig(a,k)
                distinct = orig(a,k,False)
                cases+=1
                if old != correct and first1 is None:
                    first1=(a,k,old,correct)
                    print('first overall mismatch',first1,flush=True)
                if old != distinct and first2 is None:
                    first2=(a,k,old,distinct,correct)
                    print('first repeat mismatch',first2,flush=True)
        print('done n',n,'cases',cases,flush=True)
    print('example', (1,1,3,4), 3, orig((1,1,3,4),3), exact((1,1,3,4),3))
