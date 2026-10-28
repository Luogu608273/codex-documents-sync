#include<iostream>
#include<string>

using namespace std;

string s, t;
int n, in[52], to[52], cnt, nn = 52;
bool vis[52], fg;

int c_to_s(char c){
	if('A' <= c && c <= 'Z') return c - 'A';
	return c - 'a' + 26;
}

void dfs(int u, int st){
	if(to[u] == -1) return;
	vis[u] = 1; if(u != to[u]) cnt++;
	if(to[u] == st && u != to[u]){
		if(nn) cnt++;
		else fg = 1;
		return;
	}
	if(vis[to[u]]) return;
	dfs(to[u], st);
}

int main(){
	cin >> n;
	while(n--){
		cin >> s >> t; cnt = 0; nn = 52; fg = 0;
		for(int i = 0; i < 52; i++) to[i] = -1, in[i] = vis[i] = 0;
		for(int i = 0; i < s.size(); i++){
			if(to[c_to_s(s[i])] == -1){
				to[c_to_s(s[i])] = c_to_s(t[i]);
				if(!in[c_to_s(t[i])]) nn--;
				in[c_to_s(t[i])]++;
			}
			else if(to[c_to_s(s[i])] != c_to_s(t[i])){
				fg = 1;
			}
		}
		for(int i = 0; i < 52; i++){
			if(fg) break;
			if(!in[i] && !vis[i]) dfs(i, i);
		}
		for(int i = 0; i < 52; i++){
			if(fg) break;
			if(!vis[i]) dfs(i, i);
		}
		if(fg) cout << -1 << '\n';
		else cout << cnt << '\n';
	}
	return 0;
}
