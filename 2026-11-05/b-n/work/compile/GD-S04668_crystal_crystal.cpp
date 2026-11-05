#include<bits/stdc++.h>
using namespace std;
int main(){
	freopen("crystal.in","r","stdin");
	freopen("crystal.out","w","stdout");
	long long n,m,middle,c,c1,d;
	cin>>n>>m;
	int a[n];
	for(int i=0;i<n;i++){
		cin>>a[i];
		middle+=a[i]; 
	}
	sort(a,a+n);
	middle/=n;
	for(int i=0;i<n;i++){
		if(a[i]==a[i+1]){
			continue;
		}
		if(a[i]<=middle&&a[i+1]>middle){
			c=a[i];
			c1=i;
			break;
		}
		d+=a[i];
	}
	while(1){
		if(c1<0){
			break;
		}
		if(c*c1-d<=m&&(c1+1)*a[c1+1]-d>m){
			cout<<c1+1;
			return 0;
		}else if(c*c1-d>m){
			c1-=1;
			c=a[c1];
		}else if((c1+1)*a[c1+1]-d<=m){
			c1+=1;
			c=a[c1];
		}
		d=0;
		for(int i=0;i<n;i++){
			d+=a[i];
		}
	}
	return 0;
}

