#include<set>
#include<map>
#include<ctime>
#include<cmath>
#include<queue>
#include<stack>
#include<cstdio>
#include<vector>
#include<string>
#include<bitset>
#include<cstring>
#include<cstdlib>
#include<numeric>
#include<iostream>
#include<algorithm>
using namespace std;
const int MAXN=5e5+10;
const int N=5e5;
const int INF=0x3f3f3f3f;
const long long LINF=0x3f3f3f3f3f3f3f3f;
int n,ans=1;
long long m;
long long a[MAXN];
inline void solve(){
	scanf("%d%lld",&n,&m);
	for(int i=1;i<=n;i++)
	{
		scanf("%lld",&a[i]);
	}
	sort(a+1,a+1+n);
	int p=1;
	long long s=0;
	for(int i=2;i<=n;i++)
	{
		s+=(a[i]-a[i-1])*(i-p);
		while(s>m)
		{
			s-=a[i]-a[p];
			p++;
		}
		ans=max(ans,i-p+1);
	}
	printf("%d\n",ans);
}
signed main(){
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",stdout);
	#ifdef LOCAL
	atexit([](){fprintf(stderr,"%.3lfs\n",(double)clock()/CLOCKS_PER_SEC);});
	#endif
	solve();
	return 0;
}