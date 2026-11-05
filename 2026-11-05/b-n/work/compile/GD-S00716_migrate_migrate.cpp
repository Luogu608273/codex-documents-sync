#include <bits/stdc++.h>
#define int long long
#define N 2000005
#define rep(x, y, z) for (int x = y; x <= z; x++)
#define rrep(x, y, z) for (int x = y; x >= z; x--)
using namespace std;
int c, T, n, d, a[N], ans, L[N], R[N];
int get(int x) {
	int k = upper_bound(a + 1, a + 1 + n, a[x] + d) - a - 1;
	return k; 
}
priority_queue<pair<int, int> > q;
int dis[N], cnt[N];
#undef int
int main() {
#define int long long	
	ios::sync_with_stdio(0), cin.tie(0);
	freopen("migrate.in", "r", stdin), freopen("migrate.out", "w", stdout);
	cin >> c >> T;
	while (T--) {
		ans = 0;
		cin >> n >> d;
		rep (i, 1, n) cin >> a[i];
//		rep (u, 1, n) {
//			int k = get(u);
//			
//			int j = k - 1;
//			int i = k - 2;
//			if (i < u) continue;
//			//u i j k v
//			i = get(i) + 1;
//			j = get(j);
//			if (i > n || i < u) continue;
//			ans += max(0ll, j - max(i, k + 1) + 1);
//		}
		if (n * n * 16 <= 2e18) {
			rep (i, 1, n) {
				rep (j, i + 1, n) dis[j] = 1e18, cnt[j] = 0;
				while (!q.empty()) q.pop();
				q.push({0, i});
				dis[i] = 0;
				while (q.size()) {
					int u = q.top().second;
					q.pop();
					rep (v, u + 1, n) if (a[v] - a[u] <= d) {
						if (dis[u] + 1 < dis[v]) {
							dis[v] = dis[u] + 1;
							q.push({-dis[v], v});
							cnt[v] = 1;
						} else if (dis[u] + 1 == dis[v]) cnt[v]++, q.push({-dis[v], v});
					} else break;
				}
				rep (j, i + 1, n) if (cnt[j] == 2) ans++;
			}
			cout << ans << '\n';
		} else {
			rep (i, 1, n) {
				int l = i - 1;
				while (l >= 1 && get(l) == l + 1) l--;
				int r = i + 1;
				while (r <= n && get(r - 1) == r && get(r - 2) < r) r++;
				L[i] = l + 1, R[i] = r - 1;
			}
			rep (u, 1, n)
				rep (v, u + 1, n) {
					int k = get(u);
					if (k >= v || k == u) continue;
					if (a[v] - a[k] <= d && a[v] - a[k - 1] <= d && (k == u + 2 || a[v] - a[k - 2] > d)) {
						ans += (R[v] - v + 1) * (u - L[u] + 1);
//						cout << u << ' ' << v << ' ' << L[u] << ' ' << R[v] << "!\n";
					}
				}
			cout << ans << '\n';
		}
	}
	return 0;
}
/*
0 1
5 3
0 2 4 5 7

0 1
7 3
0 2 4 5 6 7 9

0 2
5 3
-2 -1 0 1 2
6 2
-4 -3 -2 -1 3 6

0 1
197 66
0 2 66 68 69 132 135 136 198 202 203 264 269 270 330 336 337 396 403 404 462 470 471 528 537 538 594 604 605 660 671 672 726 738 739 792 805 806 858 872 873 924 939 940 990 1006 1007 1056 1073 1074 1122 1140 1141 1188 1207 1208 1254 1274 1275 1320 1341 1342 1386 1408 1409 1452 1475 1476 1518 1542 1543 1584 1609 1610 1650 1676 1677 1716 1743 1744 1782 1810 1811 1848 1877 1878 1914 1944 1945 1980 2011 2012 2046 2078 2079 2112 2145 2146 2178 2212 2213 2244 2279 2280 2310 2346 2347 2376 2413 2414 2442 2480 2481 2508 2547 2548 2574 2614 2615 2640 2681 2682 2706 2748 2749 2772 2815 2816 2838 2882 2883 2904 2949 2950 2970 3016 3017 3036 3083 3084 3102 3150 3151 3168 3217 3218 3234 3284 3285 3300 3351 3352 3366 3418 3419 3432 3485 3486 3498 3552 3553 3564 3619 3620 3630 3686 3687 3696 3753 3754 3762 3820 3821 3828 3887 3888 3894 3954 3955 3960 4021 4022 4026 4088 4089 4092 4155 4156 4158 4222 4223 4224 4289 4356 4421 4422 4487

*/
