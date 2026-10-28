#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

// O(n^3) 时间上界、O(n^2) 空间；适用于 n<=500。
const int N = 505;
int k, n, a[26][26], st[N], top;
bool ok[N][N];
string s, f[N];

void solve() {
    cin >> k >> n;
    for (int i = 0; i < k; i++) {
        string t;
        cin >> t;
        for (int j = 0; j < k; j++) a[i][j] = t[j] - '0';
    }
    cin >> s;
    for (int r = 1; r <= n; r++) {
        top = 0;
        for (int l = r; l >= 1; l--) {
            while (top && a[s[l - 1] - 'a'][s[st[top] - 1] - 'a']) top--;
            st[++top] = l;
            ok[l][r] = top == 1;
        }
    }
    for (int i = n; i >= 1; i--) {
        string t = f[i + 1];
        for (int j = i + 1; j <= n; j++)
            if (ok[i][j] && f[j + 1] < t) t = f[j + 1];
        f[i] = s[i - 1] + t;
    }
    cout << f[1] << endl;
}

int main() {
#ifndef LOCAL
    freopen("crystal.in", "r", stdin);
    freopen("crystal.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
