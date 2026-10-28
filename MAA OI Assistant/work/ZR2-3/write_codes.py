from pathlib import Path
root=Path('outputs/ZR2-3')
for name in ['color','greedy','brackets','noise']:
    (root/name).mkdir(parents=True,exist_ok=True)
def put(name,kind,body):
    pre='#include <bits/stdc++.h>\n#define endl \'\\n\'\nusing namespace std;\nusing ll = long long;\n\n'
    main='''
int main() {
#ifndef LOCAL
    freopen("NAME.in", "r", stdin);
    freopen("NAME.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    RUN
    return 0;
}
'''.replace('NAME',name).replace('RUN','solve();' if name=='greedy' else 'int _;\n    cin >> _;\n    while (_--) solve();')
    (root/name/(kind+'.cpp')).write_text(pre+body+main,encoding='utf-8')
color='''int get(char c) {
    if (c == 'R') return 1;
    if (c == 'Y') return 2;
    if (c == 'B') return 4;
    if (c == 'O') return 3;
    if (c == 'P') return 5;
    if (c == 'G') return 6;
    if (c == 'A') return 7;
    return 0;
}

void solve() {
    int n, pre = 0, ans = 0;
    string s;
    cin >> n >> s;
    for (char c : s) {
        int x = get(c);
        ans += __builtin_popcount((unsigned)(x & ~pre));
        pre = x;
    }
    cout << ans << endl;
}
'''
put('color','std',color)
put('color','partial',color[:color.index('void solve()')]+'''const int N = 1005;
int a[N];

// Only the N <= 1000 subtask is supported.
void solve() {
    int n, ans = 0;
    string s;
    cin >> n >> s;
    if (n > 1000) exit(1);
    for (int i = 1; i <= n; i++) a[i] = get(s[i - 1]);
    for (int b = 1; b <= 4; b <<= 1) {
        for (int l = 1; l <= n; l++) {
            if (!(a[l] & b)) continue;
            int r = l;
            while (r < n && (a[r + 1] & b)) r++;
            for (int i = l; i <= r; i++) a[i] ^= b;
            ans++;
        }
    }
    cout << ans << endl;
}
''')
put('greedy','std','''const int N = 155;
const ll V = -(1LL << 60);
int n, A, B;
struct Node {
    int c;
    ll u, v;
} a[N];
ll f[N][N][N];

bool cmp(Node x, Node y) {
    return x.c > y.c;
}

void solve() {
    cin >> n >> A >> B;
    for (int i = 1; i <= n; i++) cin >> a[i].c >> a[i].u >> a[i].v;
    sort(a + 1, a + n + 1, cmp);
    int m = min(A, B);
    for (int r = 0; r <= m; r++)
        for (int x = 0; x <= A; x++)
            for (int y = 0; y <= B; y++) f[r][x][y] = V;
    for (int r = 0; r <= m; r++) f[r][A - r][B - r] = 0;
    for (int i = 1; i <= n; i++) {
        int c = a[i].c;
        ll u = a[i].u, v = a[i].v;
        // Every transition decreases the lexicographic order of (r,x,y).
        for (int r = 0; r <= m; r++) {
            for (int x = 0; x + r <= A; x++) {
                for (int y = 0; y + r <= B; y++) {
                    ll z = f[r][x][y];
                    if (z == V) continue;
                    if (r >= c) f[r - c][x][y] = max(f[r - c][x][y], z + u + v);
                    if (x >= c && y < c) f[r][x - c][y] = max(f[r][x - c][y], z + u);
                    if (y >= c && x < c) f[r][x][y - c] = max(f[r][x][y - c], z + v);
                }
            }
        }
    }
    ll ans = 0;
    for (int x = 0; x <= A; x++)
        for (int y = 0; y <= B; y++) ans = max(ans, f[0][x][y]);
    cout << ans << endl;
}
''')
put('greedy','partial','''const int N = 155;
int n, A, B, c[N], vis[N];
ll u[N], v[N], f[N], ans;

void dfs(int k, int x, int y, ll z) {
    if (k > n) {
        ans = max(ans, z);
        return;
    }
    for (int i = 1; i <= n; i++) {
        if (vis[i]) continue;
        vis[i] = 1;
        int a = x, b = y;
        ll w = z;
        if (a >= c[i]) a -= c[i], w += u[i];
        if (b >= c[i]) b -= c[i], w += v[i];
        dfs(k + 1, a, b, w);
        vis[i] = 0;
    }
}

// Supports n <= 8, or A == B (35% of the listed test points).
void solve() {
    cin >> n >> A >> B;
    for (int i = 1; i <= n; i++) cin >> c[i] >> u[i] >> v[i];
    if (A == B) {
        for (int i = 1; i <= n; i++)
            for (int j = A; j >= c[i]; j--) f[j] = max(f[j], f[j - c[i]] + u[i] + v[i]);
        cout << f[A] << endl;
    } else {
        if (n > 8) exit(1);
        dfs(1, A, B, 0);
        cout << ans << endl;
    }
}
''')
put('brackets','std','''using Node = pair<int, int>;

struct Solver {
    priority_queue<Node> no;
    priority_queue<Node, vector<Node>, greater<Node>> yes;
    Node first, last;
    ll ans = 0;
    bool empty = true;
    void front(Node a, Node b) {
        if (empty) {
            first = a, last = b;
            ans = a.first;
            empty = false;
            return;
        }
        yes.push(b);
        yes.push(first);
        Node z = yes.top();
        yes.pop();
        no.push(z);
        ans += (ll)a.first + b.first - z.first;
        first = a;
    }
    void back(Node a, Node b) {
        if (empty) {
            front(a, b);
            return;
        }
        no.push(last);
        no.push(a);
        Node z = no.top();
        no.pop();
        yes.push(z);
        ans += z.first;
        last = b;
    }
};

void solve() {
    int q;
    cin >> q;
    Solver all, inner;
    for (int i = 1; i <= q; i++) {
        int t, x, y;
        cin >> t >> x >> y;
        Node a = {x, i * 2}, b = {y, i * 2 + 1};
        if (all.empty) {
            if (t == 1) all.front(b, a);
            else all.back(a, b);
        } else {
            Node f = all.first, l = all.last;
            if (t == 1) {
                all.front(b, a);
                inner.front(a, f);
            } else if (t == 3) {
                all.back(a, b);
                inner.back(l, a);
            } else {
                swap(all, inner);
                all.front(a, f);
                all.back(l, b);
            }
        }
        cout << all.ans << endl;
    }
}
''')
put('brackets','partial','''// Recompute the optimum by balance DP after every operation: Q <= 100.
const int N = 205;
const ll V = -(1LL << 60);
ll f[N], g[N];

void solve() {
    int q;
    cin >> q;
    if (q > 100) exit(1);
    deque<int> a;
    while (q--) {
        int t, x, y;
        cin >> t >> x >> y;
        if (t == 1) a.push_front(x), a.push_front(y);
        if (t == 2) a.push_front(x), a.push_back(y);
        if (t == 3) a.push_back(x), a.push_back(y);
        int n = (int)a.size();
        fill(f, f + n + 1, V);
        f[0] = 0;
        for (int w : a) {
            fill(g, g + n + 1, V);
            for (int j = 0; j <= n; j++) {
                if (f[j] == V) continue;
                if (j < n) g[j + 1] = max(g[j + 1], f[j] + w);
                if (j) g[j - 1] = max(g[j - 1], f[j]);
            }
            copy(g, g + n + 1, f);
        }
        cout << f[0] << endl;
    }
}
''')
put('noise','std','''const int N = 500005, K = 19;
int n, a[N], b[N], sa[N], x[N], y[N], c[N * 2], lg[N];

struct LCE {
    int rk[N], f[K][N];
    void build() {
        int m = n * 2 + 1;
        fill(c, c + m + 1, 0);
        for (int i = 1; i <= n; i++) c[x[i] = b[i] + n + 1]++;
        for (int i = 1; i <= m; i++) c[i] += c[i - 1];
        for (int i = n; i; i--) sa[c[x[i]]--] = i;
        for (int k = 1, p = 0; k < n; k <<= 1) {
            p = 0;
            for (int i = n - k + 1; i <= n; i++) y[++p] = i;
            for (int i = 1; i <= n; i++) if (sa[i] > k) y[++p] = sa[i] - k;
            fill(c, c + m + 1, 0);
            for (int i = 1; i <= n; i++) c[x[y[i]]]++;
            for (int i = 1; i <= m; i++) c[i] += c[i - 1];
            for (int i = n; i; i--) sa[c[x[y[i]]]--] = y[i];
            copy(x + 1, x + n + 1, y + 1);
            p = 1;
            x[sa[1]] = 1;
            for (int i = 2; i <= n; i++) {
                int u = sa[i], v = sa[i - 1];
                if (y[u] != y[v] || (u + k <= n ? y[u + k] : 0) != (v + k <= n ? y[v + k] : 0)) p++;
                x[u] = p;
            }
            if (p == n) break;
            m = p;
        }
        for (int i = 1; i <= n; i++) rk[sa[i]] = i;
        for (int i = 1, k = 0; i <= n; i++) {
            if (rk[i] == 1) {
                f[0][1] = 0;
                continue;
            }
            int j = sa[rk[i] - 1];
            while (i + k <= n && j + k <= n && b[i + k] == b[j + k]) k++;
            f[0][rk[i]] = k;
            if (k) k--;
        }
        for (int j = 1; (1 << j) <= n; j++)
            for (int i = 1; i + (1 << j) - 1 <= n; i++)
                f[j][i] = min(f[j - 1][i], f[j - 1][i + (1 << (j - 1))]);
    }
    int query(int p, int q) {
        if (p == q) return n - p + 1;
        int l = rk[p], r = rk[q];
        if (l > r) swap(l, r);
        l++;
        int k = lg[r - l + 1];
        return min(f[k][l], f[k][r - (1 << k) + 1]);
    }
} s, t;

int right(int p, int q) {
    if (a[p] != -a[q]) return 0;
    return min(n - q + 1, 1 + s.query(p, q));
}

int left(int p, int q) {
    if (!p || a[p] != -a[q]) return 0;
    return min(p, 1 + t.query(n - p + 1, n - q + 1));
}

void solve() {
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    lg[1] = 0;
    for (int i = 2; i <= n; i++) lg[i] = lg[i >> 1] + 1;
    // b[i] is unchanged if every value in a is negated.
    for (int i = 1; i < n; i++) b[i] = a[i] > 0 ? a[i + 1] : -a[i + 1];
    b[n] = 0;
    s.build();
    for (int i = 1; i < n; i++) {
        int p = n - i + 1;
        b[i] = a[p] > 0 ? a[p - 1] : -a[p - 1];
    }
    b[n] = 0;
    t.build();
    ll ans = 0;
    for (int m = 1; m * 2 <= n; m++) {
        for (int i = 1; i + m <= n; i += m) {
            int r = min(m, right(i, i + m));
            if (!r) continue;
            int l = min(m - 1, left(i - 1, i + m - 1));
            if (l + r >= m) ans += l + r - m + 1;
        }
    }
    cout << ans << endl;
}
''')
put('noise','partial','''const int N = 2005;
int a[N];

// Supports N <= 2000: all half-lengths, consecutive matching runs.
void solve() {
    int n;
    cin >> n;
    if (n > 2000) exit(1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    ll ans = 0;
    for (int m = 1; m * 2 <= n; m++) {
        int cnt = 0;
        for (int i = 1; i + m <= n; i++) {
            if (a[i] == -a[i + m]) cnt++;
            else cnt = 0;
            if (cnt >= m) ans++;
        }
    }
    cout << ans << endl;
}
''')
print('wrote 8 C++ files')
