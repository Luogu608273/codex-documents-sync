from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / 'outputs'
TASK = Path(__file__).resolve().parent
HEAD = "#include <bits/stdc++.h>\n#define endl '\\n'\nusing namespace std;\nusing ll = long long;\n"

def put(group, name, code, partial=False):
    p=OUT/group/name
    p.mkdir(parents=True,exist_ok=True)
    (p/('partial.cpp' if partial else 'std.cpp')).write_text(HEAD+code,encoding='utf-8')

def main(body, file, multi=False):
    return body + '\nint main() {\n#ifndef LOCAL\n    freopen("'+file+'.in", "r", stdin);\n    freopen("'+file+'.out", "w", stdout);\n#endif\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n'+('    int _;\n    cin >> _;\n    while (_--) solve();\n' if multi else '    solve();\n')+'    return 0;\n}\n'

put('S17','A_sam',main(r'''
const int N = 1000005;
int n, q, f[26][N];
char s[N];

void solve() {
    cin >> n >> q >> (s + 1);
    for (int c = 0; c < 26; c++)
        for (int i = 1; i <= n; i++)
            f[c][i] = f[c][i - 1] + (s[i] - 'a' == c);
    while (q--) {
        int l, r, ans = 0;
        cin >> l >> r;
        for (int c = 0; c < 26; c++) ans = max(ans, f[c][r] - f[c][l - 1]);
        cout << ans << endl;
    }
}
''','sam'))
put('S17','A_sam',main(r'''
// 逐询问扫描：适用于 n,q <= 5000，或所有询问长度之和 <= 2e6。
void solve() {
    int n, q;
    string s;
    cin >> n >> q >> s;
    while (q--) {
        int l, r, c[26] = {}, ans = 0;
        cin >> l >> r;
        for (int i = l - 1; i < r; i++) ans = max(ans, ++c[s[i] - 'a']);
        cout << ans << endl;
    }
}
''','sam'),True)

put('S17','B_lis',main(r'''
const int N = 1000005;
int n, t[N], f[N], len;

void solve() {
    cin >> n;
    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        int p = lower_bound(t + 1, t + len + 1, x) - t;
        t[p] = x;
        len = max(len, p);
        f[x] = p;
    }
    for (int i = 1; i <= n; i++) {
        f[i] = max(f[i], f[i - 1]);
        cout << f[i] << (i == n ? '\n' : ' ');
    }
}
''','lis'))
put('S17','B_lis',main(r'''
// O(n^2)，适用于 n <= 5000。
const int N = 5005;
int n, a[N], f[N], ans[N];

void solve() {
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        f[i] = 1;
        for (int j = 1; j < i; j++)
            if (a[j] < a[i]) f[i] = max(f[i], f[j] + 1);
        ans[a[i]] = f[i];
    }
    for (int i = 1; i <= n; i++) {
        ans[i] = max(ans[i], ans[i - 1]);
        cout << ans[i] << (i == n ? '\n' : ' ');
    }
}
''','lis'),True)

