#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

int main() {
#ifndef LOCAL
    freopen("card.in", "r", stdin);
    freopen("card.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) {
        int n, m;
        cin >> n >> m;
        vector<int> off(n * m + 1), val, f(m, m);
        for (int i = 0, c; i < n * m; i++) {
            cin >> c;
            off[i + 1] = off[i] + c;
        }
        val.resize(off.back());
        for (int &x : val) cin >> x;
        for (int i = 0; i < n * m; i++)
            sort(val.begin() + off[i], val.begin() + off[i + 1]);
        for (int x = 0; x < n; x++) {
            for (int y = x + 1; y < n; y++) {
                int p = 0, q = 0;
                for (int j = 0; j < m; j++) {
                    int u = x * m + j, v = y * m + j;
                    int l = off[u], r = off[v];
                    while (l < off[u + 1] && r < off[v + 1] && val[l] != val[r]) {
                        if (val[l] < val[r]) l++;
                        else r++;
                    }
                    if (l == off[u + 1] || r == off[v + 1]) q = p, p = j + 1;
                    f[j] = min(f[j], q);
                }
            }
        }
        ll ans = 0;
        if (n == 1) ans = 1LL * m * (m + 1) / 2;
        else for (int x : f) ans += x;
        cout << ans << endl;
    }
    return 0;
}
