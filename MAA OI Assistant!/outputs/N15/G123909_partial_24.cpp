#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 1005, K = 25, P = 1000000007;
int n, k, q, a[N], f[K], ans[N][N];

void solve() {
    cin >> n >> k;
    for (int i = 1; i <= n; ++i) cin >> a[i];
    for (int l = 1; l <= n; ++l) {
        fill(f, f + k + 1, 0);
        int res = 1;
        for (int r = l; r <= n; ++r) {
            int s = 1;
            for (int i = 1; i <= a[r]; ++i) (s += f[i]) >= P ? s -= P : 0;
            (f[a[r]] += s) >= P ? f[a[r]] -= P : 0;
            (res += s) >= P ? res -= P : 0;
            ans[l][r] = res;
        }
    }
    cin >> q;
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << ans[l][r] << endl;
    }
}

int main() {
#ifndef LOCAL
    freopen("subseq.in", "r", stdin);
    freopen("subseq.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _ = 1;
    while (_--) solve();
    return 0;
}
