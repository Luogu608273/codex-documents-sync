#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 500005, L = 19, P = 1000000007, Q = 1000000009, B = 911382323;
int n, k, a[26][26], st[N], top, h[N], to[N], nx[N], ec;
int f[L][N], len[N], u[L][N], v[L][N], pw[L], qw[L];
string s;

void add(int x, int y) {
    to[++ec] = y;
    nx[ec] = h[x];
    h[x] = ec;
}

int cmp(int x, int y) {
    int a = x, b = y;
    for (int j = L - 1; j >= 0; j--) {
        if (len[x] >= (1 << j) && len[y] >= (1 << j) && u[j][x] == u[j][y] && v[j][x] == v[j][y]) {
            x = f[j][x];
            y = f[j][y];
        }
    }
    if (!len[x]) return a;
    if (!len[y]) return b;
    return s[x - 1] < s[y - 1] ? a : b;
}

void solve() {
    cin >> k >> n;
    for (int i = 0; i < k; i++) {
        string t;
        cin >> t;
        for (int j = 0; j < k; j++) a[i][j] = t[j] - '0';
    }
    cin >> s;
    for (int i = n; i >= 1; i--) {
        while (top && a[s[i - 1] - 'a'][s[st[top] - 1] - 'a']) add(i, st[top--]);
        st[++top] = i;
    }
    pw[0] = qw[0] = B;
    for (int j = 1; j < L; j++) {
        pw[j] = (ll)pw[j - 1] * pw[j - 1] % P;
        qw[j] = (ll)qw[j - 1] * qw[j - 1] % Q;
    }
    for (int j = 0; j < L; j++) f[j][n + 1] = n + 1;
    for (int i = n; i >= 1; i--) {
        int x = i + 1;
        for (int j = h[i]; j; j = nx[j]) x = cmp(x, f[0][to[j]]);
        f[0][i] = x;
        len[i] = len[x] + 1;
        u[0][i] = v[0][i] = s[i - 1] - 'a' + 1;
        for (int j = 1; j < L; j++) {
            int x = f[j - 1][i];
            f[j][i] = f[j - 1][x];
            u[j][i] = ((ll)u[j - 1][i] * pw[j - 1] + u[j - 1][x]) % P;
            v[j][i] = ((ll)v[j - 1][i] * qw[j - 1] + v[j - 1][x]) % Q;
        }
    }
    for (int i = 1; i <= n; i = f[0][i]) cout << s[i - 1];
    cout << endl;
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
