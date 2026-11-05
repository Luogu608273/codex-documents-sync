#include<bits/stdc+++.h>
using namespace std;
int u[100005];
int v[100005];
int main(){
	freopen("hub.in","r",stdin);
	freopen("hub.out","w",stdout);
	int c,t,minn=999999;
	cin>>c>>t>>endl;
	int n,k;
	cin>>n>>k;
	for(int i=1;i<=n-1;i++){
		cin>>u[i]>>v[i];
		if(u[i]<=minn||v[i]<=minn){
			minn=min(u[i],v[i]);
		} 
	}
	cout<<minn<<minn+1; 
	
	return 0;
}
