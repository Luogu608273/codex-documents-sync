#include<bits/stdc++.h>
using namespace std;
long long n,m;
long long a[500010],b[500010];
long long last=1,ans=1;
bool cmp(long long x,long long y){
	return x<y;
}
int main(){
	freopen("crystal.in","r","stdin");
	freopen("crystal.out","w","stdout");
	scanf("%lld%lld",&n,&m);
	for(long long i=1;i<=n;i++){
		scanf("%lld",&a[i]);
	}
	sort(1+a,1+a+n,cmp);
	for(long long i=2;i<=n;i++){
		m-=(i-last)*(a[i]-a[i-1]);
		while(m<0){
			m+=(a[i]-a[last]);
			last++;
		}
		ans=max(ans,i-last+1);
	}
	printf("%lld",ans);
	return 0;
}
