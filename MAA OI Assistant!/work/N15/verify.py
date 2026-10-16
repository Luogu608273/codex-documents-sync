from pathlib import Path
import subprocess, random, itertools, functools, json, time, concurrent.futures

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'outputs/N15'
TMP = ROOT / 'work/N15'
BIN = TMP / 'bin'
CXX = 'C:/TDM-GCC-64/bin/g++.exe'
SEED = 20261013
rng = random.Random(SEED)
report = {'seed': SEED, 'compiler': CXX, 'flags': '-std=c++17 -O2 -Wall -Wextra -DLOCAL', 'tests': []}

RESET = {
    'G123907_partial_57': 'tot = 0; memset(h, 0, sizeof h); memset(f, 0, sizeof f); memset(g, 0, sizeof g);',
    'G123908_std': 'tot = k = 0; memset(h, 0, sizeof h); memset(id, 0, sizeof id);',
    'G123909_std': 'memset(f, 0, sizeof f); memset(g, 0, sizeof g); memset(u[0], 0, sizeof u[0]); memset(v[0], 0, sizeof v[0]);',
    'G123910_std': 'memset(h, 0, (n + 2) * sizeof(int)); memset(mx, 0, (4 * m + 12) * sizeof(ll)); memset(tag, 0, (4 * m + 12) * sizeof(ll)); memset(sum, 0, (4 * m + 12) * sizeof(ll));',
    'G123910_partial_10': 'f[0] = 0;',
}

def compile_one(p):
    name = p.stem
    wrapper = TMP / (name + '_batch.cpp')
    wrapper.write_text('#define main original_main\n#include "' + p.as_posix() + '"\n#undef main\n'
        + 'int main() { ios::sync_with_stdio(false); cin.tie(nullptr); int z; cin >> z; while (z--) { solve(); '
        + RESET.get(name, '') + ' } }\n', encoding='utf-8')
    out = BIN / (name + '_batch.exe')
    proc = subprocess.run([CXX, '-std=c++17', '-O2', '-Wall', '-Wextra', '-DLOCAL', str(wrapper), '-o', str(out)], capture_output=True, text=True)
    if proc.returncode or proc.stderr:
        raise RuntimeError((name, proc.returncode, proc.stderr))
    proc = subprocess.run([CXX, '-std=c++17', '-O2', '-Wall', '-Wextra', '-DLOCAL', str(p), '-o', str(BIN / (name + '.exe'))], capture_output=True, text=True)
    if proc.returncode or proc.stderr:
        raise RuntimeError((name, proc.returncode, proc.stderr))
    return name

def check(name, cases, answers, label):
    data = str(len(cases)) + '\n' + ''.join(cases)
    begin = time.perf_counter()
    proc = subprocess.run([str(BIN / (name + '_batch.exe'))], input=data, capture_output=True, text=True, timeout=120)
    got = [int(x) for x in proc.stdout.split()]
    flat = [y for x in answers for y in x]
    if proc.returncode or got != flat:
        (TMP / 'first_failure_batch.in').write_text(data, encoding='utf-8')
        (TMP / 'first_failure_expected.json').write_text(json.dumps(flat), encoding='utf-8')
        raise AssertionError((name, proc.returncode, next(((i, x, y) for i, (x, y) in enumerate(zip(got, flat)) if x != y), None), len(got), len(flat), proc.stderr))
    row = {'program': name, 'test': label, 'cases': len(cases), 'answers': len(flat), 'seconds': round(time.perf_counter() - begin, 3), 'result': 'PASS'}
    report['tests'].append(row)
    print(row, flush=True)

@functools.lru_cache(None)
def erase(s):
    ans = 0
    for i in range(len(s)):
        for j in range(i + 1, len(s)):
            if s[i] + s[j] in ('AB', 'BC'):
                ans = max(ans, 1 + erase(s[:i] + s[i+1:j] + s[j+1:]))
    return ans

def floyd(n, es):
    inf = 10 ** 20
    d = [[inf] * n for _ in range(n)]
    for i in range(n): d[i][i] = 0
    for u, v, w, _ in es: d[u][v] = d[v][u] = min(d[u][v], w)
    for k in range(n):
        for i in range(n):
            for j in range(n):
                d[i][j] = min(d[i][j], d[i][k] + d[k][j])
    return d

def upkeep(n, es):
    ref = floyd(n, es)
    ans = sum(e[3] for e in es)
    for mask in range(1 << len(es)):
        chosen = [e for i, e in enumerate(es) if mask >> i & 1]
        cost = sum(e[3] for e in chosen)
        if cost < ans and floyd(n, chosen) == ref: ans = cost
    return ans

def cook(A, B):
    n, m = len(A), len(B)
    aa, bb = [0], [0]
    for x, _, _ in A: aa.append(aa[-1] + x)
    for x, _, _ in B: bb.append(bb[-1] + x)
    f = [[-10 ** 30] * (m + 1) for _ in range(n + 1)]
    f[0][0] = 0
    for i in range(n + 1):
        for j in range(m + 1):
            t = aa[i] + bb[j]
            if i: f[i][j] = max(f[i][j], f[i-1][j] + (A[i-1][2] if t <= A[i-1][1] else 0))
            if j: f[i][j] = max(f[i][j], f[i][j-1] + (B[j-1][2] if t <= B[j-1][1] else 0))
    return f[n][m]

