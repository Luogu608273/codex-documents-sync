#include <bits/stdc++.h>
using namespace std ;

int main() {
	
	freopen("crystal.in","r",sdin) ;
	freopen("crystal.out","w",sdout) ;
	
	long long n , m ;
	cin >> n >> m ;
	
	vector <long long> numS (n) ;
	long long first = 1e12+1e1, second = 1e12+1e1;
	for (long long i = 0 ; i < n ; i++){
		cin >> numS[i] ;
		if (first == 1e12+1e1){
			first = min(first,numS[i]);
		}else if (first != numS[i]){
			if (numS[i]>first){
				second = min(second,numS[i]) ;
			}else if (numS[i]<first){
				second = first ;
				first = min(first,numS[i]) ;
			}
		}
	}
	
	if (n>=1001){
//		cout << first << " " << second << endl ;
		long long temp = abs(second-first) ;
		m /= temp ;
		temp = 0 ;
		for (long long i = 1 ;m>0;i++){
			if (m<i)
				break ;
			
			m -= i ;
			
			temp ++ ;
//			cout << endl << temp << " " << m << " " << i << endl ;
		}
		cout << temp ;
		return 0 ;
	}
	
	sort (numS.begin(),numS.end()) ;
	long long ans = 1 ;
	
	for (int i = 1 ; i < n ; i++){
		long long temp = abs(numS[i]-numS[i-1]) ;
		if (m >= i*temp){
			m-=i*temp ;
			ans = i+1 ;
		}else{
			break ;
		}
	}
	
	cout << ans ;
	
	return 0 ;
} 
