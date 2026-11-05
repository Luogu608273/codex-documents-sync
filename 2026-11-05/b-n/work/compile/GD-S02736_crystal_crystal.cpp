#include<bits/stdc++.h>
using namespace std;
typedef long long ll;
const int N=5e5+10;
int n;
ll m;
ll a[N];
bool check(int x){
	ll cnt=0 , res=0 ,Min=0x3f3f3f3f3f3f3f3f;
	for(int i=n-x+1;i < n;i++){
		cnt+=a[n]-a[i];
	}
	Min=min(Min ,cnt);
	for(int i=n-1;i >= x;i--){
		ll res=cnt-(x-1)*(a[i+1]-a[i])+(a[i]-a[i-x+1]);
		cnt=res;
		Min=min(Min ,res);
	}
	return Min <= m;
}
int main(){
	ios::sync_with_stdio(0);
	cin.tie(0);
	cout.tie(0);
	freopen("crystal.in" ,"r" .stdin);
	freopen("crystal.out" ,"w" ,stdout);
	cin >> n >> m;
	for(int i=1;i <= n;i++){
		cin >> a[i];
	}
	sort(a+1 ,a+n+1);
	int l=1 ,r=n ,ans=1;
	while(l <= r){
		int mid=(l+r)/2;
		if(check(mid)){
			l=mid+1;
			ans=mid;
		}else{
			r=mid-1;
		}
	}
	cout << ans << '\n';
	return 0;
}
