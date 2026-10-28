#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const int N = 20005, P = 1000000007, K = 60;

struct Mat {
    ll a[4][4];
};

ll n, f[4];
int m;
pair<ll, int> a[N];
Mat t[4], pw[K];

Mat mul(const Mat &a, const Mat &b) {
    Mat c = {};
    for (int i = 0; i < 4; i++)
        for (int k = 0; k < 4; k++)
            for (int j = 0; j < 4; j++)
                (c.a[i][j] += a.a[i][k] * b.a[k][j]) %= P;
    return c;
}

void update(const Mat &a) {
    ll g[4] = {};
    for (int i = 0; i < 4; i++)
        for (int j = 0; j < 4; j++)
            (g[j] += f[i] * a.a[i][j]) %= P;
    for (int i = 0; i < 4; i++) f[i] = g[i];
}

void jump(ll len) {
    for (int k = 0; len; k++, len >>= 1)
        if (len & 1) update(pw[k]);
}

void init() {
    int l[4] = {3, 2, 3, 1};
    int r[4] = {2, 3, 1, 3};
    for (int b = 0; b < 4; b++) {
        for (int s = 0; s < 4; s++) {
            if (s & b) continue;
            int v = s | b;
            t[b].a[s][0] = 1;
            for (int k = 0; k < 4; k++)
                if (!(v & l[k])) t[b].a[s][r[k]]++;
        }
    }
    pw[0] = t[0];
    for (int i = 1; i < K; i++) pw[i] = mul(pw[i - 1], pw[i - 1]);
}

void solve() {
    cin >> n >> m;
    for (int i = 1; i <= m; i++) {
        int x;
        ll y;
        cin >> x >> y;
        a[i] = {y, 1 << (x - 1)};
    }
    sort(a + 1, a + m + 1);
    f[0] = 1;
    ll last = 0;
    for (int i = 1; i <= m; ) {
        int j = i, b = 0;
        ll y = a[i].first;
        while (j <= m && a[j].first == y) {
            b |= a[j].second;
            j++;
        }
        jump(y - last - 1);
        update(t[b]);
        last = y;
        i = j;
    }
    jump(n - last);
    cout << f[0] << endl;
}

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    init();
    solve();
    return 0;
}
