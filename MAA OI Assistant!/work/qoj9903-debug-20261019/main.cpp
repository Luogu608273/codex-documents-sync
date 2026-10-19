#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
using tup = tuple<int, int, int>;
const ll N = 305, M = 5e5 + 5;
int n, m;
ll mp[N][N], ans[M];
vector<tup> q[N];
vector<int> vec, tvec;
void init() {}
void add(int k)
{
    vec.push_back(k);
    for (auto i : vec)
    {
        for (auto j : vec)
            mp[i][j] = min(mp[i][j], mp[i][k] + mp[k][j]);
    }
}
void solve(int l, int r)
{
    if (l == r)
    {
        for (auto [s, t, id] : q[l])
            ans[id] = mp[s][t];
        return;
    }
    int mid = (l + r) >> 1;
    ll tmp[N][N];
    memcpy(tmp, mp, sizeof mp);
    tvec = vec;
    for (int i = mid + 1; i <= r; ++i)
        add(i);
    solve(l, mid);
    memcpy(mp, tmp, sizeof tmp);
    vec = tvec;
    for (int i = l; i <= mid; ++i)
        add(i);
    solve(mid + 1, r);
}
void solve()
{
    cin >> n >> m;
    for (int i = 1; i <= n; ++i)
        for (int j = 1; j <= n; ++j)
            cin >> mp[i][j];
    for (int i = 1, s, t, p; i <= m; ++i)
    {
        cin >> s >> t >> p;
        q[p].emplace_back(s, t, i);
    }
    solve(1, n);
    for (int i = 1; i <= m; ++i)
        cout << ans[i] << endl;
}
int main()
{
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cout.tie(nullptr);
    int _ = 1;
    init();
    while (_--) solve();
    return 0;
}
