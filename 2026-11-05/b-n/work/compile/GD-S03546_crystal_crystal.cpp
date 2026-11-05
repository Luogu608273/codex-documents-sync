#include<iostream>
#include<algorithm>
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
using namespace std;

const int maxn=514514;
int n, m, a[maxn], b[maxn], ans;

bool check(int mid, int i){
	return mid*a[i]-(b[i-1]-b[i-mid-1])<=m;
}

int bs(int i){
	int l=0, r=i-1, ret=-1;
	while(l<=r){
		int mid=((l+r)>>1);
		if(check(mid, i)){
			l = mid+1;
			ret = mid;
		}
		else{
			r = mid-1;
		}
	}
	return ret;
}

int main(){
	fropen("crystal");
	closeios();
	cin >> n >> m;
	for(int i=1;i<=n;i++){
		cin >> a[i];
	}
	sort(a+1, a+n+1);
	for(int i=1;i<=n;i++) b[i] = b[i-1]+a[i];
	for(int i=1;i<=n;i++) ans = max(ans, bs(i)+1);
	cout << ans;
	return 0;
}