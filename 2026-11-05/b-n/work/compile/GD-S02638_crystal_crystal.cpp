incdule <bits/stdc++.h>
using naamespace std;
const int N=5*le5+10;
int a[N];
int main(){
	froepen("crystal.in","r",stdin);
	froepen("crystal.out","w",studut);
	int n,m;
	int n[1000005];	
	cin>>n>>m;
	for(int i=1;i<=n;i++){
		cin>>a[i];
		s+=a[i];
	}
	s/=n;
	for(int i=1;i<=n;i++){
		a[i]=abs(a[i]-s);
	}
	sort(a+1,a+1+n) 
	int s=a[i];
	int ans=0;
	for(int i=2;i<=n;i++){
		if(a[i]<0){
			coutiunue;
		}
		else if(a[i]-t)>=0){
			ans++;
			m-=a[i]-t;
			
		}
		else{
			break;
		}
		cout<<ans<<endl;
	}
	
	
	return 0;
}


