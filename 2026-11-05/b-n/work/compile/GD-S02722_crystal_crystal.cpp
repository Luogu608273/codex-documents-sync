#include<bits/stdc++.h>
using namespace std;
map<long long int,long long int> cnt;
long long int crystal[50005];
int main(){
	//freopen("crystal.in","r",stdin);\
	freopen("crystal.out","w",stdout);
	int n;
	long long int m,maxn=1;
	cin>>n>>m;
	for(int i=0;i<n;i++){
		cin>>crystal[i];
		cnt[crystal[i]]++;
	}
	for(long long int i=0;i<=m;i++){
		sort(crystal,crystal+n);
		if(crystal[0]==crystal[n-1]){
			cout<<n;
			return 0;
		}
		crystal[0]++;
		cnt[crystal[0]-1]--;
		cnt[crystal[0]]++;
		maxn=max(maxn,cnt[crystal[0]]);
	}
	cout<<maxn;
	return 0;
}.
