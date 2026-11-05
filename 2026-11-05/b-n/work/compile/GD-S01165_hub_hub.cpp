#include<set>
#include<map>
#include<ctime>
#include<cmath>
#include<queue>
#include<stack>
#include<cstdio>
#include<vector>
#include<string>
#include<bitset>
#include<cstring>
#include<cstdlib>
#include<numeric>
#include<iostream>
#include<algorithm>
using namespace std;
const int MAXN=2e6+10;
const int N=2e6;
const int INF=0x3f3f3f3f;
const long long LINF=0x3f3f3f3f3f3f3f3f;
inline int read(){
	char c=getchar();
	while(c<0x2d)
	{
		c=getchar();
	}
	int num=0;
	while(c>=0x30)
	{
		num=num*10+(c^0x30);
		c=getchar();
	}
	return num;
}
int n,m,k;
basic_string <int> tr[MAXN];
inline void add_edge(int x,int y){
	tr[x].push_back(y);
}
int fat[MAXN],dep[MAXN];
void dfs_(int x){
	dep[x]=dep[fat[x]]+1;
	for(int y:tr[x])
	{
		tr[y].erase(find(tr[y].begin(),tr[y].end(),x));
		fat[y]=x;
		dfs_(y);
	}
}
int f[MAXN],d[MAXN];
void dfs(int x){
	d[x]=0;
	for(int y:tr[x])
	{
		fat[y]=x;
		dfs(y);
		f[x]+=f[y];
		d[x]=max(d[x],d[y]+1);
	}
	sort(tr[x].begin(),tr[x].end(),[&](int x,int y){return d[x]>d[y];});
	if(f[x]||d[x]>k){
		f[x]++;
	}
}
bool F=false;
void cal(int x,vector <pair<int,int>> s,int p=0,int ex=0){
	int siz=(int)tr[x].size();
	for(auto [L,P]:s)
	{
		if(L+P-p>k&&L+dep[x]-P>k){
			ex+=P-p;
			p=P;
		}
	}
	while(!s.empty()&&s[0].second<=p)
	{
		s.erase(s.begin());
	}
	if(max(f[x],1)+ex<=m){
		F=true;
		return ;
	}
	for(int i=0;i<siz;i++)
	{
		int y=tr[x][i];
		int E=ex;
		int P=p;
		vector <pair<int,int>> t=s;
		if(f[x]-f[y]-1){
			P=dep[x];
			E+=f[x]-f[y];
			t.clear();
		}
		else{
			int len=1;
			if(siz>1){
				int z=i?tr[x][i-1]:tr[x][i+1];
				len=d[z]+1;
			}
			t.push_back({len,dep[x]});
		}
		cal(y,t,P,E);
	}
}
inline bool chk(int x){
	F=false;
	k=x;
	dfs(1);
	cal(1,vector<pair<int,int>>());
	return F;
}
inline void solve(){
	n=read();
	m=read();
	for(int i=1;i<=n;i++)
	{
		tr[i].clear();
	}
	for(int i=1;i<n;i++)
	{
		int x=read(),y=read();
		add_edge(x,y);
		add_edge(y,x);
	}
	dfs_(1);
	int l=1,r=n,mid;
	while(l<r)
	{
		mid=(l+r)>>1;
		if(chk(mid)){
			r=mid;
		}
		else{
			l=mid+1;
		}
	}
	printf("%d\n",l);
}
signed main(){
	freopen("hub.in","r",stdin);
	freopen("hub.out","w",stdout);
	#ifdef LOCAL
	atexit([](){fprintf(stderr,"%.3lfs\n",(double)clock()/CLOCKS_PER_SEC);});
	#endif
	read();
	int t=read();
	while(t--)
	{
		solve();
	}
	return 0;
}