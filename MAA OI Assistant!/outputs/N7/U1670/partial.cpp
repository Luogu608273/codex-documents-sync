// 适用：n <= 6（测试点 1~4）。枚举 Prüfer 序列及非树边子集。
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int P = 998244353;
int n, m, a[7][7], t[7][7], p[7], deg[7], par[7][7], dep[7][7];
int eu[20], ev[20], ok[20], f[1 << 15], ans;

void dfs(int r, int u, int fa) {
    par[r][u] = fa;
    for (int v = 1; v <= n; v++) {
        if (!t[u][v] || v == fa) continue;
        dep[r][v] = dep[r][u] + 1;
        dfs(r, v, u);
    }
}

bool ancestor(int r, int x, int y) {
    while (dep[r][y] > dep[r][x]) y = par[r][y];
    return x == y;
}

void calc() {
    memset(t, 0, sizeof(t));
    for (int i = 1; i <= n; i++) deg[i] = 1;
    for (int i = 1; i <= n - 2; i++) deg[p[i]]++;
    for (int i = 1; i <= n - 2; i++) {
        int u = 1;
        while (deg[u] != 1) u++;
        int v = p[i];
        if (!a[u][v]) return;
        t[u][v] = t[v][u] = 1;
        deg[u]--, deg[v]--;
    }
    int u = 1, v = n;
    while (deg[u] != 1) u++;
    while (deg[v] != 1) v--;
    if (!a[u][v]) return;
    t[u][v] = t[v][u] = 1;
    for (int r = 1; r <= n; r++) {
        dep[r][r] = 0;
        dfs(r, r, 0);
    }
    int k = 0;
    for (int i = 1; i <= m; i++) {
        u = eu[i], v = ev[i];
        if (t[u][v]) continue;
        ok[k] = 0;
        for (int r = 1; r <= n; r++)
            if (!ancestor(r, u, v) && !ancestor(r, v, u)) ok[k] |= 1 << (r - 1);
        k++;
    }
    f[0] = (1 << n) - 1;
    if (++ans == P) ans = 0;
    for (int s = 1; s < (1 << k); s++) {
        int j = __builtin_ctz((unsigned)s);
        f[s] = f[s ^ (1 << j)] & ok[j];
        if (f[s] && ++ans == P) ans = 0;
    }
}

void enumerate(int x) {
    if (x > n - 2) {
        calc();
        return;
    }
    for (int i = 1; i <= n; i++) {
        p[x] = i;
        enumerate(x + 1);
    }
}

void solve() {
    cin >> n >> m;
    for (int i = 1; i <= m; i++) {
        cin >> eu[i] >> ev[i];
        a[eu[i]][ev[i]] = a[ev[i]][eu[i]] = 1;
    }
    enumerate(1);
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("ndfs.in", "r", stdin);
    freopen("ndfs.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
