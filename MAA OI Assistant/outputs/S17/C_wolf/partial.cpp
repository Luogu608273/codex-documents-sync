#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

// O(n^2) 时间、O(n) 空间；目标 n <= 5000。
const int N = 5005, P = 998244353;
int n, b[N], f[N], a[N];
string s;

void solve() {
    cin >> n >> s;
    for (int i = 1; i <= n; i++) cin >> b[i];
    int ans = 0;
    for (int q = 0; q <= (n + 1) / 2; q++) {
        for (int i = 1; i <= n; i++) a[i] = s[i - 1] == 'L' ? b[i] : q - b[i];
        f[1] = a[1] == 0;
        f[2] = (a[2] == 1) + (a[2] == a[1]) * f[1];
        for (int i = 3; i <= n; i++)
            f[i] = ((a[i] == a[i - 1]) * f[i - 1] + (a[i] == a[i - 2] + 1) * f[i - 2]) % P;
        if (a[n] == q) ans = (ans + f[n]) % P;
        if (a[n - 1] == q - 1) ans = (ans + f[n - 1]) % P;
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("wolf.in", "r", stdin);
    freopen("wolf.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
