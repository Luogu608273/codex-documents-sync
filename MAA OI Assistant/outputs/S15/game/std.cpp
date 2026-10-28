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
        int m = max(a, b);
        cout << (long double)(m - 1) / (2 * m - 1) << endl;
    }
    return 0;
}
