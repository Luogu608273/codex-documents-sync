#include<iostream>
#include<algorithm>
using namespace std;
const int N = 2e5 + 10;
int t, n, k, c[N], ans[N], cnt[N];
struct pii{
	int x, y, z, id;
} a[N];
bool cmp1(pii x, pii y){
	if(x.x == y.x){
		if(x.y == y.y) return x.z < y.z;
		return x.y < y.y;
	}
	return x.x < y.x;
}
bool cmp2(pii x, pii y){
	if(x.y == y.y) return x.z < y.z;
	return x.y < y.y;
}
void add(int x, int y){
	while(x <= k){
		c[x] += y;
		x += x & -x;
	}
}
int qry(int x){
	int res = 0;
	while(x){
		res += c[x];
		x -= x & -x;
	}
	return res;
}
void solve(int l, int r){
	if(l == r) return;
	int mid = (l + r) / 2;
	solve(l, mid);
	solve(mid+1, r);
	int sz1 = mid - l + 1, sz2 = r - mid;
	sort(a + l, a + mid + 1, cmp2);
	sort(a + mid + 1, a + r + 1, cmp2);
	int j = l, mx = 0;
	for(int i = mid+1; i <= r; i++){
		while(j <= mid && a[j].y <= a[i].y){
			add(a[j++].z, 1);
		}
		ans[a[i].id] += qry(a[i].z);
	}
	for(int i = l; i < j; i++){
		add(a[i].z, -1);
	}
	sort(a + l, a + r + 1, cmp1);
}
int main(){
	cin >> n >> k;
	for(int i = 1; i <= n; i++){
		cin >> a[i].x >> a[i].y >> a[i].z;
		a[i].id = i;
	}
	sort(a + 1, a + 1 + n, cmp1);
	solve(1, n);
	sort(a + 1, a + 1 + n, cmp1);
	for(int i = n-1; i >= 1; i--){
		if(a[i].x == a[i+1].x && a[i].y == a[i+1].y && a[i].z == a[i+1].z){
			ans[a[i].id] = ans[a[i+1].id];
		}
	}
	for(int i = 1; i <= n; i++) cnt[ans[i]]++;
	for(int i = 0; i < n; i++) cout << cnt[i] << '\n';
	return 0;
}
