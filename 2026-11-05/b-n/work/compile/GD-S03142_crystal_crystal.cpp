#include<bits\stdc++.h>
using namespace std;
long long n;
long long m;
int a[500005];
int he[500005];
int main()
{
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",stdout);
	ios::sync_with_stdio(false);
	cin.tie(0);
	cout.tie(0);
	cin>>n>>m;
	for(int i=1;i<=n;i++){
		cin>>a[i];
	}
	sort(a+1,a+1+n);
	long long ans=1,jjj;
	long long ji=0;
	long long lll,rrr,mid;
	he[1]=a[1];
	for(int i=2;i<=n;i++){
		he[i]=he[i-1]+a[i];
	}
	for(int i=2;i<=n;i++){
		lll=1,rrr=i;
		while(lll<=rrr){
			mid=(lll+rrr)/2;
			jjj=(i-mid+1)*a[i]-(he[i]-he[mid-1]);
			if(jjj>m){
				lll=mid+1;
			}else if(jjj<m){
				rrr=mid-1;
			}else if(jjj==m){
				lll=mid;
				break;
			}
		}
		ans=max(ans,(i-lll+1));
	}
	cout<<ans;
	return 0;
}
