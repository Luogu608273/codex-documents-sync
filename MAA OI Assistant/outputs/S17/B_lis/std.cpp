#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 1000005;
int n, t[N], f[N], len;

void solve() {
    cin >> n;
    for (int i = 1; i <= n; i++) {
        int x;
        cin >> x;
        int p = lower_bound(t + 1, t + len + 1, x) - t;
        t[p] = x;
        len = max(len, p);
        f[x] = p;
    }
    for (int i = 1; i <= n; i++) {
        f[i] = max(f[i], f[i - 1]);
        cout << f[i] << (i == n ? '\n' : ' ');
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
