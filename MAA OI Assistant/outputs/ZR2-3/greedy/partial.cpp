#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 155;
int n, A, B, c[N], vis[N];
ll u[N], v[N], f[N], ans;

void dfs(int k, int x, int y, ll z) {
    if (k > n) {
        ans = max(ans, z);
        return;
    }
    for (int i = 1; i <= n; i++) {
        if (vis[i]) continue;
        vis[i] = 1;
        int a = x, b = y;
        ll w = z;
        if (a >= c[i]) a -= c[i], w += u[i];
        if (b >= c[i]) b -= c[i], w += v[i];
        dfs(k + 1, a, b, w);
        vis[i] = 0;
    }
}

// Supports n <= 8, or A == B (35% of the listed test points).
void solve() {
    cin >> n >> A >> B;
    for (int i = 1; i <= n; i++) cin >> c[i] >> u[i] >> v[i];
    if (A == B) {
        for (int i = 1; i <= n; i++)
            for (int j = A; j >= c[i]; j--) f[j] = max(f[j], f[j - c[i]] + u[i] + v[i]);
        cout << f[A] << endl;
    } else {
        if (n > 8) exit(1);
        dfs(1, A, B, 0);
        cout << ans << endl;
    }
}

int main() {
#ifndef LOCAL
    freopen("greedy.in", "r", stdin);
    freopen("greedy.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
