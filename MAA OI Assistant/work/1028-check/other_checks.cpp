#include <bits/stdc++.h>
using namespace std;
using ll = long long;
const ll P = 998244353;
mt19937 rng(20261028);

vector<int> seq(vector<int> c, int C, const vector<pair<int, int>> &q)
{
	int n = c.size() - 1;
	vector<int> h(n + 1), z(n + 1);
	for (auto p : q) h[p.first] = p.second;
	for (int i = 1; i <= n; ++i) z[i] = !c[i];
	int mx = 0, last = 0;
	for (int i = 1; i <= n; ++i)
	{
		if (z[i]) last = i;
		if (!c[i]) c[i] = 1;
		mx = max(mx, c[i]);
		if (!h[i]) continue;
		int r = h[i], need = mx;
		for (int j = i + 1; j < r; ++j)
		{
			if (h[j] && h[j] != r) return {};
			need = max(need, c[j]);
		}
		if (need > mx)
		{
			if (!last) return {};
			c[last] = need;
			mx = need;
		}
		for (int j = i + 1; j < r; ++j)
			if (z[j]) c[j] = 1, last = j;
		if (!c[r]) c[r] = mx + 1;
		if (c[r] <= mx || c[r] > C) return {};
		i = r - 1;
	}
	vector<int> pre(n + 1);
	for (int i = 1; i <= n; ++i) pre[i] = max(pre[i - 1], c[i]);
	for (auto p : q)
		if (pre[p.second - 1] != pre[p.first] || c[p.second] <= pre[p.first]) return {};
	return c;
}
bool seq_ok(const vector<int> &c, const vector<pair<int, int>> &q)
{
	for (auto p : q)
	{
		int mx = 0, h = c.size();
		for (int i = 1; i <= p.first; ++i) mx = max(mx, c[i]);
		for (int i = p.first + 1; i < (int)c.size(); ++i)
			if (c[i] > mx) { h = i; break; }
		if (h != p.second) return false;
	}
	return true;
}
bool seq_dfs(vector<int> &c, int p, int C, const vector<pair<int, int>> &q)
{
	if (p == (int)c.size()) return seq_ok(c, q);
	if (c[p]) return seq_dfs(c, p + 1, C, q);
	for (int x = 1; x <= C; ++x)
	{
		c[p] = x;
		if (seq_dfs(c, p + 1, C, q)) return true;
	}
	c[p] = 0;
	return false;
}

vector<ll> poly(const vector<ll> &a, int k)
{
	multiset<ll> s;
	multiset<ll>::iterator left;
	__int128 sum = 0;
	ll ans = -1;
	vector<ll> res;
	for (ll x : a)
	{
		s.insert(x);
		if ((int)s.size() <= k) sum += x, left = s.begin();
		else if (x >= *left) sum += x - *left, ++left;
		if ((int)s.size() >= k)
		{
			auto l = left, r = prev(s.end());
			__int128 now = sum;
			while (*r > ans)
			{
				if (now > (__int128)2 * *r) { ans = *r; break; }
				if (l == s.begin()) break;
				now -= *r;
				--l, --r;
				now += *l;
			}
		}
		res.push_back(ans);
	}
	return res;
}
vector<ll> poly_brute(const vector<ll> &a, int k)
{
	vector<ll> res;
	for (int i = 1; i <= (int)a.size(); ++i)
	{
		ll ans = -1;
		for (int s = 0; s < (1 << i); ++s)
			if (__builtin_popcount((unsigned)s) == k)
			{
				__int128 sum = 0;
				ll mx = 0;
				for (int j = 0; j < i; ++j)
					if (s >> j & 1) sum += a[j], mx = max(mx, a[j]);
				if (sum > (__int128)2 * mx) ans = max(ans, mx);
			}
		res.push_back(ans);
	}
	return res;
}

ll power(ll x, int y)
{
	ll res = 1;
	for (; y; y >>= 1, x = x * x % P) if (y & 1) res = res * x % P;
	return res;
}
ll name(const vector<int> &b)
{
	int n = b.size() - 1, mx = -1, end = 0, K = 0;
	vector<int> last(n + 1);
	for (int i = 1; i <= n; ++i)
		if (b[i] != -1)
		{
			if (b[i] < mx || b[i] > i) return 0;
			if (b[i] != mx) ++K;
			mx = b[i], last[mx] = i, end = i;
		}
	if (!end) return power(n + 1, n);
	int U = n + 1 - K, F = 0, S = 0, active = -1;
	vector<ll> f(n + 2), g(n + 2), nf(n + 2), ng(n + 2);
	f[0] = 1;
	for (int i = 1; i <= end; ++i)
	{
		fill(nf.begin(), nf.end(), 0);
		fill(ng.begin(), ng.end(), 0);
		for (int j = 0; j <= U; ++j)
		{
			nf[j] = (nf[j] + f[j] * (F + S + j)) % P;
			ng[j] = (ng[j] + g[j] * (F + S + j + 1)) % P;
			if (j < U)
			{
				nf[j + 1] = (nf[j + 1] + f[j] * (j + 1)) % P;
				ng[j + 1] = (ng[j + 1] + g[j] * (j + 1)) % P;
			}
			if (active != -1 && i > last[active]) ng[j] = (ng[j] + f[j]) % P;
		}
		f.swap(nf), g.swap(ng);
		if (b[i] != -1)
		{
			if (b[i] == active) { fill(g.begin(), g.end(), 0); continue; }
			if (active != -1) f.swap(g), ++S;
			int d = b[i] - S - F;
			if (d < 0 || d > U) return 0;
			for (int j = 0; j <= U - d; ++j) f[j] = f[j + d];
			for (int j = U - d + 1; j <= n + 1; ++j) f[j] = 0;
			F += d, U -= d, active = b[i];
			fill(g.begin(), g.end(), 0);
		}
	}
	ll ans = 0, binom = 1;
	for (int j = 0; j <= U; ++j)
	{
		ans = (ans + binom * f[j]) % P;
		binom = binom * (U - j) % P * power(j + 1, P - 2) % P;
	}
	return ans * power(n + 1, n - end) % P;
}
void name_dfs(int n, int p, vector<int> &a, unordered_map<int, ll> &freq)
{
	if (p <= n)
	{
		for (int x = 0; x <= n; ++x) a[p] = x, name_dfs(n, p + 1, a, freq);
		return;
	}
	int seen = 0, mex = 0, key = 0;
	for (int i = 1; i <= n; ++i)
	{
		seen |= 1 << a[i];
		while (seen >> mex & 1) ++mex;
		key = key * (n + 2) + mex + 1;
	}
	++freq[key];
}