wolf=r'''
const int N = 500005, P = 998244353;
struct Mat {
    int a, b, c, d;
} tr[N * 4];
int n, b[N], v[N][2], hd[N], to[N * 4], nx[N * 4], ec;
char s[N];

Mat mul(Mat x, Mat y) {
    return {int(((ll)x.a * y.a + (ll)x.b * y.c) % P),
            int(((ll)x.a * y.b + (ll)x.b * y.d) % P),
            int(((ll)x.c * y.a + (ll)x.d * y.c) % P),
            int(((ll)x.c * y.b + (ll)x.d * y.d) % P)};
}

void build(int p, int l, int r) {
    if (l == r) {
        tr[p] = {v[l][0], v[l][1], 1, 0};
        return;
    }
    int m = (l + r) / 2;
    build(p * 2, l, m);
    build(p * 2 + 1, m + 1, r);
    tr[p] = mul(tr[p * 2 + 1], tr[p * 2]);
}

void modify(int p, int l, int r, int x) {
    if (l == r) {
        tr[p] = {v[l][0], v[l][1], 1, 0};
        return;
    }
    int m = (l + r) / 2;
    if (x <= m) modify(p * 2, l, m, x);
    else modify(p * 2 + 1, m + 1, r, x);
    tr[p] = mul(tr[p * 2 + 1], tr[p * 2]);
}

void add(int q, int id) {
    to[++ec] = id;
    nx[ec] = hd[q];
    hd[q] = ec;
}

int val(int i, int q) {
    return s[i] == 'L' ? b[i] : q - b[i];
}

void solve() {
    cin >> n >> (s + 1);
    for (int i = 1; i <= n; i++) cin >> b[i];
    int m = (n + 1) / 2;
    fill(hd, hd + m + 2, 0);
    ec = 0;
    for (int i = 3; i <= n; i++) {
        for (int t = 0; t < 2; t++) {
            int j = i - t - 1;
            int a = (s[i] == 'R') - (s[j] == 'R');
            int c = (s[i] == 'L' ? b[i] : -b[i]) - (s[j] == 'L' ? b[j] : -b[j]);
            v[i][t] = !a && c == t;
            if (a) {
                int q = (t - c) / a;
                if (0 <= q && q <= m) {
                    add(q, i * 2 + t);
                    add(q + 1, i * 2 + t);
                }
            }
        }
    }
    if (n >= 3) build(1, 3, n);
    int ans = 0;
    for (int q = 0; q <= m; q++) {
        for (int e = hd[q]; e; e = nx[e]) {
            int i = to[e] / 2, t = to[e] % 2;
            v[i][t] ^= 1;
            modify(1, 3, n, i);
        }
        int x = val(1, q) == 0;
        int y = ((val(2, q) == 1) + (val(2, q) == val(1, q)) * x) % P;
        int u = y, w = x;
        if (n >= 3) {
            u = ((ll)tr[1].a * y + (ll)tr[1].b * x) % P;
            w = ((ll)tr[1].c * y + (ll)tr[1].d * x) % P;
        }
        if (val(n, q) == q) ans = (ans + u) % P;
        if (val(n - 1, q) == q - 1) ans = (ans + w) % P;
    }
    cout << ans << endl;
}
'''
put('S17','C_wolf',main(wolf,'wolf',True))
put('S17','C_wolf',main(r'''
// O(n^2) 时间、O(n) 空间；目标 n <= 5000。
const int N = 5005, P = 998244353;
int n, b[N], f[N], a[N];
string s;

void solve() {
    cin >> n >> s;
    for (int i = 1; i <= n; i++) cin >> b[i];
    int ans = 0;
    for (int q = 0; q <= (n + 1) / 2; q++) {
        for (int i = 1; i <= n; i++) a[i] = s[i - 1] == 'L' ? b[i] : q - b[i];
        f[1] = a[1] == 0;
        f[2] = (a[2] == 1) + (a[2] == a[1]) * f[1];
        for (int i = 3; i <= n; i++)
            f[i] = ((a[i] == a[i - 1]) * f[i - 1] + (a[i] == a[i - 2] + 1) * f[i - 2]) % P;
        if (a[n] == q) ans = (ans + f[n]) % P;
        if (a[n - 1] == q - 1) ans = (ans + f[n - 1]) % P;
    }
    cout << ans << endl;
}
''','wolf',True),True)

