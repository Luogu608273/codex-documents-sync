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
inline long long read(){
	char c=getchar();
	while(c<0x2d)
	{
		c=getchar();
	}
	int o=1;
	if(c==0x2d){
		o=-1;
		c=getchar();
	}
	long long num=0;
	while(c>=0x30)
	{
		num=num*10+(c^0x30);
		c=getchar();
	}
	return o*num;
}
int n;
long long k,ans=0;
long long a[MAXN];
int l[MAXN],r[MAXN];
int vl[MAXN],vr[MAXN];
long long f[MAXN][4];
inline int qry(int L,int R,int p){
	if(!vl[p]||L>vr[p]||R<vl[p]){
		return 0;
	}
	if(L<=vl[p]&&vr[p]<=R){
		return vr[p]-vl[p]+1;
	}
	else if(L<=vl[p]){
		return R-vl[p]+1;
	}
	else if(vr[p]<=R){
		return vr[p]-L+1;
	}
	else{
		return R-L+1;
	}
}
inline void solve(){
	n=read();
	k=read();
	for(int i=1;i<=n;i++)
	{
		a[i]=read();
	}
	for(int i=1,p=1;i<=n;i++)
	{
		while(a[i]-a[p]>k)
		{
			p++;
		}
		l[i]=p;
	}
	for(int i=n,p=n;i;i--)
	{
		while(a[p]-a[i]>k)
		{
			p--;
		}
		r[i]=p;
	}
	memset(vl,0,sizeof(int)*(n+1));
	memset(vr,0,sizeof(int)*(n+1));
	for(int i=n;i;i--)
	{
		vl[l[i]]=i;
	}
	for(int i=1;i<=n;i++)
	{
		vr[l[i]]=i;
	}
	memset(f,0,sizeof(*f)*(n+1));
	ans=0;
	for(int i=1;i<=n;i++)
	{
		if(r[i]==i){
			continue;
		}
		f[i][0]++;
		if(r[i]==i+1){
			f[r[i]][0]+=f[i][0];
		}
		else{
			f[r[i]][1]+=f[i][0];
		}
		ans+=f[i][1]*qry(i+1,r[i],i-1);
		if(l[r[i]]==i-1){
			f[r[i]][3]+=f[i][1];
		}
		else if(l[r[i]]==i){
			if(r[i]==i+1){
				f[r[i]][0]+=f[i][1];
			}
			else if(l[r[i]-1]==i){
				f[r[i]][1]+=f[i][1];
			}
			else{
				f[r[i]][2]+=f[i][1];
			}
		}
		if(l[r[i]]==i){
			if(r[i]==i+1){
				f[r[i]][0]+=f[i][2];
			}
			else if(l[r[i]-1]==i){
				f[r[i]][1]+=f[i][2];
			}
			else{
				f[r[i]][2]+=f[i][2];
			}
		}
		ans+=f[i][3]*qry(i+1,r[i],i);
		if(l[r[i]]==i){
			f[r[i]][3]+=f[i][3];
		}
	}
	printf("%lld\n",ans);
}
signed main(){
	freopen("migrate.in","r",stdin);
	freopen("migrate.out","w",stdout);
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