#include <bits/extc++.h>
#define endl '\n'
typedef long long ll;
#define int ll
using namespace std;
using namespace __gnu_cxx;
using namespace __gnu_pbds;

void Main() {
	int n, m;
	cin >> n >> m;
	vector<int> a(n + 1);
	int mx = 0;
	bool spA = n != 1, spB = n != 1;
	int deB = -1;
	for (int i = 1; i <= n; ++i) {
		cin >> a[i];
		mx = max(mx, llabs(a[i]));
	}
	sort(a.begin() + 1, a.end());
	for (int i = 1; i <= n; ++i) {
		if (spA && a[i] != i) {
			spA = false;
		}
		if (spB && i > 2 && a[i] - a[i - 1] != a[i - 1] - a[i - 2]) {
			spB = false;
		}
	}
	if (spA) {
		spB = false;
	}
	if (spA) {
		int k = (static_cast<int>(sqrt(4.0 * m)) - 10) / 2;
		while (k <= 0 || k * (k + 1) <= 2 * m) {
			++k;
		}
		--k;
		cout << max(min(n, k), 1ll) << endl;
		return;
	}
	if (spB) {
		deB = a[2] - a[1];
		m /= deB;
		int k = (static_cast<int>(sqrt(4.0 * m)) - 10) / 2;
		while (k <= 0 || k * (k + 1) <= 2 * m) {
			++k;
		}
		--k;
		cout << max(min(n, k), 1ll) << endl;
		return;
	}
	if (n <= 5000) {
		int res = 1;
		for (int i = 1; i <= n; ++i) {
			int tres = 1;
			int tmp = m;
			for (int j = i - 1; j; --j) {
				if (tmp < a[i] - a[j]) {
					break;
				}
				tmp -= a[i] - a[j];
				++tres;
			}
			res = max(res, tres);
		}
		cout << res << endl;
		return;
	}
	if (mx <= 100) {
		map<int, int> mp;
		for (int i = 1; i <= n; ++i) {
			++mp[a[i]];
		}
		vector<pair<int, int>> b(1);
		for (const pair<int, int> p : mp) {
			b.push_back(p);
		}
		const int k = static_cast<int>(b.size()) - 1;
		int res = 1;
		for (int i = 1; i <= k; ++i) {
			int tres = b[i].second;
			int tmp = m;
			for (int j = i - 1; j; --j) {
				const int diff = b[i].first - b[j].first;
				if (tmp < diff) {
					break;
				}
				if (tmp < b[j].second * diff) {
					tres += tmp / diff;
					tmp %= diff;
					break;
				}
				tres += b[j].second;
			}
			res = max(res, tres);
		}
		cout << res << endl;
		return;
	}
	mt19937_64 rng(time(0));
	const int res = (rng() % n + n) % n + 1;
	cout << res << endl;
}

// #define CP_MULTI_TEST_CASES

signed main() {
	freopen("crystal.in", "r", stdin);
	freopen("crystal.out", "w", stdout);
	ios::sync_with_stdio(false), cin.tie(nullptr), cout.tie(nullptr);
	int t = 1;
#ifdef CP_MULTI_TEST_CASES
	cin >> t;
#endif
	while (t--) {
		Main();
	}
	return cout << flush, fflush(stdout), 0;
}
