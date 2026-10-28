#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const ll N = 2e6 + 5;

int n, m, cnt, deg[N], head[N], tg[N], c[N];
bool f[N][2];
struct node
{
	int v, next;
};
vector<node> e;

void add(int u, int v)
{
	e.push_back({v, head[u]});
	head[u] = ++cnt;
}

int read()
{
	string s;
	cin >> s;
	if (s[0] == 'a')
		return n + 1;
	if (s[0] == 'b')
		return n + 2;
	return atoi(s.c_str());
}

void init() {}

void topo()
{
	queue<pair<int, int>> q;
	f[n + 1][1] = f[n + 2][1] = 1;
	q.push({n + 1, 1});
	q.push({n + 2, 1});
	for (int i = n + 3; i <= n + m + 2; ++i)
	{
		if (!deg[i] && !f[c[i]][0])
		{
			f[c[i]][0] = 1;
			q.push({c[i], 0});
		}
	}
	for (int u, p; q.size();)
	{
		u = q.front().first;
		p = q.front().second;
		q.pop();
		for (int i = head[u], v; i; i = e[i].next)
		{
			v = e[i].v;
			if (!tg[u])
			{
				--deg[v];
				if (p)
					swap(f[v][0], f[v][1]);
			}
			else
				f[v][0] = f[v][1] = 1;
			if (!deg[v])
			{
				for (int j = 0; j < 2; ++j)
				{
					if (f[v][j] && !f[c[v]][j])
					{
						f[c[v]][j] = 1;
						q.push({c[v], j});
					}
				}
			}
		}
		++tg[u];
	}
}

void solve()
{
	cin >> n >> m;
	for (int i = 1; i <= n + m + 2; ++i)
		f[i][0] = f[i][1] = deg[i] = head[i] = tg[i] = 0;
	cnt = 0;
	e.clear();
	e.push_back({0, 0});
	for (int i = 1, k; i <= m; ++i)
	{
		int u = i + n + 2;
		cin >> c[u] >> k;
		deg[u] = k;
		f[u][0] = 1;
		for (int j = 1, x; j <= k; ++j)
		{
			x = read();
			add(x, u);
		}
	}
	topo();
	cout << (f[1][1] ? "YES" : "NO") << endl;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	int _ = 1;
	cin >> _;
	init();
	while (_--)
		solve();
	return 0;
}
