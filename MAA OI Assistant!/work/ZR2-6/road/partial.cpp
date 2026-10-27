#include <bits/stdc++.h>
#define endl '\n'

using namespace std;
using ll = long long;

const int N = 1e5 + 5, M = 2e6 + 5, V = 1002005;
const ll INF = 4e18;
int n, m, x, a[N], head[N], to[M], nxt[M], w[M], tot, off[N], who[V];
ll f[V];
priority_queue<pair<ll, int>, vector<pair<ll, int>>, greater<pair<ll, int>>> q;

void init() {}

void add(int u, int v, int t)
{
	to[++tot] = v;
	w[tot] = t;
	nxt[tot] = head[u];
	head[u] = tot;
}

void update(int u, ll d)
{
	if (d < f[u])
	{
		f[u] = d;
		q.push({d, u});
	}
}

void solve()
{
	cin >> n >> m >> x;
	int mx = 0;
	bool same = true;
	for (int i = 1; i <= n; ++i)
	{
		cin >> a[i];
		mx = max(mx, a[i]);
		same &= a[i] == a[1];
	}
	for (int i = 1, u, v, t; i <= m; ++i)
	{
		cin >> u >> v >> t;
		add(u, v, t);
		add(v, u, t);
	}
	if (x == 0 || same || n > 1000 || m > 1000 || mx > 1000)
	{
		fill(f + 1, f + n + 1, INF);
		update(1, 0);
		while (!q.empty())
		{
			auto [d, u] = q.top();
			q.pop();
			if (d != f[u])
				continue;
			for (int i = head[u]; i; i = nxt[i])
				if (w[i] <= a[u])
					update(to[i], d + w[i]);
		}
		cout << (f[n] == INF ? -1 : 2 * f[n] + a[n] - x) << endl;
		return;
	}
	int cnt = 0;
	for (int i = 1; i <= n; ++i)
	{
		off[i] = cnt + 1;
		for (int j = 0; j <= a[i]; ++j)
			who[++cnt] = i;
	}
	fill(f + 1, f + cnt + 1, INF);
	update(off[1] + x, 0);
	while (!q.empty())
	{
		auto [d, p] = q.top();
		q.pop();
		if (d != f[p])
			continue;
		int u = who[p], h = p - off[u];
		if (h)
			update(p - 1, d + 1);
		if (h < a[u])
			update(p + 1, d + 1);
		for (int i = head[u]; i; i = nxt[i])
			if (h >= w[i] && h - w[i] <= a[to[i]])
				update(off[to[i]] + h - w[i], d + w[i]);
	}
	ll ans = f[off[n] + a[n]];
	cout << (ans == INF ? -1 : ans) << endl;
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
