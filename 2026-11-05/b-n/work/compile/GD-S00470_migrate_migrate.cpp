#include <bits/stdc++.h> 
#define ll long long
using namespace std;
const int N = 2e6 + 10;
ll c,T,n,m,x,a[N];
ll ans;
inline void solve(){
	scanf("%d%d",&n,&m);
	for(ll i = 1;i <= n;i ++){
		scanf("%lld",a + i);		
	}for(ll i = 2;i <= n;i ++){
		if(i == 2){
			x = a[i] - a[i - 1];
		}else if(x != a[i] - a[i - 1]){
			f = true;
		}
	}if(!f){
		if(x <= m){
			ans = 0;
			for(ll i = 1;i <= n - 3;i ++){
				ans += dfs(i);
			}printf("%lld\n",ans);
		}else{
			printf("0\n");
		}
	}
}
int main(){
	freopen("migrate.in","r",stdin);
	freopen("migrate.out","w",strout);
	scanf("%d%d",&c,&T);
	while(T --){
		solve();
	}return 0;
}
