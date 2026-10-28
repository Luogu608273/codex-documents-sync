#define main original_main
#include "optimized.cpp"
#undef main

mt19937 rnd(112342023);
int val[20], player[20], win[20], limc, sz, rounds;
string dd[6];
ll checked;

void brute(int p)
{
	if (p <= sz)
	{
		for (int z = 0; z <= rounds; ++z)
			val[p] = z, brute(p + 1);
		return;
	}
	for (int i = 1; i <= sz; ++i)
		player[i] = i;
	int num = sz;
	for (int r = 1; r <= rounds; ++r)
	{
		for (int g = 1; g <= num / 2; ++g)
		{
			int u = player[g * 2 - 1], v = player[g * 2];
			int h = dd[r][g - 1] == '0' ? u : v;
			player[g] = val[h] >= r ? h : u + v - h;
		}
		num /= 2;
	}
	win[player[1]] = 1;
}

ll oracle(int cnt, const vector<int> &ability)
{
	limc = cnt;
	sz = 1;
	rounds = 0;
	while (sz < cnt)
		sz *= 2, ++rounds;
	fill(win, win + 20, 0);
	for (int i = 1; i <= cnt; ++i)
		val[i] = ability[i];
	brute(cnt + 1);
	ll ret = 0;
	for (int i = 1; i <= sz; ++i)
		if (win[i])
			ret += i;
	++checked;
	return ret;
}

bool test(int id, int count, int groups)
{
	int kk = 0;
	while ((1 << kk) < count)
		++kk;
	int queries = count + 5;
	vector<int> raw(count + 1), query(queries + 1);
	vector<array<int, 4>> masks(groups);
	for (int t = 0; t < groups; ++t)
		for (int j = 0; j < 4; ++j)
			masks[t][j] = id % 3 == 0 ? rnd() & INT_MAX : rnd() % 16;
	for (int i = 1; i <= count; ++i)
		raw[i] = id % 2 == 0 ? masks[0][i % 4] ^ int(rnd() % (kk + 3)) : rnd() % (kk + 5);
	for (int i = 1; i <= queries; ++i)
		query[i] = i <= count ? i : rnd() % count + 1;
	shuffle(query.begin() + 1, query.end(), rnd);
	for (int r = 1; r <= kk; ++r)
	{
		dd[r].clear();
		for (int i = 0; i < (1 << (kk - r)); ++i)
			dd[r] += char('0' + rnd() % 2);
	}
	ostringstream input;
	input << count << ' ' << queries << '\n';
	for (int i = 1; i <= count; ++i)
		input << raw[i] << ' ';
	input << '\n';
	for (int i = 1; i <= queries; ++i)
		input << query[i] << ' ';
	input << '\n';
	for (int r = 1; r <= kk; ++r)
		input << dd[r] << '\n';
	input << groups << '\n';
	for (int t = 0; t < groups; ++t)
		input << masks[t][0] << ' ' << masks[t][1] << ' ' << masks[t][2] << ' ' << masks[t][3] << '\n';
	vector<ll> expected(groups), last(count + 1);
	for (int t = 0; t < groups; ++t)
	{
		vector<int> ability(count + 1);
		vector<ll> pref(count + 1);
		for (int i = 1; i <= count; ++i)
			ability[i] = raw[i] ^ masks[t][i % 4];
		for (int i = 1; i <= count; ++i)
			pref[i] = oracle(i, ability);
		for (int i = 1; i <= queries; ++i)
			expected[t] ^= i * pref[query[i]];
		last = pref;
	}
	istringstream in(input.str());
	ostringstream out;
	streambuf *oldin = cin.rdbuf(in.rdbuf());
	streambuf *oldout = cout.rdbuf(out.rdbuf());
	cin.clear();
	cout.clear();
	solve();
	cin.rdbuf(oldin);
	cout.rdbuf(oldout);
	cin.clear();
	cout.clear();
	istringstream result(out.str());
	bool pass = true;
	for (int t = 0; t < groups; ++t)
	{
		ll z = -1;
		result >> z;
		if (z != expected[t])
			pass = false;
	}
	for (int i = 1; i <= count; ++i)
		if (ans[i] != last[i])
		{
			cerr << "prefix=" << i << " actual=" << ans[i] << " expected=" << last[i] << '\n';
			pass = false;
		}
	if (!pass)
	{
		ofstream("first_mismatch.in") << input.str();
		cerr << "FAIL case=" << id << " seed=112342023\n";
	}
	return pass;
}

int main()
{
	for (int i = 1; i <= 4500; ++i)
		if (!test(i, 2 + rnd() % 7, i <= 4000 ? 1 : 1 + rnd() % 4))
			return 1;
	for (int i = 4501; i <= 4510; ++i)
		if (!test(i, 9 + rnd() % 8, 1))
			return 1;
	cout << "PASS cases=4510 prefix_checks=" << checked << " seed=112342023\n";
}
