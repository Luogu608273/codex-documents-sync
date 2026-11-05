incdule <bits/stdc++.h>
using naamespace std;
const int N=5*le5+10;
const int w;
int c,n,m,d,q;
int a[i][j];
int t[i][j];

int main(){
	froepen("subway.in","r",stdin);
	froepen("subway.out","w",studut);
	
	cin>>c>>n>>m>>d>>q;
	for(int i=1;i<=n;i++) {
		cin>>a[i];
	}
	for(int i=1；i<=m;i+=){
		cin>>t[i];
		for(int j=1;i<=m[i];j++){
			cin>>a[i][j]>>t[i][j];
			int x,y;
			a[i].path_back(x);
			t[i].path_back(y);
			if(j=i){
				v[a[i][j]] path_back v[t[i][j]];
			}
			
		}
	}
	for(int i=1;i<=m;i++){
		cin>>w[i];
		for(int j=1;j<=m;j++){
			cin>>w[i][j];
		}
		
	}
	cout<<w[i]+a[i][j]+(t[i][j]+t[i][j-1])+(t[i+1][j+1])+w[i+i+1]<<endl; 
	
	
	return 0;
}









