#include <bits/stdc++.h>
using namespace std;
int main() {
    freopen("sect.in", "r", stdin);
    freopen("sect.out", "w", stdout);
    ios::sync_with_stdio(false); cin.tie(nullptr);
    int n,k; cin >> n >> k;
    vector<vector<int>> tr(n+1);
    for (int i=1,u,v; i<n; ++i) cin >> u >> v,tr[u].push_back(v),tr[v].push_back(u);
    vector<int> c(n+1), count(k+1), par(n+1), order(1,1), same(k+1);
    for (int i=1; i<=n; ++i) cin >> c[i],++count[c[i]];
    vector<long long> w(k+1); for (int i=1; i<=k; ++i) cin >> w[i];
    for (int i=0; i<n; ++i) for (int v:tr[order[i]]) if (v!=par[order[i]])
        par[v]=order[i],order.push_back(v);
    for (int v=2; v<=n; ++v) if(c[v]==c[par[v]]) ++same[c[v]];
    for (int t=1; t<=k; ++t) if(same[t]==count[t]-1) {cout<<0<<'\n';return 0;}
    vector<vector<int>> g(k+1);
    vector<int> sub(n+1), mark(k+1);
    for(int t=1; t<=k; ++t) {
        for(int v=1; v<=n; ++v) sub[v]=(c[v]==t);
        for(int i=n-1; i>0; --i) sub[par[order[i]]]+=sub[order[i]];
        g[t].push_back(t); mark[t]=t;
        for(int v=2; v<=n; ++v) if(sub[v]>0 && sub[v]<count[t]) {
            for(int u:{v,par[v]}) if(mark[c[u]]!=t)
                mark[c[u]]=t,g[t].push_back(c[u]);
        }
    }
    vector<int> dfn(k+1),low(k+1),comp(k+1),st;
    vector<char> in(k+1);int timer=0,cc=0;
    function<void(int)> dfs=[&](int u) {
        dfn[u]=low[u]=++timer;st.push_back(u);in[u]=1;
        for(int v:g[u]) if(!dfn[v]) dfs(v),low[u]=min(low[u],low[v]);
        else if(in[v]) low[u]=min(low[u],dfn[v]);
        if(low[u]==dfn[u]) {++cc;while(true){int v=st.back();st.pop_back();in[v]=0;comp[v]=cc;if(v==u)break;}}
    };
    for(int t=1;t<=k;++t) if(!dfn[t]) dfs(t);
    vector<long long> sum(cc+1),mx(cc+1);vector<char> out(cc+1);
    for(int t=1;t<=k;++t) {sum[comp[t]]+=w[t];mx[comp[t]]=max(mx[comp[t]],w[t]);
        for(int v:g[t]) if(comp[t]!=comp[v])out[comp[t]]=1;}
    long long ans=LLONG_MAX;
    for(int i=1;i<=cc;++i)if(!out[i])ans=min(ans,sum[i]-mx[i]);
    cout<<ans<<'\n';
}
