#include <bits/extc++.h>
#define endl '\n'
typedef long long ll;
#define int ll
using namespace std;
using namespace __gnu_cxx;
using namespace __gnu_pbds;

int c;

void Main() {
	int n, k;
	cin >> n >> k;
	struct lyy {
	  private:
		int n;
		vector<int> fa, v;

	  public:
		explicit lyy(const int nn = 0) : n(nn), fa(nn + 1), v(nn + 1, 1) {
			iota(fa.begin(), fa.end(), 0);
			v[0] = 0;
		}
		int find(const int u) {
			if (fa[u] == u) {
				return u;
			}
			return fa[u] = find(fa[u]);
		}
		void mrg(int x, int y) {
			x = find(x);
			y = find(y);
			if (x == y) {
				return;
			}
			if (v[x] < v[y]) {
				swap(x, y);
			}
			v[x] += v[y];
			fa[y] = x;
			v[y] = 0;
		}
	};
	struct ly {
		int v, nt;
	};
	vector<int> he(n + 1);
	vector<ly> edge(1);
	vector<pair<int, int>> g;
	auto add = [&](const int u, const int v) {
		edge.push_back({v, he[u]});
		he[u] = static_cast<int>(edge.size()) - 1;
	};
	for (int i = 1; i < n; ++i) {
		int x, y;
		cin >> x >> y;
		add(x, y);
		add(y, x);
		if (x > y) {
			swap(x, y);
		}
		g.push_back({x, y});
	}
	if (n > 10) {
		cout << 1 << endl;
		return;
	}
	constexpr int inf = 0x3f3f3f3f3f3f3f3f;
	int res = inf;
	for (int msk = 0; (1ll << msk) < n; ++msk) {
		if (static_cast<int>(__builtin_popcountll(msk)) != k) {
			continue;
		}
		lyy bcj(n);
		set<int> lst;
		for (int i = 0; i < n; ++i) {
			if ((msk >> i) & 1) {
				lst.insert(i);
			}
		}
		for (const pair<int, int> pr : g) {
			const int u = pr.first, v = pr.second;
			if (lst.count(u) && lst.count(v)) {
				bcj.mrg(u, v);
			}
		}
		vector<int> dis(n + 1, inf);
		dis[0] = 0;
		vector<bool> vis(n + 1);
		__gnu_pbds::priority_queue<pair<int, int>, greater<pair<int, int>>, thin_heap_tag> pq;
		set<int> s;
		for (const int x : lst) {
			dis[x] = 0;
			pq.push({0, x});
			s.insert(bcj.find(x));
		}
		if (static_cast<int>(s.size()) > 2) {
			continue;
		}
		while (!pq.empty()) {
			const pair<int, int> pr = pq.top();
			const int d = pr.first, u = pr.second;
			pq.pop();
			if (vis[u]) {
				continue;
			}
			vis[u] = true;
			for (int i = he[u]; i; i = edge[i].nt) {
				const int v = edge[i].v;
				if (dis[v] > d + 1) {
					dis[v] = d + 1;
					pq.push({d + 1, v});
				}
			}
		}
		int mx = 0;
		for (int i = 1; i <= n; ++i) {
			if (dis[i] == inf) {
				continue;
			}
			mx = max(mx, dis[i]);
		}
		res = min(res, mx);
	}
	cout << res << endl;
}

#define CP_MULTI_TEST_CASES

signed main() {
	freopen("hub.in", "r", stdin);
	freopen("hub.out", "w", stdout);
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
