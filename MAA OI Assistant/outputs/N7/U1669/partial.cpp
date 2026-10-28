// 适用：n,q <= 5000（测试点 1~4）。O(nq) 时间，O(n) 空间。
#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 5005;
const ll INF = 4000000000000000000LL;
int n, q;
ll a[N], b[N];

void solve() {
    int c;
    cin >> c >> n >> q;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i <= n; i++) cin >> b[i];
    while (q--) {
        int op, l, r;
        ll x;
        cin >> op >> l;
        if (op <= 2) {
            cin >> x;
            if (op == 1) a[l] = x;
            else b[l] = x;
        } else {
            cin >> r >> x;
            ll s = 0, t = INF, ans = x;
            for (int i = r; i >= l; i--) {
                t = min(t, b[i] + s);
                s += a[i];
                ans = max(ans, min(x + s, t));
            }
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
