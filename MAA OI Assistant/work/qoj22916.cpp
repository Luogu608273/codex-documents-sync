#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 200005, M = 400005;
int n, m, h[N], to[M], ne[M], tot;
int dfn[N], low[N], f[N], cnt;
string a, b, ans;

void add(int u, int v) {
    to[++tot] = v, ne[tot] = h[u], h[u] = tot;
}

void dfs(int u, int p) {
    dfn[u] = low[u] = ++cnt;
    for (int i = h[u]; i; i = ne[i]) {
        if (i == (p ^ 1)) continue;
        int v = to[i];
        if (dfn[v]) low[u] = min(low[u], dfn[v]);
        else {
            dfs(v, i);
            low[u] = min(low[u], low[v]);
            if (low[v] > dfn[u] && f[v]) ans[(i >> 1) - 1] = '0';
            f[u] ^= f[v];
        }
    }
}

void init() {
    tot = 1, cnt = 0;
    for (int i = 1; i <= n + 1; i++) {
        h[i] = dfn[i] = low[i] = f[i] = 0;
    }
}

void solve() {
    cin >> n >> m >> a >> b;
    init();
    int p = 0;
    for (int i = 1; i <= n; i++) {
        int x = a[i - 1] ^ b[i - 1];
        f[i] = x ^ p, p = x;
    }
    f[n + 1] = p;
    for (int i = 1, l, r; i <= m; i++) {
        cin >> l >> r;
        add(l, r + 1), add(r + 1, l);
    }
    ans = string(m, '1');
    bool ok = true;
    for (int rt = 1; rt <= n + 1; rt++) {
        if (dfn[rt]) continue;
        dfs(rt, 0);
        if (f[rt]) ok = false;
    }
    if (!ok) ans = string(m, '0');
    cout << ans << endl;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
