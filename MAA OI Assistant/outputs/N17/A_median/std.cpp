#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 200005;
int n, a[N], pre[N], suf[N];
priority_queue<int> l;
priority_queue<int, vector<int>, greater<int>> r;

void add(int x) {
    if (l.empty() || x <= l.top()) l.push(x);
    else r.push(x);
    if (l.size() < r.size()) {
        l.push(r.top());
        r.pop();
    }
    if (l.size() > r.size() + 1) {
        r.push(l.top());
        l.pop();
    }
}

void solve() {
    cin >> n;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i <= n; i++) {
        add(a[i]);
        if (i & 1) pre[i] = l.top();
    }
    while (!l.empty()) l.pop();
    while (!r.empty()) r.pop();
    for (int i = n; i >= 1; i--) {
        add(a[i]);
        if (!(i & 1)) suf[i] = l.top();
    }
    for (int i = 1; i < n; i += 2) {
        if (pre[i] == suf[i + 1]) {
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
