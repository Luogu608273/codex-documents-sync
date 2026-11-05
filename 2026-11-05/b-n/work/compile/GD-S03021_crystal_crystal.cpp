#include<bits/stdc++.h>
namespace KH{
using namespace std;
#define int long long
void solve(){
	int n,m;
	cin>>n>>m;
	vector<int> a(n+1);
	for(int i=1;i<=n;i++) cin>>a[i];
	sort(a.begin()+1,a.end());
	int ans=0;
	vector<int> b(n+1);
	for(int i=1;i<=n;i++){
		b[i]=b[i-1]+a[i];
		int l=0,r=i+1;
		while(l+1<r){
			const int Mid=((r-l)>>1)+l;
			if(Mid>0&&a[i]*(i-Mid)-b[i-1]+b[Mid-1]<=m) r=Mid;
			else l=Mid;
		}
		ans=max(i-r+1,ans);
	}
	cout<<ans<<'\n';
}
void main(){
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",stdout);
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int T=1;
	while(T--){
		solve();
	}
}
#undef int
}
int main(){KH::main();}
