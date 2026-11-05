#include <cctype>
#include <cerrno>
#include <cfloat>
#include <ciso646>
#include <climits>
#include <clocale>
#include <cmath>
#include <csetjmp>
#include <csignal>
#include <cstdarg>
#include <cstddef>
#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <ctime>
#include <cwchar>
#include <cwctype>
#include <complex>
#include <deque>
#include <exception>
#include <fstream>
#include <functional>
#include <iomanip>
#include <ios>
#include <iosfwd>
#include <iostream>
#include <istream>
#include <iterator>
#include <limits>
#include <list>
#include <locale>
#include <map>
#include <memory>
#include <new>
#include <numeric>
#include <ostream>
#include <queue>
#include <set>
#include <sstream>
#include <stack>
#include <stdexcept>
#include <streambuf>
#include <string>
#include <typeinfo>
#include <utility>
#include <valarray>
#include <vector>
#include <algorithm>
#include <bitset>
#include <functional>
#include <iterator>
#include <limits>
#include <memory>
#include <new>
#include <numeric>
#include <typeinfo>
#include <utility>
using namespace std;

int c,n,m,d,q,k[505],w[500005],f,to;
vector<int> a[505],v[500005];
vector<pair<int,int> > sdt[500005];
map<pair<int,int>,int> t;
bool vis[500005];
int dfs(int s,int e,int r,int z){
	if(s==e) return z+t[{r,s}];
	int ans=INT_MAX;
	for(auto i:sdt[s]){
		if(!vis[i.second]){
			//cout<<1;
			vis[i.second]=1;
			//if(r) cout<<"+"<<t[{i.first,s}]<<" ";
			if(r==0) ans=min(ans,dfs(i.second,e,i.first,z+t[{i.first,s}]));
			else ans=min(ans,dfs(i.second,e,i.first,z+(r==i.first?0:t[{r,s}]+t[{i.first,s}])));
			vis[i.second]=0;
		}
	}
	return ans;
}
signed main(){
	freopen("subway.in","r",stdin);
	freopen("subway.out","w",stdout);
	cin>>c>>n>>m>>d>>q;
	for(int i=1;i<=m;i++){
		cin>>w[i];
	}
	for(int i=1;i<=n;i++){
		cin>>k[i];
		a[i].push_back(0);
		for(int j=1;j<=k[i];j++){
			int x,y;
			cin>>x>>y;
			a[i].push_back(x);
			t[{i,x}]=y;
			if(j>=2){
				sdt[a[i][j]].push_back({i,a[i][j-1]});
				sdt[a[i][j-1]].push_back({i,a[i][j]});
			}
		}
	}
	for(int i=1;i<=q;i++){
		cin>>f>>to;
		printf("%d\n",dfs(f,to,0,w[f]+w[to]));
	}
	return 0;
}

