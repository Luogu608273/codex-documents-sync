#include <bits/stdc++.h>
using namespace std;
int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    int c, t;
    cin >> c >> t;
    while (t--) {
        int n;
        cin >> n;
        vector<int> a(n);
        int w = 1;
        for (int &x : a) cin >> x;
        while (w <= *max_element(a.begin(), a.end())) w *= 2;
        int k = 1;
        while (k < n) k *= 2;
        w *= k;
        vector<int> f(w, 1), h(w), suf(w + 1, n + 1);
        f[a.back()] = 0;
        for (int i = n - 2; i >= 0; --i) {
            for (int x = w - 1; x >= 0; --x) suf[x] = min(suf[x + 1], f[x]);
            int d = a[i] ^ a[i + 1];
            for (int x = 0; x < w; ++x) {
                h[x] = suf[x] + 1;
                if (x <= (x ^ d)) h[x] = min(h[x], f[x ^ d]);
            }
            f.swap(h);
        }
        cout << *min_element(f.begin(), f.end()) << '\n';
    }
}
