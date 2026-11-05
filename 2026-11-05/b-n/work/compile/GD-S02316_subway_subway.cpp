#include <bits/stdc++.h>

using namespace std;

//#define LOCAL
#define int long long

namespace my {
	typedef long long ll;
	
	constexpr int M = 5e5 + 5;
	constexpr int N = 505;
	constexpr int P = M * 3 + N;
	constexpr int MOD = 998244353;
	constexpr ll INFLL = 0x3f3f3f3f3f3f3f3f;

	typedef long long ll;
	
	ll line_dis[N][N];
	ll w[N];
	
	struct Edge {
		int to; ll dis;
		
		bool operator < (const Edge& rhs) const {
			return to < rhs.to;
		} 
	};
	
	list <Edge> lines[M];
	unordered_map <int, ll> line2stat[N];

	int main() {
		#ifndef LOCAL
			freopen("subway.in", "r", stdin);
			freopen("subway.out", "w", stdout);
			
			ios::sync_with_stdio(false);
			cin.tie(nullptr);
		#endif

		int C, n, m, d, q;
		cin >> C >> n >> m >> d >> q;
		
		for (int i = 1; i <= m; i++)
			cin >> w[i];
			
		for (int i = 1; i <= n; i++) {
			int k; cin >> k;
			
			while (k--) {
				int a; ll t; cin >> a >> t;
				
				lines[a].push_back({i, t});
				line2stat[i][a] = t;
			}
		}
		
		for (int i = 1; i <= n; i++)
			for (int j = 1; j <= n; j++)
				line_dis[i][j] = i == j ? 0 : INFLL;
				
		for (int i = 1; i <= n; i++)
			for (int j = 1; j <= n; j++)
				if (i != j) {
					auto& li = line2stat[i], lj = line2stat[j];
					
					for (auto p : li) {
						int to = p.first; ll dis = p.second;
						
						if (lj.count(to)) {
//							cout << "Common Pair: " << i << ' ' << j << " at " << to << '\n';
							
							line_dis[i][j] = min(line_dis[i][j], dis + lj[to]);
						}
					}
				}
				
		for (int k = 1; k <= n; k++)
			for (int i = 1; i <= n; i++)
				for (int j = 1; j <= n; j++)
					line_dis[i][j] = min(line_dis[i][j], line_dis[i][k] + line_dis[k][j]);
					
		while (q--) {
			int x, y; cin >> x >> y;
			
			ll mind = INFLL;
			for (const Edge& ex : lines[x])
				for (const Edge& ey : lines[y])
					mind = min(mind, line_dis[ex.to][ey.to] + ex.dis + ey.dis);
					
			mind += w[x] + w[y];
			
			cout << mind << '\n';
		}
		
		cout << flush;

		#ifndef LOCAL
			fclose(stdin);
			fclose(stdout);
		#endif

		return 0;
	}
}

signed main() {
	my::main();

	return 0;
}

