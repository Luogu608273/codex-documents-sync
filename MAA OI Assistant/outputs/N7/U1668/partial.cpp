// 适用：n <= 2000（测试点 1~5）。O(n^2+q) 时间，O(n^2) 空间。
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 2005;
int n, q, a[N], f[N][N];

void solve() {
    int c;
    cin >> c >> n >> q;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int l = n; l; l--) {
        int cnt[4] = {};
        for (int r = l; r <= n; r++) {
            cnt[a[r]]++;
            f[l][r] = max(f[l + 1][r], f[l][r - 1]);
            if (cnt[1] != cnt[2] && cnt[1] != cnt[3] && cnt[2] != cnt[3])
                f[l][r] = r - l + 1;
        }
    }
    while (q--) {
        int l, r;
        cin >> l >> r;
        cout << f[l][r] << endl;
    }
}

int main() {
#ifndef LOCAL
    freopen("three.in", "r", stdin);
    freopen("three.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
