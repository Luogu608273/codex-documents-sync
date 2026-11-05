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
const int MAXN=512;
const int MAXM=5e5+10;
const int INF=0x3f3f3f3f;
const long long LINF=0x3f3f3f3f3f3f3f3f;
int n,m,q;
int a[MAXM];
vector <pair<int,int>> G[MAXM];
long long d[MAXN][MAXN];
inline void solve(){
	scanf("%*d%d%d%*d%d",&n,&m,&q);
	for(int i=1;i<=m;i++)
	{
		scanf("%d",&a[i]);
	}
	for(int i=1;i<=n;i++)
	{
		int k;
		scanf("%d",&k);
		while(k--)
		{
			int x,w;
			scanf("%d%d",&x,&w);
			G[x].push_back({i,w});
		}
	}
	for(int i=1;i<=n;i++)
	{
		memset(d[i],0x3f,sizeof(long long)*(n+1));
		d[i][i]=0;
	}
	for(int i=1;i<=m;i++)
	{
		for(auto [x,p]:G[i])
		{
			for(auto [y,q]:G[i])
			{
				d[x][y]=min(d[x][y],(long long)p+q);
			}
		}
	}
	for(int k=1;k<=n;k++)
	{
		for(int i=1;i<=n;i++)
		{
			for(int j=1;j<=n;j++)
			{
				d[i][j]=min(d[i][j],d[i][k]+d[k][j]);
			}
		}
	}
	while(q--)
	{
		int u,v;
		scanf("%d%d",&u,&v);
		long long res=LINF;
		for(auto [x,p]:G[u])
		{
			for(auto [y,q]:G[v])
			{
				res=min(res,d[x][y]+p+q);
			}
		}
		res+=a[u]+a[v];
		printf("%lld\n",res);
	}
}
signed main(){
	freopen("subway.in","r",stdin);
	freopen("subway.out","w",stdout);
	#ifdef LOCAL
	atexit([](){fprintf(stderr,"%.3lfs\n",(double)clock()/CLOCKS_PER_SEC);});
	#endif
	solve();
	return 0;
}