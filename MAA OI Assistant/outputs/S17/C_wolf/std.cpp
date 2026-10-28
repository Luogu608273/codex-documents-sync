#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 500005, P = 998244353;
struct Mat {
    int a, b, c, d;
} tr[N * 4];
int n, b[N], v[N][2], hd[N], to[N * 4], nx[N * 4], ec;
char s[N];

Mat mul(Mat x, Mat y) {
    return {int(((ll)x.a * y.a + (ll)x.b * y.c) % P),
            int(((ll)x.a * y.b + (ll)x.b * y.d) % P),
            int(((ll)x.c * y.a + (ll)x.d * y.c) % P),
            int(((ll)x.c * y.b + (ll)x.d * y.d) % P)};
}

void build(int p, int l, int r) {
    if (l == r) {
        tr[p] = {v[l][0], v[l][1], 1, 0};
        return;
    }
    int m = (l + r) / 2;
    build(p * 2, l, m);
    build(p * 2 + 1, m + 1, r);
    tr[p] = mul(tr[p * 2 + 1], tr[p * 2]);
}

void modify(int p, int l, int r, int x) {
    if (l == r) {
        tr[p] = {v[l][0], v[l][1], 1, 0};
        return;
    }
    int m = (l + r) / 2;
    if (x <= m) modify(p * 2, l, m, x);
    else modify(p * 2 + 1, m + 1, r, x);
    tr[p] = mul(tr[p * 2 + 1], tr[p * 2]);
}

void add(int q, int id) {
    to[++ec] = id;
    nx[ec] = hd[q];
    hd[q] = ec;
}

int val(int i, int q) {
    return s[i] == 'L' ? b[i] : q - b[i];
}

void solve() {
    cin >> n >> (s + 1);
    for (int i = 1; i <= n; i++) cin >> b[i];
    int m = (n + 1) / 2;
    fill(hd, hd + m + 2, 0);
    ec = 0;
    for (int i = 3; i <= n; i++) {
        for (int t = 0; t < 2; t++) {
            int j = i - t - 1;
            int a = (s[i] == 'R') - (s[j] == 'R');
            int c = (s[i] == 'L' ? b[i] : -b[i]) - (s[j] == 'L' ? b[j] : -b[j]);
            v[i][t] = !a && c == t;
            if (a) {
                int q = (t - c) / a;
                if (0 <= q && q <= m) {
                    add(q, i * 2 + t);
                    add(q + 1, i * 2 + t);
                }
            }
        }
    }
    if (n >= 3) build(1, 3, n);
    int ans = 0;
    for (int q = 0; q <= m; q++) {
        for (int e = hd[q]; e; e = nx[e]) {
            int i = to[e] / 2, t = to[e] % 2;
            v[i][t] ^= 1;
            modify(1, 3, n, i);
        }
        int x = val(1, q) == 0;
        int y = ((val(2, q) == 1) + (val(2, q) == val(1, q)) * x) % P;
        int u = y, w = x;
        if (n >= 3) {
            u = ((ll)tr[1].a * y + (ll)tr[1].b * x) % P;
            w = ((ll)tr[1].c * y + (ll)tr[1].d * x) % P;
        }
        if (val(n, q) == q) ans = (ans + u) % P;
        if (val(n - 1, q) == q - 1) ans = (ans + w) % P;
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("wolf.in", "r", stdin);
    freopen("wolf.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
