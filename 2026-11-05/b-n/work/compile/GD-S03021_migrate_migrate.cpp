#include<bits/stdc++.h>
namespace KH{
using namespace std;
#define int long long
int c,n,d;
vector<int> x;
void solve1(){
	vector<vector<int> > f(n+1,vector<int> (n+1));
	f[1][1]=1;
	int lsr=1;
	vector<int> now(n+1);
	for(int l=1,r=1;l<=n;l++){
		while(x[r+1]-x[l]<=d&&r+1<=n) r++;
		for(int i=l;i<=lsr;i++){
			now[l]+=f[l][i];
			for(int j=i+1;j<=r;j++){
				f[j][r]+=f[l][i];
			}
		}
		lsr=r;
	}
	int ans=0;
	for(int i=1;i<=n;i++){
		if(now[i]==2) ans++;
	}
	cout<<ans<<'\n';
}
void solve(){
	cin>>n>>d;
	x.resize(n+1);
	for(int i=1;i<=n;i++)
		cin>>x[i];
	solve1();
}
void main(){
	freopen("migrate.in","r",stdin);
	freopen("migrate.out","w",stdout);
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int T=1;
	cin>>c>>T;
	while(T--){
		solve();
	}
}
#undef int
}
int main(){KH::main();}
