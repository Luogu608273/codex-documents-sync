#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 1e5 + 5;
int n, q, c, a[N], b[N];
bool f[N];
void init() {}
void solve()
{
	cin >> n >> q >> c;
	for (int i = 1; i <= n; ++i)
	{
		cin >> a[i];
		f[i] = !a[i];
		if (f[i]) a[i] = 1;
		b[i] = 0;
	}
	for (int i = 1, l, r; i <= q; ++i)
	{
		cin >> l >> r;
		b[l] = r;
	}
	for (int i = 1, maxn = 0, p = 0, lst = 0, v; i <= n; ++i)
	{
		if (f[i]) p = i;
		maxn = max(maxn, a[i]);
		if (!b[i]) continue;
		v = maxn;
		for (int j = i + 1; j < b[i]; ++j)
		{
			if (b[j] && b[j] != b[i])
			{
				cout << -1 << endl;
				return;
			}
			v = max(v, a[j]);
		}
		if (v > maxn)
		{
			if (!p || p < lst)
			{
				cout << -1 << endl;
				return;
			}
			a[p] = maxn = v;
		}
		for (int j = b[i] - 1; j > i; --j)
			if (f[j]) { p = j; break; }
		if (f[b[i]]) a[b[i]] = maxn + 1;
		if (a[b[i]] <= maxn || a[b[i]] > c)
		{
			cout << -1 << endl;
			return;
		}
		lst = b[i];
		i = b[i] - 1;
	}
	for (int i = 1; i <= n; ++i) cout << a[i] << " \n"[i == n];
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
	while (_--) solve();
	return 0;
}
