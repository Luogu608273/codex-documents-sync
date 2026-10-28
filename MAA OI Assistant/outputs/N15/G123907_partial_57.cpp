#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 1005, M = 1000005;
int n, tot, h[N], to[M], nxt[M], f[N], g[N], d[N];
string s;

void add(int u, int v) {
    to[++tot] = v;
    nxt[tot] = h[u];
    h[u] = tot;
}

bool bfs() {
    queue<int> q;
    fill(d, d + n + 1, -1);
    for (int i = 1; i <= n; ++i)
        if (s[i] == 'B' && !f[i]) d[i] = 0, q.push(i);
    while (!q.empty()) {
        int u = q.front();
        q.pop();
        if (d[0] != -1 && d[u] >= d[0]) continue;
        for (int i = h[u]; i; i = nxt[i]) {
            int v = to[i];
            if (d[g[v]] == -1) {
                d[g[v]] = d[u] + 1;
                if (g[v]) q.push(g[v]);
            }
        }
    }
    return d[0] != -1;
}

bool dfs(int u) {
    for (int i = h[u]; i; i = nxt[i]) {
        int v = to[i];
        if (d[g[v]] == d[u] + 1 && (!g[v] || dfs(g[v]))) {
            f[u] = v;
            g[v] = u;
            return true;
        }
    }
    d[u] = -1;
    return false;
}

void solve() {
    cin >> s;
    bool ok = s.find('C') == string::npos;
    if (ok) {
        int cnt = 0, ans = 0;
        for (char x : s) {
            if (x == 'A') ++cnt;
            else if (cnt) --cnt, ++ans;
        }
        cout << ans << endl;
        return;
    }
    n = s.size();
    s = " " + s;
    for (int i = 1; i <= n; ++i) {
        if (s[i] != 'B') continue;
        for (int j = 1; j < i; ++j) if (s[j] == 'A') add(i, j);
        for (int j = i + 1; j <= n; ++j) if (s[j] == 'C') add(i, j);
    }
    int ans = 0;
    while (bfs())
        for (int i = 1; i <= n; ++i)
            if (s[i] == 'B' && !f[i] && dfs(i)) ++ans;
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("erase.in", "r", stdin);
    freopen("erase.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _ = 1;
    while (_--) solve();
    return 0;
}
