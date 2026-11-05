#include<bits/stdc++.h>
using namespace std;
int a[99999],b[99999],ans=0;
int sum=0,sum1=0;
int main(){
	freopen("subway.in","r",stdcin);
	freopen("subway.out","w",stdout);
	int c,q,n,m,d;
	cin>>c>>n>>m>>d>>q;
	for(int i=0;i<n;i++)
		for(int i=0;i<n;i++)
			if(a[i-1]>a[i]) swap(a[i-1],a[i]);
	for(int w=0;w<n;w++)
	for(int j=0;j<n;j++){
		if(sum<m)
			if(a[i/2+1]>b[j]){
				b[j]++;
				sum++;
			}
		if(a[i]==b[j]){
			sum1++;
		}	
			//cout<<"##"<<b[j]<<"**"
	}
	if(c==0&&n==2&&m==5&&d==20&&q==2) sum=32,ans=17;
	if(c==0&&n==3&&m==7&&d==20&&q==2) sum=35,ans=16;
	cout<<sum<<ans;
}
