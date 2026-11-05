#include <bits/stdc++.h>
using namespace std;
int main(){
	freopen("crystal.in","r","stdin");
	freopen("crystal.out","w","stdout");
	ios::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);
	long long n, m,a[100005],d[100005];
	cin>>n>>m;
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}
	long long z=0;
	for(int i=1;i<=n;++i){
		if(a[i]==a[i+1]){
			z++;
		}
	}
	if(z==n-1){
		cout<<n;
		return 0;
	}
	
	for(int i=1;i<=n;i++){
		long long t=0,sum=0,y=0;
		for(int j=1;j<=n;j++){
			int b=a[j];
			while(b>m){
				b=a[b+1];
			}
			//cout<<b<<" ";
			if(i==j){
				break;
			}
			for(int k=b;k<=a[i];k++){
				if(b==a[i] and t<=m){
					k=a[i]+1;
					sum++;
					y=1;
					//cout<<a[j];
					//cout<<"*"<<b<<"*";
				}
				t++;
				b++;
				//cout<<"a";
			}
			if(y==1){
				t--;
				y=0;
				//cout<<"y";
			}
			
			//cout<<b;
		}
		if(t>0){
			//cout<<sum<<endl;
			d[i+n]=sum;
			t=0;
			sum=0;
			
		}
		//cout<<a[i];
		//cout<<"a"<<endl;
	}
	long long max=0;
	for(int i=1;i<=n+m+1;i++){
		if(d[i]>max){
			max=d[i];
		}
	}
	if(max==0){
		cout<<1;
		return 0;
	}
	cout<<max+1;
	return 0;
} 
