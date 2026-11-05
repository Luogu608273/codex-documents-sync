#include <bits/stdc++.h>
using namespace std;
void solve();
int main() {
	freopen("hub.in", "r", stdin);
	freopen("hub.out", "w", stdout);
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int T = 1, c;
	cin >> c >> T;
	while (T--) solve();
	return 0;
}
#define int long long
struct DSU{
	vector<int> fa;
	DSU(int n) {
		fa.resize(n+1);
		iota(fa.begin(), fa.end(), 0);
	}
	int find(int x) {
		while (x != fa[x]) x = fa[x] = fa[fa[x]];
		return x;
	}
	bool same(int a, int b) {
		a = find(a), b = find(b);
		if (a == b) return 1;
		return 0;
	}
	void merge(int a, int b) {
		a = find(a), b = find(b);
		if (a == b) return;
		fa[b] = a;
	}
};
void solve() {
	int n, k;
	cin >> n >> k;
	vector<vector<int>> e(n+1);
	for (int i = 0; i < n-1; i++) {
		int u, v;
		cin >> u >> v;
		e[u].push_back(v);
		e[v].push_back(u);
	}
	vector<int> d(n+1);
	vector<vector<int>> p(n+1, vector<int>(21));
	auto dfs=[&](auto &dfs, int x, int fa, int dep)->void {
		d[x] = dep;
		for (auto v : e[x]) {
			if (v == fa) continue;
			p[v][0] = x;
			dfs(dfs, v, x, dep+1);
		}
	};
	dfs(dfs, 1, 0, 0);
	for (int i = 1; i <= 20; i++) {
		for (int j = 1; j <= n; j++) p[j][i] = p[p[j][i-1]][i-1];
	}
	auto LCA=[&](int a, int b)->int {
		if (d[a] < d[b]) swap(a, b);
		for (int i = 20; i >= 0; i--) {
			if (d[p[a][i]] > d[b]) a = p[a][i];
		}
		a = p[a][0];
		if (a == b) return a;
		for (int i = 20; i >= 0; i--) {
			if (p[a][i] != p[b][i]) {
				a = p[a][i];
				b = p[b][i];
			}
		}
		return p[a][0];
	};
	vector<int> a(n+1);
	for (int i = 1; i <= n; i++) {
		for (int j = i+1; j <= n; j++) {
			int lca = LCA(i, j);
			a[i] = max(a[i], d[i]+d[j]-(lca<<1));
			a[j] = max(a[j], d[i]+d[j]-(lca<<1));
		}
	}
	int ans = 0x3f3f3f3f;
	vector<int> dis(k);
	vector<bool> vis(n+1);
	auto dfs2=[&](auto &dfs2, int dep)->void {
		if (dep == k) {
			DSU f(n+1);
			int x = 0, y = 0;
			bool k = 1;
			for (int i = 0; i < k; i++) {
				int u = dis[i];
				u = f.find(u);
				if (x == 0) x = u;
				else {
					if (p[x][0] == u || p[u][0] == x) {
						f.merge(u, x);
						x = f.find(x);
					} else {
						if (y == 0) y = u;
						else if (p[y][0] == u || p[u][0] == y) {
							f.merge(u, y);
							y = f.find(y);
						} else {
							k = 0;
							break;
						}
					}
				}
			}
			if (k) {
				int mx = 0;
				for (int i = 1; i <= n; i++) {
					if (vis[i] == 0) mx = max(mx, a[i]);
				}
				ans = min(ans, mx);
			}
			return ;
		}
		for (int i = 1; i <= n; i++) {
			if (!vis[i]) {
				vis[i] = 1;
				dis[dep] = i;
				dfs2(dfs2, dep+1);
				vis[i] = 0;
			}
		}
	};
	dfs2(dfs2, 0);
	cout << ans << "\n";
	return ;
}
