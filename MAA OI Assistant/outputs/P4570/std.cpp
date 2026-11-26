#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int V = 60;
ll a[V + 1], b[V], mask[V];
int w[V + 1], cnt;

// 插入成功返回 0，否则返回表示 x 的已选元素集合。
ll insert(ll x, int p) {
    ll s = 0;
    for (int i = V - 1; i >= 0; i--) {
        if (!(x >> i & 1)) continue;
        if (!b[i]) {
            b[i] = x;
            mask[i] = s | (1LL << p);
            return 0;
        }
        x ^= b[i];
        s ^= mask[i];
    }
    return s;
}

void build() {
    memset(b, 0, sizeof(b));
    memset(mask, 0, sizeof(mask));
    for (int i = 1; i <= cnt; i++) insert(a[i], i);
}

void solve() {
    int n;
    cin >> n;
    while (n--) {
        ll x;
        int v;
        cin >> x >> v;
        ll s = insert(x, cnt + 1);
        if (!s) {
            cnt++;
            a[cnt] = x;
            w[cnt] = v;
            continue;
        }
        int p = 0;
        for (int i = 1; i <= cnt; i++) {
            if ((s >> i & 1) && (!p || w[i] < w[p])) p = i;
        }
        if (v <= w[p]) continue;
        a[p] = x;
        w[p] = v;
        build();
    }
    int ans = 0;
    for (int i = 1; i <= cnt; i++) ans += w[i];
    cout << ans << endl;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