put('S17','D_power',main(r'''
const int P = 998244353, B = 15, N = 1 << B;
using ull = unsigned long long;
unsigned f[30][30][30], a[N][30], b[N][30];
int w[30];

void init() {
    f[0][0][0] = w[0];
    for (int t = 1; t < 30; t++) {
        for (int l = 0; l < t; l++) {
            for (int r = l; r < t; r++) {
                ull s = 0;
                for (int j = l; j <= r; j++) {
                    s += (ull)f[t - 1][l][j] * f[t - 1][j][r];
                    if ((j & 7) == 7) s %= P;
                }
                f[t][l][r] = s % P;
            }
        }
        for (int l = 0; l <= t; l++) f[t][l][t] = w[t];
    }
    a[0][0] = 1;
    for (int j = 0; j < 30; j++) b[0][j] = 1;
    for (int m = 1; m < N; m++) {
        int t = 31 - __builtin_clz(m), z = m ^ (1 << t);
        for (int r = 0; r <= t; r++) {
            ull s = 0;
            for (int l = 0; l <= r; l++) {
                s += (ull)a[z][l] * f[t][l][r];
                if ((l & 7) == 7) s %= P;
            }
            a[m][r] = s % P;
        }
        t = __builtin_ctz(m);
        z = m ^ (1 << t);
        t += B;
        for (int l = 0; l <= t; l++) {
            ull s = 0;
            for (int r = l; r <= t; r++) {
                s += (ull)f[t][l][r] * b[z][r];
                if ((r & 7) == 7) s %= P;
            }
            b[m][l] = s % P;
        }
    }
}

void solve() {
    for (int i = 0; i < 30; i++) cin >> w[i];
    init();
    int q;
    cin >> q;
    for (int i = 1; i <= q; i++) {
        int x;
        cin >> x;
        ull s = 0;
        for (int j = 0; j < B; j++) {
            s += (ull)a[x & (N - 1)][j] * b[x >> B][j];
            if ((j & 7) == 7) s %= P;
        }
        cout << s % P << (i == q ? '\n' : ' ');
    }
}
''','power'))
put('S17','D_power',main(r'''
// 完全背包，适用于所有询问 n < 2^16。
const int N = 1 << 16, P = 998244353;
int w[30], f[N];

void solve() {
    for (int i = 0; i < 30; i++) cin >> w[i];
    f[0] = 1;
    for (int j = 0; j < 16; j++)
        for (int i = 1 << j; i < N; i++)
            f[i] = (f[i] + (ll)w[j] * f[i - (1 << j)]) % P;
    int q;
    cin >> q;
    for (int i = 1; i <= q; i++) {
        int x;
        cin >> x;
        cout << f[x] << (i == q ? '\n' : ' ');
    }
}
''','power'),True)

put('N17','A_median',main(r'''
const int N = 200005;
int n, a[N], pre[N], suf[N];
priority_queue<int> l;
priority_queue<int, vector<int>, greater<int>> r;

void add(int x) {
    if (l.empty() || x <= l.top()) l.push(x);
    else r.push(x);
    if (l.size() < r.size()) {
        l.push(r.top());
        r.pop();
    }
    if (l.size() > r.size() + 1) {
        r.push(l.top());
        l.pop();
    }
}

void solve() {
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i <= n; i++) {
        add(a[i]);
        if (i & 1) pre[i] = l.top();
    }
    while (!l.empty()) l.pop();
    while (!r.empty()) r.pop();
    for (int i = n; i >= 1; i--) {
        add(a[i]);
        if (!(i & 1)) suf[i] = l.top();
    }
    for (int i = 1; i < n; i += 2) {
        if (pre[i] == suf[i + 1]) {
            cout << "Yes" << endl;
            return;
        }
    }
    cout << "No" << endl;
}
''','median'))
put('N17','A_median',main(r'''
// O(n^2 log n)，适用于 n <= 2000。
const int N = 2005;
int n, a[N], b[N];

int query(int l, int r) {
    int m = 0;
    for (int i = l; i <= r; i++) b[++m] = a[i];
    sort(b + 1, b + m + 1);
    return b[(m + 1) / 2];
}

void solve() {
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i < n; i += 2) {
        int x = query(1, i), y = query(i + 1, n);
        if (x == y) {
            cout << "Yes" << endl;
            return;
        }
    }
    cout << "No" << endl;
}
''','median'),True)

put('N17','B_tramcar',main(r'''
const int N = 300005;
int n, a[N], b[N], c[N], f[N], nd[N], z;
ll k;

void add(int x) {
    for (; x <= n; x += x & -x) c[x]++;
}

int query(int x) {
    int s = 0;
    for (; x; x -= x & -x) s += c[x];
    return s;
}

bool check(int m) {
    fill(nd, nd + z + 2, 0);
    int now = 0;
    for (int i = 1; i <= n; i++) {
        if (!a[i]) now++;
        else {
            int r = max(f[i] - m, 0);
            if (r > z - now) return false;
            if (r) nd[z - r + 1] = max(nd[z - r + 1], a[i]);
        }
    }
    ll s = 0;
    for (int i = 1; i <= z; i++) {
        nd[i] = max(nd[i], nd[i - 1]);
        s += nd[i];
    }
    return s <= k;
}

void solve() {
    cin >> n >> k;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        b[i] = a[i];
        z += !a[i];
    }
    sort(b + 1, b + n + 1);
    int m = unique(b + 1, b + n + 1) - b - 1;
    for (int i = n; i >= 1; i--) {
        int p = lower_bound(b + 1, b + m + 1, a[i]) - b;
        f[i] = query(p - 1);
        add(p);
    }
    int l = 0, r = n - 1;
    while (l < r) {
        int m = (l + r) / 2;
        if (check(m)) r = m;
        else l = m + 1;
    }
    cout << l << endl;
}
''','tramcar'))
put('N17','B_tramcar',main(r'''
// 仅适用于 K=0；O(n^2)，对应 N<=5000、K=0 的子任务。
const int N = 5005;
int n, a[N];
ll k;

void solve() {
    cin >> n >> k;
    for (int i = 1; i <= n; i++) cin >> a[i];
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        int s = 0;
        for (int j = i + 1; j <= n; j++) s += a[j] < a[i];
        ans = max(ans, s);
    }
    cout << ans << endl;
}
''','tramcar'),True)

