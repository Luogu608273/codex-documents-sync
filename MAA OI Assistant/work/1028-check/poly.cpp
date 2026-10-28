#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 1e6 + 5;
int n, k, cnt[N];
ll a[N], ans = -1;
__int128 sum[N];
set<pair<ll, int>> s;
set<pair<ll, int>>::iterator p[N];

void update(int x)
{
	if (cnt[x] == k && sum[x] > (__int128)2 * a[x])
		ans = max(ans, a[x]);
}

void init() {}

void solve()
{
	cin >> n >> k;
	for (int i = 1; i <= n; ++i)
	{
		cin >> a[i];
		auto t = s.insert({a[i], i}).first;
		p[i] = t;
		cnt[i] = 1;
		sum[i] = a[i];
		for (int j = 1; j < k && p[i] != s.begin(); ++j)
		{
			--p[i];
			sum[i] += p[i]->first;
			++cnt[i];
		}
		update(i);
		auto it = t;
		for (int j = 1; j < k; ++j)
		{
			++it;
			if (it == s.end())
				break;
			int x = it->second;
			sum[x] += a[i];
			if (cnt[x] == k)
			{
				sum[x] -= p[x]->first;
				++p[x];
			}
			else
			{
				++cnt[x];
				p[x] = s.begin();
			}
			update(x);
		}
		cout << ans << " \n"[i == n];
	}
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	freopen("poly.in", "r", stdin);
	freopen("poly.out", "w", stdout);
	int _ = 1;
	// cin >> _;
	init();
	while (_--)
		solve();
	return 0;
}
