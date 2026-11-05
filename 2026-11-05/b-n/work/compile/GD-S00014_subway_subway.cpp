#include<bits/stdc++.h>
using namespace std;

int c,n,m,d,q,x,y,k,t;
int ans[100005],cnt[100004];
int w[5000005],a[505][500005];



int main(){
	fropen("subway.in","r",stdin);
	fropen("subway.out","w",stdout);
	cin >> c >> n >> m >> d >> q;

	for(int i=1;i<=m;i++){
		cin >> w[i];
	}
	for(int i=1;i<=n;i++){
		cin >> k;
		cnt[i]=2*k;
		for(int j=1;j<=2*k;j++){
			
			cin >> a[i][j];
		}
	}
	
	for(int i=1;i<=q;i++){
		cin >> x >> y;
		ans[i]+=w[x]+w[y];
		for(int y=1;y<=n;y++){
			for(int j=1;j<=cnt[y];j+=2){
				for(int k=1;k<=cnt[y+1];k+=2){
					if(a[y][j]==a[y+1][k]){
						ans[i]+=a[y][j-1]+a[y][k-1];
					}
				}
			}
		}
	}
	for(int i=1;i<=q;i++){
		cout << ans[i] << endl;
	}
}
