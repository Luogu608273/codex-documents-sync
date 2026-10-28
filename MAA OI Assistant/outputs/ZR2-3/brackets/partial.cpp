#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

// Supports Q <= 2000: rebuild the forward greedy heap after every query.
void solve() {
    int q;
    cin >> q;
    if (q > 2000) exit(1);
    deque<int> a;
    while (q--) {
        int t, x, y;
        cin >> t >> x >> y;
        if (t == 1) a.push_front(x), a.push_front(y);
        if (t == 2) a.push_front(x), a.push_back(y);
        if (t == 3) a.push_back(x), a.push_back(y);
        ll ans = a[0];
        priority_queue<int> h;
        int n = (int)a.size();
        for (int i = 1; i + 1 < n; i += 2) {
            h.push(a[i]);
            h.push(a[i + 1]);
            ans += h.top();
            h.pop();
        }
        cout << ans << endl;
    }
}

int main() {
#ifndef LOCAL
    freopen("brackets.in", "r", stdin);
    freopen("brackets.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
