#include<iostream>
#include<cmath>
#include<set>
#include<queue>
using namespace std;
typedef long long ll;
const int N = 2e5 + 10, M = 410, B = 400, inf = 1e9+1;
int n, q, a[N], rt[N], op, x, y;
set<int> st; ll ans = 0;
struct piii{
	int l, r, mn;
	bool operator < (const piii & o) const{
		return a[mn] > a[o.mn];
	}
};
priority_queue<piii> pq;
struct Tree1{
	int t[N];
	void upd(int x, int v){
		while(x <= n){
			t[x] += v;
			x += x & -x;
		}
	}
	int qry(int x){
		int res = 0;
		while(x){
			res += t[x];
			x -= x & -x;
		}
		return res;
	}
} c[M];
struct Tree2{
	int mx[N*4], mn[N*4], L, R; ll s[N*4];
	inline void mg(int & u){
		mx[u] = max(mx[u*2], mx[u*2+1]);
		s[u] = s[u*2] + s[u*2+1];
		if(a[mn[u*2]] <= a[mn[u*2+1]]) mn[u] = mn[u*2];
		else mn[u] = mn[u*2+1];
	}
	inline void setnd(int & u, int & i){
		mx[u] = s[u] = a[i];
		if(a[i] <= B) mn[u] = n+1;
		else mn[u] = i;
	}
	void build(int u, int l, int r){
		if(l == r){ setnd(u, l); return; }
		int mid = (l + r) / 2;
		build(u*2, l, mid);
		build(u*2+1, mid+1, r);
		mg(u);
	}
	void update(int u, int l, int r){
		if(l == r){ setnd(u, l); return; }
		int mid = (l + r) / 2;
		if(L <= mid) update(u*2, l, mid);
		else update(u*2+1, mid+1, r);
		mg(u);
	}
	int query1(int u, int l, int r){
		if(L <= l && r <= R) return mx[u];
		int mid = (l + r) / 2, res = 0;
		if(L <= mid) res = max(res, query1(u*2, l, mid));
		if(mid < R) res = max(res, query1(u*2+1, mid+1, r));
		return res;
	}
	int query2(int u, int l, int r){
		if(L <= l && r <= R) return mn[u];
		int mid = (l + r) / 2, res = n+1;
		if(L <= mid){
			int mnp = query2(u*2, l, mid);
			if(a[mnp] <= a[res]) swap(mnp, res);
		}
		if(mid < R){
			int mnp = query2(u*2+1, mid+1, r);
			if(a[mnp] <= a[res]) swap(mnp, res);
		}
		return res;
	}
	ll query3(int u, int l, int r){
		if(L <= l && r <= R) return s[u];
		int mid = (l + r) / 2; ll res = 0;
		if(L <= mid) res += query3(u*2, l, mid);
		if(mid < R) res += query3(u*2+1, mid+1, r);
		return res;
	}
	inline void upd(int p){ L = p; update(1, 1, n); }
	inline int qry1(int p1, int p2){ L = p1; R = p2; return query1(1, 1, n); }
	inline int qry2(int p1, int p2){ L = p1; R = p2; return query2(1, 1, n); }
	inline ll qry3(int p1, int p2){ L = p1; R = p2; return query3(1, 1, n); }
} d;
inline void delnum(int i){
	if(a[i] <= B) c[a[i]].upd(i, -1);
	else st.erase(i);
}
inline void addnum(int i){
	if(a[i] <= B) c[a[i]].upd(i, 1);
	else st.insert(a[i]);
}
void add_ls(int l, int r){
	if(l > r) return;
	int res = d.qry2(l, r);
	if(a[res] == inf) return;
	pq.push({l, r, res});
}
ll qry(int l, int r){
	ll s = 0; int mx = d.qry1(l, r); bool fg = 0;
	for(int i = 1; i <= B; i++){
		if(s+1 < i) return s+1;
		s += ((ll)c[i].qry(r) - c[i].qry(l-1))*i;
		if(s >= mx) return d.qry3(l, r)+1;
	}
	while(pq.size()) pq.pop();
	add_ls(l, r);
	while(pq.size()){
		piii tp = pq.top();
		pq.pop();
		if(s+1 < a[tp.mn]) return s+1;
		s += tp.mn;
		if(s >= mx) return d.qry3(l, r)+1;
		add_ls(tp.l, tp.mn-1);
		add_ls(tp.mn+1, tp.r);
	}
	return s+1;
}
int main(){
	cin >> n >> q;
	for(int i = 1; i <= n; i++){
		cin >> a[i];
		addnum(i);
	}
	a[n+1] = inf;
	d.build(1, 1, n);
	st.insert(n+1);
	while(q--){
		cin >> op >> x >> y;
		if(op == 1){
			delnum(x);
			a[x] = y;
			addnum(x);
			d.upd(x);
		}
		else cout << qry(x, y) << '\n';
	}
	return 0;
}
