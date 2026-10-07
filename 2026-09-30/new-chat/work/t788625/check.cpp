#define main solution_main
#include "main.cpp"
#undef main
#include <boost/multiprecision/cpp_int.hpp>
using boost::multiprecision::cpp_int;
cpp_int fac[201];

int main() {
    init();
    fac[0] = 1;
    for (int i = 1; i <= 200; i++) fac[i] = fac[i - 1] * i;
    stringstream in, out;
    vector<ll> ans;
    for (int n = 1; n <= 200; n++) {
        for (int m = 1; m <= 200; m++) {
            in << n << ' ' << m << '\n';
            if (n % m) ans.push_back(0);
            else {
                int k = n / m;
                cpp_int d = fac[k];
                for (int i = 1; i <= k; i++) d *= m;
                cpp_int a = fac[n] / d % m;
                ans.push_back(a.convert_to<ll>());
            }
        }
    }
    ll n[] = {4, 13, 15, 39, 28, 2000000014ll, 1000000000000000000ll, 9998200081ll};
    ll m[] = {4, 1, 4, 13, 7, 1000000007ll, 10000000000ll, 9998200081ll};
    ll a[] = {2, 0, 0, 12, 1, 1, 0, 0};
    for (int i = 0; i < 8; i++) {
        in << n[i] << ' ' << m[i] << '\n';
        ans.push_back(a[i]);
    }
    auto cin_buf = cin.rdbuf(in.rdbuf());
    auto cout_buf = cout.rdbuf(out.rdbuf());
    for (size_t i = 0; i < ans.size(); i++) solve();
    cin.rdbuf(cin_buf);
    cout.rdbuf(cout_buf);
    ll x;
    for (size_t i = 0; i < ans.size(); i++) {
        if (!(out >> x) || x != ans[i]) {
            cerr << "Mismatch at case " << i + 1 << ", expected " << ans[i] << ", got " << x << '\n';
            return 1;
        }
    }
    cout << "Verified " << ans.size() << " cases.\n";
}
