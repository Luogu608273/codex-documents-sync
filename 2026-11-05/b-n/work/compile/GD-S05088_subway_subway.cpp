#include<bits/stdc++.h>
//priority_queue<int,vector<int>,greater<int> > q;
using namespace std;
int c,n,m,d,q,ans;
int w[500005],dis[500005];
bool vis[500005];
struct edge{
	int u,v,t;
};
edge g[505];
bool cmp(edge x,edge y)
{
	return x.t<y.t;
}
void dij(int s,int p)
{
	memset(dis,0x3f,sizeof(dis));
	dis[s]=0;
	for(int i=1;i<=n;i++)
	{
		if(g[i].u==s)
		{
			for(int j=1;j<=n;j++)
			{
				if(g[j].u==g[i].v)
				{
					int u=g[i].v,v=g[j].v;
					if(vis[u]==1) continue;
					if(dis[v]>dis[u]+g[j].t)
					{
						dis[v]=dis[u]+g[j].t;
						vis[j]=1;
					}
				}
			}
			vis[i]=1;
		}
	}
}
int main(){
	freopen("subway.in","r","stdin");
	freopen("subway.out","w","stdout");
	ios::sync_with_stdio(false);
	cin.tie(0);
	cin>>c>>n>>m>>d>>q;
	for(int i=1;i<=m;i++)
	{
		cin>>w[i];
	}
	for(int i=1;i<=m;i++)
	{
		int k;
		cin>>k;
		for(int j=1;j<=k;j++)
		{
			int a,p;
			cin>>a>>p;
			//e.push_back({i,a,p});
			g[i].u=i;
			g[i].v=j;
			g[i].t=p;
		}
	}
	sort(g+1,g+n+1,cmp);
	for(int i=1;i<=q;i++)
	{
		int u,v;
		cin>>u>>v;
		dij(u,v);
		ans=dis[v]+w[u]+w[v];
		cout<<ans<<"\n";
	}
	return 0;
}
