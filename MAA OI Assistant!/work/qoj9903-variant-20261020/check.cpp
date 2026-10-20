#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll INF = (1LL << 60);
struct Edge { int u, v, w; };
int n;
vector<Edge> e;
vector<pair<int, int>> g[20];
ll d[20];
int fa[20], pe[20];
void dij(int ban, ll *dis, bool tree)
{
    fill(dis, dis + n + 1, INF);
    priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> q;
    dis[1] = 0;
    q.push({0, 1});
    while (!q.empty())
    {
        auto [du, u] = q.top(); q.pop();
        if (du != dis[u]) continue;
        for (auto [v, id] : g[u])
        {
            if (id == ban || dis[v] <= du + e[id].w) continue;
            dis[v] = du + e[id].w;
            if (tree) fa[v] = u, pe[v] = id;
            q.push({dis[v], v});
        }
    }
}
bool inside(int u, int x)
{
    while (u && u != x) u = fa[u];
    return u == x;
}
int main()
{
    mt19937 rng(9903);
    int cnt = 0;
    for (int tt = 1; tt <= 10000; ++tt)
    {
        n = rng() % 14 + 2;
        e.clear();
        bool used[20][20] = {};
        for (int i = 1; i <= n; ++i) g[i].clear(), fa[i] = 0;
        for (int v = 2; v <= n; ++v)
        {
            int u = rng() % (v - 1) + 1;
            e.push_back({u, v, int(rng() % 20 + 1)});
            used[u][v] = used[v][u] = true;
        }
        for (int u = 1; u <= n; ++u)
            for (int v = u + 1; v <= n; ++v)
                if (!used[u][v] && rng() % 3 == 0)
                    e.push_back({u, v, int(rng() % 20 + 1)});
        for (int i = 0; i < (int)e.size(); ++i)
        {
            g[e[i].u].push_back({e[i].v, i});
            g[e[i].v].push_back({e[i].u, i});
        }
        dij(-1, d, true);
        for (int x = 2; x <= n; ++x)
        {
            ll cur[20], ans = INF;
            dij(pe[x], cur, false);
            for (int i = 0; i < (int)e.size(); ++i)
                if (i != pe[x] && inside(e[i].u, x) != inside(e[i].v, x))
                    ans = min(ans, d[e[i].u] + e[i].w + d[e[i].v] - d[x]);
            if (ans != cur[x])
            {
                cout << "Mismatch seed=9903 case=" << tt << " target=" << x << '\n';
                return 1;
            }
            ++cnt;
        }
    }
    cout << "seed=9903 graphs=10000 deletion_checks=" << cnt << " passed\n";
}
