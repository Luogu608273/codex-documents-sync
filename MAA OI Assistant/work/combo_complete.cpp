#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const int N = 1e6 + 5, M = 2e6 + 5;

int n, m, tot, cnt, head[M], ch[M][4], sum[M], ed[M], fail[M], out[M], a[M], nxt[M], pre[M], dep[M], q[M];
bool ok[M];
string s;
struct
{
	int v, next;
} e[N << 1];

void add(int u, int v)
{
	e[++cnt] = {v, head[u]};
	head[u] = cnt;
}

void insert(const string &s)
{
	int p = 0;
	for (int i = 0, c; i < (int)s.size(); ++i)
	{
		c = s[i] - 'a';
		if (!ch[p][c])
		{
			ch[p][c] = ++tot;
			dep[tot] = dep[p] + 1;
		}
		p = ch[p][c];
		++sum[p];
	}
	++ed[p];
}

void getfail()
{
	int l = 1, r = 0;
	q[0] = 0;
	for (int i = 0; i < 4; ++i)
	{
		if (ch[0][i])
		{
			add(0, ch[0][i]);
			q[++r] = ch[0][i];
		}
	}
	while (l <= r)
	{
		int u = q[l++];
		for (int i = 0; i < 4; ++i)
		{
			if (ch[u][i])
			{
				fail[ch[u][i]] = ch[fail[u]][i];
				add(fail[ch[u][i]], ch[u][i]);
				q[++r] = ch[u][i];
			}
			else
				ch[u][i] = ch[fail[u]][i];
		}
	}
}

void dfs1(int u)
{
	for (int j = tot; j >= 0; --j)
	{
		u = q[j];
		for (int i = head[u], v; i; i = e[i].next)
		{
			v = e[i].v;
			sum[u] += sum[v];
		}
		ok[u] = ed[u] > 0 && sum[u] == ed[u];
	}
}

void dfs2(int u)
{
	out[u] = 0;
	for (int i = 1; i <= tot; ++i)
	{
		u = q[i];
		out[u] = ok[u] ? u : out[fail[u]];
	}
}

ll work(const string &s)
{
	int v = 0;
	for (int i = 1; i <= tot; ++i)
	{
		if (ok[i])
		{
			nxt[v] = i;
			pre[i] = v;
			v = i;
		}
	}
	nxt[v] = 0;
	pre[0] = v;
	ll ans = 0;
	for (int i = 1, p = 0, c; i <= m; ++i)
	{
		c = s[i] - 'a';
		p = ch[p][c];
		v = out[p];
		if (v)
		{
			a[v] = i - dep[v] + 1;
			nxt[pre[v]] = nxt[v];
			pre[nxt[v]] = pre[v];
			pre[v] = pre[0];
			nxt[v] = 0;
			nxt[pre[0]] = v;
			pre[0] = v;
		}
		ans += a[nxt[0]];
	}
	return ans;
}

void init()
{
	for (int i = 0; i <= tot; ++i)
	{
		head[i] = sum[i] = ed[i] = fail[i] = out[i] = a[i] = 0;
		nxt[i] = pre[i] = dep[i] = 0;
		ok[i] = false;
		memset(ch[i], 0, sizeof ch[i]);
	}
	cnt = tot = 0;
}

void solve()
{
	init();
	cin >> n;
	for (int i = 1; i <= n; ++i)
	{
		cin >> s;
		insert(s);
	}
	getfail();
	dfs1(0);
	dfs2(0);
	cin >> s;
	m = s.size();
	s = ' ' + s;
	cout << work(s) << endl;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	int _ = 1;
	cin >> _;
	while (_--)
		solve();
	return 0;
}
