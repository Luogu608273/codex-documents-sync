#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;
using pli = pair<ll, int>;

const ll N = 3e5 + 5;
const ll INF = 1e18;

int n, m;
ll a[N], b[N], ans, t1, t2, t3;
bool v1[N], v2[N];
priority_queue<pli, vector<pli>, greater<pli>> q1, q2, q3;
priority_queue<pli> q4;

void init() {}

void solve()
{
	cin >> n >> m;
	for (int i = 1; i <= n; ++i)
	{
		cin >> a[i] >> b[i];
		q1.emplace(a[i], i), q2.emplace(b[i], i);
	}
	for (int i = 1; i <= m; ++i)
	{
		while (q1.size() && v1[q1.top().second])
			q1.pop();
		while (q2.size() && v1[q2.top().second])
			q2.pop();
		while (q3.size() && (!v1[q3.top().second] || v2[q3.top().second]))
			q3.pop();
		while (q4.size())
		{
			int x = q4.top().second;
			if (v1[x] && q4.top().first == (v2[x] ? b[x] - a[x] : a[x]))
				break;
			q4.pop();
		}
		t1 = t2 = t3 = INF;
		if (q1.size())
			t1 = q1.top().first;
		if (q3.size())
			t2 = q3.top().first;
		if (q2.size() && q4.size())
			t3 = q2.top().first - q4.top().first;
		ans += min({t1, t2, t3});
		if (min({t1, t2, t3}) == t1)
		{
			int x = q1.top().second;
			q1.pop();
			v1[x] = 1;
			q3.emplace(b[x] - a[x], x);
			q4.emplace(a[x], x);
		}
		else if (min({t1, t2, t3}) == t2)
		{
			int x = q3.top().second;
			q3.pop();
			v2[x] = 1;
			q4.emplace(b[x] - a[x], x);
		}
		else
		{
			int x = q2.top().second, y = q4.top().second;
			q2.pop(), q4.pop();
			v1[x] = v2[x] = 1;
			q4.emplace(b[x] - a[x], x);
			if (v2[y])
			{
				v2[y] = 0;
				q3.emplace(b[y] - a[y], y);
				q4.emplace(a[y], y);
			}
			else
			{
				v1[y] = 0;
				q1.emplace(a[y], y);
				q2.emplace(b[y], y);
			}
		}
	}
	cout << ans << endl;
	for (int i = 1; i <= n; ++i)
		cout << (v2[i] ? 2 : v1[i] ? 1 : 0);
	cout << endl;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	int _ = 1;
	// cin >> _;
	init();
	while (_--)
		solve();
	return 0;
}
