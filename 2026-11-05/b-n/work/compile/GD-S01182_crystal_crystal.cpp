#include <bits/stdc++.h>
using namespace std;
void solve();
int main() {
	freopen("crystal.in", "r", stdin);
	freopen("crystal.out", "w", stdout);
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	int T = 1;
//	cin >> T;
	while (T--) solve();
	return 0;
}
#define int long long
void solve() {
	int n, m;
	cin>> n >> m;
	vector<int> a(n+1), s(n+1);
	for (int i = 1; i <= n; i++) cin >> a[i];
	sort(a.begin()+1, a.end());
	for (int i = 1; i <= n; i++) s[i] = s[i-1] + a[i];
	auto check=[&](int x)->bool {
		bool k = 0;
		for (int i = x; i <= n; i++) {
			int u = a[i] * (x-1), v = s[i-1] - s[i-x];
			if (u-v <= m) {
				k = 1;
				break;
			}
		}
		return k;
	};
	int l = 0, r = n;
	while (l < r) {
		int mid = (l+r) >> 1;
		if (check(mid+1)) l = mid+1;
		else r = mid;
	}
	cout << l << "\n";
	return ;
}
