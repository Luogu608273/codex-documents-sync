#include<iostream>
#include<vector>
#include<algorithm>

using namespace std;
typedef long long ll;
typedef pair<int, int> pii;

const int N = 2e5 + 10; const ll inf = 1e18;
int n, q, k, a[N], u, v, sz[N], rt[N];
int dep[N], fa[N], pth[N], len[N];
int lnd[N], out[N], nn, ps[N];
vector<int> G[N];

bool cmp(int x, int y){
	return sz[x] > sz[y];
}

void dfs1(int u, int fa_){
	sz[u] = 1; dep[u] = dep[fa_] + 1; fa[u] = fa_;
	for(int v: G[u]){
		if(v == fa_) continue;
		dfs1(v, u);
		sz[u] += sz[v];
	}
	sort(G[u].begin(), G[u].end(), cmp);
}

void dfs2(int u, int fa_, int r){
	rt[u] = r; pth[++nn] = u;
	if(u == r) lnd[r] = nn;
	ps[u] = nn-lnd[r]+1;
	bool fg = 1;
	for(int v: G[u]){
		if(v == fa_) continue;
		if(fg){
			dfs2(v, u, r);
			fg = 0;
		}
		else dfs2(v, u, v);
	}
}

int lca(int u, int v){
	while(rt[u] != rt[v]){
		if(dep[rt[u]] > dep[rt[v]]) u = fa[rt[u]];
		else v = fa[rt[v]];
	}
	return (dep[u] < dep[v] ? u : v);
}

struct Rect{
	ll a[3][3];
	inline void allinf(){
		a[0][0] = a[0][1] = a[0][2] = inf;
		a[1][0] = a[1][1] = a[1][2] = inf;
		a[2][0] = a[2][1] = a[2][2] = inf;
	}
	inline void setup(){
		a[0][0] = 0; a[0][1] = a[0][2] = inf;
		a[1][1] = 0; a[1][0] = a[1][2] = inf;
		a[2][2] = 0; a[2][0] = a[2][1] = inf;
	}
	inline void upd(int v){
		a[0][0] = v; a[0][1] = (k >= 2 ? v : inf); a[0][2] = (k >= 3 ? v : inf);
		a[1][0] = 0; a[1][1] = a[1][2] = inf;
		a[2][0] = a[2][2] = inf; a[2][1] = 0;
	}
};

inline void mul(Rect u, Rect v, Rect & res){
	res.allinf();
	for(int i = 0; i < 3; i++){
		for(int j = 0; j < 3; j++){
			for(int k = 0; k < 3; k++){
				res.a[i][j] = min(res.a[i][j], u.a[i][k] + v.a[k][j]);
			}
		}
	}
}

struct Line{
	ll a[3];
	inline void setup(int x){
		a[0] = a[1] = a[2] = x;
	}
};

inline void upd(Rect u, Line & v){
	Line nw;
	nw.a[0] = min(min(v.a[0] + u.a[0][0], v.a[1] + u.a[0][1]), v.a[2] + u.a[0][2]);
	nw.a[1] = min(min(v.a[0] + u.a[1][0], v.a[1] + u.a[1][1]), v.a[2] + u.a[1][2]);
	nw.a[2] = min(min(v.a[0] + u.a[2][0], v.a[1] + u.a[2][1]), v.a[2] + u.a[2][2]);
	v = nw;
}

struct Node{
	Rect x;
	void mg(Node & u, Node & v){
		mul(u.x, v.x, x);
	}
};

struct SegTree{
	vector<Node> vc; int n, bg, L, R;
	void build(int u, int l, int r){
		if(l == r){
			vc[u].x.upd(a[pth[bg+l-1]]);
			return;
		}
		int mid = (l + r) / 2;
		build(u*2, l, mid);
		build(u*2+1, mid+1, r);
		vc[u].mg(vc[u*2], vc[u*2+1]);
	}
	void setup(int nd, int bg_){
		n = nd; bg = bg_;
		vc.resize(n*4);
		build(1, 1, n);
	}
	void query(int u, int l, int r, Rect & rc){
		if(L <= l && r <= R){
			mul(rc, vc[u].x, rc);
			return;
		}
		int mid = (l + r) / 2;
		if(mid < R) query(u*2+1, mid+1, r, rc);
		if(L <= mid) query(u*2, l, mid, rc);
	}
	Rect qry(int l, int r){
		L = l, R = r; Rect res;
		res.setup();
		query(1, 1, n, res);
		return res;
	}
} t[N];

void dp1(int u, int v, Line & Li){
	while(rt[u] != rt[v]){
		upd(t[rt[u]].qry(1, ps[u]), Li);
		u = fa[rt[u]];
	}
	if(ps[v]+1 <= ps[u]) upd(t[rt[u]].qry(ps[v]+1, ps[u]), Li);
}

ll dp2(int u, int v){
	int w = lca(u, v);
	Line l1, l2;
	l1.setup(a[u]);
	l2.setup(a[v]);
	if(w == u || w == v){
		if(w == u){
			swap(u, v);
			l1.setup(a[u]);
		}
		dp1(u, w, l1);
		ll mn = inf;
		for(int i = 1; i <= k; i++) mn = min(mn, l1.a[i-1]);
		return mn + a[w];
	}
	dp1(u, w, l1);
	dp1(v, w, l2);
	ll res = 1e18;
	for(int i = 1; i <= k; i++){
		for(int j = 1; i+j <= k; j++){
			res = min(res, l1.a[i-1] + l2.a[j-1]);
		}
	}
	ll mn1 = inf, mn2 = inf;
	for(int i = 1; i <= k; i++) mn1 = min(mn1, l1.a[i-1]);
	for(int i = 1; i <= k; i++) mn2 = min(mn2, l2.a[i-1]);
	return min(res, mn1 + a[w] + mn2);
}

int main(){
	freopen("transmit2.in", "r", stdin);
	cin >> n >> q >> k;
	for(int i = 1; i <= n; i++) cin >> a[i];
	for(int i = 1; i < n; i++){
		cin >> u >> v;
		G[u].push_back(v);
		G[v].push_back(u);
	}
	dfs1(1, 0);
	dfs2(1, 0, 1);
	for(int i = 1; i <= n; i++) len[rt[i]]++;
	for(int i = 1; i <= n; i++){
		if(rt[i] == i) t[i].setup(len[i], lnd[i]);
	}
	while(q--){
		cin >> u >> v;
		cout << dp2(u, v) << '\n';
	}
	return 0;
}
