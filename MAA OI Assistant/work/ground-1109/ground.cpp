#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const int N = 505, M = 1000005, D = 245, P = 998244353;

int n, m, cnt, d[D], id[M], to[D][D], f[2][N][D];

void solve()
{
	cin >> n >> m;
	for (int i = 1; i <= m; ++i)
		if (m % i == 0)
		{
			d[++cnt] = i;
			for (int j = i; j <= m; j += i)
				id[j] = cnt;
		}
	id[0] = cnt;
	for (int i = 1; i <= cnt; ++i)
		for (int j = 1; j <= cnt; ++j)
			to[i][j] = id[1LL * d[i] * d[j] % m];
	f[0][1][1] = 1;
	for (int i = 1; i <= n; ++i)
	{
		int p = i & 1;
		for (int j = 1; j <= n; ++j)
		{
			int x;
			cin >> x;
			fill(f[p][j] + 1, f[p][j] + cnt + 1, 0);
			if (x == -1)
				continue;
			int *t = to[id[x % m]];
			for (int k = 1; k <= cnt; ++k)
			{
				int v = f[p ^ 1][j][k] + f[p][j - 1][k];
				if (v >= P) v -= P;
				int &s = f[p][j][t[k]];
				if ((s += v) >= P) s -= P;
			}
		}
	}
	cout << f[n & 1][n][cnt] << endl;
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	// freopen("ground.in", "r", stdin);
	// freopen("ground.out", "w", stdout);
	solve();
	return 0;
}
