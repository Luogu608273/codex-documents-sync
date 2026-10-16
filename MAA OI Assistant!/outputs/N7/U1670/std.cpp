#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
using ull = unsigned long long;
const int N = 18, M = 1 << N, P = 998244353;
int n, m, lim, adj[N], g[N][M], b[N][M], pw[155], ipw[155];
bool con[M];

int power(int a, int k) {
    int res = 1;
    for (; k; k >>= 1, a = (ll)a * a % P)
        if (k & 1) res = (ll)res * a % P;
    return res;
}

void init() {
    pw[0] = ipw[0] = 1;
    for (int i = 1; i <= m; i++) {
        pw[i] = (ll)pw[i - 1] * 2 % P;
        ipw[i] = (ll)ipw[i - 1] * ((P + 1) / 2) % P;
    }
    for (int s = 1; s < lim; s++) {
        int t = s & -s, vis = 0;
        while (t) {
            int v = __builtin_ctz((unsigned)t);
            t ^= 1 << v;
            vis |= 1 << v;
            t |= adj[v] & s & ~vis;
        }
        con[s] = vis == s;
    }
    for (int i = 0; i < n; i++) g[i][0] = 1;
}

void solve() {
    cin >> n >> m;
    lim = 1 << n;
    for (int i = 1, u, v; i <= m; i++) {
        cin >> u >> v;
        u--, v--;
        adj[u] |= 1 << v;
        adj[v] |= 1 << u;
    }
    init();
    for (int s = 1; s < lim; s++) {
        int out = (lim - 1) ^ s;
        for (int t = s; t; t &= t - 1) {
            int v = __builtin_ctz((unsigned)t);
            int z = (ll)g[v][s ^ (1 << v)] * ipw[__builtin_popcount((unsigned)(adj[v] & s))] % P;
            for (int u = adj[v] & out; u; u &= u - 1) {
                int r = __builtin_ctz((unsigned)u);
                (b[r][s] += z) >= P ? b[r][s] -= P : 0;
            }
        }
        int mask = s ^ (s & -s);
        for (int t = out; t; t &= t - 1) {
            int r = __builtin_ctz((unsigned)t);
            if (!con[s | (1 << r)]) continue;
            ull res = b[r][s];
            int cnt = 0;
            for (int u = mask; u; u = (u - 1) & mask) {
                res += (ull)g[r][u] * b[r][s ^ u];
                if (++cnt == 16) res %= P, cnt = 0;
            }
            g[r][s] = res % P;
        }
    }
    int all = lim - 1, ans = 0;
    for (int r = 0; r < n; r++) {
        int z = ipw[__builtin_popcount((unsigned)adj[r])];
        for (int s = 1 << r; s < lim; s = (s + 1) | (1 << r))
            b[r][s] = (ll)g[r][s ^ (1 << r)] * z % P;
        (ans += b[r][all]) >= P ? ans -= P : 0;
    }
    ull res = 0;
    int cnt = 0;
    for (int s = 1; s < all; s += 2) {
        int t = all ^ s;
        for (int u = s; u; u &= u - 1) {
            int x = __builtin_ctz((unsigned)u);
            for (int v = adj[x] & t; v; v &= v - 1) {
                int y = __builtin_ctz((unsigned)v);
                res += (ull)b[x][s] * b[y][t];
                if (++cnt == 16) res %= P, cnt = 0;
            }
        }
    }
    ans = (ans - (ll)(res % P) * 2 % P + P) % P;
    cout << (ll)ans * pw[m] % P << endl;
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
