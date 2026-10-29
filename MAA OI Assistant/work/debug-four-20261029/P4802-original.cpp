#include<iostream>
#include<vector>

using namespace std;

const int N = 30, M = 1e6 + 5e4, inf = 1e9;
int n, m, a[N][N], f[N][M], u, v, w, z = 0, ans = inf;
vector<int> state[N];

int cnt(int x){
	int res = 0;
	while(x){
		res++;
		x -= x & -x;
	}
	return res;
}

int main(){
	cin >> n >> m; z = (1 << n);
	for(int i = 0; i < n; i++){
		for(int j = 0; j < n; j++) a[i][j] = -inf;
	}
	while(m--){
		cin >> u >> v >> w;
		a[u][v] = w;
	}
	for(int i = 0; i <= z; i++){
		state[cnt(i)].push_back(i);
	}
	for(int i = 0; i < n; i++){
		for(int j = 0; j <= z; j++){
//			if(cnt(j) > 1) cout << i << ' ' << j << '\n';
			f[i][j] = -inf;
		}
	}
	f[0][1] = 0;
	for(int i = 1; i < n; i++){
		for(int j: state[i]){
			for(int s = 0; s < n; s++){
				if((j & (1 << s))){
					for(int k = 0; k < n; k++){
						if((j & (1 << k)) == 0){
//							cout << s << ' ' << j << ' ' << k << ' ' << (j|(1 << k)) << ' ' << f[k][j|(1 << k)] << ' ';
							f[k][j|(1 << k)] = max(f[k][j|(1 << k)], f[s][j] + a[s][k]);
//							cout << "-> " << f[k][j|(1 << k)] << '\n';
						}
					}
				}
			}
		}
	}
//	for(int i = 0; i < n; i++){
//		for(int j: state[5]){
//			cout << i << ' ' << j << ' ' << f[i][j] << '\n';
//		}
//	}
	
//	for(int i = 0; i < n; i++) ans = min(ans, f[i][z-1]);
	cout << f[n-1][z-1];
	return 0;
} 
