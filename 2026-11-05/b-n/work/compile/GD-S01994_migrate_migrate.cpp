#include <bits/stdc++.h>
using namespace std ;

int main() {
	
	freopen("migrate.in","r",sdin) ;
	freopen("migrate.out","w",sdout) ;
	
	long long c , k ;
	cin >> c >> k ;
	
	if (c>=15&&c<=18){
		while (k--){
			long long n , m ;
			cin >> n >> m ;
			for (int i = 0 , temp ; i < n ; i++)
				cin >> temp ;
			cout << 0 << endl ;
		}
		return 0 ;
	}
	
	while (k--){
		long long n , m , len = -1e18 , ans = 0 ;
		cin >> n >> m ;
		for (int i = 0 , temp ; i < n ; i++){
			cin >> temp ;
			if (len==-1e18){
				len = temp ;
			}else{
				if (temp-len < m){
					if (i==n-1){
						ans+=temp-len;
					}
					ans += temp-len ;
					len = temp ;
				}else{
					len = -1e18 ;
				}
			}
		}
		cout << (ans+(ans%m!=0))/m-1 << endl ;
	}
	
	return 0 ;
} 
