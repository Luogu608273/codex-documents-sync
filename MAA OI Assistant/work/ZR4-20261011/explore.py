from functools import lru_cache
from itertools import product
@lru_cache(None)
def f(s):
    if not s or len(set(s)-{0})<=1: return False
    return not f(s[1:]) or not f(s[:-1])
for n in range(2,9):
    d={}
    bad=None
    for s in product([-1,0,1],repeat=n):
        if len(set(s)-{0})<=1: continue
        p=next(i for i in range(n) if len(set(s[:i+1])-{0})==2)
        q=next(i for i in range(n-1,-1,-1) if len(set(s[i:])-{0})==2)
        key=(p,q)
        if key in d and d[key][0]!=f(s): bad=(d[key],(f(s),s),key);break
        d[key]=(f(s),s)
    print(n,'same prefix/suffix enough?',bad is None,bad)
    if bad:break
for n in range(2,8):
    print('n',n)
    d={}
    for s in product([-1,1],repeat=n):
        if len(set(s))==1:continue
        l=next(i for i in range(n) if s[i]!=s[0])
        r=next(i for i in range(n) if s[n-i-1]!=s[-1])
        key=(s[0]==s[-1],l,r)
        d.setdefault(key,set()).add(f(s))
    print(d)
