#include<iostream>
using namespace std;
const int N = 510;
int n, m, x, y, r, z, a[N][N], b[N][N];
void f(int x, int y, int r, int z){
    if(z^1){
        for(int i = x - r, p = x + r; i <= x + r; i++, p--){
            for(int j = y - r; j <= y + r; j++){
                b[x + j - y][y + i - x] = a[p][j];
            }
        }
    }
    else{
        for(int i = x - r; i <= x + r; i++){
            for(int j = y - r, p = y + r; j <= y + r; j++, p--){
                b[x + j - y][y + i - x] = a[i][p];
            }
        }
    }
    for(int i = x - r; i <= x + r; i++){
        for(int j = y - r; j <= y + r; j++){
            a[i][j] = b[i][j];
        }
    }
}
int main(){
    cin >> n >> m;
    for(int i = 0; i < n * n; i++) a[i / n][i % n] = i + 1;
    for(int i = 0; i < m; i++){
        cin >> x >> y >> r >> z;
        f(x-1, y-1, r, z);
    }
    for(int j = 0; j < n; j++){
        for(int k = 0; k < n; k++) cout << a[j][k] << ' ';
        cout << endl;
    }
    return 0;
}
