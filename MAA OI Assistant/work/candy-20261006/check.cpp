#define main candy_main
#include "candy.cpp"
#undef main

const ll INF = 4e18;
int tn, tc, pos[12], bx[12], sy[12];
ll f[12], g[12], h[12];

ll brute()
{
	fill(f, f + tc + 1, INF);
	f[0] = 0;
	for (int i = 0; i < tn; ++i)
	{
		fill(g, g + tc + 1, INF);
		for (int k = 0; k <= tc; ++k)
		{
			if (f[k] == INF)
				continue;
			for (int j = 0; j <= tc; ++j)
			{
				ll cost = j >= k ? 1ll * (j - k) * bx[i] : 1ll * (j - k) * sy[i];
				g[j] = min(g[j], f[k] + cost);
			}
		}
		fill(h, h + tc + 1, INF);
		int d = pos[i + 1] - pos[i];
		for (int j = d; j <= tc; ++j)
			h[j - d] = g[j];
		copy(h, h + tc + 1, f);
	}
	return *min_element(f, f + tc + 1);
}

bool check(unsigned seed, int id)
{
	ostringstream data;
	data << tn << ' ' << tc << '\n';
	for (int i = 1; i <= tn; ++i)
		data << pos[i] << (i == tn ? '\n' : ' ');
	for (int i = 0; i < tn; ++i)
		data << bx[i] << ' ' << sy[i] << '\n';
	istringstream in(data.str());
	ostringstream out;
	streambuf *ci = cin.rdbuf(in.rdbuf()), *co = cout.rdbuf(out.rdbuf());
	cin.clear();
	init();
	solve();
	cin.rdbuf(ci);
	cout.rdbuf(co);
	cin.clear();
	ll got = stoll(out.str()), want = brute();
	bool ok = got == want;
	int cnt = 0, lst = -1;
	for (node t : q)
	{
		ok &= t.cnt > 0 && t.v > lst;
		cnt += t.cnt;
		lst = t.v;
	}
	ok &= cnt == tc - (pos[tn] - pos[tn - 1]);
	if (!ok)
	{
		ofstream("first-fail.in") << data.str();
		ofstream("first-fail.txt") << "seed=" << seed << " case=" << id << " got=" << got << " want=" << want << '\n';
		cerr << "Mismatch: seed=" << seed << " case=" << id << " got=" << got << " want=" << want << '\n';
	}
	return ok;
}

int main()
{
	const unsigned seed = 20261006;
	mt19937 rng(seed);
	int tot = 0;
	for (tc = 2; tc <= 5; ++tc)
		for (int d = 1; d < tc; ++d)
			for (int b = 0; b <= 5; ++b)
				for (int s = 0; s <= b; ++s)
				{
					tn = 1;
					pos[0] = 0, pos[1] = d;
					bx[0] = b, sy[0] = s;
					if (!check(seed, ++tot))
						return 1;
					}
	for (int t = 1; t <= 20000; ++t)
	{
		tn = rng() % 8 + 1, tc = rng() % 7 + 2;
		pos[0] = 0;
		for (int i = 1; i <= tn; ++i)
			pos[i] = pos[i - 1] + rng() % (tc - 1) + 1;
		for (int i = 0; i < tn; ++i)
		{
			bx[i] = rng() % 21;
			sy[i] = rng() % (bx[i] + 1);
		}
		if (!check(seed, ++tot))
			return 1;
	}
	cout << "PASS " << tot << " cases, seed=" << seed << '\n';
	return 0;
}
