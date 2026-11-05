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

ifstream cin("hub.in");
ofstream cout("hub.out");

array<vector<int>,1000001> T;
array<int,1000001> vfa,deg,deg0,va;
vector<int> qu,qu0;

void DFS_init(int u,int fa)
{
    vfa[u]=fa;
    for(int i:T[u])
        if(i!=fa)
            DFS_init(i,u);
}
void DFS_col(int u,int fa,int a)
{
	va[u]=a;
    for(int i:T[u])
        if(i!=fa)
            DFS_col(i,u,a);
}

int solve(int n,int m,int u,int v)
{
    qu.clear(),qu0.clear();
    int c0=0,c1=0;
    fori(i,1,n)
    	if(va[i])
    		++c1;
    	else
    		++c0;
    fori(i,1,n)
        if(deg[i]<=1)
            qu.push_back(i),deg[i]=-1;
    int a=n,res=0;
    while(a+!c0+!c1>m)
    {
        ++res,a-=qu.size();
        for(int i:qu)
        {
        	if(va[i])
        		--c1;
        	else
        		--c0;
            for(int j:T[i])
            {
            	if(i==u&&j==v||i==v&&j==u)
            		continue;
                if(deg[j]>=0&&--deg[j]<=1)
                    deg[j]=-1,qu0.push_back(j);
			}
		}
        qu=qu0,qu0.clear();
    }
    return res;
}

int main(int argc,char* argv[])
{
    ios::sync_with_stdio(false);
    int testcase,testcnt;
    cin>>testcase>>testcnt;
    while(testcnt--)
    {
        int n,m,ans;
        cin>>n>>m;
        fori(i,2,n)
        {
            int u,v;
            cin>>u>>v;
            T[u].push_back(v),T[v].push_back(u),++deg0[u],++deg0[v];
        }
        fori(i,1,n)
        	deg[i]=deg0[i];
        DFS_init(1,0);
        ans=solve(n,m,0,0);
        fori(i,1,n)
            for(auto j:T[i])
                if(j!=vfa[i])
                {
                    fori(k,1,n)
                        deg[k]=deg0[k];
                    DFS_col(i,j,0),DFS_col(j,i,1);
                    --deg[i],--deg[j],ans=min(ans,solve(n,m,i,j));
//                    cout<<i<<' '<<j<<' '<<ans<<'\n';
                }
        cout<<ans<<'\n';
        fori(i,1,n)
            T[i].clear(),vfa[i]=deg[i]=deg0[i]=va[i]=0;
        qu.clear(),qu0.clear();
    }//CLEAR
    return 0;
}
