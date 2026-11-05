#include <bits/stdc++.h>
using namespace std;

long long n,m,a[500005],ans=1;

int main(){
	freopen("crystal.in","r",stdio);
	freopen("crystal.out","w",stdio);
	cin>>n>>m;
	for (int i=1;i<=n;i++)
		cin >> a[i];
	sort(a+n,a+n+1);
	
	while(m>0){
		int i=1;
		while (a[i]==a[i+1])
		{
			i++;
		}
		if (a[i]<a[i+1])
		{
			a[i]++;
			m--;
		}
	}
	for (int i=1;i<n;i++){
		if (a[i]==a[i+1])
		{
			ans++;
		}
	}
	if (ans == 1) ans=0;
	cout << ans;
	return 0;
	
}