def cook_enum(A, B):
    def dfs(i, j, t, val):
        if i == len(A) and j == len(B): return val
        res = -10 ** 30
        if i < len(A):
            x, d, w = A[i]
            res = max(res, dfs(i+1, j, t+x, val + (w if t+x <= d else 0)))
        if j < len(B):
            x, d, w = B[j]
            res = max(res, dfs(i, j+1, t+x, val + (w if t+x <= d else 0)))
        return res
    return dfs(0, 0, 0, 0)

def subseq(a):
    ans = 0
    for mask in range(1 << len(a)):
        p = 0
        for i, x in enumerate(a):
            if mask >> i & 1:
                if x < p: break
                p = x
        else: ans += 1
    return ans % 1000000007

def subseq_dp(a, k):
    f = [0] * (k + 1)
    f[0] = 1
    for x in a: f[x] = (f[x] + sum(f[:x+1])) % 1000000007
    return sum(f) % 1000000007

if __name__ == '__main__':
    BIN.mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        print('Compiled:', list(pool.map(compile_one, SRC.glob('*.cpp'))), flush=True)
    cases, answers = [], []
    for n in range(1, 11):
        for t in itertools.product('ABC', repeat=n):
            s = ''.join(t)
            cases.append(s + '\n'); answers.append([erase(s)])
    check('G123907_std', cases, answers, 'all ABC strings of lengths 1..10, original-operation exhaustive oracle')
    indices = [i for i, s in enumerate(cases) if len(s) <= 9]
    check('G123907_partial_57', [cases[i] for i in indices], [answers[i] for i in indices], 'all ABC strings of lengths 1..8')
    indices = [i for i, s in enumerate(cases) if 'C' not in s]
    check('G123907_partial_5', [cases[i] for i in indices], [answers[i] for i in indices], 'all AB strings of lengths 1..10')
    cases, answers, zero_cases, zero_answers = [], [], [], []
    for z in range(500):
        n = rng.randint(2, 6); m = rng.randint(1, 9)
        es = []
        for _ in range(m):
            u, v = rng.sample(range(n), 2)
            es.append((u, v, 0 if z < 100 else rng.randint(0, 8), rng.randint(1, 12)))
        data = f'{n} {m}\n' + ''.join(f'{u+1} {v+1} {w} {c}\n' for u, v, w, c in es)
        val = [upkeep(n, es)]
        cases.append(data); answers.append(val)
        if z < 100: zero_cases.append(data); zero_answers.append(val)
    check('G123908_std', cases, answers, 'enumerate every edge subset, compare all-pairs distances; includes zero edges, parallel edges, disconnected graphs')
    check('G123908_partial_20', zero_cases, zero_answers, 'all edge lengths zero')
    cases, answers = [], []
    for z in range(600):
        n = rng.randint(1, 10); k = rng.randint(1, 20)
        a = [rng.randint(1, k) for _ in range(n)]
        qs = [(l, r) for l in range(n) for r in range(l, n)]
        cases.append(f'{n} {k}\n' + ' '.join(map(str, a)) + f'\n{len(qs)}\n' + ''.join(f'{l+1} {r+1}\n' for l, r in qs))
        answers.append([subseq(a[l:r+1]) for l, r in qs])
    check('G123909_std', cases, answers, 'all intervals, enumerate subsequence index masks including empty')
    check('G123909_partial_24', cases, answers, 'same independent exhaustive oracle')
    cases, answers = [], []
    for z in range(100):
        n = rng.randint(100, 500); k = rng.randint(1, 20)
        a = [rng.randint(1, k) for _ in range(n)]
        qs = [(0, n-1)]
        for _ in range(25):
            l = rng.randrange(n); r = rng.randrange(l, n); qs.append((l, r))
        cases.append(f'{n} {k}\n' + ' '.join(map(str, a)) + f'\n{len(qs)}\n' + ''.join(f'{l+1} {r+1}\n' for l, r in qs))
        answers.append([subseq_dp(a[l:r+1], k) for l, r in qs])
    check('G123909_std', cases, answers, 'larger intervals and modular wraparound, ordinary linear DP oracle')
    check('G123909_partial_24', cases, answers, 'same linear DP oracle')
    cases, answers, common_cases, common_answers = [], [], [], []
    for z in range(2500):
        n = rng.randint(1, 20); m = rng.randint(1, 20)
        common = rng.randint(1, 300)
        A = [(rng.randint(1, 20), common if z < 500 else rng.randint(1, 500), rng.randint(-30, 30)) for _ in range(n)]
        B = [(rng.randint(1, 20), common if z < 500 else rng.randint(1, 500), rng.randint(-30, 30)) for _ in range(m)]
        val = cook(A, B)
        if n <= 4 and m <= 4: assert val == cook_enum(A, B)
        data = f'{n} {m}\n' + ''.join(f'{x} {d} {w}\n' for x, d, w in A+B)
        cases.append(data); answers.append([val])
        if z < 500: common_cases.append(data); common_answers.append([val])
    check('G123910_std', cases, answers, 'grid DP oracle; negative/zero/positive scores, equal deadlines; tiny cases also enumerate schedules')
    check('G123910_partial_10', cases, answers, 'same oracle')
    check('G123910_partial_5', common_cases, common_answers, 'equal-deadline cases, including negative scores')
    (TMP / 'verification.json').write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding='utf-8')
    print('ALL PASS', flush=True)
