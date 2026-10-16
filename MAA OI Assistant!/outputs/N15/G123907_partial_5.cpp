#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

void solve() {
    string s;
    cin >> s;
    int cnt = 0, ans = 0;
    for (char x : s) {
        if (x == 'A') ++cnt;
        else if (x == 'B' && cnt) --cnt, ++ans;
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("erase.in", "r", stdin);
    freopen("erase.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _ = 1;
    while (_--) solve();
    return 0;
}
