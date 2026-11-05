#include<bits\stdc++.h>
using namespace std;
int c,n,m,d,q,lin,tim=0;
int rtz[50],ztc[20][1000],t[1000][20];//t[车站][线路]；rtc[车站]：出入站时间 
int same(int w,int to){
	int minni=12212121;
	for(int i=1;i<=n;i++){
		if(t[w][i]!=0&&t[to][i]!=0){
			if(t[w][i]+t[to][i]<minni) minni=t[w][i]+t[to][i];
		}
	}
	if(minni==12212121) return -1;
	return minni;
}
int sum(int w,int to,int timing){
    if(same(w,to)==-1){
    	for(int i=1;i<=n;i++){
    		if(t[w][i]!=0){
    			for(int j=1;j<=m;j++){
    				if(ztc[i][j]==0) break;
    				if(ztc[i][j]==w) continue;
    				cout << same(w,j) << ztc[i][j] <<endl;
    				sum(ztc[i][j],to,timing+=same(w,j));
				}
			}
		}
	}else if(same(w,to)!=0){
	    return timing + same(w,to);
	}

}
int main(){
	freopen("subway.in","r",stdin);
	freopen("subway.out","w",stdout); 
	cin >> c>>n>>m>>d>>q;
    for(int i=1;i<=m;i++){
    	cin >> rtz[i];
	}
	for(int i=1;i<=n;i++){
	    cin >> lin;
	    for(int j=1;j<=lin;j++){
	    	cin >> ztc[i][j];
	    	int u=ztc[i][j];
	    	cin >> t[u][i];
		}
	}
	for(int i=0;i<q;i++){
		int t1,t2;
		cin >> t1 >> t2;
		tim+=rtz[t1]+rtz[t2];
		tim+=sum(t1,t2,0);
		cout << tim;
	}
	return 0;
}
