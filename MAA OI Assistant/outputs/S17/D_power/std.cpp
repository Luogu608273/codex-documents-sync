#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

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

int main() {
#ifndef LOCAL
    freopen("power.in", "r", stdin);
    freopen("power.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
