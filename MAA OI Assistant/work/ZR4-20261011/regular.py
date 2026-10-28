from functools import lru_cache
from itertools import product
@lru_cache(None)
def f(s):
    if len(set(s)-{0})<=1:return False
    return not f(s[1:]) or not f(s[:-1])
for alph in ((-1,1),(-1,0,1)):
    for k in range(1,6):
        suff=[s for j in range(k+1) for s in product(alph,repeat=j)]
        pre=[s for j in range(k+1) for s in product(alph,repeat=j)]
        sig={tuple(f(p+s) for s in suff) for p in pre}
        print(alph,k,len(sig),flush=True)
