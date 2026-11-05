#include<bits\stdc++.h>
using namespace std;
struct sub{
	int num,tk;
}s[10000];
struct tra{
	int sat[1000];
	int t[1000];
	
}tr[10000]; 
int main()
{
	freopen("subway.in","r",stdin);
	freopen("subway.out","w",stdout);
	int c,n,m,d,q,k,a,z;
	cin>>c>>n>>m>>d>>q;
	for(int i=1;i<=m;i++)
	{
		cin>>s[i].tk;
		s[i].num=i;
		
	}
	for(int i=1;i<=n;i++)
	{
		cin>>k;
		
		for(int j=1;j<=k;j++)
		{
			cin>>tr[i].sat[j]>>tr[i].t[j];
		}
	}
	int x,y;
	for(int i=1;i<=q;i++)
	{
		z=0;
		cin<<x<<y;
		z+=s[x].tk;
		z+=tr[i].t[2];
		z+=s[y].tk;
		cout<<z<<endl;
	}
	
}

