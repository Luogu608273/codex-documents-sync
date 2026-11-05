#include <bits/stdc++.H>

#define LL long long

using namespace std;
typedef pair<int, int> pii;
const int N = 510, M = 5e5 + 10;
int a[M];
vector<pii> su[M];
LL dis[N][N];
int main(){
	freopen("subway.in", "r", stdin);
	freopen("subway.out", "w", stdout); 
	ios::sync_with_stdio(0);
	cin.tie(0);
	int C, n, m, d, q;
	cin >> C >> n >> m >> d >> q;
	for(int i = 1;i <= m;i ++)
		cin >> a[i];
	for(int i = 1;i <= n;i ++){
		for(int j = 1;j <= n;j ++)
			if(i != j) dis[i][j] = 0x3f3f3f3f3f3f3f3f;
		int k;
		cin >> k;
		for(int j = 1;j <= k;j ++){
			int u, t;
			cin >> u >> t;
			su[u].push_back(make_pair(i, t));
		}
	}
	for(int u = 1;u <= m;u ++){
		for(pii x : su[u]){
			int i = x.first, xt = x.second;
			for(pii y : su[u]){
				int j = y.first, yt = y.second;
				if(i == j) continue ;
				dis[i][j] = min(dis[i][j], 1ll * xt + yt);
				dis[j][i] = dis[i][j];
			}
		}
	}
	for(int k = 1;k <= n;k ++)
		for(int i = 1;i <= n;i ++)
			for(int j = 1;j <= n;j ++)
				dis[i][j] = min(dis[i][j], dis[i][k] + dis[k][j]);
	while(q--){
		int u, v;
		cin >> u >> v;
		LL ans = 0x3f3f3f3f3f3f3f3f;
		for(pii x : su[u]){
			int i = x.first, xt = x.second;
			for(pii y : su[v]){
				int j = y.first, yt = y.second;
				LL cost = dis[i][j] + xt + yt + a[u] + a[v];
				ans = min(ans, cost);
			}
		}
		cout << ans << "\n";
	} 
	return 0;
}
