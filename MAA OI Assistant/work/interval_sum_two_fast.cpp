#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 5e5 + 5;
const int B = 5000000;
int n, m, l[N], r[N], head[N], dis[N], tot[N], q[N];
int h, t, top, sum, scans, mode;
bool vis[N];
struct Edge { int v, w; } e[N << 1];

void init() {}

inline int relax(int v, int d, int c)
{
	if (dis[v] <= d) return 1;
	dis[v] = d;
	tot[v] = c;
	if (tot[v] >= n + 1) return 0;
	if (++sum >= (mode == 2 ? B * 2 : B)) return -1;
	if (!vis[v])
	{
		vis[v] = 1;
		if (mode == 2) q[++top] = v;
		else if (h != t && dis[v] < dis[q[h]])
		{
			if (--h < 0) h = n + 1;
			q[h] = v;
		}
		else
		{
			q[t++] = v;
			if (t == n + 2) t = 0;
		}
	}
	return 1;
}

int spfa(int op)
{
	mode = op;
	sum = scans = 0;
	h = 0, t = n + 1, top = n + 1;
	for (int i = 1; i <= n + 1; ++i)
	{
		vis[i] = 1;
		if (op == 2) q[i] = i;
		else q[i - 1] = op == 0 ? n + 2 - i : i;
	}
	while (op == 2 ? top != 0 : h != t)
	{
		int u;
		if (op == 2) u = q[top--];
		else
		{
			u = q[h++];
			if (h == n + 2) h = 0;
		}
		vis[u] = 0;
		int res, d = dis[u], c = tot[u] + 1;
		if (u > 1 && (res = relax(u - 1, d, c)) != 1) return res;
		for (int i = head[u]; i < head[u + 1]; ++i)
		{
			if ((res = relax(e[i].v, d + e[i].w, c)) != 1) return res;
			if (++scans >= (op == 2 ? B * 4 : B * 2)) return -1;
		}
		if (u <= n && (res = relax(u + 1, d + 1, c)) != 1) return res;
	}
	return 1;
}

void solve()
{
	cin >> n >> m;
	for (int i = 1; i <= n + 2; ++i) head[i] = 0;
	for (int i = 1; i <= m; ++i)
	{
		cin >> l[i] >> r[i];
		++r[i];
		++head[l[i] + 1];
		++head[r[i] + 1];
	}
	for (int i = 1; i <= n + 1; ++i)
	{
		head[i + 1] += head[i];
		tot[i] = head[i];
	}
	for (int i = 1; i <= m; ++i)
	{
		e[tot[l[i]]++] = {r[i], 2};
		e[tot[r[i]]++] = {l[i], -2};
	}
	for (int i = 1; i <= n + 1; ++i) dis[i] = tot[i] = 0;
	int res = -1;
	int order[3] = {2, 0, 1};
	for (int i = 0; i < 3 && res == -1; ++i)
	{
		int op = order[i];
		res = spfa(op);
	}
	cout << (res == 1 ? "Yes" : "No") << endl;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	int _ = 1;
	cin >> _;
	init();
	while (_--) solve();
	return 0;
}
