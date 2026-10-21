#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

// 仅适用于 K=0；O(n^2)，对应 N<=5000、K=0 的子任务。
const int N = 5005;
int n, a[N];
ll k;

void solve() {
    cin >> n >> k;
    for (int i = 1; i <= n; i++) cin >> a[i];
    int ans = 0;
    for (int i = 1; i <= n; i++) {
        int s = 0;
        for (int j = i + 1; j <= n; j++) s += a[j] < a[i];
        ans = max(ans, s);
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("tramcar.in", "r", stdin);
    freopen("tramcar.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