put('N17','C_connected',main(r'''
const int N = 100005, M = 800005, V = 0x3f3f3f3f;
int n, m, h[N * 2], to[M], nx[M], ec, d[N * 2], q[N * 2];
struct Node {
    int x, y;
    bool operator < (const Node &b) const {
        if (x + y != b.x + b.y) return x + y < b.x + b.y;
        return x < b.x;
    }
    bool operator == (const Node &b) const { return x == b.x && y == b.y; }
} a[N];

void add(int x, int y) {
    to[++ec] = y;
    nx[ec] = h[x];
    h[x] = ec;
}

void solve() {
    cin >> n >> m;
    fill(h + 1, h + n * 2 + 1, 0);
    fill(d + 1, d + n * 2 + 1, V);
    ec = 0;
    for (int i = 1; i <= m; i++) {
        int x, y;
        cin >> x >> y;
        add(x, y + n);
        add(y + n, x);
        add(y, x + n);
        add(x + n, y);
    }
    int l = 0, r = 1;
    q[0] = 1;
    d[1] = 0;
    while (l < r) {
        int x = q[l++];
        for (int i = h[x]; i; i = nx[i]) {
            int y = to[i];
            if (d[y] == V) {
                d[y] = d[x] + 1;
                q[r++] = y;
            }
        }
    }
    if (d[n + 1] == V) {
        cout << n - 1 << endl;
        return;
    }
    for (int i = 1; i <= n; i++) a[i] = {min(d[i], d[i + n]), max(d[i], d[i + n])};
    sort(a + 1, a + n + 1);
    set<pair<int, int>> s;
    ll ans = 0;
    int t = 0;
    for (int i = 1; i <= n;) {
        int j = i;
        while (j < n && a[j + 1] == a[i]) j++;
        int c = j - i + 1;
        bool ok = s.count({a[i].x - 1, a[i].y - 1});
        s.insert({a[i].x, a[i].y});
        if (i > 1) ans += max(c, t);
        t = ok ? min(c, t) : c;
        if (j == n || a[j + 1].x != a[i].x + 1 || a[j + 1].y != a[i].y - 1) {
            ans += a[i].y == a[i].x + 1 ? (t + 1) / 2 : t;
            t = 0;
        }
        i = j + 1;
    }
    cout << ans << endl;
}
''','connected',True))
put('N17','C_connected',main(r'''
// 仅适用于 n<=5。枚举全部带自环的简单无向图，不限于原图的子图。
const int N = 5, V = 1000000;
int n, m, e[15][2], a[N][2], b[N][2], g[N][N];

void bfs(int d[N][2]) {
    for (int i = 0; i < n; i++) d[i][0] = d[i][1] = V;
    queue<pair<int, int>> q;
    d[0][0] = 0;
    q.push({0, 0});
    while (!q.empty()) {
        int x = q.front().first, p = q.front().second;
        q.pop();
        for (int y = 0; y < n; y++) {
            if (g[x][y] && d[y][p ^ 1] == V) {
                d[y][p ^ 1] = d[x][p] + 1;
                q.push({y, p ^ 1});
            }
        }
    }
}

void solve() {
    cin >> n >> m;
    memset(g, 0, sizeof(g));
    for (int i = 1; i <= m; i++) {
        int x, y;
        cin >> x >> y;
        g[x - 1][y - 1] = g[y - 1][x - 1] = 1;
    }
    bfs(a);
    int tot = 0, ans = m;
    for (int i = 0; i < n; i++)
        for (int j = i; j < n; j++) {
            e[tot][0] = i;
            e[tot++][1] = j;
        }
    for (int s = 0; s < (1 << tot); s++) {
        int c = __builtin_popcount((unsigned)s);
        if (c < n - 1 || c >= ans) continue;
        memset(g, 0, sizeof(g));
        for (int j = 0; j < tot; j++)
            if (s >> j & 1) g[e[j][0]][e[j][1]] = g[e[j][1]][e[j][0]] = 1;
        bfs(b);
        bool ok = true;
        for (int i = 0; i < n; i++)
            for (int j = 0; j < 2; j++) ok &= a[i][j] == b[i][j];
        if (ok) ans = c;
    }
    cout << ans << endl;
}
''','connected',True),True)

