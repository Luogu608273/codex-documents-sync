#include <bits\stdc++.h>
using namespace std;
int c,t;
long long n,d;

int main(){
	//freopen("migrate.in","r",stdio);
	//freopen("migrate.out","w",stdio);
	cin >> c >> t;
	while(t--)
	{
		cin >> n >> d;
		int s[100005] = {0},a[100005] = {0};
		for (int i=1 ;i<=n;i++)
		{
			cin >> s[i];
			a[s[i]]++;
		}
		int ans = 0;
		
		for (int i=1 ;i<=n;i++)
		{
			int bol=0;
			for (int j=d ;j>0;j--)
			{
				int o=1;
				if (a[s[i]+j]==1)
					if(bol==0)
					{
						bol++;
						ans++;
					}
					else
					{
						ans--;
						//o=0;
						break;
					}
				//if (o==0) 
			}
		}
		cout << ans <<endl;
	}
	
	return 0;
}

