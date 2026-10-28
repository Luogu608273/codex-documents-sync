#define main seq_main
#include "seq.cpp"
#undef main

bool ok(const vector<int> &b, const vector<pair<int, int>> &qs)
{
	for (auto x : qs)
	{
		int mx = 0, r = b.size();
		for (int i = 1; i <= x.first; ++i) mx = max(mx, b[i]);
		for (int i = x.first + 1; i < (int)b.size(); ++i)
			if (b[i] > mx) { r = i; break; }
		if (r != x.second) return false;
	}
	return true;
}

bool dfs(vector<int> &b, int p, int C, const vector<pair<int, int>> &qs)
{
	if (p == (int)b.size()) return ok(b, qs);
	if (b[p]) return dfs(b, p + 1, C, qs);
	for (int x = 1; x <= C; ++x)
	{
		b[p] = x;
		if (dfs(b, p + 1, C, qs)) return true;
	}
	b[p] = 0;
	return false;
}

int main()
{
	mt19937 rng(20261028);
	for (int test = 1; test <= 50000; ++test)
	{
		int nn = rng() % 7 + 2, C = rng() % 4 + 1;
		vector<int> b(nn + 1);
		for (int i = 1; i <= nn; ++i) b[i] = rng() % (C + 1);
		vector<pair<int, int>> qs;
		for (int i = 1; i < nn; ++i) if (rng() % 2) qs.push_back({i, i + 1 + rng() % (nn - i)});
		if (qs.empty()) qs.push_back({1, nn});
		auto want = b;
		if (!dfs(want, 1, C, qs)) want.clear();
		ostringstream data, output;
		data << nn << ' ' << qs.size() << ' ' << C << '\n';
		for (int i = 1; i <= nn; ++i) data << b[i] << ' ';
		data << '\n';
		for (auto x : qs) data << x.first << ' ' << x.second << '\n';
		istringstream input(data.str());
		auto old_in = cin.rdbuf(input.rdbuf());
		auto old_out = cout.rdbuf(output.rdbuf());
		solve();
		cin.rdbuf(old_in), cout.rdbuf(old_out);
		istringstream result(output.str());
		int x;
		vector<int> got(1);
		while (result >> x) got.push_back(x);
		if (got.size() == 2 && got[1] == -1) got.clear();
		if (got != want)
		{
			ofstream out("seq_std_first_mismatch.in");
			out << 1 << '\n' << data.str();
			cerr << "FAIL test=" << test << " seed=20261028\n";
			return 1;
		}
	}
	cout << "STD PASS 50000 seed=20261028\n";
}
