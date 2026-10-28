#include <bits/stdc++.h>
using namespace std;
struct Node { long long c1; int lc, rc; bool tg; };
const long long V = 1000000000000000000LL;
int main() {
    long long pre[61], nodes = 1, first = 0;
    fill(pre, pre + 61, -1);
    for (int i = 1; i <= 200000; ++i) {
        long long p = i * 5000000000000LL, l = 1, r = V;
        for (int d = 1; l < r; ++d) {
            long long mid = (l + r) / 2;
            if (p <= mid) r = mid;
            else l = mid + 1;
            if (pre[d] != l) ++nodes;
            pre[d] = l;
        }
        if (!first && nodes > 8000400) first = i;
    }
    long long bound = 1;
    for (int d = 0; d < 60; ++d) bound += 2 * min(1LL << d, 400000LL);
    cout << "sizeof(Node)=" << sizeof(Node) << '\n';
    cout << "point_update_nodes=" << nodes << '\n';
    cout << "first_exceed_capacity=" << first << '\n';
    cout << "all_operations_node_bound=" << bound << '\n';
}
