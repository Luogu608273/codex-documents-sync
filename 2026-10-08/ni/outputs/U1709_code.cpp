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
    for (int i = 0; i < n; ++i) pre[i+1] = pre[i] + a[i];
    int r = ((2-n)%3+3)%3;
    vector<long long> b;
    for (int p = r; p+3 <= n; p += 3) b.push_back(pre[p+3]-pre[p]);
    while (q--) {
        long long k; cin >> k;
        int lo = 0, hi = b.size();
        while (lo < hi) {
            int mid = (lo+hi)/2;
            if (b[mid] >= k) lo = mid+1;
            else hi = mid;
        }
        int p = r+3*lo;
        cout << 2*pre[p]-pre[n]+(long long)(n+1-2*p)/3*k << '\n';
    }
}
