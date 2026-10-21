#include <iostream>
#include <string>
using namespace std;
const int N = 2e5 + 10;
int t, n, k, c[N], ans; string s;
int main(){
    cin >> t;
    while(t--){
        cin >> n >> k >> s; ans = 0;
        for(int i = 0, j = 0, cnt = 0; i < s.size(); i++){
            if(s[i] == '(') cnt++;
            else {c[j++] = cnt; cnt = 0;}
        }
        int s = 0;
        for(int i = 0; i <= k; i++){
            s += c[i];
            ans = max(ans, min(n/2, s+(k-i)));
        }
        s = 0;
        for(int i = 1, j = 1; i <= n/2; i++){
            s += c[i]-1;
            while(j < i && (c[j] < 0 || i-j > k)) s -= c[j++];
            ans = max(ans, s+1);
        }
        cout << ans << '\n';
    }
    return 0;
}
