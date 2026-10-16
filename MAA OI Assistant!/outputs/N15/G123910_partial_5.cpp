#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 200005;
const ll V = -4000000000000000000ll;
int n, m;
ll a[N], b[N], p[N], q[N], mx[N << 2];

void build(int u, int l, int r) {
    if (l == r) {
        mx[u] = q[l];
        return;
    }
    int mid = (l + r) >> 1;
    build(u << 1, l, mid);
    build(u << 1 | 1, mid + 1, r);
    mx[u] = max(mx[u << 1], mx[u << 1 | 1]);
}

ll query(int u, int l, int r, int x, int y) {
    if (x <= l && r <= y) return mx[u];
    int mid = (l + r) >> 1;
    ll res = V;
    if (x <= mid) res = max(res, query(u << 1, l, mid, x, y));
    if (y > mid) res = max(res, query(u << 1 | 1, mid + 1, r, x, y));
    return res;
}

void solve() {
    cin >> n >> m;
    ll d, t;
    for (int i = 1; i <= n; ++i) {
        cin >> a[i] >> d >> p[i];
        a[i] += a[i - 1];
        p[i] += p[i - 1];
    }
    for (int j = 1; j <= m; ++j) {
        cin >> b[j] >> t >> q[j];
        b[j] += b[j - 1];
        q[j] += q[j - 1];
    }
    build(1, 0, m);
    ll ans = V;
    for (int i = 0; i <= n; ++i) {
        if (a[i] > d) break;
        int r = upper_bound(b, b + m + 1, d - a[i]) - b - 1;
        if (r < m || i == n) ans = max(ans, p[i] + q[r]);
        if (i < n) {
            int l = upper_bound(b, b + m + 1, d - a[i + 1]) - b;
            if (l <= r) ans = max(ans, p[i] + query(1, 0, m, l, r));
        }
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("cookoff.in", "r", stdin);
    freopen("cookoff.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _ = 1;
    while (_--) solve();
    return 0;
}
