#define main contest_main
#include "main.cpp"
#undef main

int nn, aa[N], bb[N];
ll f[35], g[35], cnt;
const unsigned SEED = 20261008;

void check(int w, ll expected)
{
	ostringstream src;
	src << nn << ' ' << w << '\n';
	for (int i = 1; i <= nn; ++i)
		src << aa[i] << ' ' << bb[i] << '\n';
	istringstream in(src.str());
	ostringstream out;
	streambuf *p = cin.rdbuf(in.rdbuf()), *q = cout.rdbuf(out.rdbuf());
	fill(v1, v1 + nn + 1, 0);
	fill(v2, v2 + nn + 1, 0);
	q1 = {}, q2 = {}, q3 = {}, q4 = {};
	ans = 0;
	cin.clear();
	solve();
	cin.rdbuf(p), cout.rdbuf(q);
	cin.clear();
	istringstream res(out.str());
	ll val, cost = 0;
	string s;
	int stars = 0;
	bool ok = bool(res >> val >> s) && int(s.size()) == nn;
	if (ok)
		for (int i = 1; i <= nn; ++i)
		{
			ok &= s[i - 1] >= '0' && s[i - 1] <= '2';
			stars += s[i - 1] - '0';
			if (s[i - 1] == '1') cost += aa[i];
			if (s[i - 1] == '2') cost += bb[i];
		}
	if (!ok || stars != w || val != cost || val != expected)
	{
		ofstream("first-failure.in") << src.str();
		ofstream("first-failure.out") << out.str();
		ofstream("first-failure.txt") << "seed=" << SEED << " expected=" << expected << '\n';
		cerr << "FAIL seed=" << SEED << " case=" << cnt << " expected=" << expected << '\n';
		exit(1);
	}
	++cnt;
}

void run()
{
	fill(f, f + 2 * nn + 1, INF);
	f[0] = 0;
	for (int i = 1; i <= nn; ++i)
	{
		fill(g, g + 2 * nn + 1, INF);
		for (int j = 0; j <= 2 * (i - 1); ++j)
		{
			g[j] = min(g[j], f[j]);
			g[j + 1] = min(g[j + 1], f[j] + aa[i]);
			g[j + 2] = min(g[j + 2], f[j] + bb[i]);
		}
		copy(g, g + 2 * nn + 1, f);
	}
	for (int w = 1; w <= 2 * nn; ++w)
		check(w, f[w]);
}

void dfs(int x)
{
	if (x > nn)
	{
		run();
		return;
	}
	for (int u = 1; u < 5; ++u)
		for (int v = u + 1; v <= 5; ++v)
		{
			aa[x] = u, bb[x] = v;
			dfs(x + 1);
		}
}

int main()
{
	for (nn = 1; nn <= 4; ++nn)
		dfs(1);
	cerr << "exhaustive=" << cnt << '\n';
	mt19937 rnd(SEED);
	for (int t = 1; t <= 2000; ++t)
	{
		nn = rnd() % 12 + 1;
		for (int i = 1; i <= nn; ++i)
		{
			int lim = t % 2 ? 20 : 1000000000;
			aa[i] = rnd() % (lim - 1) + 1;
			bb[i] = aa[i] + rnd() % (lim - aa[i]) + 1;
		}
		run();
	}
	cerr << "small-total=" << cnt << " seed=" << SEED << '\n';
	nn = 300000;
	for (int i = 1; i <= nn; ++i)
		aa[i] = 1, bb[i] = 2;
	check(450001, 450001);
	ll sum = 0;
	for (int i = 1; i <= nn; ++i)
	{
		aa[i] = rnd() % 999999999 + 1;
		bb[i] = aa[i] + rnd() % (1000000000 - aa[i]) + 1;
		sum += bb[i];
	}
	check(600000, sum);
	cerr << "PASS total=" << cnt << '\n';
}
