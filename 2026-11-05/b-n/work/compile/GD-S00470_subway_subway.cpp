#include <bits/stdc++.h> 
#define ll long long
using namespace std;
const int N = 500 + 10;
int c,n,m,d,q,cnt,ans;
int k[N],w[N];
int u[N][N],v[N][N];
int sum[N];
vector <int> v1[N];
int main(){
	freopen("subway.in","r",stdin);
	freopen("subway.out","w",strout);
	scanf("%d%d%d%d%d",&c,&n,&m,&d,&q);
	for(int i = 1;i <= m;i ++){
		scanf("%d",w + i);
	}for(int i = 1;i <= n;i ++){
		scanf("%d%d%d",k + i,u[i] + 1,v[i] + 1);
		for(int j = 2;j <= k[i];j ++){
			scanf("%d%d",u[i] + j,v[i] + j);
			sum[u[i][j]] = w[u[i][j]] + v[i][j];
		}
	}for(int i = 1;i <= q;i ++){
		int x,y;
		scanf("%d%d",&x,&y);
		ans = INT_MAX;
		dfs(x,y);
		printf("%d",ans);
	}
	return 0;
}
/*

*/
