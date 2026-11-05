#include <bits\stdc++.h>
using namespace std;

const int N=505,M=5e5+5,INFI=0x7f7f7f7f;
const long long INFL=0x7f7f7f7f7f7f7f7f;
long long rsum,rzf;
int rin;

struct stli{
	long long nam,tim;
};

struct station{
	long long tim;
	vector<stli> tli;
}sta[M];

long long ans,c,n,m,d,q,ps,pe;
long long mp[N][N];

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
	freopen("subway.in","r",stdin);
	freopen("subway.out","w",stdout);
	memset(mp,0x7f7f,sizeof(mp));
	for(int i=1;i<=500;i++) mp[i][i]=0;
	c=read(),n=read(),m=read(),d=read(),q=read();
	for(int i=1;i<=m;i++) sta[i].tim=read();
	long long itim,ista,k;                  
	for(int i=1;i<=n;i++){
		k=read(); 
		for(int j=1;j<=k;j++)
		{              
			ista=read(),itim=read();
			for(stli x:sta[ista].tli){
				mp[i][x.nam]=min(mp[i][x.nam],1LL*itim+x.tim);
				mp[x.nam][i]=mp[i][x.nam];
			}
			sta[ista].tli.push_back({i,itim});
		}                             
	} 
	for(int m=1;m<=n;m++){
		for(int r=1;r<=n;r++){
			if(m==r || mp[m][r]==INFL) continue;
			for(int l=1;l<=n;l++){
				if(l==r || l==m || mp[l][m]==INFL) continue;
				mp[l][r]=min(mp[l][r],mp[l][m]+mp[m][r]);
				mp[r][l]=mp[l][r];
			}
		}
	}
	for(int i=1;i<=q;i++){
		ps=read(),pe=read(),ans=INFL;
		for(stli sx:sta[ps].tli){   
			for(stli ex:sta[pe].tli){
				ans=min(ans,1LL*mp[sx.nam][ex.nam]+sx.tim+ex.tim+sta[ps].tim+sta[pe].tim);
			}
		}
		printf("%lld\n",ans);
	}
	return 0;
}
//what can I say?
//!?冰冰冰?!
