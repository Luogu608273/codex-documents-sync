#include<iostream>
#define ep emplace
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

const int maxn=555;
int n, d, a[maxn], dis[maxn][maxn], ans, cnt;

// 32 pts.

void dfs(int l, int r, int cur, int dd){
	if(cnt>=3) return;
	if(cur==r){
		if(dis[l][r]==dd){
			cnt++;
		}
		return;
	}
	for(int i=cur+1;i<=r;i++){
		if(cnt>=3) return;
		if(a[i]-a[cur]<=d){
			dfs(l, r, i, dd+1);
		}
	}
}

signed main(){
	fropen("migrate");
	closeios();
	int c, t;
	cin >> c >> t;
	if(c==12||c==13){
		while(t--){
			cin >> n >> d;
			int x, y;
			for(int i=1;i<n;i++){
				cin >> x;
			}
			cin >> y;
			if(n==1){
				cout << "0\n";
				continue;
			}
			int k=y-x;
			if(d<=k){
				cout << "0\n";
				continue;
			}
			cout << max(0ll, n-d/k*2+1) << "\n";
		}
		return 0;
	}
	while(t--){
		ans = 0;
		fillinf(dis);
		cin >> n >> d;
		for(int i=1;i<=n;i++){
			cin >> a[i];
		}
		for(int i=1;i<=n;i++){
			for(int j=i;j<=n;j++){
				if(a[j]-a[i]<=d){
					dis[i][j] = 1;
					dis[j][i] = 1;
				}
			}
		}
		for(int k=1;k<=n;k++) for(int i=1;i<=n;i++) for(int j=1;j<=n;j++){
			dis[i][j] = min(dis[i][j], dis[i][k]+dis[k][j]);
		}
		for(int i=1;i<=n;i++){
			for(int j=i+1;j<=n;j++){
				cnt = 0;
				dfs(i, j, i, 0);
				if(cnt==2){
					ans++;
				}
			}
		}
		cout << ans << "\n";
	}
	return 0;
}
