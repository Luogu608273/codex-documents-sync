#include<iostream>
using namespace std;
typedef long long ll;
const int N = 5e3 + 10, M = 8.3e3 + 10, V = (1 << 13) + 10, B = 13;
const ll inf = 1e18;
int t, n, a[N], b[N], bt[15][2], s;
ll f[M][V], g[M][V];
bool sub = 1;
ll solve1(){
    ll res = 0;
    for(int i = 1; i <= n; i++) f[i][0] = inf;
    f[0][0] = 0;
    for(int l = 1; l < n; l++){
        for(int j = 0; j < B; j++) bt[j][0] = 0;
        for(int i = l; i < n; i++){
            bool fg = 0;
            for(int j = 0; j < B; j++) bt[j][1] = 0;
            for(int j = B-1; j >= 0; j--){
                if(a[i] & (1 << j)){
                    if(a[i+1] & (1 << j)) bt[j][1] = 0;
                    else{
                        bt[j][1] = 2;
                        if(bt[j][0] == 1) fg = 1;
                        break;
                    }
                }
                else{
                    if(a[i+1] & (1 << j)){
                        bt[j][1] = 1;
                        if(bt[j][0] == 2) fg = 1;
                        break;
                    }
                    else bt[j][1] = 0;
                }
            }
            if(fg) break;
            for(int j = 0; j < B; j++) if(bt[j][1] != 0) bt[j][0] = bt[j][1];
            f[i][0] = min(f[i][0], f[l-1][0] + b[i]);
        }
    }
    return f[n-1][0] + b[n];
}
ll solve2(){
    for(int i = 0; i < a[n]; i++) f[n][i] = inf;
    f[n][a[n]] = 0;
    for(int i = 0; i <= a[n]; i++) g[n][i] = 0;
    for(int i = n-1; i >= 1; i--){
        g[i][a[n]+1] = inf;
        for(int j = a[n]; j >= 0; j--){
            int val = (a[i]^a[i+1]^j);
            f[i][j] = min(g[i+1][j]+b[i], ((j <= val && val <= a[n]) ? f[i+1][val] : inf));
            g[i][j] = min(f[i][j], g[i][j+1]);
        }
    }
    return g[1][0];
}
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    cin >> t;
    while(t--){
        cin >> n; sub = 1;
        for(int i = 1; i <= n; i++){
            cin >> a[i];
            sub &= (a[i-1] <= a[i]);
        }
        for(int i = 1; i <= n; i++) cin >> b[i];
        if(sub){
            cout << 0 << '\n';
            continue;
        }
        cout << min(solve1(), solve2()) << '\n';
    }
    return 0;
}
