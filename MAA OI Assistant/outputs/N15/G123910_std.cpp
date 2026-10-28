#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 1000005;
const ll V = -4000000000000000000ll;
int n, m, h[N], nxt[N], pos[N];
ll a[N], b[N], s[N], p[N], q[N], mx[N << 2], tag[N << 2], sum[N << 2];

void cover(int u, ll x) {
    mx[u] = tag[u] = x;
    sum[u] = 0;
}

void add(int u, ll x) {
    mx[u] += x;
    if (tag[u] != V) tag[u] += x;
    else sum[u] += x;
}

void pushdown(int u) {
    if (tag[u] != V) {
        cover(u << 1, tag[u]);
        cover(u << 1 | 1, tag[u]);
        tag[u] = V;
    }
    if (sum[u]) {
        add(u << 1, sum[u]);
        add(u << 1 | 1, sum[u]);
        sum[u] = 0;
    }
}

void modify(int u, int l, int r, int x, int y, ll z, bool op) {
    if (x <= l && r <= y) {
        if (op) add(u, z);
        else cover(u, z);
        return;
    }
    pushdown(u);
    int mid = (l + r) >> 1;
    if (x <= mid) modify(u << 1, l, mid, x, y, z, op);
    if (y > mid) modify(u << 1 | 1, mid + 1, r, x, y, z, op);
    mx[u] = max(mx[u << 1], mx[u << 1 | 1]);
}

ll query(int u, int l, int r, int x) {
    if (l == r) return mx[u];
    pushdown(u);
    int mid = (l + r) >> 1;
    if (x <= mid) return query(u << 1, l, mid, x);
    return query(u << 1 | 1, mid + 1, r, x);
}

int find(int u, int l, int r, int x, int y, ll z) {
    if (r < x || l > y || mx[u] < z) return m + 1;
    if (l == r) return l;
    pushdown(u);
    int mid = (l + r) >> 1;
    int res = find(u << 1, l, mid, x, y, z);
    if (res <= m) return res;
    return find(u << 1 | 1, mid + 1, r, x, y, z);
}

void solve() {
    cin >> n >> m;
    for (int i = 1; i <= n; ++i) {
        cin >> a[i] >> s[i] >> p[i];
        a[i] += a[i - 1];
    }
    ll ans = 0;
    for (int j = 1; j <= m; ++j) {
        ll t;
        cin >> b[j] >> t >> q[j];
        b[j] += b[j - 1];
        int x = upper_bound(a, a + n + 1, t - b[j]) - a - 1;
        if (x == n) ans += q[j];
        else if (x >= 0 && q[j]) nxt[j] = h[x + 1], h[x + 1] = j;
    }
    for (int i = 1; i <= n; ++i) {
        int cnt = 0;
        int x = upper_bound(b, b + m + 1, s[i] - a[i]) - b - 1;
        if (x >= 0 && p[i]) {
            modify(1, 0, m, 0, x, p[i], true);
            if (x < m) pos[++cnt] = x + 1;
        }
        for (int j = h[i]; j; j = nxt[j]) {
            modify(1, 0, m, j, m, q[j], true);
            pos[++cnt] = j;
        }
        if (!cnt) continue;
        sort(pos + 1, pos + cnt + 1);
        cnt = unique(pos + 1, pos + cnt + 1) - pos - 1;
        pos[cnt + 1] = m + 1;
        ll res = query(1, 0, m, pos[1] - 1);
        for (int j = 1; j <= cnt; ++j) {
            int l = pos[j], r = pos[j + 1] - 1;
            int t = find(1, 0, m, l, r, res);
            if (t > l) modify(1, 0, m, l, min(r, t - 1), res, false);
            res = query(1, 0, m, r);
        }
    }
    cout << ans + query(1, 0, m, m) << endl;
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
