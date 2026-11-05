#include<bits/stdc++.h>
using namespace std;
int n,m;
int a[500000+10],ans=0,sum[500000+10],r;
int main(){
	freopen("crystal.in","r",std.in);
	freopen("crystal.out","w",std.out);
	scanf("%d%d",&n,&m);
	for(int i=1;i<=n;i++){
		scanf("%d",&a[i]);
	}
	sort(a+1,a+n+1);
	for(int i=1;i<=n;i++){
		sum[i]=sum[i-1]+a[i+1]-a[i];
	}
	for(int l=1;l<=n;l++){
		while(m!=0){
			if(r>=n){
				break;
			}
			else{
				r++; 
			}
			if(sum[r]-sum[l]>m){
				break;
			}
			if(r-l+1>ans){
				ans=r-l;
			}
		}
	}
	cout<<ans;
	return 0;
} 

