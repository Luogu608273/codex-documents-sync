#include <iostream>
#include <bitset>
#include <cstring>
#include <cstdio>
#include <queue>

using namespace std;
long long c, t;
long long n, d, ans=0;
long long X[2000900];
long long dis[2000900];
long long num[2000900];
long long End[2000900];

bitset<600090> Walked;

queue<long long> Q;

void dfs(long long x, long long len){
//	cout << "point: " << x << "; len: " << len << "\n";
	for (int e = x + 1; e <= End[x]; e++){
		if (dis[e] == len + 1) num[e]++;
		dfs(e, len+1);
	}
}
void dij(long long s){
	dis[s] = 0;
	Q.push(s);
	while (!Q.empty()){
		long long e = Q.front();
		Q.pop();
		if (Walked[e]) continue;
		for (int p = e + 1; p <= End[e]; p++){
			if (1 + dis[e] < dis[p]){
				dis[p] = 1 + dis[e];
				if (!Walked[p]) Q.push(p);
			}
		}
	}
}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	
	freopen("migrate.in", "r", stdin);
	freopen("migrate.out", "w", stdout);
	cin >> c >> t;
	for (;t--;){
		
		ans = 0; 
		cin >> n >> d;
		for (int i = 1; i <= n; i++) cin >> X[i];
		for (int i = 1; i <= n; i++){
			long long R = n, L = i + 1, A=0;
			while (L <= R){
				int mid = (R + L) >> 1;
				if (X[mid] <= d + X[i]) L = mid + 1, A = mid;
				else R = mid - 1; 
			}; End[i] = A;
		}
		for (int u = 1; u <= n; u++){
			memset(dis, 0x0f, sizeof dis);
			memset(num, 0, sizeof num);
			dij(u);
			dfs(u, 0);
			for (int v = u + 1; v <= n; v++) if (num[v] == 2) ans++;
		}
		cout << ans << "\n";
	}
	return 0;
} 
