#include <bits/stdc++.h>
#define endl '\n'

using namespace std;
using ll = long long;

const int N = 1e5 + 5, M = 2e6 + 5;
const ll INF = 4e18;
int n, m, x, a[N], head[N], to[M], nxt[M], w[M], tot;
ll f[N];
priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> q;

void init() {}

void add(int u, int v, int t)
{
	to[++tot] = v;
	w[tot] = t;
	nxt[tot] = head[u];
	head[u] = tot;
}

void solve()
{
	cin >> n >> m >> x;
	for (int i = 1; i <= n; ++i)
		cin >> a[i];
	for (int i = 1, u, v, t; i <= m; ++i)
	{
		cin >> u >> v >> t;
		if (t <= a[u])
			add(u, v, t);
		if (t <= a[v])
			add(v, u, t);
	}
	fill(f + 1, f + n + 1, INF);
	f[1] = 0;
	q.push({0, 1});
	while (!q.empty())
	{
		auto [d, u] = q.top();
		q.pop();
		if (d != f[u])
			continue;
		if (u == n)
			break;
		for (int i = head[u]; i; i = nxt[i])
		{
			int v = to[i];
			ll z = max(d + w[i], (ll)x - a[v]);
			if (z < f[v])
			{
				f[v] = z;
				q.push({z, v});
			}
		}
	}
	cout << (f[n] == INF ? -1 : 2 * f[n] + a[n] - x) << endl;
}

int main()
{
#ifndef LOCAL
	freopen("road.in", "r", stdin);
	freopen("road.out", "w", stdout);
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
