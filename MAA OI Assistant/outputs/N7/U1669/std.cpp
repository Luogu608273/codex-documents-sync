#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 500005;
const ll INF = 4000000000000000000LL;
int n, q;
ll a[N], b[N];
struct Node { ll a, b; } t[N << 2];
Node cur;
ll ans;

Node merge(Node x, Node y) {
    return {x.a + y.a, min(x.b + y.a, y.b)};
}

void build(int p, int l, int r) {
    if (l == r) {
        t[p] = {a[l], b[l]};
        return;
    }
    int mid = (l + r) >> 1;
    build(p << 1, l, mid);
    build(p << 1 | 1, mid + 1, r);
    t[p] = merge(t[p << 1], t[p << 1 | 1]);
}

void modify(int p, int l, int r, int x) {
    if (l == r) {
        t[p] = {a[l], b[l]};
        return;
    }
    int mid = (l + r) >> 1;
    if (x <= mid) modify(p << 1, l, mid, x);
    else modify(p << 1 | 1, mid + 1, r, x);
    t[p] = merge(t[p << 1], t[p << 1 | 1]);
}

bool query(int p, int l, int r, int ql, int qr, ll x) {
    if (ql <= l && r <= qr) {
        Node v = merge(t[p], cur);
        if (x + v.a < v.b) {
            cur = v;
            return false;
        }
        if (l == r) {
            ans = max(v.b, x + cur.a);
            return true;
        }
    }
    int mid = (l + r) >> 1;
    if (qr > mid && query(p << 1 | 1, mid + 1, r, ql, qr, x)) return true;
    if (ql <= mid && query(p << 1, l, mid, ql, qr, x)) return true;
    return false;
}

void solve() {
    int c;
    cin >> c >> n >> q;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i <= n; i++) cin >> b[i];
    build(1, 1, n);
    while (q--) {
        int op, l, r;
        ll x;
        cin >> op >> l;
        if (op <= 2) {
            cin >> x;
            if (op == 1) a[l] = x;
            else b[l] = x;
            modify(1, 1, n, l);
        } else {
            cin >> r >> x;
            cur = {0, INF};
            if (!query(1, 1, n, l, r, x)) ans = x + cur.a;
            cout << ans << endl;
        }
    }
}

int main() {
#ifndef LOCAL
    freopen("func.in", "r", stdin);
    freopen("func.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
