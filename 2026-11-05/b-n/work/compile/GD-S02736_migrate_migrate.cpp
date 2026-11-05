#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N=2e6+10;
int n ,d;
int x[N];

int main(){
	ios::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);
	freopen("migrate.in" ,"r" .stdin);
	freopen("migrate.out" ,"w" ,stdout);
	int c ,t;
	cin >> c >> t;
	for(int i=1;i <= t;i++){
		cin >> n >> d;
		for(int j=1;j <= n;j++){
			cin >> x[j];
		}
		int ans=0;
		for(int j=1;j <= n;j++){
			for(int k=j;k <= n;k++){
				int t=(k-j)+1;
				if(t > d && t%d==1) ans++;
			}
		}
		cout << ans << '\n';
	}
	return 0;
}
