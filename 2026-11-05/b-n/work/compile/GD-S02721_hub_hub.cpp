#include<iostream>
#include<cstdio> 
#include<vector>
#include<bitset>
using namespace std;
char *p1,*p2,buf[100000];
#define nc() (p1==p2&&(p2=(p1=buf)+fread(buf,1,100000,stdin),p1==p2)?EOF:*p1++)
int read()
{
	int x=0;
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
void write(int x)
{
	if(x>9) write(x/10);
	putchar(x%10+'0');
	return;
}
int n,k,f[1000010][21],dep[1000010],ans,col[1000010];
vector<vector<int> > e;
bitset<1000010> book;
void build(int x,int fa)
{
	dep[x]=dep[fa]+1;
	f[x][0]=fa;
	for(int i=1;i<21;++i)
	{
		f[x][i]=f[f[x][i-1]][i-1];
		if(!f[x][i]) break;
	}
	for(int v:e[x]) if(v!=fa) build(v,x);
	return;
}
int lca(int a,int b)
{
	if(dep[a]<dep[b]) swap(a,b);
	for(int i=20;~i;--i)
	{
		if(dep[f[a][i]]>=dep[b])
		{
			a=f[a][i];
		}
		if(a==b) return a;
		if(dep[a]==dep[b]) break;
	}
	for(int i=20;~i;--i)
	{
		if(f[a][i]!=f[b][i])
		{
			a=f[a][i];
			b=f[b][i];
		}
	}
	return f[a][0];
}
void ddd(int x,int coo)
{
	book[x]=1;
	col[x]=coo;
	for(int v:e[x])
	{
		if(!book[v])
		{
			ddd(v,coo);
		}
	}
	return;
}
bool chick(vector<int> s)
{
	int cnt=0;
	for(int i=book._Find_first();i<=n;i=book._Find_next(i)) 
	{
		book[i]=0;
		col[i]=0;
	}
	for(int i:s)
	{
		if(!book[i])
		{
			++cnt;
			if(cnt>2) return 0;
			ddd(i,cnt);
		}
	}
	return 1;
}
int d(vector<int> s)
{
	int ma=0;
	for(int i:s)
	{
		for(int j:s)
		{
			if(col[i]==col[j]) ma=max(ma,dep[i]+dep[j]-2*dep[lca(i,j)]);
		}
	}
	return ma;
}
void dfs(int x,vector<int> s)
{
	if((int)s.size()==k)
	{
		if(chick(s))
		{
			ans=min(ans,d(s));
		}
		return;
	}
	if(x>n) return;
	dfs(x+1,s);
	s.push_back(x);
	dfs(x+1,s);
	return;
}
int main()
{
	freopen("hub.in","r",stdin);
	freopen("hub.out","w",stdout);
	int op=read(),T=read();
	while(T--)
	{
		n=read(),k=read();
		e.assign(n+1,vector<int>(0));
		for(int i=1;i<n;++i)
		{
			int u=read(),v=read();
			e[u].push_back(v);
			e[v].push_back(u);
		}
		build(1,0);
		ans=1ll<<30;
		dfs(1,vector<int>(0));
		write(ans);
		putchar('\n');
	}
	return 0;
}//多测清空！！！ 
//没调完， 
