#include<bits/stdc++.h>
using namespace std;
const int l=5001;
long long c,t,f[l][l],vis[l][l],n,m,a[l],ans;
int main(){
	freopen("migrate.in","r",stdin);
	freopen("migrate.out","w",stout);
	cin>>c>>t;
	for(int i=1;i<=t;i++){
		cin>>n>>m;
		ans=0;
		memset(vis,0,sizeof(vis));
		for(int j=1;j<=n;j++){
			for(int k=1;k<=n;k++){
				f[j][k]=1e9;
			}
		}
		for(int j=1;j<=n;j++){
			cin>>a[j];
			if(j>=2&&abs(a[j]-a[j-1])<=m){
				f[j][j-1]=abs(a[j]-a[j-1]);
				f[j-1][j]=abs(a[j]-a[j-1]);
			}
		}
		for(int k=1;k<=n;k++){
			for(int o=1;o<=n;o++){
				for(int p=1;p<=n;p++){
					if(f[o][p]==f[o][k]+f[k][p]){
					vis[o][p]++;
					}
					else if(f[o][p]>f[o][k]+f[k][p]){
					f[o][p]=f[o][k]+f[k][p];
					vis[o][p]=1;
					}
				}
			}
		}
	for(int j=1;j<=n;j++){
			for(int k=1;k<=n;k++){
				 if(vis[j][k]==2)ans++;
			}
		}
		if(ans%2==1)ans++;
		cout<<ans/2<<endl;
	}
	return 0;
}
