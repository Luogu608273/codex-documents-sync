#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 1000005;
int n, q, f[26][N];
char s[N];

void solve() {
    cin >> n >> q >> (s + 1);
    for (int c = 0; c < 26; c++)
        for (int i = 1; i <= n; i++)
            f[c][i] = f[c][i - 1] + (s[i] - 'a' == c);
    while (q--) {
        int l, r, ans = 0;
        cin >> l >> r;
        for (int c = 0; c < 26; c++) ans = max(ans, f[c][r] - f[c][l - 1]);
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
