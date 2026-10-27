#include <bits/stdc++.h>
#define endl '\n'

using namespace std;
using ll = long long;

const int N = 1e6 + 5;
int n, m, a[N], c[N], b[N], d[N];

void init() {}

void solve()
{
	cin >> n >> m;
	int s = 0;
	for (int i = 1; i <= n; ++i)
		for (int j = 1; j <= m; ++j)
		{
			cin >> a[(i - 1) * m + j];
			c[i] += a[(i - 1) * m + j];
			s += a[(i - 1) * m + j];
		}
	if (s % n)
	{
		cout << -1 << endl;
		return;
	}
	int t = s / n, ans = 0, x = 0, y = 0;
	for (int i = 1; i <= n; ++i)
	{
		ans += max(0, c[i] - t);
		if (c[i] > t)
			b[++x] = i;
		if (c[i] < t)
			d[++y] = i;
	}
	cout << ans << endl;
	int l = 1, r = 1;
	while (l <= x && r <= y)
	{
		int u = b[l], v = d[r];
		for (int j = 1; j <= m; ++j)
			if (a[(u - 1) * m + j] && !a[(v - 1) * m + j])
			{
				a[(u - 1) * m + j] = 0;
				a[(v - 1) * m + j] = 1;
				--c[u], ++c[v];
				cout << u << ' ' << v << ' ' << j << endl;
				break;
			}
		if (c[u] == t)
			++l;
		if (c[v] == t)
			++r;
	}
}

int main()
{
#ifndef LOCAL
	freopen("utopia.in", "r", stdin);
	freopen("utopia.out", "w", stdout);
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
