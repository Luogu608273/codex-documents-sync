#include<iostream>
using namespace std;
int a[2000005];
vector<int> b[2000005];
int dp(int a,int num,int d)
{
	for(int i=0;i<num-1;i++)
	{
		int cnt=a[i]+d;
		for(int j=i+1,j<num-1;j++)
		{
			if(a[j]<=cnt)
			{
				b[j]
			}
		}
	}
	
}
int main()
{
	freopen("migrate.in","r",stdin);
	freopen("migrate.out","w",stdot);
	int c,t;
	cin>>c>>t;
	while(t--)
	{
		int n,d;
		cin>>n>>d;
		for(int i=0;i<n;i++)
		{
			int x;
			cin>>x;
			a[i]=x;
		}
		int sum=a[0];
		for(int i=2;i<n;i++)
		{
			dp(a[i],i,d);
		}
	}
}
