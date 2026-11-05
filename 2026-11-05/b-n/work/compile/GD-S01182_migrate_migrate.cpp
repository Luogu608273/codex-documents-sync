#include <bits/stdc++.h>
using namespace std;
void solve();
int main() {
	freopen("migrate.in", "r", stdin);
	freopen("migrate.out", "w", stdout);
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int T = 1, c;
	cin >> c >> T;
	while (T--) solve();
	return 0;
}
#define int long long
void solve() {
	int n, d;
	cin >> n >> d;
	vector<int> a(n);
	for (auto &t : a) cin >> t;
	vector<vector<int>> e(n+1);
	for (int i = 0; i < n; i++) {
		for (int j = i+1; j < n; j++) {
			if (a[j] - a[i] <= d) e[i].push_back(j);
			else break;
		}
	}
	auto dij=[&](int s, int t)->int {
		priority_queue<pair<int, int>> q;
		vector<int> dis(n+1, 0x3f3f3f3f3f3f3f3f), cnt(n+1);
		q.push({0, s});
		dis[s] = 0;
		while (!q.empty()) {
			int x = q.top().second, c = q.top().first;
			q.pop();
			c = -c;
			if (c > dis[x]) continue;
			for (auto v : e[x]) {
				if (dis[x] + 1 < dis[v]) {
					dis[v] = dis[x] + 1;
					cnt[v] = 1;
					q.push({-dis[v], v});
				} else if (dis[x] + 1 == dis[v]) cnt[v]++;
			}
		}
		return (cnt[t] == 2);
	};
	int cnt = 0;
	for (int i = 0; i < n; i++) {
		for (int j = 1; j < n; j++) cnt += dij(i, j);
	}
	cout << cnt << "\n";
	return ;
}
