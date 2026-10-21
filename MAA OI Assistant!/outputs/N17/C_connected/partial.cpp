#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

// 仅适用于 n<=5。枚举全部带自环的简单无向图，不限于原图的子图。
const int N = 5, V = 1000000;
int n, m, e[15][2], a[N][2], b[N][2], g[N][N];

void bfs(int d[N][2]) {
    for (int i = 0; i < n; i++) d[i][0] = d[i][1] = V;
    queue<pair<int, int>> q;
    d[0][0] = 0;
    q.push({0, 0});
    while (!q.empty()) {
        int x = q.front().first, p = q.front().second;
        q.pop();
        for (int y = 0; y < n; y++) {
            if (g[x][y] && d[y][p ^ 1] == V) {
                d[y][p ^ 1] = d[x][p] + 1;
                q.push({y, p ^ 1});
            }
        }
    }
}

void solve() {
    cin >> n >> m;
    memset(g, 0, sizeof(g));
    for (int i = 1; i <= m; i++) {
        int x, y;
        cin >> x >> y;
        g[x - 1][y - 1] = g[y - 1][x - 1] = 1;
    }
    bfs(a);
    int tot = 0, ans = m;
    for (int i = 0; i < n; i++)
        for (int j = i; j < n; j++) {
            e[tot][0] = i;
            e[tot++][1] = j;
        }
    for (int s = 0; s < (1 << tot); s++) {
        int c = __builtin_popcount((unsigned)s);
        if (c < n - 1 || c >= ans) continue;
        memset(g, 0, sizeof(g));
        for (int j = 0; j < tot; j++)
            if (s >> j & 1) g[e[j][0]][e[j][1]] = g[e[j][1]][e[j][0]] = 1;
        bfs(b);
        bool ok = true;
        for (int i = 0; i < n; i++)
            for (int j = 0; j < 2; j++) ok &= a[i][j] == b[i][j];
        if (ok) ans = c;
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("connected.in", "r", stdin);
    freopen("connected.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
