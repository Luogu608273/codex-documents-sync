#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

using ll = long long;

const ll N = 1e5 + 5, M = N * 5, P = 998244353;

int n, k, tot, cnt, head[N], siz[N], l[N], r[N], d[N], f[N], b[N];
struct
{
	int v, next;
} e[N << 1];
struct
{
	int x, w, l, r;
} a[M];

void add(int u, int v)
{
	e[++cnt] = {v, head[u]};
	head[u] = cnt;
}

void push(int u, int x, int w)
{
	a[++tot] = {x - d[u], w, r[u], 0};
	if (r[u])
		a[r[u]].r = tot;
	else
		l[u] = tot;
	r[u] = tot;
}

void insert(int u, int w)
{
	a[++tot] = {-d[u], w, 0, l[u]};
	if (l[u])
		a[l[u]].l = tot;
	else
		r[u] = tot;
	l[u] = tot;
}

void merge(int u, int v)
{
	fill(b, b + k + 2, 0);
	for (int i = l[u], x, y; i; i = a[i].r)
	{
		x = a[i].x + d[u];
		for (int j = l[v]; j; j = a[j].r)
		{
			y = a[j].x + d[v];
			if (x + y > k + 1)
				break;
			b[x + y] = (b[x + y] + (ll)a[i].w * a[j].w) % P;
		}
	}
	l[u] = r[u] = d[u] = 0;
	for (int i = 0; i <= k + 1; ++i)
	{
		if (b[i])
			push(u, i, b[i]);
	}
}

void dfs(int u, int fa)
{
	siz[u] = 1;
	for (int i = head[u], v; i; i = e[i].next)
	{
		if ((v = e[i].v) == fa)
			continue;
		dfs(v, u);
		siz[u] += siz[v];
	}
	if (siz[u] < k)
		return;
	int sz = 1, p = 0, q;
	for (int i = head[u], v; i; i = e[i].next)
	{
		if ((v = e[i].v) == fa)
			continue;
		if (siz[v] < k)
			sz += siz[v];
		else if (!p)
		{
			p = v;
			l[u] = l[v], r[u] = r[v], d[u] = d[v];
		}
		else
			merge(u, v);
	}
	if (!p)
		push(u, 0, 1);
	d[u] += sz;
	while (r[u] && a[r[u]].x + d[u] > k + 1)
		r[u] = a[r[u]].l;
	if (r[u])
		a[r[u]].r = 0;
	else
		l[u] = 0;
	q = r[u];
	if (q && a[q].x + d[u] == k + 1)
	{
		f[u] = a[q].w;
		q = a[q].l;
	}
	if (q && a[q].x + d[u] == k)
		(f[u] += a[q].w) >= P ? f[u] -= P : 0;
	if (f[u])
		insert(u, f[u]);
}

void init() {}

void solve()
{
	cin >> n >> k;
	cnt = tot = 0;
	for (int i = 1; i <= n; ++i)
		head[i] = l[i] = r[i] = d[i] = f[i] = 0;
	for (int i = 1, u, v; i < n; ++i)
	{
		cin >> u >> v;
		add(u, v);
		add(v, u);
	}
	dfs(1, 0);
	cout << f[1] << endl;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int _ = 1;
	cin >> _;
	init();
	while (_--)
		solve();
	return 0;
}
