// 子任务 1、2、3：78 分。O(n log V+B)，额外空间 O(1)。
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

int main() {
#ifndef LOCAL
    freopen("counter.in", "r", stdin);
    freopen("counter.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    ll b, g = 0, mx = 0, d = 0, ans = 0;
    cin >> n >> b;
    for (int i = 1; i <= n; i++) {
        ll t, v;
        cin >> t >> v;
        mx = max(mx, v);
        if (i == 1) d = t - v;
        else g = gcd(g, abs(t - v - d));
    }
    if (!g) ans = max(0LL, b - mx);
    else for (ll k = mx + 1; k <= b; k++) ans += g % k == 0;
    cout << ans << endl;
    return 0;
}
