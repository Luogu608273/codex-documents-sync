#include<iostream>
#include<vector>

using namespace std;
typedef long long ll;

const int N = 2e6 + 10;
int c, t, n, l[N], r[N], cl1[N], cr1[N], cl2[N], cr2[N]; ll d, x[N], ans;

int main(){
	ios::sync_with_stdio(0);
	cin.tie(0); cout.tie(0);
	cin >> c >> t;
	while(t--){
		cin >> n >> d; ans = 0;
		for(int i = 1; i <= n; i++) cin >> x[i];
		for(int i = 1, j = 1; i <= n; i++){
			while(j < i && x[j]+d < x[i]) j++;
			l[i] = j;
		}
		for(int i = n, j = n; i >= 1; i--){
			while(j > i && x[j]-d > x[i]) j--;
			r[i] = j;
		}
		cl2[n] = 1;
		for(int i = n-1; i >= 1; i--){
			if(r[i] == r[i+1]) cl2[i] = cl2[i+1]+1;
			else cl2[i] = 1;
		}
		cr2[1] = 1;
		for(int i = 2; i <= n; i++){
			if(l[i] == l[i-1]) cr2[i] = cr2[i-1]+1;
			else cr2[i] = 1;
		}
		for(int i = 1; i <= n; i++){
			if(r[l[i]] == i && l[i] != i) cl1[i] = cl1[l[i]]+min(cl2[l[i]], i-l[i]);
			else cl1[i] = 0;
		}
		for(int i = n; i >= 1; i--){
			if(l[r[i]] == i && r[i] != i) cr1[i] = cr1[r[i]]+min(cr2[r[i]], r[i]-i);
			else cr1[i] = 0;
		}
		for(int i = 1; i < n; i++){
			int m1 = i, m2 = i+1;
			if(x[m2]-x[m1] > d) continue;
			int lm = l[m2], rm = r[m1];
			if(lm == m1 || rm == m2) continue;
			if(r[lm] == m2 && l[rm] == m1){
				int a = (l[m1] == lm ? cl1[lm] : 0)+min(cl2[lm], m1-lm);
				int b = (r[m2] == rm ? cr1[rm] : 0)+min(cr2[rm], rm-m2);
				ans += (ll)a*b;
			}
		}
		cout << ans << '\n';
	}
	return 0;
}
