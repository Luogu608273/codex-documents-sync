// 适用：n,m <= 4（测试点 1）。枚举无序等大集合划分。
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int P = 998244353;
int n, m, a[5][5], cnt[5], med[5], best, ans;

void dfs(int x, int k) {
    if (x > n * m) {
        for (int i = 1; i <= n; i++) med[i] = a[i][m / 2 + 1];
        sort(med + 1, med + n + 1);
        int z = med[n / 2 + 1];
        if (z > best) best = z, ans = 0;
        if (z == best && ++ans == P) ans = 0;
        return;
    }
    for (int i = 1; i <= k; i++) {
        if (cnt[i] == m) continue;
        a[i][++cnt[i]] = x;
        dfs(x + 1, k);
        cnt[i]--;
    }
    if (k < n) {
        a[k + 1][cnt[k + 1] = 1] = x;
        dfs(x + 1, k + 1);
        cnt[k + 1] = 0;
    }
}

void solve() {
    cin >> n >> m;
    best = ans = 0;
    dfs(1, 0);
    cout << best << ' ' << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("median.in", "r", stdin);
    freopen("median.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
