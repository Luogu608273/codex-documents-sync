#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const int N = 1e5 + 5;
const ll P = 1e9 + 7;

int n, d, a[N], b[N], id[N], one[N], ans[N], cnt;
ll x;

int nxt()
{
	x = (x * 37 + 10007) % P;
	return x;
}

void init()
{
	for (int i = 1; i <= n; ++i)
		a[i] = i;
	for (int i = 1; i <= n; ++i)
		swap(a[i], a[nxt() % i + 1]);
	for (int i = 1; i <= n; ++i)
		b[i] = i <= d;
	for (int i = 1; i <= n; ++i)
		swap(b[i], b[nxt() % i + 1]);
	for (int i = 1; i <= n; ++i)
	{
		id[a[i]] = i;
		if (b[i])
			one[++cnt] = i;
	}
}

void solve()
{
	cin >> n >> d >> x;
	init();
	int m = sqrt(n);
	for (int v = n; v > n - m; --v)
	{
		for (int j = 1, p; j <= cnt; ++j)
		{
			p = id[v] + one[j] - 1;
			if (p <= n && !ans[p])
				ans[p] = v;
		}
	}
	for (int i = 1; i <= n; ++i)
	{
		if (ans[i])
			continue;
		for (int j = 1; j <= cnt && one[j] <= i; ++j)
			ans[i] = max(ans[i], a[i - one[j] + 1]);
	}
	for (int i = 1; i <= n; ++i)
		cout << ans[i] << endl;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	int _ = 1;
	// cin >> _;
	while (_--)
		solve();
	return 0;
}
