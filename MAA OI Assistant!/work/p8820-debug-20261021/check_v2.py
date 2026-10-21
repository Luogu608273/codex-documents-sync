import pathlib
import subprocess
import random
import collections
import heapq

root = pathlib.Path(__file__).resolve().parent
src = (root / 'fix_both.cpp').read_text()
src = src.replace('const int N = 2e5 + 10;', 'const int N = 2e5 + 10, inf2 = 1e9+1;')
src = src.replace('nn, ps[N];', 'nn, ps[N], num[N];')
src = src.replace('for(int v: G[u]){\n\t\tif(v == fa_) continue;\n\t\tdfs1', 'for(int v: G[u]){\n\t\tnum[u] = min(a[v], num[u]);\n\t\tif(v == fa_) continue;\n\t\tdfs1')
old = '''inline void upd(int v){
		a[0][0] = v; a[0][1] = (k >= 2 ? v : inf); a[0][2] = (k >= 3 ? v : inf);
		a[1][0] = 0; a[1][1] = a[1][2] = inf;
		a[2][0] = a[2][2] = inf; a[2][1] = 0;
	}'''
new = '''inline void upd(int v, int num){
		if(k == 3){
			a[0][0] = v; a[0][1] = v; a[0][2] = v;
			a[1][0] = 0; a[1][1] = (num == inf2 ? inf : num);
			a[1][2] = (num == inf2 ? inf : num + v);
			a[2][0] = a[2][2] = inf; a[2][1] = 0;
		}
		else{
			a[0][0] = v; a[0][1] = (k >= 2 ? v : inf); a[0][2] = inf;
			a[1][0] = 0; a[1][1] = a[1][2] = inf;
			a[2][0] = a[2][2] = inf; a[2][1] = 0;
		}
	}'''
assert old in src
src = src.replace(old, new)
src = src.replace('vc[u].x.upd(a[pth[bg+l-1]]);', 'vc[u].x.upd(a[pth[bg+l-1]], num[pth[bg+l-1]]);')
src = src.replace('for(int i = 1; i <= n; i++) cin >> a[i];', 'for(int i = 1; i <= n; i++){\n\t\tcin >> a[i];\n\t\tnum[i] = inf2;\n\t}')
fixed = src.replace('return min(res, mn1 + a[w] + mn2);', '''if(k == 3){
		res = min(res, min(l1.a[0], l1.a[1]) + num[w] + min(l2.a[0], l2.a[1]));
	}
	return min(res, mn1 + a[w] + mn2);''')
for name, code in [('v2', src), ('v2_fixed', fixed)]:
    (root / (name + '.cpp')).write_text(code)
    subprocess.run(['C:/TDM-GCC-64/bin/g++.exe', '-std=c++17', '-O2', '-Wall', '-Wextra', str(root / (name + '.cpp')), '-o', str(root / (name + '.exe'))], check=True)

def data(n, k, a, edges, qs):
    lines = ['%d %d %d' % (n, len(qs), k), ' '.join(map(str, a))]
    lines += ['%d %d' % e for e in edges + qs]
    return '\n'.join(lines) + '\n'

def run(name, inp):
    return list(map(int, subprocess.check_output([str(root / (name + '.exe'))], input=inp.encode()).split()))

def brute(n, k, a, edges, qs):
    g = [[] for _ in range(n)]
    for u, v in edges:
        g[u-1].append(v-1)
        g[v-1].append(u-1)
    h = [[] for _ in range(n)]
    for s in range(n):
        d = [-1] * n
        d[s] = 0
        que = collections.deque([s])
        while que:
            u = que.popleft()
            for v in g[u]:
                if d[v] == -1:
                    d[v] = d[u] + 1
                    que.append(v)
        h[s] = [v for v in range(n) if 0 < d[v] <= k]
    ds = []
    for s in range(n):
        d = [10**30] * n
        d[s] = a[s]
        pq = [(d[s], s)]
        while pq:
            x, u = heapq.heappop(pq)
            if x != d[u]:
                continue
            for v in h[u]:
                y = x + a[v]
                if y < d[v]:
                    d[v] = y
                    heapq.heappush(pq, (y, v))
        ds.append(d)
    return [ds[u-1][v-1] for u,v in qs]

case = data(6, 3, [100,100,100,2,2,1], [(1,2),(1,3),(2,4),(3,5),(1,6)], [(4,5)])
(root / 'lca-neighbor.in').write_text(case)
print('lca-neighbor expected=5', {v:run(v,case) for v in ['v2','v2_fixed']}, flush=True)

seed = 882021
rng = random.Random(seed)
for k in [1,2,3]:
    count = 0
    for it in range(450):
        n = rng.randint(2, 25)
        a = [rng.choice([1,2,100,10**9]) for _ in range(n)]
        if it % 4 == 0:
            edges = [(v,v-1) for v in range(2,n+1)]
        elif it % 4 == 1:
            edges = [(v,1) for v in range(2,n+1)]
        else:
            edges = [(v, rng.randrange(1,v)) for v in range(2,n+1)]
        qs = [(u,v) for u in range(1,n+1) for v in range(1,n+1) if u != v]
        inp = data(n,k,a,edges,qs)
        want = brute(n,k,a,edges,qs)
        got = run('v2_fixed',inp)
        if got != want:
            idx = next(i for i in range(len(got)) if got[i] != want[i])
            bad = data(n,k,a,edges,[qs[idx]])
            (root / 'v2-unexpected.in').write_text(bad)
            print('FAIL seed=%d k=%d iteration=%d query=%s expected=%d got=%d' % (seed,k,it,qs[idx],want[idx],got[idx]),flush=True)
            print(bad,flush=True)
            raise SystemExit(1)
        count += len(qs)
    print('v2_fixed k=%d: 450 trees / %d ordered queries passed, seed=%d' % (k,count,seed), flush=True)
