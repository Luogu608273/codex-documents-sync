#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 200005, P = 998244353, V = 582309206;
int n, tot, tr[N][26], sz[N], id[N], fa[N], ch[N], it[N], st[N], ans[N];
ll d[26][26], w[26], res;
string s;

void add(int u, int b, int z) {
    for (int a = 0; a < 26; a++) {
        if (a == b || !tr[u][a]) continue;
        ll k = (ll)sz[tr[u][a]] * z;
        res += 2 * k * (d[a][b] + w[a] - w[b]) + 3 * k * k;
        d[a][b] += k;
        d[b][a] -= k;
        w[a] += k;
        w[b] -= k;
    }
}

void solve() {
    cin >> n;
    for (int i = 1; i <= n; i++) {
        cin >> s;
        int u = 0;
        for (char c : s) {
            int b = c - 'a';
            if (!tr[u][b]) {
                tr[u][b] = ++tot;
                fa[tot] = u;
                ch[tot] = b;
            }
            u = tr[u][b];
        }
        id[u] = i;
        sz[u] = 1;
    }
    for (int u = tot; u; u--) sz[fa[u]] += sz[u];
    int top = 1;
    st[1] = 0;
    while (top) {
        int u = st[top];
        if (!it[u] && id[u]) ans[id[u]] = res % P * V % P;
        while (it[u] < 26 && !tr[u][it[u]]) it[u]++;
        if (it[u] < 26) {
            int b = it[u]++;
            add(u, b, 1);
            st[++top] = tr[u][b];
        } else {
            top--;
            if (u) add(fa[u], ch[u], -1);
        }
    }
    for (int i = 1; i <= n; i++) cout << ans[i] << endl;
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
