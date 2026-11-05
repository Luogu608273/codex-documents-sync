#include <bits/stdc++.h>
#define int long long
#define N 500005
#define rep(x, y, z) for (int x = y; x <= z; x++)
#define rrep(x, y, z) for (int x = y; x >= z; x--)
#define chmax(x, y) x = max(x, y)
#define chmin(x, y) x = min(x, y)
using namespace std;
int c, T, n, k, vis[N], ans, mx, dis[N];
vector<int> g[N];
queue<int> q;
void DFS(int u, int fa) {
	dis[u] = 0;
	for (int v : g[u]) {
		if (v == fa || !vis[v]) continue;
		DFS(v, u);
	}
}
void dfs(int id, int cnt) {
	if (cnt == k) {
		rep (i, 1, n) dis[i] = 1e18;
		int Cnt = 0;
		rep (i, 1, id) if (vis[i] && dis[i] == 1e18) {
			Cnt++;
			if (Cnt > 2) continue;
			DFS(i, i);
		}
		if (Cnt > 2) return;
		while (!q.empty()) q.pop();
		rep (i, 1, id) if (vis[i]) q.push(i);
		while (!q.empty()) {
			int u = q.front();
			q.pop();
			for (int v : g[u]) {
				if (dis[u] + 1 < dis[v]) {
					dis[v] = dis[u] + 1;
					q.push(v);
				}
			}
		}
		mx = 0;
		rep (i, 1, n) chmax(mx, dis[i]);
		chmin(ans, mx);
		return;
	}
	if (cnt + n - id + 1 < k) return;
	vis[id] = 1;
	dfs(id + 1, cnt + 1);
	vis[id] = 0;
	dfs(id + 1, cnt);
}
#undef int
int main() {
#define int long long
	ios::sync_with_stdio(0), cin.tie(0);
	freopen("hub.in", "r", stdin), freopen("hub.out", "w", stdout);
	cin >> c >> T;
	while (T--) {
		cin >> n >> k;
		rep (i, 1, n) g[i].clear();
		ans = 1e18;
		rep (i, 2, n) {
			int u, v;
			cin >> u >> v;
			g[u].push_back(v);
			g[v].push_back(u);
		}
		dfs(1, 0);
		cout << ans << '\n';
	}
	return 0;
}
/*
0 2
5 2
1 2
2 3
3 4
4 5
10 3
1 2
1 3
2 4
2 5
3 6
3 7
3 8
7 9
9 10
*/
