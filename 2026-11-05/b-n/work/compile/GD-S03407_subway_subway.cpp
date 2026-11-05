//Author: mairuisheng
//#pragma GCC optimize(3)
#include<cstdio>
#include<vector>
#include<queue>
#include<bitset>
#define int long long
using namespace std;
inline int read()
{
	int x=0,f=1;
	char s;
	s=getchar();
	while(s<48||s>57)
	{
		if(s=='-')f=-f;
		s=getchar();
	}
	while(s>47&&s<58)
	{
		x=(x<<3)+(x<<1)+s-48;
		s=getchar();
	}
	return x*f;
}
constexpr int N=505,M=5e5+5,MAX=1e18;
struct Node
{
	int to,val;
}b[N],c[N];
int n,m,d,q;
int a[M];
vector<Node> g[N+M];
int f[N][N];
signed main()
{
	freopen("subway.in","r",stdin);
	freopen("subway.out","w",stdout);
	read();
	n=read();
	m=read();
	d=read();
	q=read();
	int i,j,k,s,t,va,tot,tot2;
	for(i=1;i<=m;++i)a[i]=read();
	for(i=1;i<=n;++i)
	{
		s=read();
		while(s--)
		{
			t=read();
			va=read();
			g[i].push_back({t+n,va});
			g[t+n].push_back({i,va});
		}
	}
	for(i=1;i<=n;++i)
	{
		for(j=1;j<=n;++j)
		{
			if(i!=j)f[i][j]=MAX;
		}
	}
	for(i=n+1;i<=n+m;++i)
	{
		tot=0;
		for(Node tmp:g[i])b[++tot]=tmp;
		for(j=1;j<=tot;++j)
		{
			for(k=1;k<=tot;++k)
			{
				if(j!=k)
				{
					s=b[j].to;
					t=b[k].to;
					va=b[j].val+b[k].val;
					f[s][t]=f[t][s]=min(f[s][t],va);
				}
			}
		}
	}
	for(k=1;k<=n;++k)
	{
		for(i=1;i<=n;++i)
		{
			if(i==k)continue;
			for(j=1;j<=n;++j)
			{
				if(i==j||j==k)continue;
				f[i][j]=min(f[i][j],f[i][k]+f[k][j]);
			}
		}
	}
	while(q--)
	{
		s=read();
		t=read();
		tot=tot2=0;
		va=MAX;
		for(Node tmp:g[s+n])b[++tot]=tmp;
		for(Node tmp:g[t+n])c[++tot2]=tmp;
		for(i=1;i<=tot;++i)
		{
			for(j=1;j<=tot2;++j)va=min(va,b[i].val+c[j].val+f[b[i].to][c[j].to]);
		}
		printf("%lld\n",va+a[s]+a[t]);
	}
	return 0;
}
