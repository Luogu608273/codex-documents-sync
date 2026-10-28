import pathlib
import random
import subprocess

root = pathlib.Path(__file__).resolve().parent
rng = random.Random(882001)
for n in range(3,10):
    for it in range(60):
        a = [rng.choice([1,9]) for _ in range(n)]
        qs = [(u,v) for u in range(1,n+1) for v in range(u+1,n+1)]
        lines = ['%d %d 2' % (n,len(qs)), ' '.join(map(str,a))]
        lines += ['%d %d' % (v-1,v) for v in range(2,n+1)]
        edges = lines[2:]
        lines += ['%d %d' % q for q in qs]
        inp = '\n'.join(lines)+'\n'
        got = list(map(int,subprocess.check_output([str(root/'fix_start.exe')], input=inp.encode()).split()))
        for (u,v),ans in zip(qs,got):
            f = [10**9] * n
            f[u-1] = a[u-1]
            for p in range(u,v):
                f[p] = min(f[max(u-1,p-2):p])+a[p]
            if ans != f[v-1]:
                case = '\n'.join(['%d 1 2'%n, ' '.join(map(str,a))]+edges+['%d %d'%(u,v)])+'\n'
                (root/'order-small.in').write_text(case)
                print('seed=882001 iteration=', it, 'expected=', f[v-1], 'fix_start=', ans)
                print(case)
                raise SystemExit
