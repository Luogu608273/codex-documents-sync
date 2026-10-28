#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;
const ll N = 2e6 + 5;
int n, m, cnt, deg[N], head[N], tg[N], c[N];
bool f[N][2];
struct { int v, w, next; } e[N << 1];
void add(int u, int v, int w) { e[++cnt] = {v, w, head[u]}; head[u] = cnt; }
int read() { string s; cin >> s; if (s[0] == 'a') return n + 1; if (s[0] == 'b') return n + 2; return atoi(s.c_str()); }
void topo()
{
    queue<int> q;
    for (int i = 1; i <= n + m + 2; ++i)
        if (!deg[i]) { if (i < n) continue; if (i <= n + 2) f[i][1] = 1; else f[i][0] = 1; q.push(i); }
    for (int u, res; q.size();)
    {
        u = q.front(); q.pop(); res = 0;
        for (int i = head[u], v; i; i = e[i].next)
        {
            v = e[i].v;
            if (!e[i].w)
            {
                if (u <= n + 2) { f[u][0] |= f[v][0]; f[u][1] |= f[v][1]; }
                else { if (f[v][0] && f[v][1]) f[u][0] = f[u][1] = 1; else if (f[v][1]) res ^= 1; }
                continue;
            }
            if (!(--deg[v]) && (v > n + 2 || !tg[v])) q.push(v);
        }
        if (tg[u])
        {
            if (!res && f[c[u]][1] && !(tg[u] & 1)) f[c[u]][0] = 1;
            if (res) { if (f[c[u]][0]) f[c[u]][1] = 1; if (f[c[u]][1] && (tg[u] & 1)) f[c[u]][0] = 1; }
            if (!(--tg[c[u]]) && !deg[c[u]] && (f[c[u]][0] || f[c[u]][1])) q.push(c[u]);
        }
        else if (u > n + 2) f[u][res] = 1;
    }
}
void solve()
{
    cin >> n >> m;
    for (int i = 1; i <= n + m + 2; ++i) f[i][0] = f[i][1] = deg[i] = head[i] = tg[i] = 0;
    cnt = 0;
    for (int i = 1, k; i <= m; ++i)
    {
        cin >> c[i + n + 2] >> k;
        for (int j = 1, x; j <= k; ++j)
        {
            x = read();
            if (x == c[i + n + 2]) { ++tg[i + n + 2]; ++tg[c[i + n + 2]]; continue; }
            add(x, i + n + 2, 1); add(i + n + 2, x, 0); ++deg[i + n + 2];
        }
        add(i + n + 2, c[i + n + 2], 1); add(c[i + n + 2], i + n + 2, 0); ++deg[c[i + n + 2]];
    }
    add(n + 1, n + 1, 0); add(n + 2, n + 2, 0); topo();
    cout << (f[1][1] ? "YES" : "NO") << endl;
}
int main() { ios::sync_with_stdio(false); cin.tie(nullptr); cout.tie(nullptr); int _; cin >> _; while (_--) solve(); }
