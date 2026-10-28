#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int B = 30, V = 1 << B, N = 30000005;
struct Node {
    int ch[2], t;
} tr[N];
int tot;

int read() {
    static char buf[1 << 20];
    static int p, len;
    int x = 0;
    char c;
    do {
        if (p == len) len = fread(buf, 1, sizeof(buf), stdin), p = 0;
        c = buf[p++];
    } while (c < '0' || c > '9');
    do {
        x = x * 10 + c - '0';
        if (p == len) {
            len = fread(buf, 1, sizeof(buf), stdin), p = 0;
            if (!len) break;
        }
        c = buf[p++];
    } while (c >= '0' && c <= '9');
    return x;
}

struct Trie {
    int rt, f[B][2], bad[B];
    void init() {
        rt = 0;
        memset(f, 0, sizeof(f));
        memset(bad, 0, sizeof(bad));
    }
    void modify(int k, int v, int t) {
        f[k][v] = t;
        for (int j = 0; j < B; ++j)
            bad[j] = max(j ? bad[j - 1] : 0, min(f[j][0], f[j][1]));
    }
    void clear(int &u, int k, int lim) {
        if (!u) return;
        int t = u < 0 ? -u : tr[u].t;
        if (t < lim || (k >= 0 && t < bad[k])) u = 0;
    }
    void add(int &u, int k, int lim, int a, int d, int t) {
        clear(u, k, lim);
        if (k < 0) {
            u = -t;
            return;
        }
        if (u <= 0) {
            int v = ++tot;
            tr[v].ch[0] = tr[v].ch[1] = u;
            u = v;
        }
        tr[u].t = t;
        int v = (a >> k) & 1;
        if (!((d >> k) & 1)) {
            tr[u].ch[v ^ 1] = -t;
            add(tr[u].ch[v], k - 1, max(lim, f[k][v ^ 1]), a, d, t);
        } else {
            v ^= 1;
            add(tr[u].ch[v], k - 1, max(lim, f[k][v ^ 1]), a, d, t);
        }
    }
    int query(int &u, int k, int lim, int a) {
        clear(u, k, lim);
        if (!u) return V;
        if (u < 0) {
            int t = -u, res = 0;
            for (int j = k; j >= 0; --j) {
                if (f[j][0] > t) res |= a & (1 << j);
                else if (f[j][1] > t) res |= (a ^ (V - 1)) & (1 << j);
            }
            return res;
        }
        int v = (a >> k) & 1;
        int res = query(tr[u].ch[v], k - 1, max(lim, f[k][v ^ 1]), a);
        if (res != V) return res;
        v ^= 1;
        res = query(tr[u].ch[v], k - 1, max(lim, f[k][v ^ 1]), a);
        if (res != V) return res | (1 << k);
        u = 0;
        return V;
    }
} s, q;

void solve() {
    int n = read(), a = read(), g = 1, d = 0;
    int mask = 0, val = 0;
    tot = 0;
    s.init();
    q.init();
    s.rt = -1;
    for (int i = 2; i <= n; ++i) {
        int b = read(), z = a ^ b;
        bool inc = false;
        if (z) {
            int k = 31 - __builtin_clz((unsigned) z);
            int v = (a >> k) & 1, bit = 1 << k;
            if ((mask & bit) && (((val >> k) & 1) != v)) {
                ++g;
                mask = val = 0;
                inc = true;
            } else {
                mask |= bit;
                if (v) val |= bit;
            }
            s.modify(k, v, i);
            q.modify(k, v, i);
        }
        if (inc) {
            swap(s, q);
            q.init();
        }
        if (d < V) {
            if (inc) s.add(s.rt, B - 1, 0, b, d, i);
            else q.add(q.rt, B - 1, 0, b, d, i);
        }
        d = s.query(s.rt, B - 1, 0, b);
        a = b;
    }
    printf("%d\n", g - (s.query(s.rt, B - 1, 0, 0) == 0));
}

int main() {
    int c = read(), _ = read();
    (void) c;
    while (_--) solve();
    return 0;
}
