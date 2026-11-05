#include<bits/stdc++.h>
using namespace std;
int n,m,ans,maxn;
int a[500005],b[500005],sl[500005];
//priority<int,vector<int>,greater<int> > q;
vector<int> q;
int main(){
	freopen("crystal.in","r","stdin");
	freopen("crystal.out","w","stdout");
	ios::sync_with_stdio(false);
	cin.tie(0);
	cin>>n>>m;
	if(n==1)
	{
		cout<<0;
		return 0;
	}
	for(int i=1;i<=n;i++)
	{
		cin>>a[i];
	}
	sort(a+1,a+n+1);
	for(int i=1;i<n;i++)
	{
		int cz=abs(a[i+1]-a[i]);
		b[i]=cz;
		//q.push_back(cz);
	}
	int l=1;
	for(int i=1;i<=n;i++)
	{
		if(m>0)
		{
			sl[i]++;
			m-=(b[i]*sl[i]);
			sl[i+1]+=sl[i];
		}
		if(m==0||m-sl[i]<0)
		{
			ans=sl[i];
			break;
		} 
	}
	/*while(m!=0)
	{
		int x=b[l];
		if(x<=m)
		{
			m-=x;
			tot++;
			l++;
		}
	}*/
	cout<<ans;
	return 0;
} 
