#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

void solve() {
    string s, ans;
    cin >> s;
    int n = s.size(), mx = 0, p = -1, v = 0;
    for (int i = 0; i < n; i++) {
        int l = i ? s[i - 1] - '0' : 0;
        int r = i + 1 < n ? s[i + 1] - '0' : 0;
        int x = s[i] - '0';
        int d = abs(x - l) + abs(x - r) - abs(l - r);
        if (d > mx) mx = d, p = i, v = l;
    }
    if (p != -1) s[p] = char('0' + v);
    ans.reserve(10 * n + 20);
    int d = 0;
    for (char ch : s) {
        int x = ch - '0';
        if (x > d) ans.append(x - d, '(');
        else ans.append(d - x, ')');
        ans += ch;
        d = x;
    }
    ans.append(d, ')');
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("bracket.in", "r", stdin);
    freopen("bracket.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