int main(int argc, char **argv)
{
	if (argc > 1)
	{
		string mode = argv[1];
		if (mode == "seq")
		{
			int T; cin >> T;
			while (T--)
			{
				int n, q, C; cin >> n >> q >> C;
				vector<int> a(n + 1); for (int i = 1; i <= n; ++i) cin >> a[i];
				vector<pair<int, int>> qs(q); for (auto &p : qs) cin >> p.first >> p.second;
				auto res = seq(a, C, qs);
				if (res.empty()) cout << -1 << '\n';
				else { for (int i = 1; i <= n; ++i) cout << res[i] << ' '; cout << '\n'; }
			}
		}
		if (mode == "poly")
		{
			int n, k; cin >> n >> k;
			vector<ll> a(n); for (ll &x : a) cin >> x;
			for (ll x : poly(a, k)) cout << x << ' ';
			cout << '\n';
		}
		if (mode == "name")
		{
			int n; cin >> n;
			vector<int> b(n + 1); for (int i = 1; i <= n; ++i) cin >> b[i];
			cout << name(b) << '\n';
		}
		return 0;
	}
	for (int t = 0; t < 30000; ++t)
	{
		int n = rng() % 7 + 2, C = rng() % 4 + 1;
		vector<int> a(n + 1);
		for (int i = 1; i <= n; ++i) a[i] = rng() % (C + 1);
		vector<pair<int, int>> qs;
		for (int i = 1; i < n; ++i) if (rng() % 2) qs.push_back({i, i + 1 + rng() % (n - i)});
		auto want = a;
		if (!seq_dfs(want, 1, C, qs)) want.clear();
		auto got = seq(a, C, qs);
		if (want != got)
		{
			ofstream out("seq_first_mismatch.in"); out << 1 << '\n' << n << ' ' << qs.size() << ' ' << C << '\n';
			for (int i = 1; i <= n; ++i) out << a[i] << ' '; out << '\n';
			for (auto p : qs) out << p.first << ' ' << p.second << '\n';
			cerr << "SEQ FAIL " << t << '\n'; return 1;
		}
	}
	cout << "SEQ PASS 30000 seed=20261028" << endl;
	for (int t = 0; t < 10000; ++t)
	{
		int n = rng() % 10 + 3, k = rng() % (n - 2) + 3;
		vector<ll> a(n);
		for (ll &x : a) x = rng() % 4 ? rng() % 100 + 1 : 1000000000000000000LL - rng() % 100;
		if (poly(a, k) != poly_brute(a, k)) { cerr << "POLY FAIL " << t << '\n'; return 1; }
	}
	cout << "POLY PASS 10000 seed=20261028" << endl;
	ll count = 0;
	for (int n = 1; n <= 6; ++n)
	{
		unordered_map<int, ll> full, part;
		vector<int> a(n + 1), b(n + 1);
		name_dfs(n, 1, a, full);
		for (auto p : full)
		{
			int key = p.first;
			for (int i = n; i >= 1; --i) b[i] = key % (n + 2), key /= n + 2;
			for (int s = 0; s < (1 << n); ++s)
			{
				int code = 0;
				for (int i = 1; i <= n; ++i) code = code * (n + 2) + (s >> (i - 1) & 1 ? b[i] : 0);
				part[code] += p.second;
			}
		}
		int total = 1;
		for (int i = 1; i <= n; ++i) total *= n + 2;
		for (int code = 0; code < total; ++code)
		{
			int key = code;
			for (int i = n; i >= 1; --i) b[i] = key % (n + 2) - 1, key /= n + 2;
			ll got = name(b), want = part.count(code) ? part[code] % P : 0;
			if (got != want)
			{
				ofstream out("name_first_mismatch.in"); out << n << '\n';
				for (int i = 1; i <= n; ++i) out << b[i] << ' '; out << '\n';
				cerr << "NAME FAIL got=" << got << " expected=" << want << '\n'; return 1;
			}
			++count;
		}
	}
	cout << "NAME EXHAUSTIVE PASS " << count << endl;
}
