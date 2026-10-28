#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

// 部分分：所有测试的 n 之和、m 之和均不超过 2000，对应子任务 1。
const int N = 2005;
const ll V = (1LL << 62);
int n, m, a[N], b[N], c[N];
ll d[N][N], f[N], g[N];

void solve() {
    cin >> n >> m;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i <= m; i++) cin >> b[i];
    for (int i = 1; i <= m; i++) cin >> c[i];
    for (int x = 1; x <= m; x++) {
        for (int y = 1; y <= m; y++) d[x][y] = V;
        int y = x;
        ll t = 0;
        while (d[x][y] == V) {
            d[x][y] = t;
            t += c[y];
            y = b[y];
        }
    }
    for (int v = 1; v <= m; v++) f[v] = 0;
    for (int i = 1; i <= n; i++) {
        ll mn = V;
        for (int v = 1; v <= m; v++) {
            mn = min(mn, f[v]);
            g[v] = max(mn, d[a[i]][v]);
        }
        for (int v = 1; v <= m; v++) f[v] = g[v];
    }
    ll ans = V;
    for (int v = 1; v <= m; v++) ans = min(ans, f[v]);
    cout << (ans == V ? -1 : ans) << endl;
}

int main() {
#ifndef LOCAL
    freopen("transform.in", "r", stdin);
    freopen("transform.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
