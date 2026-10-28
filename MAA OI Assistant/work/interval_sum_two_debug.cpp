#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const int N = 5e5 + 5;

int n, m, head[N], dis[N], tot[N], cnt;
bool vis[N];
struct
{
	int v, w, next;
} e[N << 2];

void add(int u, int v, int w)
{
	e[++cnt] = {v, w, head[u]};
	head[u] = cnt;
}

void init() {}

bool spfa(int s)
{
	queue<int> q;
	for (int i = 1; i <= n + 1; ++i)
		dis[i] = 0x3f3f3f3f, tot[i] = 0, vis[i] = 0;
	vis[s] = 1;
	q.push(s);
	dis[s] = 0;
	for (int u; q.size();)
	{
		u = q.front();
		q.pop();
		vis[u] = 0;
		for (int i = head[u], v; i; i = e[i].next)
		{
			if (dis[v = e[i].v] > dis[u] + e[i].w)
			{
				dis[v] = dis[u] + e[i].w;
				tot[v] = tot[u] + 1;
				if (tot[v] >= n + 1)
					return 0;
				if (!vis[v])
				{
					vis[v] = 1;
					q.push(v);
				}
			}
		}
	}
	return 1;
}

void solve()
{
	cin >> n >> m;
	cnt = 0;
	for (int i = 1; i <= n + 1; ++i)
		head[i] = 0;
	for (int i = 1, l, r; i <= m; ++i)
	{
		cin >> l >> r;
		add(l, r + 1, 2);
		add(r + 1, l, -2);
	}
	for (int i = 1; i <= n; ++i)
		add(i, i + 1, 1), add(i + 1, i, 0);
	cout << (spfa(1) ? "Yes" : "No") << endl;
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
