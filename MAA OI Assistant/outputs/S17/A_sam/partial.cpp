#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

// 逐询问扫描：适用于 n,q <= 5000，或所有询问长度之和 <= 2e6。
void solve() {
    int n, q;
    string s;
    cin >> n >> q >> s;
    while (q--) {
        int l, r, c[26] = {}, ans = 0;
        cin >> l >> r;
        for (int i = l - 1; i < r; i++) ans = max(ans, ++c[s[i] - 'a']);
        cout << ans << endl;
    }
}

int main() {
#ifndef LOCAL
    freopen("sam.in", "r", stdin);
    freopen("sam.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
