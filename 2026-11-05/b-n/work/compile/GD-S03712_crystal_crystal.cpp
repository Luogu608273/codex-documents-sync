#include<bits/stdc++.h>
using namespace std;
long long n,m,a[500000+10],sum=0,k=0,b[500000+10],xiaom;
int main(){
 	freopen("crystal.in","r","stdin");
	freopen("crystal.out","w","stdout");
	cin>>n>>m;
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}
	sort(a+1,a+n+1);
	for(int i=1;i<=n;i++){
		sum=0;
		xiaom=m;
		for(int j=1;j<=n;j++){	
			if(j!=i&&abs(a[j]-a[i])<=xiaom&&xiaom>0) sum++,xiaom=xiaom-abs(a[j]-a[i]);
		}
		b[i]=sum;
	}
	long long maxn=0;
	for(int i=1;i<=n;i++){
		maxn=max(maxn,b[i]);
	}
	cout<<maxn+1;
	return 0;
} 

