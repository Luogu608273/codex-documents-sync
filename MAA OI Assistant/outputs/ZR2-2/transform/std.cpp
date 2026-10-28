#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 1000005;
int n, m, a[N], b[N], c[N], deg[N], q[N], sz[N];
int head[N], nxt[N], rt[N], id[N], in[N], out[N], st[N];
ll dep[N], pos[N], len[N];

void init() {
    for (int i = 1; i <= m; i++) {
        deg[i] = head[i] = id[i] = 0;
        sz[i] = 1;
        dep[i] = 0;
    }
    for (int i = 1; i <= m; i++) deg[b[i]]++;
    int l = 1, r = 0;
    for (int i = 1; i <= m; i++)
        if (!deg[i]) q[++r] = i;
    while (l <= r) {
        int x = q[l++], y = b[x];
        sz[y] += sz[x];
        nxt[x] = head[y], head[y] = x;
        if (!--deg[y]) q[++r] = y;
    }
    int cnt = 0;
    for (int i = 1; i <= m; i++) {
        if (!deg[i] || id[i]) continue;
        int x = i;
        ll d = 0;
        ++cnt;
        do {
            id[x] = cnt, rt[x] = x, pos[x] = d;
            d += c[x];
            x = b[x];
        } while (x != i);
        len[cnt] = d;
    }
    for (int i = r; i >= 1; i--) {
        int x = q[i], y = b[x];
        id[x] = id[y], rt[x] = rt[y];
        dep[x] = dep[y] + c[x];
    }
    int tim = 0, top = 0;
    for (int i = 1; i <= m; i++) {
        if (!deg[i]) continue;
        st[++top] = i;
        while (top) {
            int x = st[top--];
            in[x] = ++tim, out[x] = tim + sz[x] - 1;
            for (int y = head[x]; y; y = nxt[y]) st[++top] = y;
        }
    }
}

bool reach(int x, int y, ll t) {
    if (id[x] != id[y]) return false;
    if (!deg[y])
        return in[y] <= in[x] && in[x] <= out[y] && dep[x] - dep[y] <= t;
    ll d = pos[y] - pos[rt[x]];
    if (d < 0) d += len[id[x]];
    return dep[x] + d <= t;
}

bool check(ll t) {
    int v = 1;
    for (int i = 1; i <= n; i++) {
        while (v <= m && !reach(a[i], v, t)) v++;
        if (v > m) return false;
    }
    return true;
}

void solve() {
    cin >> n >> m;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i <= m; i++) cin >> b[i];
    ll sum = 0;
    for (int i = 1; i <= m; i++) cin >> c[i], sum += c[i];
    init();
    if (!check(sum)) {
        cout << -1 << endl;
        return;
    }
    ll l = 0, r = sum;
    while (l < r) {
        ll mid = (l + r) >> 1;
        if (check(mid)) r = mid;
        else l = mid + 1;
    }
    cout << l << endl;
}

int main() {
#ifndef LOCAL
    freopen("transform.in", "r", stdin);
    freopen("transform.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
