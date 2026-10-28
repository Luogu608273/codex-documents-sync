#define main user_main
#include "poly.cpp"
#undef main
mt19937_64 rng(20261028);
vector<ll> brute(const vector<ll> &a, int k)
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
int main()
{
	streambuf *in = cin.rdbuf(), *out = cout.rdbuf();
	for (int t = 0; t < 30000; ++t)
	{
		int n = rng() % 10 + 3, k = rng() % (n - 2) + 3, mode = rng() % 5;
		vector<ll> a(n);
		for (ll &x : a)
		{
			if (mode == 0) x = rng() % 4 + 1;
			if (mode == 1) x = 1000000000000000000LL - rng() % 10;
			if (mode == 2) x = 1LL << (rng() % 60);
			if (mode == 3) x = rng() % 100 + 1;
			if (mode == 4) x = rng() % 1000000000000000000LL + 1;
		}
		if (t % 7 == 0) sort(a.begin(), a.end());
		if (t % 7 == 1) sort(a.rbegin(), a.rend());
		auto want = brute(a, k);
		ostringstream data;
		data << n << ' ' << k << '\n';
		for (ll x : a) data << x << ' '; data << '\n';
		istringstream input(data.str());
		ostringstream output;
		cin.rdbuf(input.rdbuf()), cin.clear(), cout.rdbuf(output.rdbuf());
		s.clear(), ans = -1;
		solve();
		cin.rdbuf(in), cin.clear(), cout.rdbuf(out);
		istringstream got(output.str());
		vector<ll> res;
		ll x;
		while (got >> x) res.push_back(x);
		if (want != res)
		{
			ofstream file("poly_user_first_mismatch.in"); file << data.str();
			cerr << "FAIL case=" << t << " seed=20261028\n"; return 1;
		}
	}
	cout << "USER C SET PASS 30000 seed=20261028\n";
}
