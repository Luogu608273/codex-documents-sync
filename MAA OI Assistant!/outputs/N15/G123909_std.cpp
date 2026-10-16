#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 50005, K = 21, P = 1000000007;
int n, k, q, a[N], f[K][K], g[K][K], u[N][K], v[N][K];

void solve() {
    cin >> n >> k;
    for (int i = 1; i <= n; ++i) cin >> a[i];
    for (int i = 0; i <= k; ++i) f[i][i] = g[i][i] = 1, u[0][i] = 1;
    v[0][0] = 1;
    for (int t = 1; t <= n; ++t) {
        int x = a[t];
        for (int j = 0; j <= k; ++j) {
            int s = 0;
            for (int i = 0; i <= x; ++i) (s += f[i][j]) >= P ? s -= P : 0;
            u[t][j] = u[t - 1][j];
            (u[t][j] += s) >= P ? u[t][j] -= P : 0;
            (f[x][j] += s) >= P ? f[x][j] -= P : 0;
        }
        for (int i = 0; i <= k; ++i) {
            int s = (g[i][x] + (g[i][x] & 1 ? P : 0)) / 2;
            for (int j = 0; j < x; ++j) (g[i][j] -= s) < 0 ? g[i][j] += P : 0;
            g[i][x] = s;
            v[t][i] = g[i][0];
        }
    }
    cin >> q;
    while (q--) {
        int l, r;
        cin >> l >> r;
        ll ans = 0;
        for (int i = 0; i <= k; ++i) ans = (ans + 1ll * u[r][i] * v[l - 1][i]) % P;
        cout << ans << endl;
    }
}

int main() {
#ifndef LOCAL
    freopen("subseq.in", "r", stdin);
    freopen("subseq.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _ = 1;
    while (_--) solve();
    return 0;
}
