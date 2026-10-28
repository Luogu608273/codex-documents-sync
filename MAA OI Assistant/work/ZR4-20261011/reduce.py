from functools import lru_cache
from itertools import product,groupby
@lru_cache(None)
def f(s):
    if len(set(s)-{0})<=1:return False
    return not f(s[1:]) or not f(s[:-1])
for n in range(2,15):
    fail=None
    for s in product([-1,1],repeat=n):
        t=tuple(x for v,g in groupby(s) for x in [v]*(1+(len(list(g))-1)%2))
        if f(s)!=f(t):fail=(s,t,f(s),f(t));break
    print(n,fail,flush=True)
    if fail:break
