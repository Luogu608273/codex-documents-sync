#include<iostream>
using namespace std;
const int N = 1e6 + 10, M = 5e3 + 10;
int c, t, n, a[N], hgb[N], hgv[N], v1, v2, ans, f[N], mn[N], g[40][2];
bool sub = 1, fg;
inline int highbit(int x){
 if(x == 0) return -1;
 x |= (x >> 1); x |= (x >> 2); x |= (x >> 4); x |= (x >> 8); x |= (x >> 16);
 return x - (x >> 1);
}
void clean_dfs(){ for(int i = 29; i >= 0; i--) g[i][0] = g[i][1] = -2; }
int dfs(int p, bool b, int & mn, int & l, int & v1, int & v2){
 if(p == -1) return (b ? 0 : -1);
 if(g[p][b] != -2) return g[p][b];
 int res = (1 << 30), bt = l & (1 << p), mb = mn & (1 << p);
 bool b1 = ((v1 & (1 << p)) == 0) || ((v1 & (1 << p)) && (v2 & (1 << p)));
 bool b2 = ((v1 & (1 << p)) == 0) || ((v1 & (1 << p)) && (v2 & (1 << p)) == 0);
 if(b1){
  int rt = 0;
  if(mn == -1 || mb < (bt^(1 << p))) rt = dfs(p-1, 1, mn, l, v1, v2);
  else if(mb == (bt^(1 << p))) rt = dfs(p-1, b, mn, l, v1, v2);
  if(rt != -1) res = min(res, rt|(1 << p));
 }
 if(b2){
  int rt = 0;
  if(mn == -1 || mb < bt) rt = dfs(p-1, 1, mn, l, v1, v2);
  else if(mb == bt) rt = dfs(p-1, b, mn, l, v1, v2);
  if(rt != -1) res = min(res, rt);
 }
 return g[p][b] = (res == (1 << 30) ? -1 : res);
}
int main(){
 ios::sync_with_stdio(0); cin.tie(0); cout.tie(0);
 cin >> c >> t;
 while(t--){
  cin >> n; sub = 1;
  for(int i = 1; i <= n; i++){ cin >> a[i]; sub &= (a[i-1] <= a[i]); }
  for(int i = 1; i < n; i++){ hgb[i] = highbit(a[i]^a[i+1]); if(hgb[i] != -1) hgv[i] = a[i]&hgb[i]; }
  if(sub){ cout << 0 << '\n'; continue; }
  ans = 1; v1 = v2 = 0;
  for(int i = 1; i < n; i++){
   f[i] = ans;
   if(hgb[i] == -1) continue;
   if((v1&hgb[i]) && (v2&hgb[i]) != hgv[i]){ ans++; v1 = v2 = 0; }
   else{ v1 |= hgb[i]; v2 |= hgv[i]; }
  }
  f[n] = ans;
  for(int i = 1; i < n; i++){
   v1 = v2 = 0;
   for(int j = i-1; j >= 0; j--){
    if(hgb[j] != -1 && (v1&hgb[j]) && (v2&hgb[j]) != hgv[j]) break;
    if(f[j] < f[i]-1) break;
    if(f[j] == f[i]-1){
     int nv2 = v2^a[i]; int nl = a[i]^a[j+1]; int m1 = mn[j]-1;
     clean_dfs(); mn[i] = dfs(29, 0, m1, nl, v1, nv2);
    }
    if(hgb[j] != -1) v1 |= hgb[j], v2 |= hgv[j];
   }
  }
  fg = 0;
  for(int i = n; i >= 1; i--){
   if(i < n && a[i] > a[i+1]) break;
   if(mn[i-1] <= a[i]){ fg = 1; break; }
  }
  cout << ans-fg << '\n';
 }
 return 0;
}
