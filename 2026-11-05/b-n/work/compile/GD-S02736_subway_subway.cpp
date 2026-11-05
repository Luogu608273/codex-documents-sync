#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N=5e5+10 ,M=1e5+10;
int c ,n ,m ,d ,q;
int w[N] ,k[510] ,a[N][510] ,t[N][510] ,x[M] ,y[M];
int main(){
	ios::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);
	freopen("subway.in" ,"r" .stdin);
	freopen("subway.out" ,"w" ,stdout);
	cin >> c >> n >> m >> d >> q;
	for(int i=1;i <= m;i++){
		cin >> w[i];
	} 
	for(int i=1;i <= n;i++){
		cin >> k[i];
		for(int j=1;j <= k[i];j++){
			cin >> a[i][j] >> t[i][j];
		}
	}
	for(int i=1;i <= q;i++){
		cin >> x[i] >> y[i];
		cout << x[i]+y[i] << '\n';
	}
	return 0;
}
