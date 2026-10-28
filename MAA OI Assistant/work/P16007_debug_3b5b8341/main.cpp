#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const ll N = 1e6 + 5;
int n, m, k, fa[N], siz[N], ans, res;
int find(int x) { return !fa[x] ? x : fa[x] = find(fa[x]); }
void init() {}
void solve()
{
    cin >> n >> m >> k;
    for (int i = 1; i <= n; ++i) siz[i] = 1;
    for (int i = 1, x, y; i <= m; ++i)
    {
        cin >> x >> y;
        if ((x = find(x)) == (y = find(y)))
        {
            ++res;
            continue;
        }
        fa[x] = y;
        siz[y] += siz[x];
        siz[x] = 0;
    }
    for (int i = 1, rx, cnt = 0; i <= n; ++i)
    {
        if (!siz[rx = find(i)]) continue;
        ans += siz[rx] / k * k;
        res += (siz[rx] - 1) / k;
        siz[rx] = 0;
    }
    cout << ans << ' ' << res << endl;
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
