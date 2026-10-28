#include<iostream>
#include<vector>
#include<map>

using namespace std;
typedef long long ll;
typedef unsigned long long ull;

const int N = 5e3 + 10, D = 210, bs = 35492133, mod = 998244853;
int n, k, q, u, v, i, pw[D], s, fahs[N], ans = 0, fa[D][N];
ull pw2[D], s2, fahs2[N];
vector<int> vc[D][N]; map<pair<int, ull>, int> mp;

void upd1(int u, int i, int v){
	int val = --mp[{fahs[u], fahs2[u]}];
	if(val == 0) mp.erase({fahs[u], fahs2[u]});
	ans -= val;
	fahs[u] = (fahs[u] - ((ll)fa[i][u]*pw[i]%mod) + mod) % mod;
	fahs2[u] -= (ull)fa[i][u]*pw2[i];
	fa[i][u] = v;
	vc[i][v].push_back(u);
	fahs[u] = (fahs[u] + (ll)fa[i][u]*pw[i]%mod) % mod;
	fahs2[u] += (ull)fa[i][u]*pw2[i];
	val = mp[{fahs[u], fahs2[u]}]++;
	ans += val;
}

void upd(int u, int i, int v){
	for(int p: vc[i][u]){
		upd1(p, i, v);
	}
	vc[i][u].clear();
}

int fr(int u, int i){
	if(fa[i][u] == u) return u;
	upd(u, i, fr(fa[i][u], i));
	return fa[i][u];
}

void mg(int u, int v, int i){
	u = fr(u, i); v = fr(v, i);
	if(u == v) return;
	if(vc[i][u].size() <= vc[i][v].size()) upd(u, i, v);
	else upd(v, i, u);
}

int main(){
	ios::sync_with_stdio(0);
	cin.tie(0); cout.tie(0);
	cin >> k >> n >> q;
	pw[1] = s = 1;
	pw2[1] = s2 = 1;
	for(int i = 2; i <= k; i++){
		pw[i] = (ll)pw[i-1] * bs % mod;
		s = (s + pw[i]) % mod;
		pw2[i] = pw2[i-1] * bs;
		s2 += pw2[i];
	}
	for(int i = 1; i <= n; i++){
		fahs[i] = (ll)i*s%mod;
		fahs2[i] = (ull)i*s2;
		mp[{fahs[i], fahs2[i]}] = 1;
	}
	for(int i = 1; i <= k; i++){
		for(int j = 1; j <= n; j++){
			fa[i][j] = j;
			vc[i][j].push_back(j);
		}
	}
	while(q--){
		cin >> u >> v >> i;
		mg(u, v, i);
		cout << n+ans*2 << '\n';
	}
	return 0;
}
