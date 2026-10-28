#define LOCAL
#define main old_main
#include "../../outputs/ZR4/game/code.cpp"
#undef main
bool b[100][100];
void init(int len) {
    n = len;
    z = 1;
    while (z < n) z <<= 1;
    fill(tr, tr + (z << 1), E);
    for (int i = 1; i < n; i++) tr[z + i - 1] = leaf(i);
    for (int i = z - 1; i; i--) tr[i] = merge(tr[i << 1], tr[i << 1 | 1]);
}
void brute() {
    memset(b, 0, sizeof(b));
    for (int len = 3; len <= n; len++)
        for (int l = 1, r = len; r <= n; l++, r++) {
            int mask = 0;
            for (int j = l; j < r; j++) mask |= s[j] == 1 ? 1 : s[j] == -1 ? 2 : 0;
            if (mask == 3) b[l][r] = !b[l + 1][r] || !b[l][r - 1];
        }
}
int main() {
    ll cnt = 0;
    for (int len = 1, all = 1; len <= 11; len++, all *= 3)
        for (int mask = 0; mask < all; mask++) {
            int v = mask;
            for (int i = 1; i < len; i++, v /= 3) s[i] = v % 3 - 1;
            init(len);
            brute();
            for (int l = 1; l <= n; l++)
                for (int r = l; r <= n; r++) {
                    cnt++;
                    if (win(l, r) != b[l][r]) {
                        cout << "FAIL " << len << ' ' << mask << ' ' << l << ' ' << r << endl;
                        return 1;
                    }
                }
        }
    mt19937 rng(20261011);
    for (int t = 0; t < 2000; t++) {
        n = rng() % 60 + 1;
        for (int i = 1; i <= n; i++) a[i] = rng() % 8 + 1;
        for (int i = 1; i < n; i++) s[i] = (a[i + 1] > a[i]) - (a[i + 1] < a[i]);
        init(n);
        for (int j = 0; j < 50; j++) {
            int x = rng() % n + 1;
            a[x] = rng() % 8 + 1;
            modify(x - 1);
            modify(x);
            brute();
            for (int k = 0; k < 10; k++) {
                int l = rng() % n + 1, r = rng() % n + 1;
                if (l > r) swap(l, r);
                cnt++;
                if (win(l, r) != b[l][r]) {
                    cout << "DYNAMIC FAIL " << t << ' ' << j << ' ' << l << ' ' << r << endl;
                    return 1;
                }
            }
        }
    }
    cout << "GAME PASS " << cnt << endl;
}
