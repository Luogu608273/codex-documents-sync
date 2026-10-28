#include<iostream>
using namespace std;
typedef long long ll;
const int N = 310, mod = 1e9 + 7;
int n, a[N], f[N][N][N], g[N][N][N], q, q1, q2, op, x, l, r, k;
int main(){
    ios::sync_with_stdio(0);
    cin.tie(0); cout.tie(0);
    cin >> n >> q1 >> q2;
    for(int i = 1; i <= n; i++){
        cin >> a[i];
        f[0][i][i] = 1;
        for(int j = 1; j <= i; j++) g[0][i][j] = 1;
    }
    for(int i = 1; i <= n; i++){
        for(int j = 1; j <= n; j++){
            for(int k = 1; k <= n; k++){
                f[i][j][k] = (f[i-1][j][k] + f[i][j-1][k]) % mod;
            }
        }
    }
    for(int i = 1; i <= n; i++){
        for(int j = 0; j <= n; j++){
            for(int k = 1; k <= n; k++){
                g[i][j][k] = (g[i-1][j][k] - g[i-1][j+1][k] + mod) % mod;
            }
        }
    }
    q = q1 + q2;
    while(q--){
        cin >> op >> x >> l >> r;
        if(op == 1){
            cin >> k;
            for(int i = 1; i <= n; i++){
                int val1 = ((ll)g[x][l-1][i] * k % mod + mod) % mod;
                int val2 = ((ll)g[x][r][i] * k % mod + mod) % mod;
                a[i] = (a[i] - val1 + mod) % mod;
                a[i] = (a[i] + val2) % mod;
            }
        }
        else{
            int ans = 0;
            for(int i = 1; i <= n; i++){
                int val1 = ((ll)f[x+1][l-1][i] * a[i] % mod + mod) % mod;
                int val2 = ((ll)f[x+1][r][i] * a[i] % mod + mod) % mod;
                ans = (ans - val1 + mod) % mod;
                ans = (ans + val2) % mod;
            }
            cout << ans << '\n';
        }
    }
    return 0;
}
