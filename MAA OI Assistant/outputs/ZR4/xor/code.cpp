#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 1000005, V = 1 << 20;
int n, m, a[N], f[V];

bool check(int ans, int k) {
    int h = m - k, z = 1 << h, all = z - 1;
    int p = ans >> (k + 1), ban = ((ans ^ (ans >> 1)) >> k) & all;
    int low = (1 << k) - 1;
    fill(f, f + z, -1);
    for (int i = 1; i <= n; i++) {
        int x = (a[i] >> k) ^ p;
        if (!(x & ban)) f[x] = max(f[x], a[i] & low);
    }
    for (int b = 1; b < z; b <<= 1)
        for (int l = 0; l < z; l += b << 1)
            for (int j = 0; j < b; j++)
                f[l + b + j] = max(f[l + b + j], f[l + j]);
    for (int x = 0; x < z; x++)
        if (f[x] >= 0 && f[all ^ x] >= 0 && f[x] + f[all ^ x] >= (1 << k)) return true;
    return false;
}

void solve() {
    cin >> n >> m;
    for (int i = 1; i <= n; i++) cin >> a[i];
    int ans = 0;
    for (int k = m; k >= 1; k--)
        if (check(ans | (1 << k), k)) ans |= 1 << k;
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("xor.in", "r", stdin);
    freopen("xor.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
