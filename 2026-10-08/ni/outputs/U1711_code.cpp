#include <bits/stdc++.h>
using namespace std;
using ll = long long;
struct Event { ll x,l,r; bool add; bool operator<(const Event &b) const {return x<b.x;} };
struct Runs {
    ll K, H;
    map<ll,ll> a; // y -> phase; H is a permanent sentinel.
    map<ll,int> count;
    int bad = 0;
    Runs(ll k,ll h):K(k),H(h) {a[0]=-1;a[H]=-1;}
    void contribution(map<ll,ll>::iterator it,int sign) {
        if(it->first==H || it->second<0) return;
        ll len=next(it)->first-it->first, p=it->second;
        bad += sign*(len%K!=0);
        auto q=count.find(p);
        if(sign>0) {
            if(q==count.end())count[p]=1;
            else ++q->second;
        } else if(--q->second==0)count.erase(q);
    }
    map<ll,ll>::iterator split(ll y) {
        auto it=prev(a.upper_bound(y));
        if(it->first==y)return it;
        contribution(it,-1);
        auto z=a.emplace(y,it->second).first;
        contribution(it,1);contribution(z,1);
        return z;
    }
    bool assign(ll l,ll r,ll expected,ll value) {
        auto right=split(r),left=split(l);
        for(auto it=left;it!=right;++it)if(it->second!=expected)return false;
        for(auto it=left;it!=right;++it)contribution(it,-1);
        a.erase(left,right);
        auto it=a.emplace(l,value).first;contribution(it,1);
        if(it!=a.begin()) {
            auto p=prev(it);
            if(p->second==it->second) {
                contribution(p,-1);contribution(it,-1);
                a.erase(it);it=p;contribution(it,1);
            }
        }
        auto q=next(it);
        if(q->first!=H && q->second==it->second) {
            contribution(it,-1);contribution(q,-1);
            a.erase(q);contribution(it,1);
        }
        return true;
    }
};
int main() {
    freopen("tile.in","r",stdin);
    freopen("tile.out","w",stdout);
    ios::sync_with_stdio(false);cin.tie(nullptr);
    int n;ll K;cin>>n>>K;
    vector<ll>x(n),y(n);ll H=0,M=0;
    for(int i=0;i<n;++i)cin>>x[i]>>y[i],H=max(H,y[i]),M=max(M,x[i]);
    if(K==1){cout<<M<<'\n';return 0;}
    __int128 area=0;
    for(int i=0;i<n;++i){int j=(i+1)%n;area+=(__int128)x[i]*y[j]-(__int128)x[j]*y[i];}
    vector<Event>e;
    for(int i=0;i<n;++i){int j=(i+1)%n;if(x[i]==x[j])
        e.push_back({x[i],min(y[i],y[j]),max(y[i],y[j]),(area>0)==(y[j]<y[i])});}
    sort(e.begin(),e.end());
    Runs runs(K,H);ll ans=0,last=0;
    for(int i=0;i<(int)e.size();) {
        ll X=e[i].x;
        if(runs.count.empty())ans=max(ans,X);
        else if(runs.count.size()==1) {
            ll p=runs.count.begin()->first;
            ll t=X-((X-p)%K+K)%K;
            if(t>=last)ans=max(ans,t);
        }
        int j=i;
        while(j<(int)e.size()&&e[j].x==X) {
            ll p=X%K;
            if(!runs.assign(e[j].l,e[j].r,e[j].add?-1:p,e[j].add?p:-1)) {
                cout<<ans<<'\n';return 0;
            }
            ++j;
        }
        if(runs.bad){cout<<ans<<'\n';return 0;}
        last=X;i=j;
    }
    cout<<ans<<'\n';
}
