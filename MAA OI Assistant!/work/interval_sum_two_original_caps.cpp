#include <bits/stdc++.h>
using namespace std;
using pii = pair<int, int>;
const int N = 500005;
int n, m, dis[N], tot[N], sum, q[N], top;
bool vis[N];
vector<pii> g[N];
mt19937 rnd(19260817);
bool spfa(int s)
{
    priority_queue<int, vector<int>, greater<int>> q;
    for (int i = 1; i <= n + 1; ++i)
        dis[i] = 0x3f3f3f3f, tot[i] = 0, vis[i] = 0;
    sum = 0;
    vis[s] = 1; q.push(s); dis[s] = 0;
    while (!q.empty())
    {
        int u = q.top(); q.pop(); vis[u] = 0;
        for (auto [v, w] : g[u]) if (dis[v] > dis[u] + w)
        {
            dis[v] = dis[u] + w;
            tot[v] = tot[u] + 1;
            ++sum;
            if (tot[v] >= n + 1 || ++sum >= 5000000) return 0;
            if (!vis[v]) vis[v] = 1, q.push(v);
        }
    }
    return 1;
}
bool spfa2(int s)
{
    top = 0;
    for (int i = 1; i <= n + 1; ++i)
        dis[i] = 0x3f3f3f3f, tot[i] = 0, vis[i] = 0;
    sum = 0;
    vis[s] = 1; q[++top] = s; dis[s] = 0;
    while (top)
    {
        int u = q[top--]; vis[u] = 0;
        for (auto [v, w] : g[u]) if (dis[v] > dis[u] + w)
        {
            dis[v] = dis[u] + w;
            tot[v] = tot[u] + 1;
            if (tot[v] >= n + 1) return 0;
            if (!vis[v])
            {
                if (++sum >= 10000000) return 0;
                vis[v] = 1; q[++top] = v;
            }
        }
    }
    return 1;
}
int main()
{
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int T; cin >> T;
    while (T--)
    {
        cin >> n >> m;
        for (int i = 1; i <= n + 1; ++i) g[i].clear();
        for (int i = 1, l, r; i <= m; ++i)
        {
            cin >> l >> r;
            g[l].push_back({r + 1, 2}); g[r + 1].push_back({l, -2});
        }
        for (int i = 1; i <= n; ++i)
            g[i].push_back({i + 1, 1}), g[i + 1].push_back({i, 0});
        for (int i = 1; i <= n; ++i) shuffle(g[i].begin(), g[i].end(), rnd);
        bool ans = spfa(1);
        cerr << "priority=" << ans << " count=" << sum;
        if (!ans)
        {
            ans = spfa2(1);
            cerr << " stack=" << ans << " count=" << sum;
        }
        cerr << '\n';
        cout << (ans ? "Yes" : "No") << '\n';
    }
}
