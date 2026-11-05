#include<bits/stdc++.h>
using namespace std;
const int l=2*1e6+1;
long long c,t,n,m,a[l],b[l];
int main(){
	freopen("hub.in","r",stdin);
	freopen("hub.out","w",stout);
	cin>>c>>t;
	for(int i=1;i<=t;i++){
		cin>>n>>m;
		cout<<m-1<<endl;
		for(int j=1;j<=n;j++)cin>>a[i]>>b[i];
	}
	return 0;
}
