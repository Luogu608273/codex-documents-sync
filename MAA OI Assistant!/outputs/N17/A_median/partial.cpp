#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

// O(n^2 log n)，适用于 n <= 2000。
const int N = 2005;
int n, a[N], b[N];

int query(int l, int r) {
    int m = 0;
    for (int i = l; i <= r; i++) b[++m] = a[i];
    sort(b + 1, b + m + 1);
    return b[(m + 1) / 2];
}

void solve() {
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i < n; i += 2) {
        int x = query(1, i), y = query(i + 1, n);
        if (x == y) {
            cout << "Yes" << endl;
            return;
        }
    }
    cout << "No" << endl;
}

int main() {
#ifndef LOCAL
    freopen("median.in", "r", stdin);
    freopen("median.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
