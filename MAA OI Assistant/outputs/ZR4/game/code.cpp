#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 1000005, V = 1 << 20, INF = 2000000;
struct Node {
    int fp, fm, lp, lm;
};
const Node E = {INF, INF, -INF, -INF};
Node tr[V << 1];
int n, q, a[N], s[N], z;

Node merge(Node x, Node y) {
    return {min(x.fp, y.fp), min(x.fm, y.fm), max(x.lp, y.lp), max(x.lm, y.lm)};
}

Node leaf(int i) {
    if (s[i] == 1) return {i, INF, i, -INF};
    if (s[i] == -1) return {INF, i, -INF, i};
    return E;
}

void modify(int i) {
    if (i < 1 || i >= n) return;
    s[i] = (a[i + 1] > a[i]) - (a[i + 1] < a[i]);
    int p = z + i - 1;
    tr[p] = leaf(i);
    for (p >>= 1; p; p >>= 1) tr[p] = merge(tr[p << 1], tr[p << 1 | 1]);
}

Node query(int l, int r) {
    Node res = E;
    for (l += z - 1, r += z - 1; l <= r; l >>= 1, r >>= 1) {
        if (l & 1) res = merge(res, tr[l++]);
        if (!(r & 1)) res = merge(res, tr[r--]);
    }
    return res;
}

int dist(int x, int l, int r) {
    if (x < l || x >= r) return -1;
    return min(x - l, r - x - 1);
}

bool win(int l, int r) {
    if (r - l < 2) return false;
    int mid = (l + r - 1) >> 1;
    Node x = query(l, mid), y = query(mid + 1, r - 1);
    int p = max(dist(x.lp, l, r), dist(y.fp, l, r));
    int m = max(dist(x.lm, l, r), dist(y.fm, l, r));
    if (p < 0 || m < 0) return false;
    int d = min(p, m);
    l += d;
    r -= d;
    if (s[l] == s[r - 1] && s[l]) return false;
    if (!d) return true;
    Node v = query(l, r - 1);
    int r1 = max(v.fp, v.fm);
    int r0 = max(s[l - 1] == 1 ? l - 1 : v.fp, s[l - 1] == -1 ? l - 1 : v.fm);
    bool f = false, g = false;
    if (r0 < r - 1) {
        if (r1 >= r - 1) f = true;
        else f = (((r - 1 - r1) & 1) == (r0 == r1));
    }
    int l1 = min(v.lp, v.lm) + 1;
    int l0 = min(s[r] == 1 ? r : v.lp, s[r] == -1 ? r : v.lm) + 1;
    if (l0 > l + 1) {
        if (l1 <= l + 1) g = true;
        else g = (((l1 - l - 1) & 1) == (l0 == l1));
    }
    return f || g;
}

void solve() {
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    z = 1;
    while (z < n) z <<= 1;
    fill(tr, tr + (z << 1), E);
    for (int i = 1; i < n; i++) {
        s[i] = (a[i + 1] > a[i]) - (a[i + 1] < a[i]);
        tr[z + i - 1] = leaf(i);
    }
    for (int i = z - 1; i; i--) tr[i] = merge(tr[i << 1], tr[i << 1 | 1]);
    cin >> q;
    while (q--) {
        int op, l, r;
        cin >> op >> l >> r;
        if (op == 1) {
            a[l] = r;
            modify(l - 1);
            modify(l);
        } else cout << (win(l, r) ? "Alice" : "Bob") << endl;
    }
}

int main() {
#ifndef LOCAL
    freopen("game.in", "r", stdin);
    freopen("game.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
