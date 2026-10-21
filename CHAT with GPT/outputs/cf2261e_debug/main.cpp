#include <iostream>
#include <string>
#include <algorithm>
#include <deque>

using namespace std;

const int N = 2e5 + 10;
int t, n, k, c[N], pre[N], ans;
string s;

int main(){
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
    cin >> t;
    while(t--){
        cin >> n >> k >> s; ans = 0;
        int m = 0;
        for(int i = 0, cnt = 0; i < n; i++){
            if(s[i] == '(') cnt++;
            else {c[m++] = cnt; cnt = 0;}
        }
        int sum = 0;
        for(int i = 0; i <= k && i < m; i++){
            sum += c[i];
            ans = max(ans, min(n/2, sum+(k-i)));
        }

        pre[0] = 0;
        deque<int> q;
        q.push_back(0);
        for(int i = 1; i <= m; i++){
            pre[i] = pre[i-1]+c[i-1]-1;
            while(!q.empty() && i-q.front() > k+1) q.pop_front();
            ans = max(ans, pre[i]-pre[q.front()]+1);
            while(!q.empty() && pre[q.back()] >= pre[i]) q.pop_back();
            q.push_back(i);
        }
        cout << ans << '\n';
    }
    return 0;
}
