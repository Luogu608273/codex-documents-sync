#include <bits/extc++.h>
#define endl '\n'
typedef long long ll;
#define int ll
using namespace std;
using namespace __gnu_cxx;
using namespace __gnu_pbds;

int c;

void Main() {
	constexpr int inf = 0x3f3f3f3f3f3f3f3f;
	int n, d;
	cin >> n >> d;
	vector<int> x(n + 1), l(n + 1), r(n + 1);
	for (int i = 1; i <= n; ++i) {
		cin >> x[i];
		if (i == 1) {
			l[i] = 1;
		} else {
			l[i] = l[i - 1];
			while (l[i] < n && x[i] - x[l[i]] > d) {
				++l[i];
			}
		}
	}
	for (int i = n; i; --i) {
		if (i == n) {
			r[i] = n;
		} else {
			r[i] = r[i + 1];
			while (r[i] > 1 && x[r[i]] - x[i] > d) {
				--r[i];
			}
		}
	}
	// if (n <= 300) {
	// 	int res = 0;
	// 	for (int i = 1; i < n; ++i) {
	// 		int cur = i;
	// 		while (cur <= n) {
	// 			const int tmp = r[cur];
	// 			res += r[cur + 1] - tmp;
	// 			++res;
	// 			cur = tmp;
	// 			if (cur == n) {
	// 				break;
	// 			}
	// 		}
	// 	}
	// 	cout << res << endl;
	// 	return;
	// }
	cout << 0 << endl;
}

#define CP_MULTI_TEST_CASES

signed main() {
	freopen("migrate.in", "r", stdin);
	freopen("migrate.out", "w", stdout);
	ios::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr);
	int t = 1;
#ifdef CP_MULTI_TEST_CASES
	cin >> c >> t;
#endif
	while (t--) {
		Main();
	}
	return cout << flush, fflush(stdout), 0;
}
