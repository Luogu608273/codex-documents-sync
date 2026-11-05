#include<bits\stdc++.h>
using namespace std;
int s[1000000];

int main()
{
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",stdout);
	long long n,m;
	long long a=0,b=0,z=0,w=0;
	cin>>n>>m;
	for(int i=1;i<=n;i++)
	{
		cin>>s[i];
	}
	sort(s+1,s+1+n);
	
	if(n<=20000)
	{
		for(int i=2;i<=n;i++)
		{
			a=0;b=1;
			for(int j=i-1;j>=1;j--)
			{
				w=s[i]-s[j];
				if((a+w)<=m)
				{
					a+=w;
					b++;
				}
				else
				{
					break;
				}
			}
			if(z<b)
			{
				z=b;
			}
		
		}
	}
	else
	{
		for(int j=n;j>=1;j++)
		{
			w=s[n]-s[j];
			if((a+w)<=m)
			{
				a+=w;
				b++;
			}
			else
			{
				break;
			}
		}
		z=b;
	}
	
	cout<<z<<endl;
	return 0;
}
