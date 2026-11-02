#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 13, M = 1 << 11;
int n, m, tot, a[N], s[M], b[M], res[N], ans[N][N];

bool check() {
    for (int i = 1; i <= tot; i++) {
        int t = b[i], vis = 0;
        while (t) {
            int p = t & -t;
            int c = 1 << (a[__builtin_ctz(p) + 1] - 1);
            if (vis & c) break;
            vis |= c;
            t ^= p;
        }
        if (!t) return false;
    }
    return true;
}

void dfs(int x, int k) {
    if (k + m - x + 1 <= res[n]) return;
    if (x > m) {
        if (!check()) return;
        res[n] = k;
        for (int i = 1; i < n; i++) ans[n][i] = a[i];
        return;
    }
    for (int i = k + 1; i >= 1; i--) {
        a[x] = a[n - x] = i;
        dfs(x + 1, max(k, i));
    }
}

void init() {
    m = n / 2;
    tot = 0;
    res[n] = 1;
    for (int i = 1; i < n; i++) ans[n][i] = 1;
    s[0] = 0;
    for (int i = 1; i < (1 << (n - 1)); i++) {
        int p = i & -i;
        s[i] = (s[i ^ p] + __builtin_ctz(p) + 1) % n;
        if (!s[i]) b[++tot] = i;
    }
}

void solve() {
    cin >> n;
    if (n > 12) {
        cout << 1 << endl;
        for (int i = 1; i < n; i++) cout << 1 << " \n"[i == n - 1];
        return;
    }
    if (!res[n]) {
        init();
        dfs(1, 0);
    }
    cout << res[n] << endl;
    for (int i = 1; i < n; i++) cout << ans[n][i] << " \n"[i == n - 1];
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
