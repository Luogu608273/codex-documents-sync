#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 2005;
const ll V = -4000000000000000000ll;
int n, m;
ll a[N], b[N], s[N], t[N], p[N], q[N], f[N];

void solve() {
    cin >> n >> m;
    for (int i = 1; i <= n; ++i) cin >> a[i] >> s[i] >> p[i], a[i] += a[i - 1];
    for (int j = 1; j <= m; ++j) cin >> b[j] >> t[j] >> q[j], b[j] += b[j - 1];
    for (int j = 1; j <= m; ++j) f[j] = f[j - 1] + (b[j] <= t[j] ? q[j] : 0);
    for (int i = 1; i <= n; ++i) {
        f[0] += a[i] <= s[i] ? p[i] : 0;
        for (int j = 1; j <= m; ++j) {
            ll x = a[i] + b[j];
            f[j] = max(f[j] + (x <= s[i] ? p[i] : 0), f[j - 1] + (x <= t[j] ? q[j] : 0));
        }
    }
    cout << f[m] << endl;
}

int main() {
#ifndef LOCAL
    freopen("cookoff.in", "r", stdin);
    freopen("cookoff.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _ = 1;
    while (_--) solve();
    return 0;
}
