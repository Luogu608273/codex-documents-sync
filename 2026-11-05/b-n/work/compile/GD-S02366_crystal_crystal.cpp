#include<bits/stdc++.h>
#define IL inline 
#define ll long long
#define ull unsigned long long
#define i128 __int128
#define ri register int
#define F(i,a,b) for(ri i=a;i<=b;i++)
#define FF(i,a,b) for(ri i=b;i>=a;i--)
#define vec vector
using namespace std;
const int N=1e6+5;
const ll inf=0x3f3f3f3f3f3f3f3fLL;
const double eps=1e-9;
int n;
ll m,a[N],ans;
IL bool check(ll x){
	ll res=m;
	F(i,1,n){
		if(a[i]>=x) continue;
		else if(res>=x-a[i]) res-=x-a[i];
		else return 0; 
	}
	return 1;
}
int main(){
	ios::sync_with_stdio(false);
	cin.tie(0);
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",sdtout);
	cin>>n>>m;
	F(i,1,n) cin>>a[i];	
	sort(a+1,a+n+1);
	ll l=a[1],r=a[n];
	while(l<r){
		int mid=(l+r+1)>>1;
		if(check(mid)) l=mid;
		else r=mid-1;
	}
	F(i,1,n){
		if(a[i]==l) ans++;
		else if(m>=abs(l-a[i])) m-=abs(l-a[i]),ans++;
	}
	cout<<ans;
	return 0;
}
/*
关注洛谷 UID 1542698 的用户喵
上午 J 爆炸了下午 S 复仇之战

样例 1: 
in:
5 5
1 2 4 8 9 
out:
3
样例 2:
in:
5 8
-3 -1 2 2 7 
out:
4

AFOed. 

*/
