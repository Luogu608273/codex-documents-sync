#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
using pii = pair<int, int>;
const ll N = 1e6 + 5;
int n, m, head[N], cnt, d[N][2], f[2][N], pre[N], suf[N], res;
ll ans;
vector<pii> vec[N];
bool vis[N][2];
struct
{
    int v, next;
} e[N << 1];
void add(int u, int v)
{
    e[++cnt] = {v, head[u]};
    head[u] = cnt;
}
void init() {}
void bfs()
{
    queue<pii> q;
    q.push({1, 0});
    d[1][0] = 0;
    for (int u, p; q.size();)
    {
        tie(u, p) = q.front();
        q.pop();
        for (int i = head[u], v; i; i = e[i].next)
        {
            if (d[v = e[i].v][p ^ 1] > d[u][p] + 1)
            {
                d[v][p ^ 1] = d[u][p] + 1;
                if (!vis[v][p ^ 1])
                {
                    vis[v][p ^ 1] = 1;
                    q.push({v, p ^ 1});
                }
            }
        }
    }
}
void solve()
{
    cin >> n >> m;
    cnt = 0;
    ans = 0;
    for (int i = 1; i < n << 1; ++i)
        vec[i].clear();
    for (int i = 1; i <= n; ++i)
        head[i] = vis[i][0] = vis[i][1] = 0, d[i][0] = d[i][1] = 1e9;
    for (int i = 1, u, v; i <= m; ++i)
    {
        cin >> u >> v;
        add(u, v);
        add(v, u);
    }
    bfs();
    if (d[1][1] >= 1e9)
    {
        cout << n - 1 << endl;
        return;
    }
    for (int i = 1; i <= n; ++i)
        vec[d[i][0] + d[i][1]].push_back({min(d[i][0], d[i][1]), 1});
    for (int i = 1, cnt; i < n << 1; ++i)
    {
        if (vec[i].empty())
            continue;
        sort(vec[i].begin(), vec[i].end());
        cnt = 0;
        for (int j = 1; j < vec[i].size(); ++j)
        {
            if (vec[i][j].first == vec[i][cnt].first)
                ++vec[i][cnt].second;
            else
                vec[i][++cnt] = vec[i][j];
        }
        vec[i].erase(vec[i].begin() + cnt + 1, vec[i].end());
        for (int j = 0, cnt, lst; j < vec[i].size(); ++j)
        {
            fill(f[j & 1], f[j & 1] + (cnt = vec[i][j].second) + 1, 1e9);
            bool flag = 0;
            if (i > 2)
            {
                auto it = lower_bound(vec[i - 2].begin(), vec[i - 2].end(), make_pair(vec[i][j].first - 1, 0));
                flag = it != vec[i - 2].end() && it->first == vec[i][j].first - 1;
            }
            if (!j || vec[i][j].first != vec[i][j - 1].first + 1)
            {
                if (i == d[1][1] && !vec[i][j].first)
                    f[j & 1][1] = 0;
                else if (flag)
                    f[j & 1][0] = cnt;
            }
            else
            {
                lst = vec[i][j - 1].second;
                if (flag)
                {
                    for (int k = 0; k <= cnt; ++k)
                        f[j & 1][k] = cnt - k + min(k + pre[min(k, lst)], suf[min(k, lst + 1)]);
                }
                else
                    f[j & 1][cnt] = min(cnt + pre[min(cnt, lst)], suf[min(cnt, lst + 1)]);
            }
            pre[0] = f[j & 1][0], suf[cnt + 1] = 1e9;
            for (int k = 1; k <= cnt; ++k)
                pre[k] = min(pre[k - 1], f[j & 1][k]);
            for (int k = cnt; k >= 0; --k)
                suf[k] = min(suf[k + 1], f[j & 1][k] + k);
            if (j + 1 >= vec[i].size() || vec[i][j + 1].first > vec[i][j].first + 1)
            {
                if (vec[i][j].first == (i >> 1))
                {
                    res = 1e9;
                    for (int k = 0; k <= cnt; ++k)
                        res = min(res, f[j & 1][k] + ((k + 1) >> 1));
                    ans += res;
                }
                else
                    ans += f[j & 1][0];
            }
        }
    }
    cout << ans << endl;
}
int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    int _ = 1;
    cin >> _;
    init();
    while (_--)
        solve();
    return 0;
}
