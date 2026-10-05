#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

ll a[40];

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    for (int i = 1; i <= n; ++i) cin >> a[i];
    ll ans = 0;
    for (int i = n; i >= 1; --i) ans += a[i];
    cout << ans << endl;
    return 0;
}
