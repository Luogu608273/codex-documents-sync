#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
using ull = unsigned long long;
using u128 = __uint128_t;

const int N = 2000005, V = 32;
const ull P = (1ULL << 61) - 1;
struct Op {
    ull x;
    int op, l, r;
} a[N];
int n, m, k, cnt, bit[N];
ull val[N], h[N], inv[V], pw[V], s[V], e[V];
ull *f;

struct IO {
    static const int M = 1 << 20;
    int p = 0, len = 0, q = 0;
    char s[M], t[M];
    char gc() {
        if (p == len) len = fread(s, 1, M, stdin), p = 0;
        return p == len ? 0 : s[p++];
    }
    ull read() {
        ull x = 0;
        char ch = gc();
        while (ch < '0' || ch > '9') ch = gc();
        while (ch >= '0' && ch <= '9') x = x * 10 + ch - '0', ch = gc();
        return x;
    }
    void write(int x) {
        t[q++] = char('0' + x), t[q++] = '\n';
        if (q == M) fwrite(t, 1, q, stdout), q = 0;
    }
    void flush() {
        fwrite(t, 1, q, stdout);
    }
} io;

ull add(ull x, ull y) {
    x += y;
    return x >= P ? x - P : x;
}

ull sub(ull x, ull y) {
    return x >= y ? x - y : x + P - y;
}

ull mul(ull x, ull y) {
    u128 z = u128(x) * y;
    ull res = (ull(z) & P) + ull(z >> 61);
    return res >= P ? res - P : res;
}

ull qpow(ull a, ull b) {
    ull res = 1;
    for (; b; b >>= 1, a = mul(a, a))
        if (b & 1) res = mul(res, a);
    return res;
}

void modify(int x, int d) {
    for (; x <= n; x += x & -x) {
        bit[x] += d;
        ull *p = f + size_t(x) * (k + 1);
        for (int j = 0; j <= k; j++) p[j] = add(p[j], pw[j]);
    }
}

int query(int x) {
    int res = 0;
    for (; x; x -= x & -x) res += bit[x];
    return res;
}

int query(int u, int v, int d) {
    for (int j = 0; j <= d; j++) s[j] = 0;
    // Fenwick prefixes have a common suffix; it cancels in the difference.
    while (u != v) {
        if (u > v) {
            ull *p = f + size_t(u) * (k + 1);
            for (int j = 0; j <= d; j++) s[j] = add(s[j], p[j]);
            u -= u & -u;
        } else {
            ull *p = f + size_t(v) * (k + 1);
            for (int j = 0; j <= d; j++) s[j] = sub(s[j], p[j]);
            v -= v & -v;
        }
    }
    e[0] = 1;
    for (int i = 1; i <= d + 1; i++) {
        ull res = 0;
        for (int j = 1; j <= i; j++) {
            ull x = mul(e[i - j], s[j - 1]);
            res = j & 1 ? add(res, x) : sub(res, x);
        }
        e[i] = mul(res, inv[i]);
    }
    return e[d + 1] == 0;
}

void solve() {
    n = io.read(), m = io.read(), k = io.read();
    for (int i = 1; i <= m; i++) {
        a[i].op = io.read(), a[i].l = io.read(), a[i].r = io.read();
        if (a[i].op != 3) a[i].x = io.read(), val[++cnt] = a[i].x;
    }
    sort(val + 1, val + cnt + 1);
    cnt = unique(val + 1, val + cnt + 1) - val - 1;
    mt19937_64 rng(chrono::steady_clock::now().time_since_epoch().count());
    uniform_int_distribution<ull> dis(0, P - 1);
    for (int i = 1; i <= cnt; i++) h[i] = dis(rng);
    for (int i = 1; i <= k + 1; i++) inv[i] = qpow(i, P - 2);
    f = new ull[size_t(n + 1) * (k + 1)]();
    for (int i = 1; i <= m; i++) {
        int op = a[i].op, l = a[i].l, r = a[i].r;
        if (op == 3) {
            int d = query(l) - query(r), ans = 1;
            if (d < 0) swap(l, r), d = -d, ans = 2;
            if (!query(l, r, d)) ans = 4;
            else if (!d) ans = 3;
            io.write(ans);
            continue;
        }
        int d = op == 1 ? 1 : -1;
        int x = lower_bound(val + 1, val + cnt + 1, a[i].x) - val;
        ull v = h[x], t = v;
        for (int j = 0; j <= k; j++, t = mul(t, v))
            pw[j] = d == 1 ? t : sub(0, t);
        modify(l, d);
        for (int j = 0; j <= k; j++) pw[j] = sub(0, pw[j]);
        modify(r + 1, -d);
    }
    delete[] f;
    io.flush();
}

int main() {
#ifndef LOCAL
    freopen("set.in", "r", stdin);
    freopen("set.out", "w", stdout);
#endif
    solve();
    return 0;
}
