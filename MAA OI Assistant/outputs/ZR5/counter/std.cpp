#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

int n;
ll b, g, mx, d;

void solve() {
    cin >> n >> b;
    for (int i = 1; i <= n; i++) {
        ll t, v;
        cin >> t >> v;
        mx = max(mx, v);
        if (i == 1) d = t - v;
        else g = gcd(g, abs(t - v - d));
    }
    if (!g) {
        cout << max(0LL, b - mx) << endl;
        return;
    }
    ll ans = 0;
    for (ll i = 1; i * i <= g; i++) {
        if (g % i) continue;
        if (mx < i && i <= b) ans++;
        ll j = g / i;
        if (j != i && mx < j && j <= b) ans++;
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("counter.in", "r", stdin);
    freopen("counter.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
