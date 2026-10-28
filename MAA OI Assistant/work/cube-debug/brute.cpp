#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const int N = 2e5 + 5;

int n, d, ans;
struct point
{
	int a[3];
} p[N];
struct node
{
	int l[3], r[3];
};
vector<node> b;
vector<int> fa, sz;

bool cmp(point x, point y)
{
	return x.a[d] < y.a[d];
}

int find(int x)
{
	return fa[x] == x ? x : fa[x] = find(fa[x]);
}

void dfs(int l, int r, node u)
{
	if (l > r)
	{
		b.push_back(u);
		return;
	}
	d = 0;
	for (int i = 1; i < 3; ++i)
		if (u.r[i] - u.l[i] > u.r[d] - u.l[d])
			d = i;
	if (u.r[d] - u.l[d] == 1)
		return;
	int m = (l + r) >> 1;
	nth_element(p + l, p + m, p + r + 1, cmp);
	int t = d, x = p[m].a[t];
	if (x == u.l[t])
		++x;
	int i = l, j = r;
	while (i <= j)
	{
		if (p[i].a[t] < x)
			++i;
		else
			swap(p[i], p[j--]);
	}
	node v = u;
	u.r[t] = v.l[t] = x;
	dfs(l, j, u);
	dfs(j + 1, r, v);
}

bool check(int x, int y)
{
	int cnt = 0;
	for (int i = 0; i < 3; ++i)
	{
		if (b[x].r[i] == b[y].l[i] || b[y].r[i] == b[x].l[i])
			++cnt;
		else if (max(b[x].l[i], b[y].l[i]) >= min(b[x].r[i], b[y].r[i]))
			return 0;
	}
	return cnt == 1;
}

void init()
{
	b.push_back({});
}

void solve()
{
	node u = {};
	cin >> u.r[0] >> u.r[1] >> u.r[2] >> n;
	for (int i = 1; i <= n; ++i)
		cin >> p[i].a[0] >> p[i].a[1] >> p[i].a[2];
	dfs(1, n, u);
	int m = b.size() - 1;
	fa.resize(m + 1);
	sz.assign(m + 1, 1);
	iota(fa.begin(), fa.end(), 0);
	ans = m;
	for (int i = 1; i <= m; ++i)
		for (int j = 1; j < i; ++j)
		{
			int x = find(i), y = find(j);
			if (x != y && check(i, j))
			{
				if (sz[x] < sz[y])
					swap(x, y);
				fa[y] = x;
				sz[x] += sz[y];
				--ans;
			}
		}
	cout << ans << endl;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	init();
	solve();
	return 0;
}
