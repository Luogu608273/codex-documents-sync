#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const ll N = 1e5 + 5, M = (1 << 18) + 5, K = 25;

int n, m, k, a[N], b[N], c[N], x[4], v[M], son[M], ht[M], len;
ll res, ans[N];
bool vis[M], op[M], ok[M];
string d[K];

void init() {}

void maintain(int p)
{
	int u = son[p];
	if (v[u] == -1 || v[u] >= ht[p])
		v[p] = v[u];
	else
		v[p] = v[u ^ 1];
}

void build(int k, int lim, int p = 1, int l = 1, int r = len)
{
	vis[p] = 0;
	ht[p] = k;
	if (l == r)
	{
		v[p] = l > min(n, len) ? -1 : a[l];
		ok[p] = v[p] == -1 || a[l] >= lim;
		return;
	}
	int mid = (l + r) >> 1, t = d[k][(l - 1) >> k] - 48;
	son[p] = p << 1 | t;
	build(k - 1, !t ? max(k, lim) : lim, p << 1, l, mid);
	build(k - 1, t ? max(k, lim) : lim, p << 1 | 1, mid + 1, r);
	maintain(p);
	op[p] = v[son[p]] < k;
}

void dfs(int p)
{
	if (vis[p])
		return;
	vis[p] = 1;
	if (p >= len)
	{
		if (ok[p])
			res += p - len + 1;
		return;
	}
	dfs(son[p]);
	if (op[p])
		dfs(son[p] ^ 1);
}

void update(int x)
{
	int p = len + x - 1;
	if (!ok[p])
	{
		ok[p] = 1;
		if (vis[p])
			res += x;
	}
	v[p] = -1;
	for (p >>= 1; p; p >>= 1)
	{
		if (v[p] == -1)
			break;
		int pv = v[p];
		maintain(p);
		if (!op[p] && v[son[p]] < ht[p])
		{
			op[p] = 1;
			if (vis[p])
				dfs(son[p] ^ 1);
		}
		if (v[p] == pv)
			break;
	}
}

void solve()
{
	cin >> n >> m;
	k = ceil(log2(n));
	for (int i = 1; i <= n; ++i)
		cin >> b[i];
	for (int i = 1; i <= m; ++i)
		cin >> c[i];
	for (int i = 1; i <= k; ++i)
		cin >> d[i];
	int _ = 1;
	cin >> _;
	while (_--)
	{
		cin >> x[0] >> x[1] >> x[2] >> x[3];
		for (int i = 1; i <= n; ++i)
			a[i] = b[i] ^ x[i % 4];
		for (int i = 0; i <= k; ++i)
		{
			len = 1 << i;
			build(i, 0);
			res = 0;
			dfs(1);
			ans[min(n, len)] = res;
			for (int j = min(n, len); j > (len >> 1) + 1; --j)
			{
				update(j);
				ans[j - 1] = res;
			}
		}
		res = 0;
		for (int i = 1; i <= m; i++)
			res ^= i * ans[c[i]];
		cout << res << endl;
	}
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
