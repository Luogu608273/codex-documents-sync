#include <bits/stdc++.h>
using namespace std;
void solve();
int main() {
	freopen("subway.in", "r", stdin);
	freopen("subway.out", "w", stdout);
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int T = 1;
//	cin >> T;
	while (T--) solve();
	return 0;
}
#define int long long
void solve() {
	int c, n, m, d, q;
	cin >> c >> n >> m >> d >> q;
	vector<vector<pair<int, int>>> e(m*(n+2)+1);
	for (int i = 1; i <= m; i++) {
		int x;
		cin >> x;
		e[i].push_back({x, i+m});
		e[i+m].push_back({x, i});
	}
	int lst = 0;
	for (int i = 0; i < n; i++) {
		int k;
		cin >> k;
		for (int j = 1; j <= k; j++) {
			int a, b;
			cin >> a >> b;
			e[m+a].push_back({b, (2+i)*m+j});
			e[(2+i)*m+j].push_back({b, m+a});
			if (j != 1) {
				e[(2+i)*m+j].push_back({0, lst});
				e[lst].push_back({0, (2+i)*m+j});
			}
			lst = (2+i)*m+j;
		}
	}
	while (q--) {
		int xx, yy;
		cin >> xx >> yy;
		priority_queue<pair<int, int>> q;
		q.push({0, xx});
		vector<int> dis(m*(n+2)+1, 0x3f3f3f3f);
		dis[xx] = 0;
		while (!q.empty()) {
			int x = q.top().second, c = q.top().first;
			c = -c;
			q.pop();
			if (c > dis[x]) continue;
			for (auto t : e[x]) {
				int v = t.second, w = t.first;
				if (dis[x] + w < dis[v]) {
					dis[v] = dis[x] + w;
					q.push({-dis[v], v});
				}
			}
		}
		cout << dis[yy] << "\n";
	}
	return ;
}
