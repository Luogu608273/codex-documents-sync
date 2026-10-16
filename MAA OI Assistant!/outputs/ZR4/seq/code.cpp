#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 200005;
struct Node {
    ll l, s;
} a[N];
int n, k;
ll ans;

bool cmp(Node x, Node y) {
    return x.s * y.l < y.s * x.l;
}

void solve() {
    cin >> n >> k;
    for (int i = 1; i <= n; i++) {
        cin >> a[i].l;
        for (int j = 1, x; j <= a[i].l; j++) {
            cin >> x;
            a[i].s += x;
            ans += 1LL * j * x;
        }
    }
    sort(a + 1, a + n + 1, cmp);
    ll len = 0, d = LLONG_MAX;
    for (int i = 1; i <= n; i++) {
        ans += len * a[i].s;
        len += a[i].l;
        if (i > 1) d = min(d, a[i - 1].l * a[i].s - a[i].l * a[i - 1].s);
    }
    cout << ans - (k == 2 ? d : 0) << endl;
}

int main() {
#ifndef LOCAL
    freopen("seq.in", "r", stdin);
    freopen("seq.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
