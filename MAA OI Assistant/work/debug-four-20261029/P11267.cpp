#include<iostream>
#include<string>

using namespace std;
typedef long long ll;

const ll N = 2e5 + 10, mod = 1e9 + 7;
ll n, q, f[N][70], g[N][70];
ll m, s, k;
string ss;

int main(){
	ios::sync_with_stdio(false); cin.tie(nullptr);
	cin >> n >> m >> q >> ss;
	for(ll i = 0; i < n; i++){
		f[i][0] = -1;
	}
	ll u = -1;
	for(ll i = (m%n)+n-1+((m%n==0)*n); i >= 0; i--){
		if(u != -1) while(u - i > m%n+((m%n==0)*n) || ss[u%n] == '0'){
			u--;
			if(u == i){
				u = -1; break;
			}
		}
		if(m > n && ss[i%n] == '1' && u == -1){
			u = i;
		}
		if(u != -1 && u - i <= m%n+((m%n==0)*n) && i < n){
			if(u >= n) g[i][0] = 1, f[i][0] = u-n;
			else f[i][0] = u;
		}
		if(ss[i%n] == '1' && u == -1){
			u = i;
		}
	}
	ll bk = -1;
	for(ll i = 0; i < n; i++){
		if(ss[i] == '1') bk = i;
	}
	u = -1;
	for(ll i = 0; i < n; i++){
		if(ss[i] == '1') u = i;
		if(f[i][0] == -1){
			if(m > n){
				if(bk == -1){
					f[i][0] = i+1;
					if(f[i][0] == n) f[i][0] = 0, g[i][0] = 1;
				}
				else if(u != -1){
					f[i][0] = u;
					g[i][0] = m/n % mod;
				}
				else{
					f[i][0] = bk;
					g[i][0] = (m/n-1) % mod;
				}
			}
			else{
				f[i][0] = i+1;
				if(f[i][0] == n) f[i][0] = 0, g[i][0] = 1;
			}
		}
		else g[i][0] = (m/n-(m%n==0) + g[i][0]) % mod;
	}
	for(ll j = 1; j < 70; j++){
		for(ll i = 0; i < n; i++){
			f[i][j] = f[f[i][j-1]][j-1];
			g[i][j] = (g[i][j-1] + g[f[i][j-1]][j-1]) % mod;
		}
	}
	while(q--){
		cin >> s >> k; s--;
		ll cnt = s / n % mod;
		s %= n;
		for(ll i = 60; i >= 0; i--){
			if(k & (1ll << i)){
				cnt = (g[s][i] + cnt) % mod;
				s = f[s][i];
			}
		}
		cout << ((ll)cnt*n%mod+s+1) % mod << '\n';
	}
	return 0;
}
