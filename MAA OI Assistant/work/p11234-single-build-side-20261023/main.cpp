#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const ll N = 1e5 + 5, M = (1 << 18) + 5, K = 25;

int n, m, k, a[N], b[N], c[N], x[4], v[M], son[M], ht[M], len;
int rt, num, tim, vis[M], need[M];
ll res, ans[N];
bool tg[M], op[M], ok[M];
string d[K];

void init() {}

void maintain(int p)
{
	if (tg[son[p]])
	{
		v[p] = min(ht[p], v[son[p] ^ 1]);
		tg[p] = 1;
	}
	else if (v[son[p]] >= ht[p])
	{
		v[p] = v[son[p]];
		tg[p] = 0;
	}
	else
	{
		v[p] = v[son[p] ^ 1];
		tg[p] = tg[son[p] ^ 1];
	}
}

void prepare(int p, int lim, int base)
{
	if (p >= len)
	{
		need[base + p - len] = lim;
		return;
	}
	prepare(p << 1, son[p] == (p << 1) ? max(lim, ht[p]) : lim, base);
	prepare(p << 1 | 1, son[p] == (p << 1 | 1) ? max(lim, ht[p]) : lim, base);
}

void build()
{
	for (int i = 1; i <= len; ++i)
	{
		int p = len + i - 1;
		tg[p] = i > n;
		v[p] = tg[p] ? 0 : a[i];
		ok[p] = tg[p] || a[i] >= need[p];
	}
	for (int p = len - 1; p; --p)
	{
		maintain(p);
		op[p] = v[son[p]] < ht[p];
	}
}

void dfs(int p)
{
	if (vis[p] == tim)
		return;
	vis[p] = tim;
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
		if (vis[p] == tim)
			res += x;
	}
	v[p] = 0;
	tg[p] = 1;
	for (p >>= 1; p >= rt; p >>= 1)
	{
		int pv = v[p];
		bool pt = tg[p];
		maintain(p);
		if (!op[p] && v[son[p]] < ht[p])
		{
			op[p] = 1;
			if (vis[p] == tim)
				dfs(son[p] ^ 1);
		}
		if (v[p] == pv && tg[p] == pt)
			break;
	}
}

void solve()
{
	cin >> n >> m;
	k = ceil(log2(n));
	len = 1 << k;
	for (int i = 1; i <= n; ++i)
		cin >> b[i];
	for (int i = 1; i <= m; ++i)
		cin >> c[i];
	for (int i = 1; i <= k; ++i)
	{
		cin >> d[i];
		for (int j = 0; j < (len >> i); ++j)
		{
			int p = (len >> i) + j;
			ht[p] = i;
			son[p] = p << 1 | (d[i][j] - 48);
		}
	}
	for (int i = 1; i <= len; i <<= 1)
		prepare(len / i, 0, i);
	int _ = 1;
	cin >> _;
	while (_--)
	{
		cin >> x[0] >> x[1] >> x[2] >> x[3];
		for (int i = 1; i <= n; ++i)
			a[i] = b[i] ^ x[i % 4];
		build();
		rt = 1;
		num = len;
		res = 0;
		++tim;
		dfs(rt);
		for (int i = n; i >= 1; --i)
		{
			ans[i] = res;
			if (i == 1)
				break;
			if (i - 1 == (num >> 1))
			{
				rt <<= 1;
				num >>= 1;
				for (int j = 1; j <= num; ++j)
					ok[len + j - 1] = a[j] >= need[num + j - 1];
				res = 0;
				++tim;
				dfs(rt);
			}
			else
				update(i);
		}
		res = 0;
		for (int i = 1; i <= m; ++i)
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
