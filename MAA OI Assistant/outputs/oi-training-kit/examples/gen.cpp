#include <bits/stdc++.h>
#define endl '\n'
using namespace std;
using ll = long long;

int main(int argc, char **argv) {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    if (argc != 2) return 1;
    mt19937_64 rng(strtoull(argv[1], nullptr, 10));
    int n = int(rng() % 30) + 1;
    cout << n << endl;
    for (int i = 1; i <= n; ++i)
        cout << ll(rng() % 2000001) - 1000000 << " \n"[i == n];
    return 0;
}
