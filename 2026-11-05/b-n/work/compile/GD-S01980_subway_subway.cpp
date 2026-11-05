#include<bits/stdc++.h>
using namespace std;
int c,n,m,d,q;
int w[10005],k[10005],a[10005],t[10005];
int main(){
	freopen("subway.in","r",stdin);
	freopen("subway.out","w",sdtout);
	cin >> c >> n >> m >> d >> q;
	for(int i = 1;i <= m;i++)cin >> w[i];
	for(int i = 1;i <= n;i++){
		cin >> k[i];
		for(int j = 1;j <= k[i];j++){
			cin >> a[i][j] >> t[i][j];
		}
	}
	for(int i = 1;i <= q;i++){
		int x,y;
		cin >> x >> y;
		cout << w[x] + t[x][x] + (t[x][2]+ t[2][2]) + t[2][y] + w[y] <<"\n";
	}
	fclose(stdin);
	fclose(stdout);
	return 0;
}
