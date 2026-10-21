#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

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
