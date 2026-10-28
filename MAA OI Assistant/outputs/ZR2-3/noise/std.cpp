#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 500005, K = 19;
int n, a[N], b[N], sa[N], x[N], y[N], c[N * 2], lg[N];

struct LCE {
    int rk[N], f[K][N];
    void build() {
        int m = n * 2 + 1;
        fill(c, c + m + 1, 0);
        for (int i = 1; i <= n; i++) c[x[i] = b[i] + n + 1]++;
        for (int i = 1; i <= m; i++) c[i] += c[i - 1];
        for (int i = n; i; i--) sa[c[x[i]]--] = i;
        for (int k = 1, p = 0; k < n; k <<= 1) {
            p = 0;
            for (int i = n - k + 1; i <= n; i++) y[++p] = i;
            for (int i = 1; i <= n; i++) if (sa[i] > k) y[++p] = sa[i] - k;
            fill(c, c + m + 1, 0);
            for (int i = 1; i <= n; i++) c[x[y[i]]]++;
            for (int i = 1; i <= m; i++) c[i] += c[i - 1];
            for (int i = n; i; i--) sa[c[x[y[i]]]--] = y[i];
            copy(x + 1, x + n + 1, y + 1);
            p = 1;
            x[sa[1]] = 1;
            for (int i = 2; i <= n; i++) {
                int u = sa[i], v = sa[i - 1];
                if (y[u] != y[v] || (u + k <= n ? y[u + k] : 0) != (v + k <= n ? y[v + k] : 0)) p++;
                x[u] = p;
            }
            if (p == n) break;
            m = p;
        }
        for (int i = 1; i <= n; i++) rk[sa[i]] = i;
        for (int i = 1, k = 0; i <= n; i++) {
            if (rk[i] == 1) {
                f[0][1] = 0;
                k = 0;
                continue;
            }
            int j = sa[rk[i] - 1];
            while (i + k <= n && j + k <= n && b[i + k] == b[j + k]) k++;
            f[0][rk[i]] = k;
            if (k) k--;
        }
        for (int j = 1; (1 << j) <= n; j++)
            for (int i = 1; i + (1 << j) - 1 <= n; i++)
                f[j][i] = min(f[j - 1][i], f[j - 1][i + (1 << (j - 1))]);
    }
    int query(int p, int q) {
        if (p == q) return n - p + 1;
        int l = rk[p], r = rk[q];
        if (l > r) swap(l, r);
        l++;
        int k = lg[r - l + 1];
        return min(f[k][l], f[k][r - (1 << k) + 1]);
    }
} s, t;

int right(int p, int q) {
    if (a[p] != -a[q]) return 0;
    return min(n - q + 1, 1 + s.query(p, q));
}

int left(int p, int q) {
    if (!p || a[p] != -a[q]) return 0;
    return min(p, 1 + t.query(n - p + 1, n - q + 1));
}

void solve() {
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    lg[1] = 0;
    for (int i = 2; i <= n; i++) lg[i] = lg[i >> 1] + 1;
    // b[i] is unchanged if every value in a is negated.
    for (int i = 1; i < n; i++) b[i] = a[i] > 0 ? a[i + 1] : -a[i + 1];
    b[n] = 0;
    s.build();
    for (int i = 1; i < n; i++) {
        int p = n - i + 1;
        b[i] = a[p] > 0 ? a[p - 1] : -a[p - 1];
    }
    b[n] = 0;
    t.build();
    ll ans = 0;
    for (int m = 1; m * 2 <= n; m++) {
        for (int i = 1; i + m <= n; i += m) {
            int r = min(m, right(i, i + m));
            if (!r) continue;
            int l = min(m - 1, left(i - 1, i + m - 1));
            if (l + r >= m) ans += l + r - m + 1;
        }
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("noise.in", "r", stdin);
    freopen("noise.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
