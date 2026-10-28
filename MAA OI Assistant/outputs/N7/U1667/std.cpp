#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 1000005, P = 998244353;
int fac[N], inv[N];

int power(int a, int b) {
    int res = 1;
    for (; b; b >>= 1, a = (ll)a * a % P)
        if (b & 1) res = (ll)res * a % P;
    return res;
}

void init() {
    fac[0] = 1;
    for (int i = 1; i < N; i++) fac[i] = (ll)fac[i - 1] * i % P;
    inv[N - 1] = power(fac[N - 1], P - 2);
    for (int i = N - 1; i; i--) inv[i - 1] = (ll)inv[i] * i % P;
}

void solve() {
    int n, m;
    cin >> n >> m;
    int k = (n + 1) / 2, h = (m + 1) / 2, s = k * h, t = n * m - s;
    ll ans = (ll)fac[s] * fac[t] % P * inv[k] % P * inv[n - k] % P;
    ans = ans * power((ll)inv[h] * inv[m - h] % P, k) % P;
    ans = ans * power(inv[m], n - k) % P;
    cout << t + 1 << ' ' << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("median.in", "r", stdin);
    freopen("median.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    init();
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
