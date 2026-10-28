from functools import lru_cache
from itertools import product,groupby
@lru_cache(None)
def f(s):
    if len(set(s)-{0})<=1:return False
    return not f(s[1:]) or not f(s[:-1])
for n in range(2,17):
    fail=None
    for s in product([-1,1],repeat=n):
        t=tuple(x for v,g in groupby(s) for z in [len(list(g))] for x in [v]*(z if z<=3 else 2+z%2))
        if f(s)!=f(t):fail=(s,t,f(s),f(t));break
    print(n,fail,flush=True)
    if fail:break
