#include <bits/stdc++.h>
#define endl '\n'
using namespace std;

const int M = 5400010, B = 27;
int n, q, nn;
string s1, s2, t1, t2;

struct Node{
	int nex[B], fal, w;
} t[M];

string mg(string &s1, string &s2){
	int l = 0, r = (int)s1.size() - 1;
	while(s1[l] == s2[l]) l++;
	while(s1[r] == s2[r]) r--;
	return s1.substr(0, l) + '#' + s1.substr(l, r-l+1)
		+ s2.substr(l, r-l+1) + '#' + s1.substr(r+1);
}

void add(string &s){
	int p = 0;
	for(char c: s){
		int x = c == '#' ? 26 : c - 'a';
		if(!t[p].nex[x]) t[p].nex[x] = ++nn;
		p = t[p].nex[x];
	}
	t[p].w++;
}

void bfs(){
	queue<int> q;
	for(int i = 0; i < B; i++){
		if(t[0].nex[i]) q.push(t[0].nex[i]);
	}
	while(q.size()){
		int u = q.front(); q.pop();
		t[u].w += t[t[u].fal].w;
		for(int i = 0; i < B; i++){
			if(!t[u].nex[i]) t[u].nex[i] = t[t[u].fal].nex[i];
			else{
				int v = t[u].nex[i];
				t[v].fal = t[t[u].fal].nex[i];
				q.push(v);
			}
		}
	}
}

int query(string &s){
	int p = 0, ans = 0;
	for(char c: s){
		int x = c == '#' ? 26 : c - 'a';
		p = t[p].nex[x];
		ans += t[p].w;
	}
	return ans;
}

int main(){
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cin >> n >> q;
	for(int i = 1; i <= n; i++){
		cin >> s1 >> s2;
		if(s1 == s2) continue;
		string s = mg(s1, s2);
		add(s);
	}
	bfs();
	while(q--){
		cin >> t1 >> t2;
		if(t1.size() != t2.size()){
			cout << 0 << endl;
			continue;
		}
		string s = mg(t1, t2);
		cout << query(s) << endl;
	}
	return 0;
}
