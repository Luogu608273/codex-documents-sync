#include<bits/stdc++.h>
using namespace std;
int main(){
	#define int long long
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",stdout);
	int n , m , a[50000] , k =0 , t[50000] , ans =0 , p =1 , o;
	cin >> n >> m;
	for(int i =1;i<=n;i++){
		cin >>a[i];
		if(i>2&&a[i]-a[i-1]!=a[i-1]-a[i-2]) p=0;
		else o = abs(a[i-1]-a[i]);
	}
	if(p==0){
		sort(a+1,a+n+1);
		for(int i =2;i<=n;i++){
			int k = m;
			int ans1 = 1;
			int ii = i-1;
			while(k>0&&ii>0){
				int gap = abs(a[ii]-a[i]); 
				if(k>=gap) {
					k-=gap;
					ans1++;
					ii--;
				}else break;
			}
			ans = max(ans,ans1);
		}
		cout <<ans;		
	}else {
		cout <<ceil(sqrt(2*m/o-1))-1;
	}
	return 0;
} 
/*

5 5 
1 2 4 8 9


*/
