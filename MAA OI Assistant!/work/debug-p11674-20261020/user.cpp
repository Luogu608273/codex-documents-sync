#include<iostream>
#include<string>
#include<vector>
using namespace std;
typedef long long ll;
const int N = 2e5 + 10;
int n, m, u, v, fa[N], sz[N];
string s; ll ans, a[N];
vector<int> g[N];
int fr(int u){
 if(u == fa[u]) return u;
 return fa[u] = fr(fa[u]);
}
ll pw(int x){ return (ll)x*(x-1)/2; }
void mg(int u, int v){
 u = fr(u), v = fr(v);
 if(u == v) return;
 ans -= pw(sz[u]); ans -= pw(sz[v]);
 sz[v] += sz[u]; fa[u] = v;
 ans += pw(sz[v]);
}
int main(){
 cin >> n >> m >> s;
 for(int i = 1; i <= n; i++) fa[i] = i;
 for(int i = 1; i <= m; i++){
  cin >> u >> v;
  if(u > v) swap(u, v);
  if(s[u-1] == '0') g[u].push_back(v);
  else mg(u, v);
 }
 for(int i = n; i >= 1; i--){
  for(int j: g[i]) mg(i, j);
  int u = fr(i);
  ans -= pw(sz[u]);
  sz[u]++;
  ans += pw(sz[u]);
  a[i] = ans;
 }
 for(int i = 1; i <= n; i++) cout << a[i] << '\n';
 return 0;
}
