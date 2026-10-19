#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
using i128 = __int128;

const int N = 500005, P = 998244353, M = 1 << 19;
int n, q, h[N], e[N * 2], ne[N * 2], tot;
int fa[N], ord[N], l[N], r[N], sz[N], in[N], st[N];
int g[N], out[N], pre[N], ans[N];
ll a[N], f[N], up[N];
int rt[N], lc[N], rc[N], dis[N], bs[N], dsu[N], ev[N], ze[N];
ll sum[N], lim[N];
int seg[M * 2], zc[M * 2], tag[M * 2], touched[M * 2], cnt, tim;
struct Query {
    ll x;
    int u, id;
} b[N];

void add(int u, int v) {
    e[++tot] = v;
    ne[tot] = h[u];
    h[u] = tot;
}

ll qpow(ll a, int b) {
    ll res = 1;
    for (; b; b >>= 1, a = a * a % P)
        if (b & 1) res = res * a % P;
    return res;
}

int factor(ll x, int c) {
    if (x > 0) return c;
    if (x < 0) return 1;
    return c + 1 == P ? 0 : c + 1;
}

void init() {
    int t = 1;
    ord[1] = 1;
    for (int i = 1; i <= n; i++) {
        int u = ord[i];
        l[u] = t + 1;
        for (int j = h[u]; j; j = ne[j]) {
            int v = e[j];
            if (v == fa[u]) continue;
            fa[v] = u;
            ord[++t] = v;
        }
        r[u] = t;
    }
    for (int i = n; i; i--) {
        int u = ord[i];
        sz[u] = 1;
        f[u] = a[u];
        g[u] = 1;
        for (int j = l[u]; j <= r[u]; j++) {
            int v = ord[j];
            sz[u] += sz[v];
            f[u] += max(0LL, f[v]);
            g[u] = (ll)g[u] * factor(f[v], g[v]) % P;
        }
    }
    out[1] = 1;
    for (int i = 1; i <= n; i++) {
        int u = ord[i];
        ll val = f[u] + max(0LL, up[u]);
        int cur = out[u];
        for (int j = l[u]; j <= r[u]; j++) {
            int v = ord[j];
            pre[v] = cur;
            cur = (ll)cur * factor(f[v], g[v]) % P;
        }
        cur = 1;
        for (int j = r[u]; j >= l[u]; j--) {
            int v = ord[j];
            up[v] = val - max(0LL, f[v]);
            int c = (ll)pre[v] * cur % P;
            out[v] = factor(up[v], c);
            cur = (ll)cur * factor(f[v], g[v]) % P;
        }
    }
    int top = 1, clock = 0;
    st[1] = 1;
    while (top) {
        int u = st[top--];
        in[u] = ++clock;
        for (int j = l[u]; j <= r[u]; j++) st[++top] = ord[j];
    }
}

bool lesskey(int u, int v) {
    return (i128)sum[u] * bs[v] > (i128)sum[v] * bs[u];
}

int merge(int u, int v) {
    if (!u || !v) return u + v;
    if (lesskey(v, u)) swap(u, v);
    rc[u] = merge(rc[u], v);
    if (dis[lc[u]] < dis[rc[u]]) swap(lc[u], rc[u]);
    dis[u] = dis[rc[u]] + 1;
    return u;
}

void build() {
    for (int i = n; i; i--) {
        int u = ord[i], t = 0;
        for (int j = l[u]; j <= r[u]; j++) t = merge(t, rt[ord[j]]);
        sum[u] = a[u];
        bs[u] = 1;
        while (t && lesskey(t, u)) {
            sum[u] += sum[t];
            bs[u] += bs[t];
            t = merge(lc[t], rc[t]);
        }
        lc[u] = t;
        dis[u] = 1;
        rt[u] = u;
        ll num = -sum[u];
        lim[u] = num / bs[u];
        if (num < 0 && num % bs[u]) lim[u]--;
        dsu[u] = ev[u] = u;
    }
}

int find(int u) {
    int r = u;
    while (dsu[r] != r) r = dsu[r];
    while (u != r) {
        int v = dsu[u];
        dsu[u] = r;
        u = v;
    }
    return r;
}

void modify(int p, int v, int z) {
    p += M - 1;
    seg[p] = (ll)seg[p] * v % P;
    zc[p] += z;
    while (p) {
        if (tag[p] != tim) {
            tag[p] = tim;
            touched[++cnt] = p;
        }
        p >>= 1;
        if (p) {
            seg[p] = (ll)seg[p * 2] * seg[p * 2 + 1] % P;
            zc[p] = zc[p * 2] + zc[p * 2 + 1];
        }
    }
}

int query(int u) {
    int l = in[u] + M - 1, r = in[u] + sz[u] + M - 2;
    ll res = 1;
    int z = 0;
    while (l <= r) {
        if (l & 1) res = res * seg[l] % P, z += zc[l++];
        if (!(r & 1)) res = res * seg[r] % P, z += zc[r--];
        l >>= 1;
        r >>= 1;
    }
    return z ? 0 : res;
}

void update(int u, int c) {
    int p = fa[u];
    if (!p || c == 1) return;
    int t = fa[find(p)];
    if (c) {
        modify(in[p], c, 0);
        if (t) modify(in[t], qpow(c, P - 2), 0);
    } else {
        modify(in[p], 1, 1);
        if (t) modify(in[t], 1, -1);
    }
}

bool cmp(int u, int v) {
    if (lim[u] != lim[v]) return lim[u] < lim[v];
    return in[u] > in[v];
}

bool cmpq(Query a, Query b) {
    return a.x < b.x;
}

void solve() {
    cin >> n >> q;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i < n; i++) {
        int u, v;
        cin >> u >> v;
        add(u, v);
        add(v, u);
    }
    for (int i = 1; i <= q; i++) cin >> b[i].u >> b[i].x, b[i].id = i;
    init();
    build();
    sort(ev + 1, ev + n + 1, cmp);
    int nz = 0;
    for (int i = 1; i <= n; i++)
        if (sum[ev[i]] % bs[ev[i]] == 0) ze[++nz] = ev[i];
    sort(b + 1, b + q + 1, cmpq);
    fill(seg, seg + M * 2, 1);
    int p = 1, z = 1;
    for (int i = 1; i <= q;) {
        int j = i;
        ll x = b[i].x;
        while (j <= q && b[j].x == x) j++;
        while (p <= n && lim[ev[p]] < x) {
            int u = ev[p++];
            dsu[u] = find(fa[u]);
        }
        while (z <= nz && lim[ze[z]] < x) z++;
        tim++;
        while (z <= nz && lim[ze[z]] == x) {
            int u = ze[z++], c = query(u) + 1;
            if (c == P) c = 0;
            update(u, c);
        }
        for (int k = i; k < j; k++)
            ans[b[k].id] = (ll)out[b[k].u] * query(b[k].u) % P;
        while (cnt) {
            int u = touched[cnt--];
            seg[u] = 1;
            zc[u] = 0;
        }
        i = j;
    }
    for (int i = 1; i <= q; i++) cout << ans[i] << endl;
}

int main() {
#ifndef LOCAL
    freopen("subsidy.in", "r", stdin);
    freopen("subsidy.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
