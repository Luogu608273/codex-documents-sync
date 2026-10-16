#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
using ull = unsigned long long;
const int N = 1005, B = 16;

int n, m, k, w, beg[N], row[N];
ull same[N][B], group[B];
vector<int> off, val;
vector<ull> a, b, lim, f, g;
vector<pair<int, int>> d;

void build() {
    k = (n + 63) >> 6;
    w = 0;
    lim.clear();
    for (int i = 0; i < n - 1; i++) {
        beg[i] = (i + 1) >> 6;
        row[i] = w;
        for (int j = beg[i]; j < k; j++) {
            ull t = ~0ULL;
            if (j == beg[i]) t &= ~0ULL << ((i + 1) & 63);
            if (j == k - 1 && (n & 63)) t &= (1ULL << (n & 63)) - 1;
            lim.push_back(t);
            w++;
        }
    }
    a.assign((size_t)m * w, 0);

    for (int j = 0; j < m; j++) {
        d.clear();
        for (int i = 0; i < n; i++) {
            int p = i * m + j;
            for (int t = off[p]; t < off[p + 1]; t++) d.emplace_back(val[t], i);
        }
        sort(d.begin(), d.end());
        for (int i = 0; i < n; i++) fill(same[i], same[i] + k, 0);
        for (int l = 0, r; l < (int)d.size(); l = r) {
            r = l + 1;
            while (r < (int)d.size() && d[r].first == d[l].first) r++;
            if (r - l == 1) continue;
            fill(group, group + k, 0);
            for (int t = l; t < r; t++) {
                int p = d[t].second;
                group[p >> 6] |= 1ULL << (p & 63);
            }
            for (int t = l; t < r; t++) {
                int p = d[t].second;
                for (int h = 0; h < k; h++) same[p][h] |= group[h];
            }
        }
        ull *p = a.data() + (size_t)j * w;
        for (int i = 0; i < n - 1; i++)
            for (int h = beg[i]; h < k; h++) {
                int t = row[i] + h - beg[i];
                p[t] = ~same[i][h] & lim[t];
            }
    }
}

ll solve() {
    vector<int> ans(m, m);
    for (int x = 0; x < n - 1; x++) {
        for (int y = x + 1; y < n; y++) {
            int t = row[x] + (y >> 6) - beg[x];
            ull bit = 1ULL << (y & 63);
            int p = 0, q = 0;
            for (int j = 0; j < m; j++) {
                if (a[(size_t)j * w + t] & bit) q = p, p = j + 1;
                ans[j] = min(ans[j], q);
            }
        }
    }
    ll res = 0;
    for (int v : ans) res += v;
    return res;
}

int main() {
#ifndef LOCAL
    freopen("card.in", "r", stdin);
    freopen("card.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) {
        cin >> n >> m;
        off.resize(n * m + 1);
        off[0] = 0;
        for (int i = 0, c; i < n * m; i++) {
            cin >> c;
            off[i + 1] = off[i] + c;
        }
        val.resize(off.back());
        for (int &x : val) cin >> x;
        if (n == 1) {
            cout << 1LL * m * (m + 1) / 2 << endl;
            continue;
        }
        build();
        cout << solve() << endl;
        vector<ull>().swap(a);
        vector<ull>().swap(b);
    }
    return 0;
}
