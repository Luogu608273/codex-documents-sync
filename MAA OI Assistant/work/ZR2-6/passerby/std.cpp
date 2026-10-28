#include <bits/stdc++.h>
#define endl '\n'

using namespace std;
using ll = long long;

const int N = 2e5 + 5, M = 4e5 + 5;
int n, cnt, ans[N], ys[M], mn[M << 2], mx[M << 2], tg[M << 2], ql, qr;
struct node
{
	int x, y, id, t;
} a[M];
struct rect
{
	int x1, y1, x2, y2, l, r, fa;
} b[N];
struct event
{
	int x, t, id;
} e[M];
set<tuple<int, int, int>> s;

void init() {}

bool cmp(node u, node v)
{
	if (u.x != v.x)
		return u.x > v.x;
	if (u.t != v.t)
		return u.t < v.t;
	return u.y > v.y;
}

bool cmp2(event u, event v)
{
	if (u.x != v.x)
		return u.x < v.x;
	if (u.t != v.t)
		return u.t < v.t;
	if (b[u.id].y1 != b[v.id].y1)
		return u.t ? b[u.id].y1 < b[v.id].y1 : b[u.id].y1 > b[v.id].y1;
	return u.t ? b[u.id].y2 > b[v.id].y2 : b[u.id].y2 < b[v.id].y2;
}

void update(int p, int v)
{
	mn[p] = mx[p] = tg[p] = v;
}

void pushdown(int p)
{
	if (tg[p] != -1)
	{
		update(p << 1, tg[p]);
		update(p << 1 | 1, tg[p]);
		tg[p] = -1;
	}
}

void modify(int p, int l, int r, int x, int y, int v)
{
	if (x <= l && r <= y)
	{
		update(p, v);
		return;
	}
	pushdown(p);
	int mid = (l + r) >> 1;
	if (x <= mid)
		modify(p << 1, l, mid, x, y, v);
	if (y > mid)
		modify(p << 1 | 1, mid + 1, r, x, y, v);
	mn[p] = min(mn[p << 1], mn[p << 1 | 1]);
	mx[p] = max(mx[p << 1], mx[p << 1 | 1]);
}

void query(int p, int l, int r, int x, int y)
{
	if ((x <= l && r <= y) || tg[p] != -1)
	{
		ql = min(ql, mn[p]);
		qr = max(qr, mx[p]);
		return;
	}
	int mid = (l + r) >> 1;
	if (x <= mid)
		query(p << 1, l, mid, x, y);
	if (y > mid)
		query(p << 1 | 1, mid + 1, r, x, y);
}

void solve()
{
	cin >> n;
	for (int i = 1; i <= n; ++i)
	{
		cin >> b[i].x1 >> b[i].y1;
		a[i] = {b[i].x1, b[i].y1, i, 0};
	}
	for (int i = 1, x, y; i <= n; ++i)
	{
		cin >> x >> y;
		a[n + i] = {x, y, i, 1};
	}
	sort(a + 1, a + 2 * n + 1, cmp);
	for (int i = 1; i <= 2 * n; ++i)
	{
		if (a[i].t)
		{
			s.insert({a[i].y, a[i].x, a[i].id});
			continue;
		}
		auto it = s.upper_bound({a[i].y, INT_MAX, INT_MAX});
		if (it == s.end())
		{
			cout << "No" << endl;
			return;
		}
		auto [y, x, id] = *it;
		int u = a[i].id;
		ans[u] = id;
		b[u].x2 = x;
		b[u].y2 = y;
		s.erase(it);
	}
	for (int i = 1; i <= n; ++i)
	{
		ys[++cnt] = b[i].y1;
		ys[++cnt] = b[i].y2;
		e[2 * i - 1] = {b[i].x1, 1, i};
		e[2 * i] = {b[i].x2, 0, i};
	}
	sort(ys + 1, ys + cnt + 1);
	cnt = unique(ys + 1, ys + cnt + 1) - ys - 1;
	for (int i = 1; i <= n; ++i)
	{
		b[i].l = lower_bound(ys + 1, ys + cnt + 1, b[i].y1) - ys;
		b[i].r = lower_bound(ys + 1, ys + cnt + 1, b[i].y2) - ys - 1;
	}
	sort(e + 1, e + 2 * n + 1, cmp2);
	for (int i = 1; i <= 2 * n; ++i)
	{
		int u = e[i].id;
		ql = N, qr = 0;
		query(1, 1, cnt - 1, b[u].l, b[u].r);
		if (ql != qr)
		{
			cout << "No" << endl;
			return;
		}
		if (e[i].t)
		{
			b[u].fa = ql;
			if (ql && b[ql].x2 < b[u].x2)
			{
				cout << "No" << endl;
				return;
			}
			modify(1, 1, cnt - 1, b[u].l, b[u].r, u);
		}
		else
		{
			if (ql != u)
			{
				cout << "No" << endl;
				return;
			}
			modify(1, 1, cnt - 1, b[u].l, b[u].r, b[u].fa);
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
