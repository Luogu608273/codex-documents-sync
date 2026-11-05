#include<bits/stdc++.h>
using namespace std;
int main(){
	freopen("migrate.in","r","stdin");
	freopen("migrate.out","w","stdout");
	long long c,t,i=0,key=0;
	cin>>c>>t;
	long long n[2000001],d[2000001],num[2000001];
	while(i!=t-1){
		cin>>n[i]>>d[i];
		long long count[n[i]];
		for(int z=0;z<n;z++){
			cin>>count[z];
			count[z]-=count[0]-1;
		}
		for(int z=0;z<n;z++){
			if(count[z+1]-count[z]>d[i]){
				key+=z;
				break;
			}
		}
		if(key==0){
			key=n;
		}
		for(int z=0;z<key;z++){
			if(key>=2*d[i]-z){
				num[i]+=1;
			}
		}
		i++;
		cout<<num<<endl;
	}
	return 0;
}
