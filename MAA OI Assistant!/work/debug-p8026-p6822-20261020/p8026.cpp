#include<iostream>
#include<vector>
#include<map>
using namespace std;
typedef long long ll;
const int p10 = 1e9;
const int N = 5e5 + 10, bs = 1e6 + 3;
const int mod[3] = {998244853, p10 + 3, p10 + 7};
int n, k, q, u, v, i, pw[N][3], s[3], fahs[N][3], ans = 0;
map<int, int> fa[N]; map<int, vector<int> > vc[N];
struct piii{
 int a, b, c;
 bool operator < (const piii & o) const{
  if(a == o.a){
   if(b == o.b) return c < o.c;
   return b < o.b;
  }
  return a < o.a;
 }
}; map<piii, int> mp;
inline void add_n(int u, int i){
 if(!fa[i].count(u)){
  fa[i][u] = u;
  vc[i][u].push_back(u);
 }
}
void upd1(int u, int i, int v){
 int val = --mp[{fahs[u][0], fahs[u][1], fahs[u][2]}];
 ans -= val; if(val == 0) mp.erase({fahs[u][0], fahs[u][1], fahs[u][2]});
 for(int j = 0; j < 3; j++){
  fahs[u][j] = (fahs[u][j] - ((ll)fa[i][u]*pw[i][j]%mod[j]) + mod[j]) % mod[j];
 }
 fa[i][u] = v;
 vc[i][v].push_back(u);
 for(int j = 0; j < 3; j++){
  fahs[u][j] = (fahs[u][j] + (ll)fa[i][u]*pw[i][j]%mod[j]) % mod[j];
 }
 val = mp[{fahs[u][0], fahs[u][1], fahs[u][2]}]++;
 ans += val;
}
void upd(int u, int i, int v){
 for(int p: vc[i][u]) upd1(p, i, v);
 vc[i][u].clear();
}
int fr(int u, int i){
 add_n(u, i);
 if(fa[i][u] == u) return u;
 upd(u, i, fr(fa[i][u], i));
 return fa[i][u];
}
void mg(int u, int v, int i){
 u = fr(u, i); v = fr(v, i);
 if(u == v) return;
 if(vc[i][u].size() <= vc[i][v].size()) upd(u, i, v);
 else upd(v, i, u);
}
int main(){
 ios::sync_with_stdio(0);
 cin.tie(0); cout.tie(0);
 cin >> k >> n >> q;
 pw[1][0] = pw[1][1] = pw[1][2] = s[0] = s[1] = s[2] = 1;
 for(int i = 2; i <= k; i++){
  for(int j = 0; j < 3; j++){
   pw[i][j] = (ll)pw[i-1][j] * bs % mod[j];
   s[j] = (s[j] + pw[i][j]) % mod[j];
  }
 }
 for(int i = 1; i <= n; i++){
  for(int j = 0; j < 3; j++) fahs[i][j] = (ll)i*s[j]%mod[j];
  mp[{fahs[i][0], fahs[i][1], fahs[i][2]}] = 1;
 }
 while(q--){
  cin >> u >> v >> i;
  mg(u, v, i);
  cout << n+ans*2 << '\n';
 }
 return 0;
}
