#include<iostream>
#include<string>
#include<unordered_map>

using namespace std;
typedef long long ll;

const int N = 3e4 + 10, base = 13331, mod = 1e9 + 3;
int n, l, _, nn; ll ans = 0;
string s[N]; unordered_map<int, int> mp; 

int ctox(char c){
	if('a' <= c && c <= 'z') return c - 'a' + 1;
	else if('A' <= c && c <= 'Z') return c - 'A' + 27;
	else if('0' <= c && c <= '9') return c - '0' + 53;
	else if(c == '_') return 63;
	else if(c == '@') return 64;
	return 65;
}

int hs(string s){
	int res = 0;
	for(int i = 0; i < l; i++){
		res = ((ll)res * base + ctox(s[i])) % mod;
	}
	return res;
}

int main(){
	cin >> n >> l >> _;
	for(int i = 0; i < n; i++){
		cin >> s[i];
	}
	for(int j = 0; j < l; j++){
		for(int i = 0; i < n; i++){
			char c = s[i][j];
			s[i][j] = '#';
			mp[hs(s[i])]++;
			s[i][j] = c;
		}
		for(auto i: mp){
			ans += (ll)i.second * (i.second-1) / 2;
		}
		mp.clear();
	}
	cout << ans;
	return 0;
} 
