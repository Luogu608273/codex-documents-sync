#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

// 部分分：n、m 均不超过 2000，覆盖子任务 1、2；元素支持到 10^12。
const int N = 2005;
int n, m, k;
set<ll> s[N];

int query(int u, int v) {
    bool f = includes(s[u].begin(), s[u].end(), s[v].begin(), s[v].end());
    bool g = includes(s[v].begin(), s[v].end(), s[u].begin(), s[u].end());
    if (f && g) return 3;
    if (f) return 1;
    if (g) return 2;
    return 4;
}

void solve() {
    cin >> n >> m >> k;
    while (m--) {
        int op, l, r;
        cin >> op >> l >> r;
        if (op == 3) {
            cout << query(l, r) << endl;
            continue;
        }
        ll x;
        cin >> x;
        for (int i = l; i <= r; i++) {
            if (op == 1) s[i].insert(x);
            else s[i].erase(x);
        }
    }
}

int main() {
#ifndef LOCAL
    freopen("set.in", "r", stdin);
    freopen("set.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
