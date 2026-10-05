#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const ll V = 3e5, N = V + 5, P = 998244353;

int n, head[N], dep[N], dfn[N], rnk[N], ft[N], dcnt, st[19][N], fa[N], d[N], d1[N], d2[N], cnt, ecnt, stk[N], ptr[N], top;
ll b[N], fac[N], sumd, totb = 1, sum1, sum2, ans1[N], ans2[N];
vector<int> g[N], vec1, vec2;

struct
{
	int v, next;
} e[N << 1];
struct
{
	int u, v;
} ed[N];

void add(int u, int v)
{
	e[++ecnt] = {v, head[u]};
	head[u] = ecnt;
}

void build()
{
	top = 1;
	stk[1] = 1;
	ft[1] = 0;
	dep[1] = 0;
	dfn[1] = ++dcnt;
	rnk[dcnt] = 1;
	for (int i = 1; i <= n; i++)
		ptr[i] = head[i];
	while (top > 0)
	{
		int u = stk[top], &i = ptr[u];
		bool fl = 0;
		while (i)
		{
			int v = e[i].v;
			i = e[i].next;
			if (v != ft[u])
			{
				ft[v] = u;
				dep[v] = dep[u] + 1;
				dfn[v] = ++dcnt;
				rnk[dcnt] = v;
				stk[++top] = v;
				fl = 1;
				break;
			}
		}
		if (!fl)
			top--;
	}
}

int lca(int u, int v)
{
	if (u == v)
		return u;
	int l = dfn[u], r = dfn[v], k;
	if (l > r)
		swap(l, r);
	++l, k = __lg(r - l + 1);
	return ft[dep[st[k][l]] < dep[st[k][r - (1 << k) + 1]] ? st[k][l] : st[k][r - (1 << k) + 1]];
}

int dis(int u, int v) { return dep[u] + dep[v] - (dep[lca(u, v)] << 1); }

ll qpow(ll a, ll b)
{
	ll res = 1;
	a %= P;
	while (b > 0)
	{
		if (b & 1)
			(res *= a) %= P;
		(a *= a) %= P;
		b >>= 1;
	}
	return res;
}

void init()
{
	fac[0] = 1;
	for (int i = 1; i <= V; ++i)
		fac[i] = fac[i - 1] * i % P;
}

int find(int x) { return fa[x] == x ? x : fa[x] = find(fa[x]); }

void work(int k)
{
	if (k == 1)
	{
		ans1[1] = sumd, ans2[1] = 1;
		return;
	}
	ans1[k] = sumd + k - 1;
	ll tot = (sum1 * sum1 - sum2) % P;
	if (tot < 0)
		tot += P;
	(tot *= fac[k - 2] * totb % P * qpow(2, P - 2) % P) %= P;
	ans2[k] = tot;
}

void merge(int u, int v)
{
	int ru = find(u), rv = find(v), dx1, dx2, rx, dy1, dy2, ry, dsum, dmax, nd1, nd2, osiz;
	ll tot1, tot2, sizx, sizy, dir;
	vector<int> vecx, vecy;
	bool flx, fly;
	if (ru == rv)
		return;
	--cnt;
	sumd -= d[ru] + d[rv];
	(totb *= qpow(b[ru], P - 2) * qpow(b[rv], P - 2) % P) %= P;
	tot1 = g[ru].size() * qpow(b[ru], P - 2) % P, tot2 = g[rv].size() * qpow(b[rv], P - 2) % P;
	sum1 = ((sum1 - tot1 - tot2) % P + P) % P;
	sum2 = ((sum2 - tot1 * tot1 % P - tot2 * tot2 % P) % P + P) % P;
	dx1 = dis(u, d1[ru]), dx2 = dis(u, d2[ru]), rx = max(dx1, dx2);
	flx = dx1 == rx && dx2 == rx;
	vec1.clear();
	if (!flx)
	{
		for (int p : g[ru])
		{
			if (dis(p, u) == rx)
				vec1.push_back(p);
		}
	}
	dy1 = dis(v, d1[rv]), dy2 = dis(v, d2[rv]), ry = max(dy1, dy2);
	fly = dy1 == ry && dy2 == ry;
	vec2.clear();
	if (!fly)
	{
		for (int p : g[rv])
		{
			if (dis(p, v) == ry)
				vec2.push_back(p);
		}
	}
	dsum = rx + 1 + ry, dmax = max({d[ru], d[rv], dsum});
	sizx = flx ? g[ru].size() : vec1.size(), sizy = fly ? g[rv].size() : vec2.size(), dir = 0;
	if (d[ru] == dmax)
		(dir += b[ru]) %= P;
	if (d[rv] == dmax)
		(dir += b[rv]) %= P;
	if (dsum == dmax)
		(dir += (sizx % P) * (sizy % P) % P * 2) %= P;
	nd1 = nd2 = 0;
	if (dmax == d[ru])
		nd1 = d1[ru], nd2 = d2[ru];
	else if (dmax == d[rv])
		nd1 = d1[rv], nd2 = d2[rv];
	else
		nd1 = dx1 == rx ? d1[ru] : d2[ru], nd2 = dy1 == ry ? d1[rv] : d2[rv];
	if (d[ru] == dmax)
		vecx = move(g[ru]);
	else if (dsum == dmax)
		vecx = flx ? move(g[ru]) : vec1;
	if (d[rv] == dmax)
		vecy = move(g[rv]);
	else if (dsum == dmax)
		vecy = fly ? move(g[rv]) : vec2;
	if (vecx.size() < vecy.size())
		swap(vecx, vecy);
	osiz = vecx.size();
	vecx.insert(vecx.end(), vecy.begin(), vecy.end());
	inplace_merge(vecx.begin(), vecx.begin() + osiz, vecx.end());
	vecx.erase(unique(vecx.begin(), vecx.end()), vecx.end());
	fa[rv] = ru, d[ru] = dmax, b[ru] = dir, d1[ru] = nd1, d2[ru] = nd2;
	g[ru] = move(vecx);
	g[rv].clear();
	g[rv].shrink_to_fit();
	sumd += dmax, totb = totb * dir % P;
	ll t = g[ru].size() * qpow(dir, P - 2) % P;
	(sum1 += t) %= P;
	(sum2 += t * t) %= P;
}

void solve()
{
	cin >> n;
	for (int i = 1; i < n; ++i)
	{
		cin >> ed[i].u >> ed[i].v;
		add(ed[i].u, ed[i].v);
		add(ed[i].v, ed[i].u);
	}
	build();
	for (int i = 1; i <= n; i++)
		st[0][i] = rnk[i];
	for (int j = 1; 1 << j <= n; ++j)
	{
		for (int i = 1; i + (1 << j) - 1 <= n; ++i)
			st[j][i] = dep[st[j - 1][i]] < dep[st[j - 1][i + (1 << (j - 1))]] ? st[j - 1][i] : st[j - 1][i + (1 << (j - 1))];
	}
	cnt = n, sumd = 0, totb = 1, sum1 = sum2 = n % P;
	for (int i = 1; i <= n; ++i)
		fa[i] = i, d[i] = 0, b[i] = 1, g[i] = {i}, d1[i] = i, d2[i] = i;
	work(n);
	for (int i = n - 1; i >= 1; --i)
	{
		merge(ed[i].u, ed[i].v);
		work(cnt);
	}
	for (int i = 1; i <= n; ++i)
		cout << ans1[i] << ' ' << ans2[i] << endl;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	int _ = 1;
	// cin >> _;
	init();
	while (_--)
		solve();
	return 0;
}