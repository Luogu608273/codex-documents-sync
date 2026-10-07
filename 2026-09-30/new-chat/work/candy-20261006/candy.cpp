#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const int N = 2e5 + 5;

int n, m, a[N], x[N], y[N];
ll ans;

struct node
{
	int v, cnt;
};

deque<node> q;

void walk(int d)
{
	while (d)
	{
		int t = min(d, q.front().cnt);
		ans += 1ll * q.front().v * t;
		q.front().cnt -= t;
		d -= t;
		if (!q.front().cnt)
			q.pop_front();
	}
}

void sell(int p)
{
	int cnt = 0;
	while (!q.empty() && q.front().v <= p)
	{
		ans += 1ll * (q.front().v - p) * q.front().cnt;
		cnt += q.front().cnt;
		q.pop_front();
	}
	if (cnt)
		q.push_front({p, cnt});
}

void buy(int p, int d)
{
	int cnt = d;
	while (!q.empty() && q.back().v >= p)
	{
		cnt += q.back().cnt;
		q.pop_back();
	}
	q.push_back({p, cnt});
}

void init()
{
	q.clear();
	ans = 0;
	a[0] = 0;
}

void solve()
{
	cin >> n >> m;
	for (int i = 1; i <= n; ++i)
		cin >> a[i];
	for (int i = 0; i < n; ++i)
		cin >> x[i] >> y[i];
	q.push_back({x[0], m});
	for (int i = 1; i <= n; ++i)
	{
		int d = a[i] - a[i - 1];
		walk(d);
		if (i == n)
			break;
		sell(y[i]);
		buy(x[i], d);
	}
	cout << ans << endl;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	int _ = 1;
	init();
	while (_--)
		solve();
	return 0;
}
