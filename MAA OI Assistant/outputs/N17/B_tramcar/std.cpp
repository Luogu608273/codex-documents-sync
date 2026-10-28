#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 300005;
int n, a[N], b[N], c[N], f[N], nd[N], z;
ll k;

void add(int x) {
    for (; x <= n; x += x & -x) c[x]++;
}

int query(int x) {
    int s = 0;
    for (; x; x -= x & -x) s += c[x];
    return s;
}

bool check(int m) {
    fill(nd, nd + z + 2, 0);
    int now = 0;
    for (int i = 1; i <= n; i++) {
        if (!a[i]) now++;
        else {
            int r = max(f[i] - m, 0);
            if (r > z - now) return false;
            if (r) nd[z - r + 1] = max(nd[z - r + 1], a[i]);
        }
    }
    ll s = 0;
    for (int i = 1; i <= z; i++) {
        nd[i] = max(nd[i], nd[i - 1]);
        s += nd[i];
    }
    return s <= k;
}

void solve() {
    cin >> n >> k;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        b[i] = a[i];
        z += !a[i];
    }
    sort(b + 1, b + n + 1);
    int m = unique(b + 1, b + n + 1) - b - 1;
    for (int i = n; i >= 1; i--) {
        int p = lower_bound(b + 1, b + m + 1, a[i]) - b;
        f[i] = query(p - 1);
        add(p);
    }
    int l = 0, r = n - 1;
    while (l < r) {
        int m = (l + r) / 2;
        if (check(m)) r = m;
        else l = m + 1;
    }
    cout << l << endl;
}

int main() {
#ifndef LOCAL
    freopen("tramcar.in", "r", stdin);
    freopen("tramcar.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
