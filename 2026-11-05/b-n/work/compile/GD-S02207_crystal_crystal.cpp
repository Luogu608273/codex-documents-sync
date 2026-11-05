#include<bits\stdc++.h>
using namespace std;
long long n,m,a[100005];
int main(){
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",stdout);
	cin>>n>>m;
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}
	sort(a+1,a+n+1);
	int k=0,s=1;
	for(int i=1;i<=n;i++){
		int v=a[i+1]-a[i];
		if(k+v*i<=m){
			k+=v*i;
		}
		else{
			s=i;
			break;
		}
	}
	cout<<s;
	return 0;
}
