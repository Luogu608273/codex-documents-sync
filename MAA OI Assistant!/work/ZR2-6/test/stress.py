import collections
import json
from verify import ROOT, run, check_a, check_d, fail, rng

results = []

def test(name, data, expected=None, checker=None, timeout=12):
    path = ROOT / ('stress-' + name + '.in')
    path.write_text(data, encoding='utf-8')
    output, elapsed = run(name, data, timeout=timeout)
    (ROOT / ('stress-' + name + '.out')).write_text(output, encoding='utf-8')
    ok = checker(data, output) if checker else output.split() == str(expected).split()
    if not ok:
        fail(name, data, output, expected)
    results.append({'name': name, 'seconds': round(elapsed, 4), 'input_bytes': len(data)})
    print(name, 'PASS', round(elapsed, 4), flush=True)
    return output

n, m = 2, 500000
data = f'{n} {m}\n' + '1 ' * m + '\n' + '0 ' * m + '\n'
test('utopia_std', data, checker=check_a)
n, m = 2, 500
data = f'{n} {m}\n' + '1 ' * m + '\n' + '0 ' * m + '\n'
test('utopia_partial', data, checker=check_a)

n, m = 100000, 1000000
edges = []
adj = [[] for _ in range(n)]
for delta in range(1, 12):
    for u in range(n - delta):
        if len(edges) == m:
            break
        v = u + delta
        edges.append(f'{u+1} {v+1} 1000000000\n')
        adj[u].append(v)
        adj[v].append(u)
    if len(edges) == m:
        break
dis = [-1] * n
dis[0] = 0
q = collections.deque([0])
while q:
    u = q.popleft()
    for v in adj[u]:
        if dis[v] == -1:
            dis[v] = dis[u] + 1
            q.append(v)
data = f'{n} {m} 0\n' + '1000000000 ' * n + '\n' + ''.join(edges)
expected = (2 * dis[-1] + 1) * 10**9
test('road_std', data, expected)
test('road_partial', data, expected)
del adj, edges, data

n = 1000
heights = [1000 if i % 2 == 0 else 999 for i in range(n)]
data = f'{n} {n-1} 500\n' + ' '.join(map(str, heights)) + '\n' + ''.join(f'{i} {i+1} 1\n' for i in range(1, n))
expected, _ = run('road_std', data)
test('road_partial', data, expected)

n, k = 100000, 30
data = f'{n} {k}\n' + ''.join(f'{i} {i+1}\n' for i in range(1, n))
test('moment_std', data, n-1-(n-2)//(k-1))
data = f'{n} {k}\n' + ''.join(f'1 {i}\n' for i in range(2, n+1))
test('moment_std', data, n-1)
n, k = 100, 30
data = f'{n} {k}\n' + ''.join(f'{i} {i+1}\n' for i in range(1, n))
test('moment_partial', data, n-1-(n-2)//(k-1))

n = 200000
data = str(n)+'\n'+''.join(f'{i} 0\n' for i in range(n))+''.join(f'{n+i} 1\n' for i in range(n))
expected = 'Yes\n'+'\n'.join(str(n-i) for i in range(n))+'\n'
test('passerby_std', data, expected)
test('passerby_partial', data, expected)
data = str(n)+'\n'+''.join(f'{-i} {-i}\n' for i in range(1,n+1))+''.join(f'{i} {i}\n' for i in range(1,n+1))
expected = 'Yes\n'+'\n'.join(map(str,range(1,n+1)))+'\n'
test('passerby_std', data, expected)
n = 1000
data = str(n)+'\n'+''.join(f'{-i} {-i}\n' for i in range(1,n+1))+''.join(f'{i} {i}\n' for i in range(1,n+1))
test('passerby_partial', data, checker=check_d)

(ROOT / 'stress.json').write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding='utf-8')
print('STRESS PASS', flush=True)
