#include<bits/stdc++.h>
namespace KH{
using namespace std;
#define int long long
const int INF=0x3f3f3f3f3f3f3f3f;
int c,n,m,d,q;
vector<int> w,k;
vector<vector<int> > a,t;
vector<pair<int,int> > query;
void solve__1_8(){
	const int INF=0x3f3f3f3f3f3f3f3f;
	vector<vector<int> > ed(m+1,vector<int> (m+1,INF));
	for(int i=1;i<=m;i++) ed[i][j]=0;
	for(int i=1;i<=n;i++){
		for(int ui=1;ui<=k[i];ui++){
			const int &u=a[i][ui];
			for(int vi=1;vi<=k[i];vi++){
				if(ui==vi) continue;
				const int &v=a[i][vi];
				ed[u][v]=ed[v][u]=min(ed[u][v],t[i][ui]+t[i][vi]); 
			}
		}
	}
	vector<vector<int> > dist(m+1,vector<int> (m+1,INF));
	for(int i=1;i<=m;i++){
		dist[i][i]=0;
		for(int k=1;k<=m;k++){
			for(int j=1;j<=m;j++){
				dist[i][j]=min(dist[i][j],dist[i][k]+dist[k][j]);
			}
		}
	}
}
void solve(){
	cin>>c>>n>>m>>d>>q;
	w.resize(m+1);
	for(int i=1;i<=m;i++) cin>>w[i];
	k.resize(n+1),a.resize(n+1),t.resize(n+1);
	int sksksk=0;
	for(int i=1;i<=n;i++){
		cin>>k[i];
		sksksk+=k[i];
		a[i].resize(k[i]+1),t[i].resize(k[i]+1);
		for(int j=1;j<=k[i];j++)
			cin>>a[i][j]>>t[i][j];
	}
	query.resize(q+1);
	for(int i=1;i<=q;i++) cin>>query[i].first>>query[i].second;
	if(c>=1&&c<=8||(c==0&&sksksk<=400&&n<=200&&q<=200)) {solve__1_8();return;}
}
void main(){
	freopen("subway.in","r",stdin);
	freopen("subway.out","w",stdout);
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
