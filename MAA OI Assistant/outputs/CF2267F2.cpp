#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 1e5 + 5, B = 30;
int n, q, a[N], b[3 * N], ans[2 * B + 1];

bool check(int k)
{
	ll cnt = 0;
	for (int i = 1, l = 1; i <= n; ++i)
	{
		if ((a[l] >> k) != (a[i] >> k)) l = i;
		cnt += i - l;
		if (cnt >= n) return true;
	}
	return false;
}

void solve()
{
	cin >> n >> q;
	for (int i = 1; i <= n; ++i) cin >> a[i];
	sort(a + 1, a + n + 1);
	int k = B, t = 0;
	ans[0] = a[n] - a[1];
	while (a[n])
	{
		while (k && check(k - 1)) --k;
		if (!k)
		{
			ans[++t] = 0;
			break;
		}
		int cnt = 0;
		for (int i = 1, l = 1; i <= n; ++i)
		{
			if ((a[l] >> k) != (a[i] >> k)) l = i;
			for (int j = l; j < i; ++j) b[++cnt] = a[i] ^ a[j];
		}
		sort(b + 1, b + cnt + 1);
		copy(b + 1, b + n + 1, a + 1);
		ans[++t] = a[n] - a[1];
	}
	for (int i = 1, x; i <= q; ++i)
	{
		cin >> x;
		cout << ans[min(x, t)] << endl;
	}
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	int _;
	cin >> _;
	while (_--) solve();
	return 0;
}
