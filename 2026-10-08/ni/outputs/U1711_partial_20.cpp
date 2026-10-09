#include <bits/stdc++.h>
using namespace std;
using ll=long long;
struct Event{ll x,l,r;bool add;bool operator<(const Event&b)const{return x<b.x;}};
int main(){
    freopen("tile.in","r",stdin);freopen("tile.out","w",stdout);
    ios::sync_with_stdio(false);cin.tie(nullptr);
    int n;ll K;cin>>n>>K;
    vector<ll>x(n),y(n),ys;ll M=0;
    for(int i=0;i<n;++i)cin>>x[i]>>y[i],ys.push_back(y[i]),M=max(M,x[i]);
    if(K==1){cout<<M<<'\n';return 0;}
    sort(ys.begin(),ys.end());ys.erase(unique(ys.begin(),ys.end()),ys.end());
    __int128 area=0;
    for(int i=0;i<n;++i){int j=(i+1)%n;area+=(__int128)x[i]*y[j]-(__int128)x[j]*y[i];}
    vector<Event>e;
    for(int i=0;i<n;++i){int j=(i+1)%n;if(x[i]==x[j])
        e.push_back({x[i],min(y[i],y[j]),max(y[i],y[j]),(area>0)==(y[j]<y[i])});}
    sort(e.begin(),e.end());
    int h=(int)ys.size()-1;vector<ll>phase(h,-1);ll ans=0,last=0;
    for(int i=0;i<(int)e.size();){
        ll X=e[i].x,p=-1;bool mixed=false;
        for(ll q:phase)if(q>=0){if(p==-1)p=q;else if(p!=q)mixed=true;}
        if(p==-1)ans=max(ans,X);
        else if(!mixed){ll t=X-((X-p)%K+K)%K;if(t>=last)ans=max(ans,t);}
        int j=i;
        while(j<(int)e.size()&&e[j].x==X){
            int l=lower_bound(ys.begin(),ys.end(),e[j].l)-ys.begin();
            int r=lower_bound(ys.begin(),ys.end(),e[j].r)-ys.begin();
            for(int z=l;z<r;++z){
                if(phase[z]!=(e[j].add?-1:X%K)){cout<<ans<<'\n';return 0;}
                phase[z]=e[j].add?X%K:-1;
            }
            ++j;
        }
        for(int l=0;l<h;){int r=l+1;while(r<h&&phase[r]==phase[l])++r;
            if(phase[l]>=0&&(ys[r]-ys[l])%K){cout<<ans<<'\n';return 0;}l=r;}
        last=X;i=j;
    }
    cout<<ans<<'\n';
}
