#include<bits/stdc++.h>
using namespace std;
int n,m,ans;
long long d,a[2000000+10];
bool vis[2000000+10];
int sum=0;
void dfs(int b){
	if(a[b]==m){
		sum++;
		return;
	}
	while(a[b]<=d){
		b++; 
		if(vis[b]==1) continue;
		vis[b]=1;
		dfs(b);
		vis[b]=0;		
	}
}
int main(){
	freopen("hub.in","r",std.in);
	freopen("hub.out","w",std.out);
	int c,t;
	cin>>c>>t;
	while(t--){
		cin>>n>>d;
//		for(int i=1;i<=2000000+10;i++){
//			vis[i]=1;
//      }
		for(int i=1;i<=n;i++){
			scanf("%lld",&a[i]);
		}	
		for(int i=1;i<=n;i++){
			for(int j=i+1;j<=n;j++){
				sum=0;
				m=a[j];
				dfs(i);
				if(sum==2){
					ans++;
				}
			}
		}
		cout<<ans<<endl;
	}
	return 0;
} 

