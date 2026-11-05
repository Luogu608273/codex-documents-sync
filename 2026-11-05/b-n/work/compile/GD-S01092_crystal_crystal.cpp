#include<bits\stdc++.h>
using namespace std;
int m,n,a[500000],b[5000000],big=0;
bool cmp(int w,int c){
	return w<c;
}
void sum(int min){
	int o=0,max=1;
	for(int i=min;i<n-1;i++){
		if(o+(i+1)*b[i]>m){
			if(max>=big){
				big=max;
				sum(min+1);
				break;
			}else{
				sum(min+1);
				break;
			}
		}else{
			o=o+i*b[i]+b[i];
		    max++;
		}
	}
}
int main(){
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",stdout);
	cin >> n >> m;
	for(int i=0;i<n;i++){
		cin >> a[i];
	}
	sort(a,a+n,cmp);
	for(int i=0;i<n-1;i++){
		b[i]=a[i+1]-a[i];
	}
	sum(0);
	cout << big;
	return 0;
}
