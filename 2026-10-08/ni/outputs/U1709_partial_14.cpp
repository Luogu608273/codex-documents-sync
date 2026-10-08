#include <bits/stdc++.h>
using namespace std;
int main() {
    freopen("merge.in", "r", stdin);
    freopen("merge.out", "w", stdout);
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, q; cin >> n >> q;
    vector<long long> a(n); for (auto &x : a) cin >> x;
    int all = 1 << n;
    vector<long long> low(all), high(all);
    while (q--) {
        long long k; cin >> k;
        for (int s = 1; s < all; ++s) {
            if (!(s & (s-1))) {
                low[s] = high[s] = a[__builtin_ctz((unsigned)s)];
                continue;
            }
            low[s] = LLONG_MAX; high[s] = LLONG_MIN;
            for (int t = (s-1)&s; t; t = (t-1)&s) {
                int u = s^t;
                if (t > u) continue;
                low[s] = min(low[s], k-high[t]-high[u]);
                high[s] = max(high[s], k-low[t]-low[u]);
            }
        }
        cout << high[all-1] << '\n';
    }
}
