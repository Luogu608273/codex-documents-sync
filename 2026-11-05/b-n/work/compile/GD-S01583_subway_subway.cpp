#include<bits/stdc++.h>
#define int long long
using namespace std;
int n,m,x,y,z,a[500005],b[500005],c[500005],ans=0,xl,yl;
void dfs(int s){
	for(int i=s;i<=m;i++){
		ans+=c[i];
		if(b[i]==yl)return;
	}
	for(int i=s;i<=m;i++){
		ans+=c[i];
		for(int j=i+1;j<=m;j++){
			if(b[j]==b[i]){
				i=j;
			}
		}
		if(b[i]==yl)return;
	}
}
signed main(){
	freopen("subway.in","r",stdin);
	freopen("subway.out","w",stdiout);
	cin>>n>>m>>x>>y>>z;
	for(int i=1;i<=x;i++)cin>>a[i];
	for(int i=1;i<=m;i++){
		cin>>n;
		for(int j=1;j<=m;j++)cin>>b[i]>>c[i];
	}
	while(z--){
		cin>>xl>>yl;
		ans+=a[xl]+a[yl];
		for(int i=1;i<=m;i++){
			if(b[i]==a[i]){
				dfs(i);
                cout<<ans<<endl;
				break;
			}
		}
		ans=0;
	}
	return 0;
}
