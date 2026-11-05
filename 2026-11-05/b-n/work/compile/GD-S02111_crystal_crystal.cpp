#include<bits/stdc++.h>
using namespace std;
long long n,m,a[500055],ans;
int main(){
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",stout);
	cin>>n>>m;
	for(int i=1;i<=n;i++){
	cin>>a[i];
	}
	while(ans<m){
		ans++;
		if(m>=(a[1]-a[2])*ans)m-=(abs(a[2]-a[1])*ans);

	}
	cout<<ans<<endl;
	return 0; 
}
