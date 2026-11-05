#include <algorithm>
#include <fstream>
#include <bitset>
#include <string>
#include <vector>
#include <array>

#define fori(i,l,r) for(int i=(l);i<=(r);i++)
#define fori0(i,l,r) for(int i=(l);i<(r);i++)
#define ford(i,l,r) for(int i=(l);i>=(r);i--)
#define rgall(a)    (a).begin(),(a).end()
#define rgany(a,l,r) (a).begin()+(l),(a).begin()+(r)
#define rgcnt(a,n)  rgany(a,0,n)
#define rgo1(a,n)   rgany(a,1,n+1)
#define fr first
#define sc second

using namespace std;

ifstream cin("subway.in");
ofstream cout("subway.out");

array<vector<pair<int,long long>>,500001> va;
array<array<long long,501>,501> dis;
array<long long,500001> vb;

int main(int argc,char* argv[])
{
    ios::sync_with_stdio(false);
    int testcase,n,m,maxd,q;
    cin>>testcase>>n>>m>>maxd>>q;
    fori(i,1,m)
        cin>>vb[i];
    fori(i,1,n)
    {
        dis[i].fill(1e18),dis[i][i]=0;
        int a;
        cin>>a;
        while(a--)
        {
            int b,c;
            cin>>b>>c;
            va[b].emplace_back(i,c);
        }
    }
    fori(i,1,m)
    {
        int a=va[i].size();
        auto& b=va[i];
        fori0(j,0,a)
            fori0(k,0,a)
            {
                auto& c=dis[b[j].fr][b[k].fr];
                c=min(c,b[j].sc+b[k].sc);
            }
    }
    fori(k,1,n)
        fori(i,1,n)
            fori(j,1,n)
                dis[i][j]=min(dis[i][j],dis[i][k]+dis[k][j]);
    while(q--)
    {
        long long ans=1e18;
        int u,v;
        cin>>u>>v;
        for(auto& i:va[u])
            for(auto& j:va[v])
                ans=min(ans,i.sc+dis[i.fr][j.fr]+j.sc);
        cout<<ans+vb[u]+vb[v]<<'\n';
    }
    return 0;
}
/*
0 2 5 20 2

4 1 9 2 5

3 1 5 2 7 4 6
3 2 3 3 4 5 7

1 3
1 2

*/