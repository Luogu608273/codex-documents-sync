#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

// 部分分：p、q、每次询问的 y 均不超过 1000，对应子任务 1。
const int N = 100005, M = 25;
int m[2], q, p, a[2][M], b[2][M], f[2][N];

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
        for (int x = 0; x < p; x++)
            for (int i = 1; i <= m[s]; i++)
                f[s][x] = (f[s][x] + 1LL * a[s][i] * qpow(x, b[s][i])) % p;
    while (q--) {
        int x, y, s;
        cin >> x >> y >> s;
        x %= p;
        while (y--) x = f[s][x], s ^= 1;
        cout << x << endl;
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
