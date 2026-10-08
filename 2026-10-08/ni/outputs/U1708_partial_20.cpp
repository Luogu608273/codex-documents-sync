#include <bits/stdc++.h>
using namespace std;
int main() {
    freopen("watch.in", "r", stdin);
    freopen("watch.out", "w", stdout);
    int n; long long L, R; cin >> n >> L >> R;
    vector<long long> a(n); for (auto &x : a) cin >> x;
    int ans = n;
    for (int s = 1; s < (1 << n); ++s) {
        int cnt = __builtin_popcount((unsigned)s);
        if (cnt >= ans) continue;
        bool ok = true;
        for (int i = 0; i < n && ok; ++i) if (!(s >> i & 1)) {
            long long d = LLONG_MAX;
            for (int j = 0; j < n; ++j) if (s >> j & 1)
                d = min(d, abs(a[i]-a[j]));
            if (d < L || d > R) ok = false;
        }
        if (ok) ans = cnt;
    }
    cout << ans << '\n';
}
