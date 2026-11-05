#include<iostream>
#include<vector>
#include<queue>
#include<cstring>
#include<bitset>
#include<cstdio>
#define ll long long
using namespace std;
const int N=1e3+7,M=6e5+7;
const ll inf = 1e18+7;
int C,n,m,emx,q;
vector< pair<int,ll> > G[M];
ll a[M],dist[M],dis[N][N];
queue<int> Q0;
priority_queue< pair<ll,int> ,vector< pair<ll,int> >,greater< pair<ll,int> > > Q;
void bfs(int s){
	while(!Q0.empty()) Q0.pop();
	bitset<M> b;
	dist[s+m]=0;Q0.push(s+m);b[s+m]=1;
	while(!Q0.empty()){
		int u=Q0.front();Q0.pop();
		for(auto &p : G[u]){
			int v=p.first;ll w=p.second;
			if(!b[v]){
				dist[v]=dist[u]+w;
				b[v]=1;
				Q0.push(v);
			}
		}
	}
	for(int t=1;t<=n;t++) dis[s][t]=dist[t+m];
}
void dijkstra(int s){
	while(!Q.empty()) Q.pop();
	memset(dist,0x3f,sizeof(dist));
	dist[s+m]=0;Q.push({0,s+m});
	while(!Q.empty()){
		int u=Q.top().second;ll d=Q.top().first;Q.pop();
		if(d!=dist[u]) continue;
		for(auto &p : G[u]){
			int v=p.first;ll w=p.second;
			if(dist[v]>dist[u]+w){
				dist[v]=dist[u]+w;
				Q.push({dist[v],v});
			}
		}
	}
	for(int t=1;t<=n;t++) dis[s][t]=dist[t+m];
}
int main(){
	freopen("subway.in","r",stdin);
	freopen("subway.out","w",stdout);
	scanf("%d%d%d%d%d",&C,&n,&m,&emx,&q);
	for(int i=1;i<=m;i++) scanf("%lld",&a[i]);
	for(int i=1;i<=n;i++){
		int len;scanf("%d",&len);
		for(int j=1;j<=len;j++){
			int u;ll x;
			scanf("%d%lld",&u,&x);
			G[u].push_back({m+i,x});
			G[m+i].push_back({u,x});
		}
	}
	memset(dis,0x3f,sizeof(dis));
	for(int u=1;u<=n;u++) 
		if(16<=C&&C<=19) bfs(u);
		else dijkstra(u);
//	for(int u=1;u<=n;u++)
//		for(int v=1;v<=n;v++)
//			printf("%d %d %lld\n",u,v,dis[u][v]);
	while(q--){
		int u,v;ll ans=inf;
		scanf("%d%d",&u,&v);
		if(u==v){
			printf("0\n");
			continue;
		}
		for(auto &p : G[u]){
			for(auto &g : G[v]){
				int c=p.first,d=g.first;ll w1=p.second,w2=g.second;
//				printf("	%d %d %d %d %lld %lld %lld \n",c,d,c-m,d-m,w1,w2,dis[c-m][d-m]);
				ans=min(ans,w1+dis[c-m][d-m]+w2);
			}
		}
		ans+=a[u]+a[v];
		printf("%lld\n",ans);
	}
	return 0;
} 
