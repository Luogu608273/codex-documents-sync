#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const ll N = 2e5 + 10, Q = 1e6 + 10;

int n, m, q, fa[N], l[N], r[N], tot;
ll ans[Q];
struct edge
{
	int u, v, w;
} e[N];
struct
{
	int ch[2], fa, val, minn;
	bool rev;
} t[N << 1];
struct event
{
	int x, opt, id, k, b;
} a[N * 3 + Q];

int find(int x) { return !fa[x] ? x : fa[x] = find(fa[x]); }

bool isroot(int p)
{
	int f = t[p].fa;
	return t[f].ch[0] != p && t[f].ch[1] != p;
}

void maintain(int p)
{
	t[p].minn = p;
	for (int i = 0; i < 2; ++i)
	{
		int x = t[t[p].ch[i]].minn;
		if (t[x].val < t[t[p].minn].val)
			t[p].minn = x;
	}
}

void pushrev(int p)
{
	swap(t[p].ch[0], t[p].ch[1]);
	t[p].rev ^= 1;
}

void pushdown(int p)
{
	if (!t[p].rev)
		return;
	if (t[p].ch[0])
		pushrev(t[p].ch[0]);
	if (t[p].ch[1])
		pushrev(t[p].ch[1]);
	t[p].rev = 0;
}

void pushall(int p)
{
	if (!isroot(p))
		pushall(t[p].fa);
	pushdown(p);
}

void rotate(int x)
{
	int y = t[x].fa, z = t[y].fa, k = (t[y].ch[1] == x);
	int p = t[x].ch[k ^ 1];
	if (!isroot(y))
		t[z].ch[t[z].ch[1] == y] = x;
	t[x].fa = z, t[y].fa = x;
	t[x].ch[k ^ 1] = y, t[y].ch[k] = p;
	if (p)
		t[p].fa = y;
	maintain(y), maintain(x);
}

void splay(int x)
{
	pushall(x);
	while (!isroot(x))
	{
		int y = t[x].fa, z = t[y].fa;
		if (!isroot(y))
		{
			if ((t[y].ch[1] == x) == (t[z].ch[1] == y))
				rotate(y);
			else
				rotate(x);
		}
		rotate(x);
	}
}

void access(int x)
{
	for (int y = 0; x; y = x, x = t[x].fa)
	{
		splay(x);
		t[x].ch[1] = y;
		maintain(x);
	}
}

void makeroot(int x) { access(x), splay(x), pushrev(x); }

void split(int x, int y) { makeroot(x), access(y), splay(y); }

void link(int x, int y) { makeroot(x), t[x].fa = y; }

void cut(int x, int y)
{
	split(x, y);
	t[x].fa = t[y].ch[0] = 0;
	maintain(y);
}

void add(int id)
{
	link(e[id].u, n + id);
	link(e[id].v, n + id);
}

void init() {}

void solve()
{
	cin >> n >> m;
	for (int i = 1; i <= m; ++i)
		cin >> e[i].u >> e[i].v >> e[i].w;
	sort(e + 1, e + m + 1, [](const edge &x, const edge &y)
		 { return x.w < y.w; });
	for (int i = 0; i <= n; ++i)
		t[i].val = 2e9, t[i].minn = i;
	for (int i = 1; i <= m; ++i)
		t[n + i].val = i, t[n + i].minn = n + i;
	int cnt = 0;
	for (int i = 1; i <= m; ++i)
	{
		auto [u, v, w] = e[i];
		if (u == v)
			continue;
		if (cnt < n - 1)
		{
			int x = find(u), y = find(v);
			if (x != y)
			{
				fa[x] = y;
				++cnt;
				l[i] = -1e9;
				add(i);
				continue;
			}
		}
		split(u, v);
		int id = t[v].minn - n, mid = (e[id].w + w) >> 1;
		r[id] = mid, l[i] = mid + 1;
		cut(e[id].u, n + id);
		cut(e[id].v, n + id);
		add(i);
	}
	for (int i = 1; i <= m; ++i)
	{
		if (!l[i])
			continue;
		if (!r[i])
			r[i] = 2e9;
		a[++tot] = {l[i], 1, i, -1, e[i].w};
		a[++tot] = {e[i].w + 1, 1, i, 2, -2 * e[i].w};
		a[++tot] = {r[i] + 1, 1, i, -1, e[i].w};
	}
	cin >> q;
	for (int i = 1, x; i <= q; ++i)
	{
		cin >> x;
		a[++tot] = {x, 0, i, 0, 0};
	}
	sort(a + 1, a + tot + 1, [](const event &x, const event &y)
		 {
			 if (x.x == y.x)
				 return x.opt > y.opt;
			 return x.x < y.x;
		 });
	int k = 0;
	ll b = 0;
	for (int i = 1; i <= tot; ++i)
	{
		if (a[i].opt)
			k += a[i].k, b += a[i].b;
		else
			ans[a[i].id] = 1ll * k * a[i].x + b;
	}
	for (int i = 1; i <= q; ++i)
		cout << ans[i] << endl;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	freopen("network.in", "r", stdin);
	freopen("network.out", "w", stdout);
	int _ = 1;
	// cin >> _;
	init();
	while (_--)
		solve();
	return 0;
}
