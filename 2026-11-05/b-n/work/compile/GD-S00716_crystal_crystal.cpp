#include <bits/stdc++.h>
#define int long long
#define N 500005
#define rep(x, y, z) for (int x = y; x <= z; x++)
#define rrep(x, y, z) for (int x = y; x >= z; x--)
#define chmax(x, y) x = max(x, y)
using namespace std;
int n, m, a[N], id, ans, cnt;
#undef int
int main() {
#define int long long
	ios::sync_with_stdio(0), cin.tie(0);
	freopen("crystal.in", "r", stdin), freopen("crystal.out", "w", stdout);
	cin >> n >> m;
	rep (i, 1, n) cin >> a[i];
	sort(a + 1, a + 1 + n);
	id = n - 1, cnt = ans = 1;
	rrep (i, n, 1) {
		if (id < 1) break;
		while (id >= 1 && a[i] - a[id] <= m) {
			m -= a[i] - a[id];
			id--;
			if (id != i) cnt++;
		}
		chmax(ans, cnt);
		m += (cnt - 1) * (a[i] - a[i - 1]);
		cnt--;
	}
	chmax(ans, cnt);
	cout << ans;
	return 0;
}
