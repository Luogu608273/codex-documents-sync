#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 2000005;
struct Node {
    int ch[4], fail, dep, mx, out;
    bool end, child;
} tr[N];
int q[N], pre[N], nxt[N], pos[N], tot;

void insert(const string &s) {
    int u = 0;
    for (char c : s) {
        int x = c - 'a';
        if (!tr[u].ch[x]) {
            tr[u].ch[x] = ++tot;
            tr[tot] = {};
            tr[tot].dep = tr[u].dep + 1;
            tr[u].child = true;
        }
        u = tr[u].ch[x];
    }
    tr[u].end = true;
}

int build() {
    int l = 0, r = 0, cnt = 0;
    for (int c = 0; c < 4; c++)
        if (tr[0].ch[c]) q[r++] = tr[0].ch[c];
    while (l < r) {
        int u = q[l++];
        tr[u].mx = tr[u].dep;
        for (int c = 0; c < 4; c++) {
            int v = tr[u].ch[c];
            if (v) {
                tr[v].fail = tr[tr[u].fail].ch[c];
                q[r++] = v;
            } else tr[u].ch[c] = tr[tr[u].fail].ch[c];
        }
    }
    for (int i = r - 1; i >= 0; i--) {
        int u = q[i], f = tr[u].fail;
        tr[f].mx = max(tr[f].mx, tr[u].mx);
    }
    for (int i = 0; i < r; i++) {
        int u = q[i];
        if (tr[u].end && !tr[u].child && tr[u].mx == tr[u].dep) {
            tr[u].out = ++cnt;
            pos[cnt] = 0;
            pre[cnt] = cnt - 1;
            nxt[cnt - 1] = cnt;
        } else tr[u].out = tr[tr[u].fail].out;
    }
    nxt[cnt] = 0;
    pre[0] = cnt;
    return cnt;
}

void solve() {
    int n;
    string s, t;
    cin >> n;
    tot = 0;
    tr[0] = {};
    nxt[0] = pre[0] = 0;
    for (int i = 1; i <= n; i++) {
        cin >> s;
        insert(s);
    }
    cin >> t;
    build();
    int u = 0;
    ll ans = 0;
    for (int i = 1; i <= (int)t.size(); i++) {
        u = tr[u].ch[t[i - 1] - 'a'];
        int x = tr[u].out;
        if (x) {
            // A retained terminal cannot be a proper suffix of a trie prefix.
            pos[x] = i - tr[u].dep + 1;
            nxt[pre[x]] = nxt[x];
            pre[nxt[x]] = pre[x];
            int y = pre[0];
            nxt[y] = x;
            pre[x] = y;
            nxt[x] = 0;
            pre[0] = x;
        }
        ans += pos[nxt[0]];
    }
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("combo.in", "r", stdin);
    freopen("combo.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int _;
    cin >> _;
    while (_--) solve();
    return 0;
}
