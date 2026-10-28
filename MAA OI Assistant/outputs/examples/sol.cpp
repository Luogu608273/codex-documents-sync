#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int n;
    cin >> n;
    ll ans = 0, x;
    for (int i = 1; i <= n; ++i) {
        cin >> x;
        ans += x;
    }
    cout << ans << endl;
    return 0;
}
