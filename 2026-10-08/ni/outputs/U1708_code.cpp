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
    vector<int> dp(m);
    deque<int> q;
    for (int j = 0; j < m; ++j) {
        while (p < n && a[p] < a[l[j]] - R) ++p;
        if (p) {
            long long bound = a[p-1] - R;
            while (!q.empty() && a[r[q.front()]] < bound) q.pop_front();
        }
        int best = !p ? 0 : dp[q.front()];
        dp[j] = best + r[j] - l[j] + 1;
        if (a[r[j]] >= a.back() - R) ans = min(ans, dp[j]);
        while (!q.empty() && dp[q.back()] >= dp[j]) q.pop_back();
        q.push_back(j);
    }
    cout << ans << '\n';
}
