#include <bits/stdc++.h>
using namespace std;
using ll = long long;
ll seed = 20261028, cnt;
mt19937_64 rng(seed);
int user(vector<ll> b, ll m)
{
	int n = b.size() - 1, ans = 0;
	for (int i = 1; i <= n; ++i) b[i] -= b[i - 1];
	ll l = m, r = 0;
	for (int i = 1, j = 0; i <= n; ++i)
	{
		if ((i - j) & 1) l = max(l, -b[i] - b[j]), r = min(r, m - b[i] - b[j]);
		else l = max(l, b[i] - b[j] - m), r = min(r, b[i] - b[j]);
		if (l > r)
		{
			j = i - 1;
			++ans;
			if ((i - j) & 1) l = -b[i] - b[j], r = m - b[i] - b[j];
			else l = b[i] - b[j] - m, r = b[i] - b[j];
		}
	}
	return ans - 1;
}
int brute(const vector<ll> &b, int m)
{
	vector<int> f(m + 1), g(m + 1);
	for (int i = 2; i < (int)b.size(); ++i)
	{
		fill(g.begin(), g.end(), 1000000);
		for (int x = 0; x <= m; ++x)
			for (int y = 0; y <= m; ++y)
				g[y] = min(g[y], f[x] + (x + y != b[i]));
		f.swap(g);
	}
	return *min_element(f.begin(), f.end());
}
void check(const vector<ll> &b, int m)
{
	++cnt;
	int x = user(b, m), y = brute(b, m);
	if (x == y) return;
	ofstream out("first_mismatch.in");
	out << b.size() - 1 << ' ' << m << '\n';
	for (int i = 2; i < (int)b.size(); ++i) out << b[i] << ' ';
	out << '\n';
	cerr << "FAIL seed=" << seed << " got=" << x << " expected=" << y << '\n';
	exit(1);
}
void dfs(vector<ll> &b, int p, int m)
{
	if (p == (int)b.size()) return check(b, m);
	for (int x = 0; x <= 2 * m; ++x) b[p] = x, dfs(b, p + 1, m);
}
int main()
{
	for (int m = 1; m <= 3; ++m)
		for (int n = 1; n <= (m == 1 ? 10 : m == 2 ? 8 : 7); ++n)
		{
			vector<ll> b(n + 1);
			dfs(b, 2, m);
		}
	cout << "EXHAUSTIVE PASS " << cnt << '\n';
	for (int t = 1; t <= 100000; ++t)
	{
		int n = rng() % 30 + 1, m = rng() % 10 + 1;
		vector<ll> b(n + 1);
		for (int i = 2; i <= n; ++i) b[i] = rng() % (2 * m + 1);
		check(b, m);
	}
	cout << "ALL PASS " << cnt << " seed=" << seed << '\n';
}
