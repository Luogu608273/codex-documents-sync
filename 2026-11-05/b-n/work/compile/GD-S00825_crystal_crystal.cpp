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


long long n,s,mp[5000005],qzh[5000005],m;

signed main(){
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",stdout);
	cin>>n>>m;
	for(int i=1;i<=n;i++){
		cin>>mp[i];
	}
	sort(mp+1,mp+1+n);
	for(int i=1;i<=n;i++){
		qzh[i]=qzh[i-1]+mp[i];
	}
	for(int i=1;i<=n;i++){
		if(mp[i]*i-qzh[i]<=m) s=i;
		else{
			//cout<<mp[i]*i-qzh[i]<<" "<<m<<endl;
			break;
		}
	}
	cout<<s<<endl;
	//cout<<mp[s]<<" "<<qzh[s]<<" "<<mp[315275]<<" "<<qzh[315275]<<" "<<mp[500000]<<" "<<qzh[500000];
	return 0; 
}

