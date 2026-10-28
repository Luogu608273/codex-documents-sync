#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const int N = 5e5 + 5;

int n, m, a[N], b[N], p[N], L[N], R[N];

void solve()
{
	cin >> n >> m;
	a[0] = 0;
	for (int i = 1; i <= n; ++i)
		a[i] = 0, b[i] = n + 1;
	for (int i = 1, l, r; i <= m; ++i)
	{
		cin >> l >> r;
		a[r] = max(a[r], l);
		b[r] = min(b[r], l);
	}
	for (int i = 1; i <= n; ++i)
		a[i] = max(a[i], a[i - 1]);
	for (int i = n - 1; i >= 1; --i)
		b[i] = min(b[i], b[i + 1]);
	int cnt = 0;
	p[0] = L[0] = R[0] = 0;
	int x = 0, y = -1, l = 0, r = -1;
	for (int i = 1; i <= n; ++i)
	{
		while (x <= cnt && p[x] < a[i - 1])
			++x;
		while (y < cnt && p[y + 1] < b[i])
			++y;
		while (l <= cnt && (p[l] < a[i] || R[l] < x))
			++l;
		while (r < cnt && L[r + 1] <= y)
			++r;
		if (x <= y && l <= r)
		{
			++cnt;
			p[cnt] = i;
			L[cnt] = l;
			R[cnt] = r;
		}
	}
	cout << (p[R[cnt]] >= a[n] ? "Yes" : "No") << endl;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int _;
	cin >> _;
	while (_--)
		solve();
	return 0;
}
