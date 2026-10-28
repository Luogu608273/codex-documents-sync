#define main user_main
#include "seq_user.cpp"
#undef main
mt19937 rng(20261028);
bool ok(const vector<int> &a, const vector<pair<int, int>> &q)
{
	for (auto p : q)
	{
		int mx = 0, r = a.size();
		for (int i = 1; i <= p.first; ++i) mx = max(mx, a[i]);
		for (int i = p.first + 1; i < (int)a.size(); ++i)
			if (a[i] > mx) { r = i; break; }
		if (r != p.second) return false;
	}
	return true;
}
bool brute(vector<int> &a, int i, int C, const vector<pair<int, int>> &q)
{
	if (i == (int)a.size()) return ok(a, q);
	if (a[i]) return brute(a, i + 1, C, q);
	for (int x = 1; x <= C; ++x)
	{
		a[i] = x;
		if (brute(a, i + 1, C, q)) return true;
	}
	a[i] = 0;
	return false;
}
int main()
{
	streambuf *in = cin.rdbuf(), *out = cout.rdbuf();
	for (int t = 0; t < 100000; ++t)
	{
		int n = rng() % 7 + 2, C = rng() % 4 + 1;
		vector<int> a(n + 1);
		vector<pair<int, int>> qs;
		for (int i = 1; i <= n; ++i) a[i] = rng() % (C + 1);
		for (int i = 1; i < n; ++i)
			if (rng() % 2) qs.push_back({i, i + 1 + rng() % (n - i)});
		if (qs.empty()) qs.push_back({1, 2});
		auto want = a;
		bool possible = brute(want, 1, C, qs);
		ostringstream data;
		data << n << ' ' << qs.size() << ' ' << C << '\n';
		for (int i = 1; i <= n; ++i) data << a[i] << ' '; data << '\n';
		for (auto p : qs) data << p.first << ' ' << p.second << '\n';
		istringstream input(data.str());
		ostringstream output;
		cin.rdbuf(input.rdbuf()), cin.clear(), cout.rdbuf(output.rdbuf());
		solve();
		cin.rdbuf(in), cin.clear(), cout.rdbuf(out);
		istringstream got(output.str());
		vector<int> res;
		int x;
		while (got >> x) res.push_back(x);
		if (possible) want.erase(want.begin()); else want = {-1};
		if (want != res)
		{
			ofstream file("seq_user_first_mismatch.in"); file << "1\n" << data.str();
			cerr << "FAIL case=" << t << " seed=20261028\n"; return 1;
		}
	}
	cout << "USER B PASS 100000 seed=20261028\n";
}
