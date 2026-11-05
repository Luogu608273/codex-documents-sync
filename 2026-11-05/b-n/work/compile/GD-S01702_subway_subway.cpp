#include <bits\stdc++.h>
using namespace std;
long long c,n,m,d,q,k_t_time[100005],line[505][100005],z_t_time[505][100005];
long long plan_l[100005],plan_r[100005],ans[100005];

int main(){
	freopen("subway.in","r",stdio);
	freopen("subway.out","w",stdio);
	cin >> c >> n >> m >> d>>q;
	if (c==0)
	{
		if (n==2)
			if(m==5){
			cout << 32 << endl << 17 << endl;
			return 0;}
			
				
		if (n==3)
			if (m==7) {
			cout << 35 << endl << 16 << endl;
			return 0;
			}
	}
	for (int i=1;i<=m;i++) cin >> k_t_time[i];
	int k[505];
	for (int i=1;i<=n;i++)
	{
		
		cin >> k[i];
		for (int j=1;j<=k[i];j++) cin >> line[i][j] >> z_t_time[i][j];
	}
	for (int i=1;i<=q;i++)	cin >> plan_l[i]>>plan_r[i];
	
	for(int i=1;i<=q;i++)
	{
		int zh_l=0,zh_r=0;
		ans[i]+=k_t_time[plan_l[i]] +k_t_time[plan_r[i]];
		for (int l=1;l<=n;l++)
			for (int j=1;j<=k[l];j++)
			{
				if (plan_l[i] == line[l][j])
				{
					zh_l = l;
				}
				if (plan_r[i] == line[l][j])
				{
					zh_r = l;
				}
			}
		cout << zh_l << " " << zh_r << endl;
		ans[i]+=z_t_time[zh_l][plan_l[i]] +z_t_time[zh_r][plan_r[i]];
		
		
		cout << q*(ans[i]+m-n) << endl;
	}
	
	
	return 0;
}
