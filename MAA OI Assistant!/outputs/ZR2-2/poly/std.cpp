#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 200005, M = 25, V = 30;
int m[2], q, p, a[2][M], b[2][M], f[V][N];

int qpow(int a, int b) {
    int res = 1;
    for (; b; b >>= 1, a = 1LL * a * a % p)
        if (b & 1) res = 1LL * res * a % p;
    return res;
}

void solve() {
    cin >> m[0] >> m[1] >> q >> p;
    for (int s = 0; s < 2; s++)
        for (int i = 1; i <= m[s]; i++) {
            cin >> a[s][i] >> b[s][i];
            a[s][i] %= p;
        }
    for (int s = 0; s < 2; s++)
        for (int x = 0; x < p; x++) {
            int res = 0;
            for (int i = 1; i <= m[s]; i++)
                res = (res + 1LL * a[s][i] * qpow(x, b[s][i])) % p;
            f[0][s * p + x] = (s ^ 1) * p + res;
        }
    for (int j = 1; j < V; j++)
        for (int i = 0; i < 2 * p; i++)
            f[j][i] = f[j - 1][f[j - 1][i]];
    while (q--) {
        int x, y, s;
        cin >> x >> y >> s;
        x = s * p + x % p;
        for (int j = 0; y; j++, y >>= 1)
            if (y & 1) x = f[j][x];
        cout << x % p << endl;
    }
}

int main() {
#ifndef LOCAL
    freopen("poly.in", "r", stdin);
    freopen("poly.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
