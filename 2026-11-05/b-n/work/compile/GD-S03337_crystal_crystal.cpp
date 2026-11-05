#include<bits/stdc++.h>
using namespace std;
int a[50005];	
freopen("crystal.in","r","stdin")
freopen("crystal.out","r","stdout")
int main(){

	int n,m;
	long max=0
	cin>>n>>m;
	for(int i=0;i<n;i++){
		cin>>a[i];
	}
	for(int i=0;i<m;i++){
	    if(a[i+1]-a[i]>max){
	    	max=a[i+1]-a[i];
		}
	}
	cout<<max/2-1;
	return 0;
} 
