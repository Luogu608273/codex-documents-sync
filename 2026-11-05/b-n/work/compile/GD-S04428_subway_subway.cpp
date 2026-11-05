#include <bits/stdc++.h>
using namespace std;
bool flag[500001];
int c,n,m,d,q,w[500001],a[501][500001],x1,y,minn=1e9+1;
vector<int> x[500001];
vector<int> pt[500001];
void dfs(int i,int k,int ans){
	cout<<"gg";	
	if(i==y){
	
		ans+=a[k][i];
		minn=min(minn,ans);
		return;
	}
	if(k==0){
		for(int j=0;j<pt[i].size();j++){
			for(int s=0;s<x[pt[i][j]].size();s++){
				if(!flag[x[pt[i][j]][s]])dfs(x[pt[i][j]][s],j,ans+a[j][i]);
			}
		}
		return ;
	}
	for(int j=0;j<pt[i].size();j++){
		if(pt[i][j]!=k){
			for(int s=0;s<x[pt[i][j]].size();s++){
				if(!flag[x[pt[i][j]][s]])dfs(x[pt[i][j]][s],j,ans+a[j][i]);
			}
		}
	}
	return ;
}
int main(){
	freopen("subwat.in","r",stdin);
	freopen("subway.out","w",stdour);
	cin>>c>>n>>m>>d>>q;
	for(int i=1;i<=m;i++){
		cin>>w[i];
	}
	for(int i=1;i<=n;i++){
		int k,p,o;
		cin>>k;
		for(int j=1;j<=k;j++){
			cin>>p>>o;
			pt[p].push_back(i);
			x[i].push_back(p);
			a[i][p]=o;
		}
	}
	for(int i=1;i<=q;i++){
		cin>>x1>>y;
		minn=1e9+1;
		flag[x1]=1;
		dfs(x1,0,0);
		cout<<minn<<endl;
	}
	return 0;
}
