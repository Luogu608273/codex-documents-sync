// 子任务 1--5：57 分。一般情况 O(nq)，x=0 询问 O(1)，星形树询问 O(log n)。
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 500005, P = 998244353;
int n, q, h[N], e[N * 2], ne[N * 2], tot;
int fa[N], ord[N], l[N], r[N], sz[N], in[N], st[N], df[N];
int g[N], out[N], pre[N], gp[N], pw[N];
ll a[N], f[N], up[N], fp[N], leaf[N];

void add(int u, int v) {
    e[++tot] = v;
    ne[tot] = h[u];
    h[u] = tot;
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
        int u = ord[i], cur = out[u];
        ll val = f[u] + max(0LL, up[u]);
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
        df[++clock] = u;
        in[u] = clock;
        for (int j = l[u]; j <= r[u]; j++) st[++top] = ord[j];
    }
    pw[0] = 1;
    for (int i = 1; i <= n; i++) pw[i] = pw[i - 1] * 2LL % P;
}

void solve() {
    cin >> n >> q;
    for (int i = 1; i <= n; i++) cin >> a[i];
    bool star = true;
    for (int i = 1; i < n; i++) {
        int u, v;
        cin >> u >> v;
        if (u != 1 && v != 1) star = false;
        add(u, v);
        add(v, u);
    }
    init();
    if (star) {
        for (int i = 2; i <= n; i++) leaf[i - 1] = a[i];
        sort(leaf + 1, leaf + n);
    }
    while (q--) {
        int u;
        ll x;
        cin >> u >> x;
        if (!x) {
            cout << (ll)g[u] * out[u] % P << endl;
            continue;
        }
        if (star) {
            if (u != 1) cout << out[u] << endl;
            else {
                int c = upper_bound(leaf + 1, leaf + n, -x)
                      - lower_bound(leaf + 1, leaf + n, -x);
                cout << pw[c] << endl;
            }
            continue;
        }
        for (int i = in[u] + sz[u] - 1; i >= in[u]; i--) {
            int v = df[i];
            fp[v] = a[v] + x;
            gp[v] = 1;
            for (int j = l[v]; j <= r[v]; j++) {
                int w = ord[j];
                fp[v] += max(0LL, fp[w]);
                gp[v] = (ll)gp[v] * factor(fp[w], gp[w]) % P;
            }
        }
        cout << (ll)gp[u] * out[u] % P << endl;
    }
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
