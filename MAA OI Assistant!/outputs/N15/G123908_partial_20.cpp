#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 2005;
struct node { int u, v; ll l, c; } e[N];
int n, m, f[N];

int find(int x) {
    return f[x] == x ? x : f[x] = find(f[x]);
}

bool cmp(node x, node y) {
    return x.c < y.c;
}

void solve() {
    cin >> n >> m;
    for (int i = 1; i <= n; ++i) f[i] = i;
    for (int i = 1; i <= m; ++i) cin >> e[i].u >> e[i].v >> e[i].l >> e[i].c;
    sort(e + 1, e + m + 1, cmp);
    ll ans = 0;
    for (int i = 1; i <= m; ++i) {
        int u = find(e[i].u), v = find(e[i].v);
        if (u != v) f[u] = v, ans += e[i].c;
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("upkeep.in", "r", stdin);
    freopen("upkeep.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _ = 1;
    while (_--) solve();
    return 0;
}
