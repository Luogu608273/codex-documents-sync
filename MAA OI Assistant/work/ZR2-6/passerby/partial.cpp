#include <bits/stdc++.h>
#define endl '\n'

using namespace std;
using ll = long long;

const int N = 2e5 + 5, M = 4e5 + 5;
int n, ans[N], st[N], top;
struct node
{
	int x, y, id, t;
} a[M];
struct rect
{
	int x1, y1, x2, y2;
} b[N];
int x[N], y[N];
bool vis[N];

void init() {}

bool cmp(node u, node v)
{
	if (u.x != v.x)
		return u.x > v.x;
	if (u.t != v.t)
		return u.t < v.t;
	return u.y > v.y;
}

bool cmp2(node u, node v)
{
	if (u.x != v.x)
		return u.x < v.x;
	return u.t > v.t;
}

bool check(int i, int j)
{
	if (max(b[i].x1, b[j].x1) >= min(b[i].x2, b[j].x2)
		|| max(b[i].y1, b[j].y1) >= min(b[i].y2, b[j].y2))
		return true;
	if (b[i].x1 <= b[j].x1 && b[i].y1 <= b[j].y1
		&& b[i].x2 >= b[j].x2 && b[i].y2 >= b[j].y2)
		return true;
	return b[j].x1 <= b[i].x1 && b[j].y1 <= b[i].y1
		&& b[j].x2 >= b[i].x2 && b[j].y2 >= b[i].y2;
}

void solve()
{
	cin >> n;
	bool flat = true;
	for (int i = 1; i <= n; ++i)
	{
		cin >> b[i].x1 >> b[i].y1;
		a[i] = {b[i].x1, b[i].y1, i, 0};
		flat &= b[i].y1 == 0;
	}
	for (int i = 1; i <= n; ++i)
	{
		cin >> x[i] >> y[i];
		a[n + i] = {x[i], y[i], i, 1};
		flat &= y[i] == 1;
	}
	if (flat)
	{
		sort(a + 1, a + 2 * n + 1, cmp2);
		for (int i = 1; i <= 2 * n; ++i)
			if (!a[i].t)
				st[++top] = a[i].id;
			else
			{
				if (!top)
				{
					cout << "No" << endl;
					return;
				}
				ans[st[top--]] = a[i].id;
			}
	}
	else
	{
		sort(a + 1, a + 2 * n + 1, cmp);
		for (int i = 1; i <= 2 * n; ++i)
		{
			if (a[i].t)
				continue;
			int u = a[i].id, p = 0;
			for (int j = 1; j <= n; ++j)
				if (!vis[j] && x[j] > b[u].x1 && y[j] > b[u].y1)
					if (!p || make_pair(y[j], x[j]) < make_pair(y[p], x[p]))
						p = j;
			if (!p)
			{
				cout << "No" << endl;
				return;
			}
			ans[u] = p;
			vis[p] = true;
			b[u].x2 = x[p];
			b[u].y2 = y[p];
		}
		for (int i = 1; i <= n; ++i)
			for (int j = 1; j < i; ++j)
				if (!check(i, j))
				{
					cout << "No" << endl;
					return;
				}
	}
	cout << "Yes" << endl;
	for (int i = 1; i <= n; ++i)
		cout << ans[i] << endl;
}

int main()
{
#ifndef LOCAL
	freopen("passerby.in", "r", stdin);
	freopen("passerby.out", "w", stdout);
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
