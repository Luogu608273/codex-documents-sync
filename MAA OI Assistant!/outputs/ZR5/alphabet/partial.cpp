// 子任务 1--5：62 分。一般情况 O(nL+26^2 n)，另处理小字母集和性质 C。
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 200005, P = 998244353, V = 582309206;
int n, k, len, ord[N], rk[26], cnt[26], c[26][26];
int tr[N][2], id[N], st[N], tot;
ll f[N], g[N], w[26];
string s[N];
vector<int> a;

ll qpow(ll a, int b) {
    ll res = 1;
    for (; b; b >>= 1, a = a * a % P)
        if (b & 1) res = res * a % P;
    return res;
}

bool cmp(int x, int y) {
    int m = min(s[x].size(), s[y].size());
    for (int i = 0; i < m; i++)
        if (s[x][i] != s[y][i]) return rk[s[x][i] - 'a'] < rk[s[y][i] - 'a'];
    return s[x].size() < s[y].size();
}

void solve() {
    cin >> n;
    bool same = true;
    for (int i = 1; i <= n; i++) {
        cin >> s[i];
        len += s[i].size();
        cnt[s[i][0] - 'a']++;
        for (char c : s[i]) {
            rk[c - 'a'] = 1;
            if (c != s[i][0]) same = false;
        }
    }
    for (int i = 0; i < 26; i++) if (rk[i]) a.push_back(i);
    k = a.size();
    if (k <= 2) {
        for (int i = 0; i < k; i++) rk[a[i]] = i;
        for (int i = 1; i <= n; i++) {
            int u = 0;
            for (char c : s[i]) {
                int b = rk[c - 'a'];
                if (!tr[u][b]) tr[u][b] = ++tot;
                u = tr[u][b];
            }
            id[u] = i;
        }
        for (int z = 0; z < 2; z++) {
            int top = 1, r = 0;
            st[1] = 0;
            while (top) {
                int u = st[top--];
                if (id[u]) {
                    r++;
                    f[id[u]] += r;
                    g[id[u]] += (ll)r * r;
                }
                if (tr[u][z ^ 1]) st[++top] = tr[u][z ^ 1];
                if (tr[u][z]) st[++top] = tr[u][z];
            }
        }
        const ll inv = (P + 1) / 2;
        for (int i = 1; i <= n; i++) {
            ll e = f[i] % P * inv % P;
            cout << (g[i] % P * inv % P - e * e % P + P) % P << endl;
        }
        return;
    }
    if (k <= 6 && len <= 120) {
        int tot = 0;
        do {
            for (int i = 0; i < k; i++) rk[a[i]] = i;
            iota(ord + 1, ord + n + 1, 1);
            sort(ord + 1, ord + n + 1, cmp);
            for (int i = 1; i <= n; i++) {
                f[ord[i]] += i;
                g[ord[i]] += (ll)i * i;
            }
            tot++;
        } while (next_permutation(a.begin(), a.end()));
        ll inv = qpow(tot, P - 2);
        for (int i = 1; i <= n; i++) {
            ll e = f[i] % P * inv % P;
            cout << (g[i] % P * inv % P - e * e % P + P) % P << endl;
        }
        return;
    }
    if (same) {
        ll sum = 0;
        for (int a = 0; a < 26; a++) sum += (ll)cnt[a] * cnt[a];
        for (int i = 1; i <= n; i++) {
            ll m = cnt[s[i][0] - 'a'], t = n - m;
            cout << (t * t + 2 * (sum - m * m)) % P * V % P << endl;
        }
        return;
    }
    for (int i = 1; i <= n; i++) {
        memset(c, 0, sizeof(c));
        memset(w, 0, sizeof(w));
        for (int j = 1; j <= n; j++) {
            if (i == j) continue;
            int m = min(s[i].size(), s[j].size()), p = 0;
            while (p < m && s[i][p] == s[j][p]) p++;
            if (p < m) c[s[j][p] - 'a'][s[i][p] - 'a']++;
        }
        ll res = 0;
        for (int a = 0; a < 26; a++) {
            for (int b = a + 1; b < 26; b++) {
                ll d = c[a][b] - c[b][a];
                res += d * d;
                w[a] += d;
                w[b] -= d;
            }
        }
        for (int a = 0; a < 26; a++) res += w[a] * w[a];
        cout << res % P * V % P << endl;
    }
}

int main() {
#ifndef LOCAL
    freopen("alphabet.in", "r", stdin);
    freopen("alphabet.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
