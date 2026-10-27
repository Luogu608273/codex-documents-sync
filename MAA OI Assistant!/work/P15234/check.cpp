#define main solution_main
#include "main.cpp"
#undef main

ll run(const string &s) {
    istringstream in(s);
    ostringstream out;
    streambuf *oldin = cin.rdbuf(in.rdbuf());
    streambuf *oldout = cout.rdbuf(out.rdbuf());
    fill(f, f + 4, 0);
    solve();
    cin.rdbuf(oldin);
    cout.rdbuf(oldout);
    return stoll(out.str());
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    init();
    vector<pair<string, ll>> samples = {
        {"1 1\n1 1\n", 1},
        {"2 1\n1 1\n", 2},
        {"3 2\n1 2\n2 3\n", 2}
    };
    for (auto s : samples) assert(run(s.first) == s.second);
    int cnt = 0;
    for (int len = 1; len <= 8; len++) {
        int lim = 1 << (2 * len);
        vector<int> tiles;
        for (int c = 0; c + 1 < len; c++)
            for (int miss = 0; miss < 4; miss++)
                tiles.push_back((15 ^ (1 << miss)) << (2 * c));
        vector<ll> h(lim);
        h[0] = 1;
        for (int s = 1; s < lim; s++) {
            int bit = s & -s;
            h[s] = h[s ^ bit];
            for (int tile : tiles)
                if ((tile & bit) && (s & tile) == tile)
                    (h[s] += h[s ^ tile]) %= P;
        }
        for (int blocked = 0; blocked < lim; blocked++) {
            ostringstream input;
            input << len << ' ' << __builtin_popcount((unsigned)blocked) << '\n';
            for (int c = len - 1; c >= 0; c--)
                for (int r = 0; r < 2; r++)
                    if (blocked >> (2 * c + r) & 1)
                        input << r + 1 << ' ' << c + 1 << '\n';
            ll got = run(input.str()), want = h[(lim - 1) ^ blocked];
            if (got != want) {
                ofstream fail("first-fail.in");
                fail << input.str();
                cerr << "Mismatch n=" << len << " blocked=" << blocked
                     << " got=" << got << " want=" << want << '\n';
                return 1;
            }
            cnt++;
        }
    }
    cout << "Samples: 3 passed. Exhaustive boards: " << cnt << " passed.\n";
    ostringstream large;
    large << "1000000000000000000 20000\n";
    mt19937_64 rng(15234);
    set<ll> used;
    while (used.size() < 20000) used.insert(rng() % 1000000000000000000LL + 1);
    for (ll y : used) large << (rng() % 2 + 1) << ' ' << y << '\n';
    auto start = chrono::steady_clock::now();
    ll ans = run(large.str());
    double sec = chrono::duration<double>(chrono::steady_clock::now() - start).count();
    cout << "Max-size sparse case: " << sec << " seconds; result=" << ans << '\n';
    return 0;
}
