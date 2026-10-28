#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

const int N = 155;
const ll V = -(1LL << 60);
int n, A, B;
struct Node {
    int c;
    ll u, v;
} a[N];
ll f[N][N][N];

bool cmp(Node x, Node y) {
    return x.c > y.c;
}

void solve() {
    cin >> n >> A >> B;
    for (int i = 1; i <= n; i++) cin >> a[i].c >> a[i].u >> a[i].v;
    sort(a + 1, a + n + 1, cmp);
    int m = min(A, B);
    for (int r = 0; r <= m; r++)
        for (int x = 0; x <= A; x++)
            for (int y = 0; y <= B; y++) f[r][x][y] = V;
    for (int r = 0; r <= m; r++) f[r][A - r][B - r] = 0;
    for (int i = 1; i <= n; i++) {
        int c = a[i].c;
        ll u = a[i].u, v = a[i].v;
        // Every transition decreases the lexicographic order of (r,x,y).
        for (int r = 0; r <= m; r++) {
            for (int x = 0; x + r <= A; x++) {
                for (int y = 0; y + r <= B; y++) {
                    ll z = f[r][x][y];
                    if (z == V) continue;
                    if (r >= c) f[r - c][x][y] = max(f[r - c][x][y], z + u + v);
                    if (x >= c && y < c) f[r][x - c][y] = max(f[r][x - c][y], z + u);
                    if (y >= c && x < c) f[r][x][y - c] = max(f[r][x][y - c], z + v);
                }
            }
        }
    }
    ll ans = 0;
    for (int x = 0; x <= A; x++)
        for (int y = 0; y <= B; y++) ans = max(ans, f[0][x][y]);
    cout << ans << endl;
}

int main() {
#ifndef LOCAL
    freopen("greedy.in", "r", stdin);
    freopen("greedy.out", "w", stdout);
#endif
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    solve();
    return 0;
}
