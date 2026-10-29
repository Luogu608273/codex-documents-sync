#include<iostream>
#include<string>

using namespace std;

int s_to_i(char s){
	return s - 'a';
}

const int N = 1e6 + 10;

struct Tree{
	int data[N][26], id, fa[N], end[N], to[N];

	void setup(){
		for(int i = 0; i < N; i++){
			for(int j = 0; j < 26; j++){
				data[i][j] = 0;
			}
			fa[i] = to[i] = 0;
			end[i] = -1;
		}
		id = 0;
	}

	void insert(string s, int idx){
		int cur = 0;
		for(int i = 0; i < s.size(); i++){
			int p = s_to_i(s[i]);
			if(data[cur][p] == 0){
				data[cur][p] = ++id;
				fa[id] = cur;
			}
			cur = data[cur][p];
		}
		end[cur] = idx;
	}

	void build(){
		for(int cur = id; cur >= 0; cur--){
			to[cur] = cur;
			if(end[cur] != -1) continue;
			int tmp = -1;
			for(int i = 0; i < 26; i++){
				if(data[cur][i] != 0){
					if(tmp == -1) tmp = i;
					else{
						tmp = -2; break;
					}
				}
			}
			if(tmp >= 0) to[cur] = to[data[cur][tmp]];
		}
	}

	int query(int cur){
		return to[cur];
	}

	int find_str(int cur){
		return end[cur];
	}
};

Tree tr;
int n, m, cur = 0, cnt = 0;
string s;

int main(){
	ios::sync_with_stdio(false); cin.tie(nullptr);
	tr.setup();
	cin >> n >> m;
	for(int i = 1; i <= n; i++){
		cin >> s;
		tr.insert(s, i);
	}
	tr.build();
	cin >> s;
	for(int i = 0; i < s.size(); i++){
		if(s[i] >= 'a' && s[i] <= 'z'){
			int p = s_to_i(s[i]);
			if(cnt || tr.data[cur][p] == 0) cnt++;
			else cur = tr.data[cur][p];
		}
		else if(s[i] == 'B'){
			if(cnt) cnt--;
			else cur = tr.fa[cur];
		}
		else if(s[i] == 'T'){
			if(!cnt) cur = tr.query(cur);
		}
		else if(s[i] == 'E'){
			cout << (cnt ? -1 : tr.find_str(cur)) << ' ';
			cur = cnt = 0;
		}
	}
	return 0;
}
