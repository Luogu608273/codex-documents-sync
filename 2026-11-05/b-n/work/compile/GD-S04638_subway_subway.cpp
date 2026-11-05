#include<bits.stdc++.h>
using namespace std;
int c,n,m,d,q;
int co1[500005];
//
//这道题是带权的最短路问题，教室好冷，一方面切出一道题我已经心满意足了，又因为我的图论是乐乐，最短路我只听过同学讲过但我不会，所以写个思路吧
//可以将步行时间看为权，用什么迪杰斯特拉可以做到，然后相加
//我记得有个初始化是为无穷大，所以试试吧(好吧不知道怎么写） 
//(> ^ <)不能骗分 

struct edge{
	int u,v;
};
vector <int> e[100086];
vector <edge> s;
//默写考前的仓促一眼
//e[i].size()
//s.push_back((edge){uu,vv});
 

int main(){
	freopen("subway.in","r",stdin);
	freopen("subway.out","w",stdout);
	cin>>c>>n>>m>>d>>q;
	for(int i=0;i<m;i++){
		cin>>co1[i];
	}
	for(int i=1;i<=n;i++){
		
	}
	return 0;
} 
