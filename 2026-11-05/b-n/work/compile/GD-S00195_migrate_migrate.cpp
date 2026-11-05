#include<bits/stdc++.h>
#define int long long
#define inf 0x3f3f3f3f3f3f3f3f
#define pll pair<int,int>
using namespace std;

int read() {
	int res=0,f=1;
	char ch=getchar();
	while(!isdigit(ch)) {
		if(ch=='-') f=-1;
		ch=getchar();
	}
	while(isdigit(ch)) {
		res=(res<<1)+(res<<3)+(ch^48);
		ch=getchar();
	}
	return res*f;
}
void write(int x) {
	if(x<0) putchar('-'),x=-x;
	if(x>9) write(x/10);
	putchar(x%10+'0');
}

const int maxn=5e5+5;

int C,T;
int n,d,x[maxn];

vector<pll> G[maxn];

priority_queue<pll,vector<pll>,greater<pll>> q;
int dis[maxn];
int cnt[maxn];

void dij(int st) {
	
	memset(cnt,0,sizeof(cnt));
	memset(dis,0x3f,sizeof(dis));
	dis[st]=0,q.push({0ll,st});
	
	while(!q.empty()) {
		
		auto [d,u]=q.top();
		q.pop();
		
		if(d>dis[u]) continue;
		
		for(auto [v,w]:G[u]) {
			
			if(dis[v]>dis[u]+w) {
				
				dis[v]=dis[u]+w;
				cnt[v]=1;
				q.push({dis[v],v});
			}
			else if(dis[v]==dis[u]+w) cnt[v]++;
		}
	}
}

void solve() {
	
	n=read(),d=read();
	
	int ans;
	
	for(int i=1;i<=n;i++) x[i]=read();
	
	for(int i=1;i<=n;i++) {
		
		for(int j=1;j<=n;j++) {
			
			if(i==j) continue;
			
			G[i].push_back({j,abs(x[i]-x[j])});
			G[j].push_back({i,abs(x[i]-x[j])});
		}
	}
	
	for(int i=1;i<=n;i++) {
		
		dij(i);
		
		for(int j=1;j<=n;j++) 
			if(cnt[j]==2) ans++;
	}
	write(ans),putchar('\n');
}

signed main() {

	freopen("migrate.in","r",stdin);
	froepen("migrate.out","w",stdout);
	
	C=read(),T=read();
	
	while(T--) solve();

	return 0;
}
