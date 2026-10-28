#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

using Node = pair<int, int>;

struct Solver {
    priority_queue<Node> no;
    priority_queue<Node, vector<Node>, greater<Node>> yes;
    Node first, last;
    ll ans = 0;
    bool empty = true;
    void front(Node a, Node b) {
        if (empty) {
            first = a, last = b;
            ans = a.first;
            empty = false;
            return;
        }
        yes.push(b);
        yes.push(first);
        Node z = yes.top();
        yes.pop();
        no.push(z);
        ans += (ll)a.first + b.first - z.first;
        first = a;
    }
    void back(Node a, Node b) {
        if (empty) {
            front(a, b);
            return;
        }
        no.push(last);
        no.push(a);
        Node z = no.top();
        no.pop();
        yes.push(z);
        ans += z.first;
        last = b;
    }
};

void solve() {
    int q;
    cin >> q;
    Solver all, inner;
    for (int i = 1; i <= q; i++) {
        int t, x, y;
        cin >> t >> x >> y;
        Node a = {x, i * 2}, b = {y, i * 2 + 1};
        if (all.empty) {
            if (t == 1) all.front(b, a);
            else all.back(a, b);
        } else {
            Node f = all.first, l = all.last;
            if (t == 1) {
                all.front(b, a);
                inner.front(a, f);
            } else if (t == 3) {
                all.back(a, b);
                inner.back(l, a);
            } else {
                swap(all, inner);
                all.front(a, f);
                all.back(l, b);
            }
        }
        cout << all.ans << endl;
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
