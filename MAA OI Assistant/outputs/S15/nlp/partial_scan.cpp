#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
using ull = unsigned long long;
const int N = 1000005;

struct Rule {
    ull k;
    int id;
    bool operator < (const Rule &b) const {
        return k != b.k ? k < b.k : id < b.id;
    }
} s[N];
int n, m, a[N], x[N], y[N], z[N];

ull key(int x, int y) {
    return (ull)x << 32 | (unsigned)y;
}

int find(int x, int y) {
    ull k = key(x, y);
    int l = 1, r = m;
    while (l <= r) {
        int mid = (l + r) >> 1;
        if (s[mid].k < k) l = mid + 1;
        else r = mid - 1;
    }
    return l <= m && s[l].k == k ? s[l].id : 0;
}

int main() {
#ifndef LOCAL
    freopen("nlp.in", "r", stdin);
    freopen("nlp.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> m;
    for (int i = 1; i <= n; i++) cin >> a[i];
    for (int i = 1; i <= m; i++) {
        cin >> x[i] >> y[i] >> z[i];
        s[i] = {key(x[i], y[i]), i};
    }
    if (m == 1) {
        int top = 0;
        for (int i = 1; i <= n; i++) {
            a[++top] = a[i];
            while (top >= 2 && a[top - 1] == x[1] && a[top] == y[1]) {
                a[--top] = z[1];
            }
        }
        n = top;
    } else {
        sort(s + 1, s + m + 1);
        while (true) {
            int j = m + 1, p = 0;
            for (int i = 1; i < n; i++) {
                int k = find(a[i], a[i + 1]);
                if (k && k < j) j = k, p = i;
            }
            if (!p) break;
            a[p] = z[j];
            for (int i = p + 1; i < n; i++) a[i] = a[i + 1];
            n--;
        }
    }
    cout << n << endl;
    for (int i = 1; i <= n; i++) cout << a[i] << (i == n ? '\n' : ' ');
    return 0;
}
