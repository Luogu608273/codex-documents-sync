#include <iostream>
#include <queue>
#include <cstring>
#include <bitset>
#include <cstdio>
#include <vector>
using namespace std;

long long c, n, m, d, q, x, y, a, t, k;
long long w[500090];
long long dis[600090];
bitset<600090> Walked;

struct edge{
	long long to, val;
	bool friend operator<(edge u, edge v){
		return u.val > v.val;
	}
};
vector<edge> Lnk[600090];
priority_queue<edge> Q; 

long long dij(int s, int to){
	memset(dis, 0x0f, sizeof dis);
	Walked.reset();
	dis[s] = 0;
	Q.push({s, 0});
	while (!Q.empty()){
		edge e = Q.top();
		Q.pop();
		if (Walked[e.to]) continue;
		for (edge v : Lnk[e.to]){
			if (v.val + dis[e.to] < dis[v.to]){
				dis[v.to] = v.val + dis[e.to];
				if (!Walked[v.to]) Q.push({v.to, dis[v.to]});
			}
		}
	}
	return dis[to];
}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	freopen("subway.in", "r", stdin);
	freopen("subway.out", "w", stdout);
	
	cin >> c >> n >> m >> d >> q;
	for (int i = 1; i <= m; i++) cin >> w[i];
	for (int i = 1; i <= n; i++){
		cin >> k;
		for (int j = 1; j <= k; j++){
			cin >> a >> t;
			Lnk[m + i].push_back({a, t});
			Lnk[a].push_back({m + i, t});
		} 
	}
	for (;q--;){
		cin >> x >> y;
		cout << dij(x, y) + w[x] + w[y] << "\n";
	}
	
	return 0;
}
