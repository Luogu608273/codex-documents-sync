#include<iostream>
#include<string>
#include<unordered_map>

using namespace std;
typedef long long ll;

const int N = 3e4 + 10, base = 13331, mod = 1e9 + 3, mod2 = 1e9 + 7;
int n, l, _, h[N], hh[N], pw[210], pp[210]; ll ans = 0;
string s[N]; unordered_map<ll, int> mp;

int ctox(char c){
	if('a' <= c && c <= 'z') return c - 'a' + 1;
	else if('A' <= c && c <= 'Z') return c - 'A' + 27;
	else if('0' <= c && c <= '9') return c - '0' + 53;
	else if(c == '_') return 63;
	else if(c == '@') return 64;
	return 65;
}

int hs(const string &s, int md){
	int res = 0;
	for(int i = 0; i < l; i++){
		res = ((ll)res * base + ctox(s[i])) % md;
	}
	return res;
}

int main(){
	ios::sync_with_stdio(false); cin.tie(nullptr);
	cin >> n >> l >> _;
	pw[0] = pp[0] = 1;
	for(int i = 1; i <= l; i++){
		pw[i] = (ll)pw[i-1] * base % mod;
		pp[i] = (ll)pp[i-1] * base % mod2;
	}
	for(int i = 0; i < n; i++){
		cin >> s[i];
		h[i] = hs(s[i], mod);
		hh[i] = hs(s[i], mod2);
	}
	mp.reserve(n * 2);
	for(int j = 0; j < l; j++){
		for(int i = 0; i < n; i++){
			int c = ctox(s[i][j]);
			int x = (h[i] - (ll)c * pw[l-j-1] % mod + mod) % mod;
			int y = (hh[i] - (ll)c * pp[l-j-1] % mod2 + mod2) % mod2;
			mp[(ll)x * mod2 + y]++;
		}
		for(auto i: mp){
			ans += (ll)i.second * (i.second-1) / 2;
		}
		mp.clear();
	}
	cout << ans;
	return 0;
}
