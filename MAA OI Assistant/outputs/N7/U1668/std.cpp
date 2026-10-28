#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 1000005, P = 1000003, K = 6;
int n, q, s[N][3], pre[N][K], suf[N][K], inv[P];
int b[K][K], pos[K];

void insert(int id, bool rev) {
    int x = (s[id][0] - s[id][1] + P) % P;
    int y = (s[id][1] - s[id][2] + P) % P;
    int v[K] = {1, x, y, (int)((ll)y * (2 * x + y) % P),
        (int)((ll)x * (x + 2 * y) % P), (int)((ll)x * y % P * (x + y) % P)};
    for (int i = 0; i < K; i++) {
        if (!v[i]) continue;
        if (pos[i] < 0) {
            pos[i] = id;
            for (int j = i; j < K; j++) b[i][j] = v[j];
            return;
        }
        if (rev ? id < pos[i] : id > pos[i]) {
            swap(id, pos[i]);
            for (int j = i; j < K; j++) swap(v[j], b[i][j]);
        }
        int t = (ll)v[i] * inv[b[i][i]] % P;
        for (int j = i + 1; j < K; j++) {
            v[j] = (v[j] - (ll)t * b[i][j]) % P;
            if (v[j] < 0) v[j] += P;
        }
        v[i] = 0;
    }
}

bool check(int l, int r) {
    int x = s[r][0] - s[l][0], y = s[r][1] - s[l][1], z = s[r][2] - s[l][2];
    return x != y && x != z && y != z;
}

void init() {
    inv[1] = 1;
    for (int i = 2; i < P; i++) inv[i] = P - (ll)(P / i) * inv[P % i] % P;
    memset(pos, -1, sizeof(pos));
    for (int i = 0; i <= n; i++) {
        insert(i, false);
        for (int j = 0; j < K; j++) pre[i][j] = pos[j];
    }
    memset(pos, -1, sizeof(pos));
    memset(b, 0, sizeof(b));
    for (int i = n; i >= 0; i--) {
        insert(i, true);
        for (int j = 0; j < K; j++) suf[i][j] = pos[j];
    }
}

void solve() {
    int c;
    cin >> c >> n >> q;
    for (int i = 1, x; i <= n; i++) {
        cin >> x;
        for (int j = 0; j < 3; j++) s[i][j] = s[i - 1][j];
        s[i][x - 1]++;
    }
    init();
    while (q--) {
        int l, r, ans = 0;
        cin >> l >> r;
        l--;
        if (check(l, r)) {
            cout << r - l << endl;
            continue;
        }
        for (int i = 0; i < K; i++) {
            int x = suf[l][i];
            if (x < l || x > r) continue;
            for (int j = 0; j < K; j++) {
                int y = pre[r][j];
                if (y <= x || y - x <= ans) continue;
                if (check(x, y)) ans = y - x;
            }
        }
        cout << ans << endl;
    }
}

int main() {
#ifndef LOCAL
    freopen("three.in", "r", stdin);
    freopen("three.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
