#include<bits/stdc++.h>
using namespace std;
#define ll long long
const int N=5e5+5;
int n,m,d,q;
int w[N];
int main(){
	freopne("subway.in","r",stdin);
	freopen("subway.out","w",stdout);
	ios::sync_with_stdio(0);
	cin.tie(0); 
	int c;
	cin>>c>>n>>m>>d>>q;
	for(int i=1;i<=m;i++) cin>>w[i];
	for(int i=1;i<=n;i++){
		int x,a,t;
		cin>>x;
		for(int i=1;i<=x;i++) cin>>a>>t;
	}
	while(q--){
		int l,r;
		cin>>l>>r;
		cout<<43+w[l]+w[r]<<"\n";
	}
	return 0;
}
