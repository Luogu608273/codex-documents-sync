#include<iostream>
#include<vector>
#include<algorithm>
#include<queue>
using namespace std;
typedef long long ll;
const int N = 4e5 + 10;
int n, m, u, v, w, a[N]; ll dis[N];
bool vis[N];
struct pii{
 int v, w, id;
 bool operator < (const pii & o) const{ return w < o.w; }
};
vector<pii> g1[N];
vector<pii> g2[N];
struct pii2{
 int v; ll w;
 bool operator < (const pii2 & o) const{ return w > o.w; }
};
priority_queue<pii2> pq;
int main(){
 cin >> n >> m;
 for(int i = 1; i <= m; i++){
  cin >> u >> v >> w; a[i+1] = w;
  g1[u].push_back({v, w, i+1});
  g1[v].push_back({u, w, i+1});
 }
 for(int i = 1; i <= n; i++){
  sort(g1[i].begin(), g1[i].end());
  for(int j = 0; j < g1[i].size()-1; j++){
   g2[g1[i][j].id].push_back({g1[i][j+1].id, g1[i][j+1].w-g1[i][j].w, 0});
   g2[g1[i][j+1].id].push_back({g1[i][j].id, 0, 0});
  }
 }
 for(auto i: g1[1]) g2[1].push_back({i.id, i.w, 0});
 for(auto i: g1[n]) g2[i.id].push_back({m+2, 0, 0});
 pq.push({1, 0});
 while(pq.size()){
  pii2 tp = pq.top(); pq.pop();
  if(vis[tp.v]) continue;
  dis[tp.v] = tp.w + a[tp.v]; vis[tp.v] = 1;
  for(auto ed: g2[tp.v]){
   if(vis[ed.v]) continue;
   pq.push({ed.v, tp.w+a[tp.v]+ed.w});
  }
 }
 cout << dis[m+2];
 return 0;
}
