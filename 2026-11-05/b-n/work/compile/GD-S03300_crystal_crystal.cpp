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

ifstream cin("crystal.in");
ofstream cout("crystal.out");

array<long long,500001> va,vs;

int main(int argc,char* argv[])
{
    ios::sync_with_stdio(false);
    int n;
    long long m;
    cin>>n>>m;
    fori(i,1,n)
        cin>>va[i];
    sort(rgo1(va,n));
    fori(i,1,n)
		vs[i]=vs[i-1]+va[i];
    int l=1,r=n;
    while(l<r)
    {
        int mid=l+r+1>>1;
        bool ans=false;
        fori(i,mid,n)
            if(mid*va[i]-(vs[i]-vs[i-mid])<=m)
                ans=true;
        if(ans)
            l=mid;
        else
            r=mid-1;
    }
    cout<<l;
    return 0;
}
