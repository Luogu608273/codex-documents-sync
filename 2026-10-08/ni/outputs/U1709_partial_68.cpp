#include <bits/stdc++.h>
using namespace std;
int main() {
    freopen("merge.in", "r", stdin);
    freopen("merge.out", "w", stdout);
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, q; cin >> n >> q;
    vector<long long> a(n), pre(n+1);
    for (auto &x : a) cin >> x;
    sort(a.begin(), a.end(), greater<long long>());
    for (int i = 0; i < n; ++i) pre[i+1] = pre[i]+a[i];
    int r = ((2-n)%3+3)%3;
    bool same = a.front() == a.back();
    while (q--) {
        long long k; cin >> k;
        long long ans = LLONG_MIN;
        if (same) {
            int p = 3*a[0] >= k ? r+3*((n-r)/3) : r;
            ans = 2*pre[p]-pre[n]+(long long)(n+1-2*p)/3*k;
        } else for (int p = r; p <= n; p += 3)
            ans = max(ans, 2*pre[p]-pre[n]+(long long)(n+1-2*p)/3*k);
        cout << ans << '\n';
    }
}
