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
struct Node {
    int j, p, v, w;
    bool operator < (const Node &b) const {
        return j != b.j ? j > b.j : p > b.p;
    }
};
int n, m, tot, a[N], z[N], pre[N], nxt[N], ver[N];
bool dead[N];
priority_queue<Node> q;

ull key(int x, int y) {
    return (ull)x << 32 | (unsigned)y;
}

int find(int x, int y) {
    ull k = key(x, y);
    int l = 1, r = tot;
    while (l <= r) {
        int mid = (l + r) >> 1;
        if (s[mid].k < k) l = mid + 1;
        else r = mid - 1;
    }
    return l <= tot && s[l].k == k ? s[l].id : 0;
}

void add(int p) {
    if (!p || dead[p] || !nxt[p]) return;
    int j = find(a[p], a[nxt[p]]);
    if (j) q.push({j, p, ver[p], ver[nxt[p]]});
}

int main() {
#ifndef LOCAL
    freopen("nlp.in", "r", stdin);
    freopen("nlp.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> n >> m;
    for (int i = 1; i <= n; i++) {
        cin >> a[i];
        pre[i] = i - 1;
        nxt[i] = i == n ? 0 : i + 1;
    }
    for (int i = 1, x, y; i <= m; i++) {
        cin >> x >> y >> z[i];
        s[i] = {key(x, y), i};
    }
    sort(s + 1, s + m + 1);
    for (int i = 1; i <= m; i++)
        if (!tot || s[i].k != s[tot].k) s[++tot] = s[i];
    for (int i = 1; i < n; i++) add(i);
    int len = n;
    while (!q.empty()) {
        Node t = q.top();
        q.pop();
        int p = t.p, r = nxt[p];
        if (dead[p] || !r || t.v != ver[p] || t.w != ver[r]) continue;
        a[p] = z[t.j];
        ver[p]++;
        dead[r] = true;
        nxt[p] = nxt[r];
        if (nxt[r]) pre[nxt[r]] = p;
        len--;
        add(pre[p]);
        add(p);
    }
    cout << len << endl;
    for (int p = 1; p; p = nxt[p]) cout << a[p] << (nxt[p] ? ' ' : '\n');
    return 0;
}
