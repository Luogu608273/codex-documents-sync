#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const int N = 1e5 + 5;

int n, q, c, a[N], h[N];
bool z[N];

void init() {}

void solve()
{
	cin >> n >> q >> c;
	for (int i = 1; i <= n; ++i)
	{
		cin >> a[i];
		z[i] = !a[i];
		if (z[i]) a[i] = 1;
		h[i] = 0;
	}
	for (int i = 1, x, y; i <= q; ++i)
	{
		cin >> x >> y;
		h[x] = y;
	}
	int mx = 0, p = 0, t = 0;
	for (int i = 1; i <= n; ++i)
	{
		if (z[i]) p = i;
		mx = max(mx, a[i]);
		if (!h[i]) continue;
		int r = h[i], v = mx;
		for (int j = i + 1; j < r; ++j)
		{
			if (h[j] && h[j] != r)
			{
				cout << -1 << endl;
				return;
			}
			v = max(v, a[j]);
		}
		if (v > mx)
		{
			if (!p || p < t)
			{
				cout << -1 << endl;
				return;
			}
			a[p] = mx = v;
		}
		for (int j = i + 1; j < r; ++j)
			if (z[j]) p = j;
		if (z[r]) a[r] = mx + 1;
		if (a[r] <= mx || a[r] > c)
		{
			cout << -1 << endl;
			return;
		}
		t = r;
		i = r - 1;
	}
	for (int i = 1; i <= n; ++i)
		cout << a[i] << " \n"[i == n];
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	freopen("seq.in", "r", stdin);
	freopen("seq.out", "w", stdout);
	int _ = 1;
	cin >> _;
	init();
	while (_--)
		solve();
	return 0;
}
