#include<iostream>
#include<vector>
#include<algorithm>
#define ep emplace
#define eb emplace_back
#define pb push_back
#define pq priority_queue
#define vc vector
#define pii pair<int, int>
#define gt greater
#define umap unordered_map
#define memset(dest, val, n) __builtin_memset(dest, val, n)
#define fillinf(x) memset((x), 0x3f, sizeof(x))
#define fillninf(x) memset((x), 0xc0, sizeof(x))
#define fillzero(x) memset((x), 0, sizeof(x))
#define ll long long
#define ull unsigned long long
#define closeios() ios::sync_with_stdio(false);cin.tie(0)
#define fropen(x) freopen(x".in", "r", stdin);freopen(x".out", "w", stdout)
template<typename... Args>
void errorf(const char* format, Args... arg){fprintf(stderr, format, arg...);}
#define int long long
using namespace std;

const int maxn=555, maxm=500555;
int c, n, m, d, q, w[maxm], k[maxn];
int dis[maxn][maxn];
vc<pii> conn[maxm];

signed main(){
	fropen("subway");
	closeios();
	fillinf(dis);
	cin >> c >> n >> m >> d >> q;
	for(int i=1;i<=m;i++){
		cin >> w[i];
	}
	for(int i=1;i<=n;i++){
		cin >> k[i];
		for(int j=1;j<=k[i];j++){
			int v, t;
			cin >> v >> t;
			conn[v].eb(i, t);
		}
	}
	for(int i=1;i<=n;i++) dis[i][i] = 0ll;
	for(int i=1;i<=m;i++){
		for(int j=0;j<conn[i].size();j++){
			for(int k=0;k<conn[i].size();k++){
				pii u=conn[i][j];
				pii v=conn[i][k];
				dis[u.first][v.first] = min(dis[u.first][v.first], u.second+v.second);
				dis[v.first][u.first] = min(dis[v.first][u.first], u.second+v.second);
			}
		}
	}
	for(int k=1;k<=n;k++) for(int i=1;i<=n;i++) for(int j=1;j<=n;j++){
		dis[i][j] = min(dis[i][j], dis[i][k]+dis[k][j]);
	}
	for(int i=1;i<=q;i++){
		int x, y;
		cin >> x >> y;
		int ans=1e18;
		for(int j=0;j<conn[x].size();j++) for(int k=0;k<conn[y].size();k++){
			pii u=conn[x][j];
			pii v=conn[y][k];
			ans = min(ans, dis[u.first][v.first]+u.second+v.second);
		}
		cout << ans+w[x]+w[y] << "\n";
	}
	return 0;
}