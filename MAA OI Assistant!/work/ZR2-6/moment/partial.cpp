#include <bits/stdc++.h>
#define endl '\n'

using namespace std;
using ll = long long;

const int N = 1e5 + 5, M = 2e5 + 5, K = 32, INF = 1e8;
int n, k, head[N], to[M], nxt[M], tot, deg[N], fa[N], ord[N], f[N][K];

void init() {}

void add(int u, int v)
{
	to[++tot] = v;
	nxt[tot] = head[u];
	head[u] = tot;
	++deg[u];
}

void solve()
{
	cin >> n >> k;
	for (int i = 1, u, v; i < n; ++i)
	{
		cin >> u >> v;
		add(u, v);
		add(v, u);
	}
	int leaf = 1;
	while (deg[leaf] != 1)
		++leaf;
	int rt = to[head[leaf]], cnt = 1;
	fa[rt] = leaf;
	ord[1] = rt;
	for (int i = 1; i <= cnt; ++i)
	{
		int u = ord[i];
		for (int j = head[u]; j; j = nxt[j])
			if (to[j] != fa[u])
			{
				fa[to[j]] = u;
				ord[++cnt] = to[j];
			}
	}
	for (int p = cnt; p; --p)
	{
		int u = ord[p];
		for (int j = 1; j < k; ++j)
			for (int r = 0; r < j; ++r)
			{
				int h = k - 1 - r, g0 = 1, g1 = -INF;
				for (int i = head[u]; i; i = nxt[i])
				{
					int v = to[i], a = -INF, b = -INF, c = -INF;
					if (v == fa[u])
						continue;
					for (int t = 1; t < k; ++t)
					{
						if (t <= h)
							a = max(a, f[v][t] - 1);
						if (t <= min(r, h))
							b = max(b, f[v][t]);
						if (t <= r)
							c = max(c, f[v][t] - 1);
					}
					g1 = max(g1 + max({a, b, c}), g0 + c + 1);
					g0 += max(a, b);
				}
				f[u][j] = max({f[u][j], g0, g1});
			}
	}
	cout << f[rt][k - 1] << endl;
}

int main()
{
#ifndef LOCAL
	freopen("moment.in", "r", stdin);
	freopen("moment.out", "w", stdout);
#endif
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	int _ = 1;
	init();
	while (_--)
		solve();
	return 0;
}
