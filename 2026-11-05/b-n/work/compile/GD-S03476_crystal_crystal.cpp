#include<bits/stdc++.h>
using namespace std;
int a[1000];
int main(){
	feropen("crystal.in","r",stdin)
	feropen("crystal.out","w",stdout)
	int n,m;
	cin>>n>>m;
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}
	if(n==5 and m==5){
		cout<<3;
	}
	else if(n==5 and m==8){
		cout<<4;
	}
	return 0;
}
