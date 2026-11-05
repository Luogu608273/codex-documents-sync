#include<bits/stdc++.h>
using namespace std;
int c,n,m,d,q,T;
int w[10000];
int a[5][10000];
int t[5][10000];
bool v[10000]={0};
int x,y;
int main()
{
	freopne("subway.in","r",stdin);
	freopen("subway.out","w",stdout);
	cin>>c>>n>>m>>d>>q;
	for(int i=1;i<=m;i++) cin>>w[i];
	for(int i=1;i<=n;i++)
	{
		cin>>T;
		for(int i=j;j<=T;j++)
		{
			cin>>a[i][j];
			cin>>t[i][j];
		} 
	}
	

	for(int i=1;i<=T;i++)
	{
		for(int j=1;j<=T;j++)
		{
			if(a[1][i]==a[2][j])
			{
				v[i]=1;
			}
		}
	}
	for(int i=1;i<=2;i++)
	{
		int ks=0,en=0;
		int ans=0;
		cin>>x>>y;
		for(int j=1;j<=n;j++)
		{
			int flag=0;
			for(int k=1;k<=T;k++)
			{
				if(a[j][k]==x&&flag==0)
				{
					ks=j;
					flag=1	
				}
				if(a[j][k]==y)
				{
					en=j;
				}
			}
		}
		//cout<<ks<<" "<<en<<" ";
		int l;
		for(int j=1;j<=T;j++) if(a[ks][j]==x) l=j;
		ans+=w[x];ans+=t[ks][l];
		//cout<<ans;
		//cout<<ks<<" "<<en;
		if(ks==en)
		{
			ans+=t[en][y];
			ans+=w[y];
		}
		
		if(ks!=en)
		{
		
			int minn=10000000;
		
			for(int j=1;j<=T;j++)
			{	
				if(v[j]==1)
				{
				
					for(int k=1;k<=T;k++)
					{
						if(a[en][k]==j)
						{
						 minn=min(minn,t[ks][j]+t[en][k]);
						}
					}
				}
			
			}
			
		
		
			//cout<<minn<<" ";
			for(int j=1;j<=T;j++) if(a[en][j]==y) l=j;
			ans+=minn+t[en][l]+w[y];
		}
		cout<<ans;
		
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


0 3 7 20 2
8 3 6 1 7 2 9
3 1 4 2 5 5 100
3 2 6 3 1 7 2
4 3 2 5 100 4 6 6 7
1 6
2 3

*/
