#include<bits/stdc++.h>
using namespace std;
int main(){
	freeopen("crystal.in","r",stdin);
	freeopen("crystal.out","w",stdout);
	int n,m;
	int a[100005];
	cin>>n>>m;
	for(int i=0;i<n;i++){
		cin>>a[i];
	} 
	sort(a,a+n);
	int num=0;
	for(int i=n-1;i>=0;i--){
		int num2=0;
		int t=m;
		for(int j=0;j<i;j++){
			if(a[j]!=a[i]){
				while(t--){
					a[j]++;
					if(a[j]==a[i]){
						num2++;
						break;
					}
				}
			}
			if(t==0)	break;
		}
		if(num2>num){
			num=num2;
		}
	}
	cout<<num;
	return 0;
}  
