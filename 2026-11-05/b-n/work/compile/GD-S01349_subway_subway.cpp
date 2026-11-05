#include<bits/stdc++.h>
using namespace std;
long long c,n,m,d,q;
struct nod{
	long long id,t;
};
vector<nod> times[500010];
long long dis[500010],w[500010];
vector<pair<long long,long long> > question[100010];
set<long long> kkk;
long long ans[100010];
long long xxx,yy,zz;
int vis[500010];

long long as[500010],cnt=2;
struct node{
	long long star,en,belong,last;
}head[1000010];
void build(long long x,long long y,long long senx){
	head[cnt].star=x;
	head[cnt].en=y;
	head[cnt].last=as[x];
	head[cnt].belong=senx;
	as[x]=cnt;
	cnt++;
}
void dijie(long long x){
	memset(dis,0x3f3f3f3f3f3f,sizeof(dis));
	memset(vis,0,sizeof(vis));
	dis[x]=w[x];
	queue<pair<long long,long long> > p;
	p.push({x,0});
	vis[x]=1;
	while(!p.empty()){
		long long v22=p.front().first,v33=p.front().second;
		vis[v22]=0;
		p.pop();
		for(long long i=as[v22];i;i=head[i].last){
			long long u=head[i].en;
			if(head[i].belong==v33){
				if(dis[u]>dis[v22]){
					dis[u]=dis[v22];
					if(!vis[u]){
						p.push({u,head[i].belong});
						vis[u]==1;
					}
				}
			}
			else{
				long long k11=0,k22=0;
				for(nod l:times[v22]){
					if(l.id==v33){
						k11=l.t;
					}
					if(l.id==head[i].belong){
						k22=l.t;
					}
				}
				if(dis[u]>dis[v22]+k11+k22){
					dis[u]=dis[v22]+k11+k22;
					if(!vis[u]){
						p.push({u,head[i].belong});
						vis[u]==1;
					}
				}
			}
		}
	}
	return;
}
int main(){
	freopen("subway.in","r","stdin");
	freopen("subway.out","w","stdout");
	scanf("%lld%lld%lld%lld%lld",&c,&n,&m,&d,&q);
	for(long long i=1;i<=m;i++){
		scanf("%lld",&w[i]);
	}
	for(long long i=1;i<=n;i++){
		scanf("%lld",&zz);
		for(long long j=1;j<=zz;j++){
			long long xx=xxx;
			scanf("%lld%lld",&xxx,&yy);
			times[xxx].push_back({i,yy});
			if(j>=2){
				build(xx,xxx,i);
				build(xxx,xx,i);
			} 
		}
	}
	for(long long i=1;i<=q;i++){
		scanf("%lld%lld",&xxx,&yy);
		kkk.insert(xxx);
		question[xxx].push_back({yy,i});
	}
	for(long long i:kkk){
		dijie(i);
		for(auto j:question[i]){
			ans[j.second]=dis[j.first]+w[j.first];
		}
	}
	for(long long i=1;i<=q;i++){
		printf("%lld\n",ans[i]);
	}
	return 0;
}

