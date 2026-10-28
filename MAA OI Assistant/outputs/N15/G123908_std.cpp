#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 2005, M = 4005;
const ll V = 4e18;
struct node { int u, v; ll l, c; } e[M], a[M];
int n, m, k, tot, f[N], id[N], h[N], to[M], nxt[M], cnt[N];
ll w[M], d[N];

int find(int x) {
    return f[x] == x ? x : f[x] = find(f[x]);
}

bool cmp1(node x, node y) {
    return x.c < y.c;
}

bool cmp2(node x, node y) {
    if (x.u != y.u) return x.u < y.u;
    if (x.v != y.v) return x.v < y.v;
    if (x.l != y.l) return x.l < y.l;
    return x.c < y.c;
}

void add(int u, int v, ll x) {
    to[++tot] = v;
    w[tot] = x;
    nxt[tot] = h[u];
    h[u] = tot;
}

void dijkstra(int s) {
    fill(d + 1, d + k + 1, V);
    fill(cnt + 1, cnt + k + 1, 0);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> q;
    d[s] = 0;
    q.push({0, s});
    while (!q.empty()) {
        auto [x, u] = q.top();
        q.pop();
        if (x != d[u]) continue;
        for (int i = h[u]; i; i = nxt[i]) {
            int v = to[i], c = min(2, cnt[u] + 1);
            ll y = x + w[i];
            if (y < d[v]) d[v] = y, cnt[v] = c, q.push({y, v});
            else if (y == d[v]) cnt[v] = max(cnt[v], c);
        }
    }
}

void solve() {
    cin >> n >> m;
    for (int i = 1; i <= n; ++i) f[i] = i;
    for (int i = 1; i <= m; ++i) cin >> e[i].u >> e[i].v >> e[i].l >> e[i].c;
    sort(e + 1, e + m + 1, cmp1);
    ll ans = 0;
    for (int i = 1; i <= m; ++i) {
        if (e[i].l) continue;
        int u = find(e[i].u), v = find(e[i].v);
        if (u != v) f[u] = v, ans += e[i].c;
    }
    for (int i = 1; i <= n; ++i) if (find(i) == i) id[i] = ++k;
    int t = 0;
    for (int i = 1; i <= m; ++i) {
        int u = id[find(e[i].u)], v = id[find(e[i].v)];
        if (u == v) continue;
        if (u > v) swap(u, v);
        a[++t] = {u, v, e[i].l, e[i].c};
    }
    sort(a + 1, a + t + 1, cmp2);
    int z = 0;
    for (int i = 1; i <= t; ) {
        int j = i + 1;
        while (j <= t && a[j].u == a[i].u && a[j].v == a[i].v) ++j;
        a[++z] = a[i];
        i = j;
    }
    for (int i = 1; i <= z; ++i) add(a[i].u, a[i].v, a[i].l), add(a[i].v, a[i].u, a[i].l);
    for (int s = 1; s <= k; ++s) {
        dijkstra(s);
        for (int i = 1; i <= z; ++i)
            if (a[i].u == s && d[a[i].v] == a[i].l && cnt[a[i].v] == 1) ans += a[i].c;
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("upkeep.in", "r", stdin);
    freopen("upkeep.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _ = 1;
    while (_--) solve();
    return 0;
}
