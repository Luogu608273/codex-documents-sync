#include <bits/extc++.h>
#define endl '\n'
typedef long long ll;
#define int ll
using namespace std;
using namespace __gnu_cxx;
using namespace __gnu_pbds;

void Main() {
	int c, n, m, d, q;
	cin >> c >> n >> m >> d >> q;
	struct ly {
		int v, nt, w;
	};
	vector<int> he(n + m + 1);
	vector<ly> edge(1);
	auto add = [&](const int u, const int v, const int w) {
		edge.push_back({v, he[u], w});
		he[u] = static_cast<int>(edge.size()) - 1;
	};
	vector<int> w(m + 1);
	for (int i = 1; i <= m; ++i) {
		cin >> w[i];
	}
	vector<int> k(n + 1);
	vector<vector<int>> a(n + 1), t(n + 1);
	for (int i = 1; i <= n; ++i) {
		cin >> k[i];
		a[i].resize(k[i] + 1);
		t[i].resize(k[i] + 1);
		for (int j = 1; j <= k[i]; ++j) {
			cin >> a[i][j] >> t[i][j];
			add(i, a[i][j] + n, t[i][j]);
			add(a[i][j] + n, i, t[i][j]);
		}
	}
	auto dij = [&](const int s) {
		constexpr int inf = 0x3f3f3f3f3f3f3f3f;
		vector<int> dis(n + m + 1, inf);
		vector<bool> vis(n + m + 1);
		__gnu_pbds::priority_queue<pair<int, int>, greater<pair<int, int>>, thin_heap_tag> pq;
		dis[0] = dis[s] = 0;
		pq.push({0, s});
		while (!pq.empty()) {
			const pair<int, int> p = pq.top();
			const int d = p.first, u = p.second;
			pq.pop();
			if (vis[u]) {
				continue;
			}
			vis[u] = true;
			for (int i = he[u]; i; i = edge[i].nt) {
				const int v = edge[i].v, w = edge[i].w;
				if (dis[v] > d + w) {
					dis[v] = d + w;
					pq.push({dis[v], v});
				}
			}
		}
		return dis;
	};
	vector<bool> vis(m + 1);
	vector<vector<int>> dis(m + 1);
	while (q--) {
		int x, y;
		cin >> x >> y;
		if (x > y) {
			swap(x, y);
		}
		if (!vis[x] && !vis[y]) {
			vis[x] = true;
			dis[x] = dij(x + n);
		}
		if (vis[x]) {
			cout << w[x] + w[y] + dis[x][y + n] << endl;
		} else {
			cout << w[x] + w[y] + dis[y][x + n] << endl;
		}
	}
}

// #define CP_MULTI_TEST_CASES

signed main() {
	freopen("subway.in", "r", stdin);
	freopen("subway.out", "w", stdout);
	ios::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr);
	int t = 1;
#ifdef CP_MULTI_TEST_CASES
	cin >> t;
#endif
	while (t--) {
		Main();
	}
	return cout << flush, fflush(stdout), 0;
}
