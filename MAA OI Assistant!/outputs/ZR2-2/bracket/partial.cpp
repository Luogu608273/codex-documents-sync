#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

// 部分分：所有字符串总长度不超过 1000，对应子任务 1。
int calc(const string &s) {
    int res = 0, d = 0;
    for (char ch : s) {
        int x = ch - '0';
        res += abs(x - d);
        d = x;
    }
    return res + d;
}

void solve() {
    string s, ans;
    cin >> s;
    int n = s.size(), mn = calc(s), p = -1, v = 0;
    for (int i = 0; i < n; i++) {
        char old = s[i];
        for (int x = 0; x <= 9; x++) {
            s[i] = char('0' + x);
            int res = calc(s);
            if (res < mn) mn = res, p = i, v = x;
        }
        s[i] = old;
    }
    if (p != -1) s[p] = char('0' + v);
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
