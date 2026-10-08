#include <bits/stdc++.h>
using namespace std;
int main() {
    freopen("watch.in", "r", stdin);
    freopen("watch.out", "w", stdout);
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n; long long L, R; cin >> n >> L >> R;
    vector<long long> a(n);
    for (auto &x : a) cin >> x;
    vector<int> l, r;
    for (int i = 0; i < n; ++i) {
        if (!i || a[i] - a[i-1] >= L) l.push_back(i), r.push_back(i);
        else r.back() = i;
    }
    int m = l.size(), p = 0, ans = n;
    vector<int> dp(m, n+1);
    for (int j = 0; j < m; ++j) {
        while (p < n && a[p] < a[l[j]] - R) ++p;
        int best = !p ? 0 : n+1;
        for (int i = 0; i < j; ++i)
            if (!p || a[r[i]] >= a[p-1] - R) best = min(best, dp[i]);
        dp[j] = best + r[j] - l[j] + 1;
        if (a[r[j]] >= a.back() - R) ans = min(ans, dp[j]);
    }
    cout << ans << '\n';
}
