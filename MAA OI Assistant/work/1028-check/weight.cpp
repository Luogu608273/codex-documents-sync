#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const ll N = 2e5 + 5;

int n, ans;
ll m, a[N], l, r, t;

void init() {}

void solve()
{
	cin >> n >> m;
	for (int i = 2; i <= n; ++i)
		cin >> a[i];
	for (int i = 1; i <= n; ++i)
		a[i] -= a[i - 1];
	l = m, r = 0;
	for (int i = 1, j = 0; i <= n; ++i)
	{
		if ((i - j) & 1)
			l = max(l, -a[i] - a[j]), r = min(r, m - a[i] - a[j]);
		else
			l = max(l, a[i] - a[j] - m), r = min(r, a[i] - a[j]);
		if (l > r)
		{
			j = i - 1;
			++ans;
			if ((i - j) & 1)
				l = -a[i] - a[j], r = m - a[i] - a[j];
			else
				l = a[i] - a[j] - m, r = a[i] - a[j];
		}
	}
	cout << ans - 1 << endl;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	freopen("weight.in", "r", stdin);
	freopen("weight.out", "w", stdout);
	int _ = 1;
	// cin >> _;
	init();
	while (_--)
		solve();
	return 0;
}
