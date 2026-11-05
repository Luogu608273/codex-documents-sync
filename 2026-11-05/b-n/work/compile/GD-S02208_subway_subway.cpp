#include<bits/stdc++.h>
using namespace std;
int w[500005],a[500005];
vector<vector<pair<int, int>>> e;
int main()
{
	freopen("subway.in","r",stdin);
	freopen("subway.out","w".stdout);
	int c,n,m,d,Q;
	cin >> c >> n >> m >> d >> Q;
	for(int i=1;i<=m;i++) cin >> w[i];
	for(int i=1;i<=n;i++){
		int k1;
		cin >> k1;
		for(int j=1;j<=k1;j++){
			int t;
			cin >> a[i] >> t;
		}
		for(int j=1;j<=k1;j++){
			for(int k=1;k<=k1;k++) e[a[j]].push_back({a[k],a[j]+a[k]});
		}
	}
	while(Q--){
		int x,y,minn=0x3f3f3f3f,cur=0;
		cin >> x >> y;
		vector<vector<pair<int,int>>> q;
		q.push_back(e[x]);
		while(!q.empty()){
			int cnt=0;
			vector<pair<int, int>> qt=q[cur++];
			for(auto p:qt){
				if(p.first==y){
					minn=min(minn,cnt);
					cnt=0;
				} else {
					q.push_back(e[p.first]);
					cnt+=p.second;
				}
			}
		}
		cout << minn << ' ';
	}
	return 0;
}
