#include<bits/stdc++.h>
using namespace std;
int n,m,a[999999],s[999999],sum,maxx;
int main(){
	fropen("crystal.in","r",stdin);
	fropen("crystal.out","w",stdout);
	cin>>n>>m;
	for(int i=1;i<=n;i++){
		cin>>a[i];
		s[i]=a[i]+a[i-1];
	}
	for(int i=1;i<=n;i++){
		int j=i+1;
		while(abs(a[j]*(j-1)-s[j-1]+s[i-1])<=m){
			maxx=max(maxx,j-i+1);
			j++;
		}
	}
	cout<<maxx;
	return 0;
}
