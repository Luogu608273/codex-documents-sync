#include<bits/stdc++.h>
using namespace std;
#define int long long
typedef long long ll;
const int N=5e9+5;
int n,m;
ll a[N];
ll b[N];
ll sum[N];
bool check(){
	ll cnt=0;
	int x;
	for(int i=1;i<=n;i++){
		cnt+=i*b[i];
	}
	if(cnt<=m) {
		return 1;
	}
	for(int i=x;i<n;i++){
		cnt=cnt-sum[i]+b[i+1]*x;		
	}
	if(cnt<=m){
		return 1;
	}
}
void sovel(){
	cin>>n>>m;
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}
	sort(a+1,a+n+1);
	for(int i=2;i<=n;i++){
		b[i-1]=a[i]-a[i];
	}
}
int main(){
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",stdout);
	return 0;
}
