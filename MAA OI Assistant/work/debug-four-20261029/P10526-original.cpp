#include<iostream>
#include<string>
#include<vector>

using namespace std;

int s_to_i(char s){
	if (s >= 'a' && s <= 'z'){
		return s - 'a';
	}
}
const int N = 1e6 + 10, M = 1e5 + 10;

struct Tree{
	int data[N][26], id, cnt[N], end[N];
	vector<int> vec[N];
	
	void setup(){
		for(int i = 0; i < N; i++){
			for(int j = 0; j < 26; j++){
				data[i][j] = 0;
			}
			cnt[i] = 0;
			end[i] = -1;
		}
		id = 0;
	}
	
	void insert(string s, int idx){
		int cur = 0;
		for(int i = 0; i < s.size(); i++){
			int p = s_to_i(s[i]);
			if(data[cur][p] == 0) data[cur][p] = ++id;
			cur = data[cur][p];
			vec[cur].push_back(idx);
		}
		end[cur] = idx;
	}
	
	string query(string s){
		int cur = 0;
		for(int i = 0; i < s.size(); i++){
			int p = s_to_i(s[i]);
			if(data[cur][p] == 0){
				return "N";
			}
			cur = data[cur][p];
		}
		int num = vec[cur].size();
		while(true){
			bool flag = false;
			int tmp = -1;
			for(int i = 0; i < 26; i++){
				if(data[cur][i] != 0 && tmp == -1) tmp = i;
				else if(data[cur][i] != 0) flag = true;
			}
			cur = data[cur][tmp];
			if(flag || tmp == -1 || num != vec[cur].size()) break;
			else s += (tmp + 'a');
		}
		return s;
	}
	
	int find_str(string s){
		int cur = 0;
		for(int i = 0; i < s.size(); i++){
			int p = s_to_i(s[i]);
			if(data[cur][p] == 0){
				return -1;
			}
			cur = data[cur][p];
		}
		return end[cur];
	}
};

Tree tr;
int n, m;
string s, p, tmp;

int main(){
	tr.setup();
	cin >> n >> m;
	for(int i = 1; i <= n; i++){
		cin >> s;
		tr.insert(s, i);
	}
	cin >> s;
	for(int i = 0; i < s.size(); i++){
		if(s[i] >= 'a' && s[i] <= 'z'){
			p += s[i];
		}
		else if(s[i] == 'B'){
			if(p.size() > 0) p = p.substr(0, p.size() - 1); 
		}
		else if(s[i] == 'T'){
			tmp = tr.query(p);
			if(tmp != "N") p = tmp;
		}
		else if(s[i] == 'E'){
			cout << tr.find_str(p) << ' ';
			p = "";
		}
//		cout << p << endl;
	}
	return 0;
}
//
//10 1
//ab
//abc
//abcd
//abcde
//ccb
//ccd
//ccde
//e
//g
//x
//aTEccTeEeEgExE
