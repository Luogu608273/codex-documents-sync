#include<bits/stdc++.h>
using namespace std;
long long n,m;
long long a[500005];
long long b[500005];
int ans=0;
int main(){
	cin>>n>>m;
	freopen("crystal.in","r","stdin");
	freopen("crystal.out","w","stdout");
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}
	sort(a+1,a+n+1);
	for(int i=1;i<n;i++){
		b[i]=abs(a[i+1]-a[i]);
	}
	long long num=0;
	for(int i=1;i<n;i++){
		num+=b[i]*i;
		if(num>m){
			cout<<i;
			return 0;
		}
	}
	if(ans==0)cout<<n;
}
