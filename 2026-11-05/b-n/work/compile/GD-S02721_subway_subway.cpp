#include<iostream>
#include<cstdio> 
#include<vector>
#include<queue>
#include<bitset>
using namespace std;
char *p1,*p2,buf[100000];
#define nc() (p1==p2&&(p2=(p1=buf)+fread(buf,1,100000,stdin),p1==p2)?EOF:*p1++)
long long read()
{
	long long x=0;
	char ch=nc();
	while(ch>'9'||ch<'0')
	{
		ch=nc();
	}
	while(ch>='0'&&ch<='9')
	{
		x*=10;
		x+=ch-'0';
		ch=nc();
	}
	return x;
}
void write(long long x)
{
	if(x>9) write(x/10);
	putchar(x%10+'0');
	return;
}
constexpr long long inf=1ll<<60;
int c,n,m,M,T;
vector<int> k;
vector<long long> w,d;
vector<vector<int> > e;
vector<vector<long long> > s;
vector<vector<pair<int,int> > > a;
bitset<500010> book;
long long bfs(int l,int r)
{
	d.assign(m+1,inf);//多测记得清空 
	d[l]=0;
	queue<int> q;
	q.push(l);
	while(!q.empty())
	{
		int u=q.front();
		book[u]=1;
		q.pop();
		book[u]=0;
		for(auto &[i,k]:a[u])
		{
			for(int j=0;j<e[i].size();++j)
			{
				long long tw=d[u]+s[i][k]+s[i][j];
				int v=e[i][j];
				if(d[v]>tw)
				{
					d[v]=tw;
					if(!book[v]) q.push(v);
				}
			}
		}
	}
	return d[r];
}
int main()
{
	freopen("subway.in","r",stdin);
	freopen("subway.out","w",stdout);
	c=read(),n=read(),m=read(),M=read(),T=read();
	w.assign(m+1,0);
	k.assign(n+1,0);
	for(int i=1;i<=m;++i) w[i]=read();
	e.assign(n+1,vector<int>(0));
	s.assign(n+1,vector<long long>(0));
	a.assign(m+1,vector<pair<int,int> >(0));
	for(int i=1;i<=n;++i)
	{
		k[i]=read();
		for(int j=1;j<=k[i];++j)
		{
			int ta=read();
			long long tt=read();
			e[i].push_back(ta);
			s[i].push_back(tt);
			a[ta].push_back({i,j-1});
		}
	}
	while(T--)
	{
		int xr=read(),yr=read();
		write(bfs(xr,yr)+w[xr]+w[yr]);
		putchar('\n');
	}
	return 0;
}
