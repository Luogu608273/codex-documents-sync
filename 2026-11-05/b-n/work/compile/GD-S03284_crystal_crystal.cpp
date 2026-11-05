#include <bits\stdc++.h>
using namespace std;

const int N=5e5+5;
long long rsum,rzf;
int rin;

int n,ans=0;
long long m,a[N],b[N];

long long read(){
	rin=getchar(),rsum=0,rzf=1;
	while(rin<48 || rin>57){
		if(rin==45) rzf=-1;
		if(rin==-1) return 0; 
		rin=getchar();
	}
	while(rin>=48 && rin<=57) rsum*=10,rsum+=rin-48,rin=getchar();
	return rsum*rzf;
}

int main(){
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","W",stdout);
	n=read(),m=read();
	for(int i=1;i<=n;i++) a[i]=read();
	sort(a+1,a+1+n);
	for(int i=2;i<=n;i++) b[i]=a[i]-a[i-1];
	for(int i=1,j=1,sum=1;i<=n;){
		if(m-1LL*(i-j)*b[i+1]>=0){
			i++,sum++,m-=1LL*(i-j)*b[i];
			ans=max(sum,ans);
		}
		else{
			if(i==j){
				i++,j++;
				continue;
			}
			m+=a[i]-a[j],j++,sum--;
		}
	}
	printf("%d\n",ans);
	return 0;
} 
