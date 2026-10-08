#include <bits/stdc++.h>
using namespace std;
struct Graph {
    vector<int> head, to, nxt;
    Graph(int k) : head(k+1, -1) {}
    int node() { head.push_back(-1); return (int)head.size()-1; }
    void add(int u, int v) {
        if (u == v) return;
        to.push_back(v); nxt.push_back(head[u]); head[u] = (int)to.size()-1;
    }
};
int main() {
    freopen("sect.in", "r", stdin);
    freopen("sect.out", "w", stdout);
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n, k; cin >> n >> k;
    vector<vector<int>> tree(n+1);
    for (int i = 1, u, v; i < n; ++i) {
        cin >> u >> v; tree[u].push_back(v); tree[v].push_back(u);
    }
    vector<int> c(n+1), top(k+1), cnt(k+1);
    for (int i = 1; i <= n; ++i) cin >> c[i], ++cnt[c[i]];
    vector<long long> w(k+1);
    for (int i = 1; i <= k; ++i) cin >> w[i];
    int lg = 1; while ((1 << lg) <= n) ++lg;
    vector<vector<int>> up(lg, vector<int>(n+1)), seg(lg, vector<int>(n+1));
    vector<int> depth(n+1), order(1, 1);
    for (int i = 0; i < n; ++i) {
        int u = order[i];
        for (int v : tree[u]) if (v != up[0][u]) {
            up[0][v] = u; depth[v] = depth[u]+1; order.push_back(v);
        }
    }
    for (int j = 1; j < lg; ++j)
        for (int v = 1; v <= n; ++v) up[j][v] = up[j-1][up[j-1][v]];
    auto lca = [&](int u, int v) {
        if (depth[u] < depth[v]) swap(u,v);
        int d = depth[u]-depth[v];
        for (int j = 0; j < lg; ++j) if (d >> j & 1) u = up[j][u];
        if (u == v) return u;
        for (int j = lg-1; j >= 0; --j) if (up[j][u] != up[j][v])
            u = up[j][u], v = up[j][v];
        return up[0][u];
    };
    for (int v = 1; v <= n; ++v) {
        int t = c[v]; top[t] = top[t] ? lca(top[t],v) : v;
        seg[0][v] = t;
    }
    // A connected color class itself is a feasible singleton.
    vector<int> same(k+1);
    for (int v = 2; v <= n; ++v) if (c[v] == c[up[0][v]]) ++same[c[v]];
    for (int t = 1; t <= k; ++t) if (same[t] == cnt[t]-1) {
        cout << 0 << '\n'; return 0;
    }
    Graph g(k);
    g.head.reserve(k+n*lg); g.to.reserve(3*n*lg); g.nxt.reserve(3*n*lg);
    function<int(int,int)> get = [&](int v, int j) -> int {
        if (seg[j][v]) return seg[j][v];
        int a = get(v,j-1), b = get(up[j-1][v],j-1);
        if (a == b) return seg[j][v] = a;
        int z = g.node(); g.add(z,a); g.add(z,b);
        return seg[j][v] = z;
    };
    for (int v = 1; v <= n; ++v) {
        int t = c[v], u = v, len = depth[v]-depth[top[t]]+1;
        for (int j = 0; j < lg; ++j) if (len >> j & 1) {
            g.add(t,get(u,j)); u = up[j][u];
        }
    }
    int V = (int)g.head.size()-1;
    vector<int> dfn(V+1), low(V+1), comp(V+1), active(V+1), st, dfs, edge;
    int timer = 0, cc = 0;
    auto enter = [&](int u) {
        dfn[u] = low[u] = ++timer; active[u] = 1;
        st.push_back(u); dfs.push_back(u); edge.push_back(g.head[u]);
    };
    for (int root = 1; root <= V; ++root) if (!dfn[root]) {
        enter(root);
        while (!dfs.empty()) {
            int u = dfs.back(), e = edge.back();
            if (e != -1) {
                edge.back() = g.nxt[e]; int v = g.to[e];
                if (!dfn[v]) enter(v);
                else if (active[v]) low[u] = min(low[u],dfn[v]);
            } else {
                if (low[u] == dfn[u]) {
                    ++cc;
                    while (true) {
                        int v = st.back(); st.pop_back(); active[v] = 0; comp[v] = cc;
                        if (v == u) break;
                    }
                }
                dfs.pop_back(); edge.pop_back();
                if (!dfs.empty()) low[dfs.back()] = min(low[dfs.back()],low[u]);
            }
        }
    }
    vector<long long> sum(cc+1), mx(cc+1);
    vector<char> out(cc+1);
    for (int t = 1; t <= k; ++t) sum[comp[t]] += w[t], mx[comp[t]] = max(mx[comp[t]],w[t]);
    for (int u = 1; u <= V; ++u)
        for (int e = g.head[u]; e != -1; e = g.nxt[e])
            if (comp[u] != comp[g.to[e]]) out[comp[u]] = 1;
    long long ans = LLONG_MAX;
    for (int i = 1; i <= cc; ++i) if (!out[i] && sum[i]) ans = min(ans,sum[i]-mx[i]);
    cout << ans << '\n';
}
