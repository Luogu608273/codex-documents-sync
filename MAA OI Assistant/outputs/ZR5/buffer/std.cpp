#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 6005, V = 1000000000;
int n, f[N], h[N];
unsigned short a[N][N], b[N][N];
char s[N], t[N];

void init() {
    for (int i = n; i >= 1; i--) {
        for (int j = n; j >= 1; j--)
            if (s[i] == t[j]) a[i][j] = a[i + 1][j + 1] + 1;
        for (int j = 1; j <= n; j++)
            if (s[i] == t[j]) b[i][j] = b[i + 1][j - 1] + 1;
    }
    fill(f + 1, f + n + 1, V);
}

void solve() {
    cin >> n >> (s + 1) >> (t + 1);
    init();
    for (int l = 1; l <= n; l++) {
        if (f[l - 1] == V) continue;
        if (s[l] == t[l]) f[l] = min(f[l], f[l - 1]);
        h[l - 1] = 0;
        for (int m = l; m <= n; m++)
            h[m] = max(h[m - 1], m + (int)a[m + 1][l]);
        for (int r = l; r <= n; r++) {
            int k = min(r, l + (int)b[l][r] - 1);
            if (k >= l && h[k] >= r) f[r] = min(f[r], f[l - 1] + 1);
        }
    }
    cout << (f[n] == V ? -1 : f[n]) << endl;
}

int main() {
#ifndef LOCAL
    freopen("buffer.in", "r", stdin);
    freopen("buffer.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
