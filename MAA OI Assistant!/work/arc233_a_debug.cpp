#include<iostream>
#include<bitset>
#include<string>

using namespace std;

const int N = 2e5 + 10;
int t, n, a[N], cnt, ans;
bool fg, vis[N]; bitset<N> bt;
string s;

int main(){
	cin >> t;
	while(t--){
		cin >> n; ans = -1; cnt = 0;
		for(int i = 1; i <= n; i++) vis[i] = 0;
		for(int i = 1; i <= n/2; i++){
			cout << "? " << i << endl;
			cin >> s;
			if(s == "-1") return 0;
			vis[i] = (s == "Yes");
			cnt += vis[i];
		}
		if(cnt <= n/4) fg = 1;
		else fg = 0;
		for(int i = n/2+1; i < n; i++){
			if(vis[n-i] == fg){
				cout << "? " << i << endl;
				cin >> s;
				if(s == "-1") return 0;
				vis[i] = (s == "Yes");
				if(vis[i] == fg){
					ans = 2;
					break;
				}
			}
		}
		if(ans == 2){
			cout << "! 2" << endl;
			continue;
		}
		for(int i = n/2+1; i < n; i++){
			vis[i] = vis[n-i]^1;
		}
		cnt = 0;
		for(int i = 1; i < n; i++) cnt += vis[i];
		if(cnt < n/2){
			cout << "! 2" << endl;
			continue;
		}
		bt.reset();
		bt[0] = 1;
		for(int i = 1; i < n; i++) if(vis[i]) bt |= (bt << i);
		if(bt[n]) cout << "! 3" << endl;
		else cout << "! -1" << endl;
	}
	return 0;
}
