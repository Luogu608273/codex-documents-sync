#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

int get(char c) {
    if (c == 'R') return 1;
    if (c == 'Y') return 2;
    if (c == 'B') return 4;
    if (c == 'O') return 3;
    if (c == 'P') return 5;
    if (c == 'G') return 6;
    if (c == 'A') return 7;
    return 0;
}

void solve() {
    int n, pre = 0, ans = 0;
    string s;
    cin >> n >> s;
    for (char c : s) {
        int x = get(c);
        ans += __builtin_popcount((unsigned)(x & ~pre));
        pre = x;
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("color.in", "r", stdin);
    freopen("color.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
