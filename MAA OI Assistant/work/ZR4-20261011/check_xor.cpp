#define LOCAL
#define main old_main
#include "../../outputs/ZR4/xor/code.cpp"
#undef main
bool test() {
    int ans = 0, res = 0;
    for (int k = m; k >= 1; k--)
        if (check(ans | (1 << k), k)) ans |= 1 << k;
    for (int i = 1; i <= n; i++)
        for (int j = 1; j <= n; j++) res = max(res, (a[i] ^ a[j]) ^ (a[i] + a[j]));
    if (ans != res) {
        cout << "FAIL " << m << ' ' << n << ' ' << ans << ' ' << res << endl;
        for (int i = 1; i <= n; i++) cout << a[i] << ' ';
        cout << endl;
        return false;
    }
    return true;
}
int main() {
    ll cnt = 0;
    m = 4;
    for (int mask = 1; mask < (1 << 16); mask++) {
        n = 0;
        for (int x = 0; x < 16; x++) if (mask >> x & 1) a[++n] = x;
        if (!test()) return 1;
        cnt++;
    }
    mt19937 rng(20261011);
    for (int t = 0; t < 20000; t++) {
        m = rng() % 11;
        n = rng() % 80 + 1;
        for (int i = 1; i <= n; i++) a[i] = rng() % (1 << m);
        if (!test()) return 1;
        cnt++;
    }
    cout << "XOR PASS " << cnt << endl;
}
