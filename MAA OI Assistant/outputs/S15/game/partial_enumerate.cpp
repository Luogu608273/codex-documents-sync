#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

int main() {
#ifndef LOCAL
    freopen("game.in", "r", stdin);
    freopen("game.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _, a, b;
    cin >> _;
    cout << fixed << setprecision(5);
    while (_--) {
        cin >> a >> b;
        if (a > b) swap(a, b);
        long double ans = 1;
        for (ll x = a; x <= b; x++) {
            long double p = (long double)(x * (x - 1) + 1LL * b * (b - 1))
                          / ((x + b) * (x + b - 1));
            ans = min(ans, p);
        }
        cout << ans << endl;
    }
    return 0;
}