put('N17','D_crystal',main(r'''
const int N = 500005, L = 19, P = 1000000007, Q = 1000000009, B = 911382323;
int n, k, a[26][26], st[N], top, h[N], to[N], nx[N], ec;
int f[L][N], len[N], u[L][N], v[L][N], pw[L], qw[L];
string s;

void add(int x, int y) {
    to[++ec] = y;
    nx[ec] = h[x];
    h[x] = ec;
}

int cmp(int x, int y) {
    int a = x, b = y;
    for (int j = L - 1; j >= 0; j--) {
        if (len[x] >= (1 << j) && len[y] >= (1 << j) && u[j][x] == u[j][y] && v[j][x] == v[j][y]) {
            x = f[j][x];
            y = f[j][y];
        }
    }
    if (!len[x]) return a;
    if (!len[y]) return b;
    return s[x - 1] < s[y - 1] ? a : b;
}

void solve() {
    cin >> k >> n;
    for (int i = 0; i < k; i++) {
        string t;
        cin >> t;
        for (int j = 0; j < k; j++) a[i][j] = t[j] - '0';
    }
    cin >> s;
    for (int i = n; i >= 1; i--) {
        while (top && a[s[i - 1] - 'a'][s[st[top] - 1] - 'a']) add(i, st[top--]);
        st[++top] = i;
    }
    pw[0] = qw[0] = B;
    for (int j = 1; j < L; j++) {
        pw[j] = (ll)pw[j - 1] * pw[j - 1] % P;
        qw[j] = (ll)qw[j - 1] * qw[j - 1] % Q;
    }
    for (int j = 0; j < L; j++) f[j][n + 1] = n + 1;
    for (int i = n; i >= 1; i--) {
        int x = i + 1;
        for (int j = h[i]; j; j = nx[j]) x = cmp(x, f[0][to[j]]);
        f[0][i] = x;
        len[i] = len[x] + 1;
        u[0][i] = v[0][i] = s[i - 1] - 'a' + 1;
        for (int j = 1; j < L; j++) {
            int x = f[j - 1][i];
            f[j][i] = f[j - 1][x];
            u[j][i] = ((ll)u[j - 1][i] * pw[j - 1] + u[j - 1][x]) % P;
            v[j][i] = ((ll)v[j - 1][i] * qw[j - 1] + v[j - 1][x]) % Q;
        }
    }
    for (int i = 1; i <= n; i = f[0][i]) cout << s[i - 1];
    cout << endl;
}
''','crystal'))
put('N17','D_crystal',main(r'''
// O(n^3) 时间上界、O(n^2) 空间；适用于 n<=500。
const int N = 505;
int k, n, a[26][26], st[N], top;
bool ok[N][N];
string s, f[N];

void solve() {
    cin >> k >> n;
    for (int i = 0; i < k; i++) {
        string t;
        cin >> t;
        for (int j = 0; j < k; j++) a[i][j] = t[j] - '0';
    }
    cin >> s;
    for (int r = 1; r <= n; r++) {
        top = 0;
        for (int l = r; l >= 1; l--) {
            while (top && a[s[l - 1] - 'a'][s[st[top] - 1] - 'a']) top--;
            st[++top] = l;
            ok[l][r] = top == 1;
        }
    }
    for (int i = n; i >= 1; i--) {
        string t = f[i + 1];
        for (int j = i + 1; j <= n; j++)
            if (ok[i][j] && f[j + 1] < t) t = f[j + 1];
        f[i] = s[i - 1] + t;
    }
    cout << f[1] << endl;
}
''','crystal'),True)

print('Created 16 C++ files.')
