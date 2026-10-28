#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 2005;
int a[N];

// Supports N <= 2000: all half-lengths, consecutive matching runs.
void solve() {
    int n;
    cin >> n;
    if (n > 2000) exit(1);
    for (int i = 1; i <= n; i++) cin >> a[i];
    ll ans = 0;
    for (int m = 1; m * 2 <= n; m++) {
        int cnt = 0;
        for (int i = 1; i + m <= n; i++) {
            if (a[i] == -a[i + m]) cnt++;
            else cnt = 0;
            if (cnt >= m) ans++;
        }
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("noise.in", "r", stdin);
    freopen("noise.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
