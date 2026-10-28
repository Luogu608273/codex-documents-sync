#include<iostream>
#include<vector>

using namespace std;
typedef long long ll;

const int N = 1e5 + 10, V = 1e5;
int n, k; bool b[N];
vector<int> p;

int main(){
	for(int i = 2; i <= V; i++){
		if(!b[i]){
			p.push_back(i);
			for(ll j = (ll)i*i; j <= V; j += i) b[j] = 1;
		}
	}
	cin >> n;
	for(int i = 0; i <= 14; i++){
		if((1 << i) >= n){
			cout << i << '\n';
			k = i;
			break;
		}
	}
	int cnt = 0;
	for(int i = 0; i < (1 << k) && cnt < n; i++){
		ll x = 1;
		for(int j = 0; j < k; j++){
			if(i & (1 << j)) x *= p[j*2];
			else x *= p[j*2+1];
		}
		if(x > 300000000000000000LL) continue;
		cout << k << ' ';
		for(int j = 0; j < k; j++){
			if(i & (1 << j)) cout << p[j*2] << ' ';
			else cout << p[j*2+1] << ' ';
		}
		cout << '\n';
		cnt++;
	}
	return 0;
}
