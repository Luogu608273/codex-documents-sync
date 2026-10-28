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

const int N = 1005;
int a[N], f[N];

// Only the N <= 1000 subtask is supported.
void solve() {
    int n, ans = 0;
    string s;
    cin >> n >> s;
    if (n > 1000) exit(1);
    for (int i = 1; i <= n; i++) a[i] = get(s[i - 1]);
    for (int b = 1; b <= 4; b <<= 1) {
        f[0] = 0;
        for (int i = 1; i <= n; i++) {
            if (!(a[i] & b)) {
                f[i] = f[i - 1];
                continue;
            }
            f[i] = n + 1;
            for (int j = i; j >= 1 && (a[j] & b); j--)
                f[i] = min(f[i], f[j - 1] + 1);
        }
        ans += f[n];
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
