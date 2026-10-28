#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 100005;
int p[N], vis[N], tot;

void init() {
    for (int i = 2; i <= 100000; i++) {
        if (!vis[i]) p[++tot] = i;
        for (int j = 1; j <= tot && 1ll * i * p[j] <= 100000; j++) {
            vis[i * p[j]] = 1;
            if (i % p[j] == 0) break;
        }
    }
}

bool prime(ll x) {
    for (int i = 1; i <= tot && 1ll * p[i] * p[i] <= x; i++) {
        if (x % p[i] == 0) return false;
    }
    return x >= 2;
}

void solve() {
    ll n, m;
    cin >> n >> m;
    if (m == 1 || n % m) {
        cout << 0 << endl;
        return;
    }
    ll k = n / m;
    if (m == 4) cout << (k == 1 ? 2 : 0) << endl;
    else if (prime(m)) cout << (k & 1 ? m - 1 : 1) << endl;
    else cout << 0 << endl;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    init();
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
