#include<bits\stdc++.h>
using namespace std;
long long n,m,t,s,r,im;
long long a[500005],d[500005];
int main(){
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",stdout);
	cin>>n>>m;
	if(n<=10000){
		for(long long i=1;i<=n;i++) cin>>a[i];
		for(long long i=1;i<=n-1;i++){
			for(int j=2;j<=n-i+1;j++){
				if(a[j-1]>a[j]){
					t=a[j];
					a[j]=a[j-1];
					a[j-1]=t;
				}
			}
		}
		for(long long i=2;i<=n;i++){
			d[i]=a[i]-a[i-1];
		}
		for(long long i=3;i<=n;i++) d[i]=d[i-1]+d[i]*(i-1);
		for(s=2;s<=n;s++){
			if(d[s]>m) break;
		}
		cout<<s-1;
	}
	else{
		r=a[2]-a[1];
		for(im=1;im<=n;im++){
			if((im+1)*im*0.5*r>m) break;
		}
		if((im+1)*im*0.5*r>m) cout<<im;
		else cout<<im-1;
	}
}
