#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 100005, M = 800005, V = 0x3f3f3f3f;
int n, m, h[N * 2], to[M], nx[M], ec, d[N * 2], q[N * 2];
struct Node {
    int x, y;
    bool operator < (const Node &b) const {
        if (x + y != b.x + b.y) return x + y < b.x + b.y;
        return x < b.x;
    }
    bool operator == (const Node &b) const { return x == b.x && y == b.y; }
} a[N];

void add(int x, int y) {
    to[++ec] = y;
    nx[ec] = h[x];
    h[x] = ec;
}

void solve() {
    cin >> n >> m;
    fill(h + 1, h + n * 2 + 1, 0);
    fill(d + 1, d + n * 2 + 1, V);
    ec = 0;
    for (int i = 1; i <= m; i++) {
        int x, y;
        cin >> x >> y;
        add(x, y + n);
        add(y + n, x);
        add(y, x + n);
        add(x + n, y);
    }
    int l = 0, r = 1;
    q[0] = 1;
    d[1] = 0;
    while (l < r) {
        int x = q[l++];
        for (int i = h[x]; i; i = nx[i]) {
            int y = to[i];
            if (d[y] == V) {
                d[y] = d[x] + 1;
                q[r++] = y;
            }
        }
    }
    if (d[n + 1] == V) {
        cout << n - 1 << endl;
        return;
    }
    for (int i = 1; i <= n; i++) a[i] = {min(d[i], d[i + n]), max(d[i], d[i + n])};
    sort(a + 1, a + n + 1);
    set<pair<int, int>> s;
    ll ans = 0;
    int t = 0;
    for (int i = 1; i <= n;) {
        int j = i;
        while (j < n && a[j + 1] == a[i]) j++;
        int c = j - i + 1;
        bool ok = s.count({a[i].x - 1, a[i].y - 1});
        s.insert({a[i].x, a[i].y});
        if (i > 1) ans += max(c, t);
        t = ok ? min(c, t) : c;
        if (j == n || a[j + 1].x != a[i].x + 1 || a[j + 1].y != a[i].y - 1) {
            ans += a[i].y == a[i].x + 1 ? (t + 1) / 2 : t;
            t = 0;
        }
        i = j + 1;
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("connected.in", "r", stdin);
    freopen("connected.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
