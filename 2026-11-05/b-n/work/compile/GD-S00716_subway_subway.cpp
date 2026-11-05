#include <bits/stdc++.h>
#define int long long
#define N 500005
#define M 505
#define rep(x, y, z) for (int x = y; x <= z; x++)
#define rrep(x, y, z) for (int x = y; x >= z; x--)
#define chmin(x, y) x = min(x, y)
using namespace std;
int c, n, m, d, q, w[N];
struct edge {
	int v, w;
};
vector<edge> g[N + M];
int dis[M][M];
//测试点c n个线路 m个地铁站 每个地铁站最多d通过 查询q次
// m个站厅 站厅到此地铁站的各个线路的站台最多d个

//solution:
//创建m个站台点和n个线路点 
//求出线路点两两之间的最短路O(n^3)，枚举x,y用哪两个线路点到达O(d^2)
#undef int
int main() {
#define int long long
	ios::sync_with_stdio(0), cin.tie(0);
	freopen("subway.in", "r", stdin), freopen("subway.out", "w", stdout);
	cin >> c >> n >> m >> d >> q;
	memset(dis, 0x3f, sizeof dis);
	rep (i, 1, m) cin >> w[i];
	rep (i, 1, n) {
		dis[i][i] = 0;
		int k;
		cin >> k;
		rep (j, 1, k) {
			int x, t;
			cin >> x >> t;
			g[m + i].push_back({x, t});
			g[x].push_back({m + i, t});
		}
	}
	rep (i, 1, m) {
		//初始化dis
		for (edge e1 : g[i]) for (edge e2 : g[i]) {
			int u = e1.v, v = e2.v;
			if (u == v) continue;
			chmin(dis[u - m][v - m], e1.w + e2.w);
			chmin(dis[v - m][u - m], e1.w + e2.w);
		}
		//复杂度O(md^2)
	}
	rep (k, 1, n) rep (i, 1, n) rep (j, 1, n) {
		chmin(dis[i][j], dis[i][k] + dis[k][j]);
	}
	while (q--) {
		int u, v;
		cin >> u >> v;
		int def = w[u] + w[v], ans = 1e18;
		for (edge e1 : g[u]) for (edge e2 : g[v]) {
			chmin(ans, e1.w + e2.w + dis[e1.v - m][e2.v - m]);
		}
		ans += def;
		cout << ans << '\n';
	}
	return 0;
}
