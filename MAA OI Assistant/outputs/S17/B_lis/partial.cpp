#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

// O(n^2)，适用于 n <= 5000。
const int N = 5005;
int n, a[N], f[N], ans[N];

void solve() {
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        f[i] = 1;
        for (int j = 1; j < i; j++)
            if (a[j] < a[i]) f[i] = max(f[i], f[j] + 1);
        ans[a[i]] = f[i];
    }
    for (int i = 1; i <= n; i++) {
        ans[i] = max(ans[i], ans[i - 1]);
        cout << ans[i] << (i == n ? '\n' : ' ');
    }
}

int main() {
#ifndef LOCAL
    freopen("lis.in", "r", stdin);
    freopen("lis.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
