#include<bits/stdc++.h >
using namespace std;
int a[500005];
int c[500005];
int d[500005];
int n,m;
int main(){
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",stdout);
	cin>>n>>m;
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}
	sort(a,a+n);
	int g=1;
	for(int i=1;i<n;i++){
		c[i]=a[i+1]-a[i];
		d[i]=c[i]*g+d[i-1];
		g++;
	}
	int cnt=0;
	for(int i=1;i<=n;i++){
		for(int j=i;j<=n;j++){
			int k=d[j-1]-d[i-1]-(i-1)*c[j-1];
			if(k<=m&&j-i+1>cnt){
				cnt=j-i+1;
			}
		}
	}
	cout<<cnt;
}
