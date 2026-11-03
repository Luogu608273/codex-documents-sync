#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;
using lll = __int128;

const ll N = 32768, V = 20, P = 1e9 + 7, G = 3;
const ll P1 = 167772161, P2 = 998244353, P3 = 1004535809;

ll qpow(ll a, ll b, ll p)
{
	ll res = 1;
	while (b)
	{
		if (b & 1)
			res = res * a % p;
		b >>= 1;
		a = a * a % p;
	}
	return res;
}

namespace Poly_mod
{
	int L, r[N];
	ll pw[V][5], iv[V][5], num[N], inva, invab;

	void init()
	{
		for (int i = 1, j = 2; j <= N; ++i, j <<= 1)
		{
			pw[i][1] = qpow(G, (P1 - 1) / j, P1);
			iv[i][1] = qpow(pw[i][1], P1 - 2, P1);
			pw[i][2] = qpow(G, (P2 - 1) / j, P2);
			iv[i][2] = qpow(pw[i][2], P2 - 2, P2);
			pw[i][3] = qpow(G, (P3 - 1) / j, P3);
			iv[i][3] = qpow(pw[i][3], P3 - 2, P3);
		}
		num[1] = 1;
		for (int i = 2; i < N; ++i)
			num[i] = (P - P / i) * num[P % i] % P;
		inva = qpow(P1, P2 - 2, P2);
		invab = qpow(P1 * P2 % P3, P3 - 2, P3);
	}

	void calc(int n)
	{
		L = 1;
		while (L < n)
			L <<= 1;
		for (int i = 0; i < L; ++i)
			r[i] = (r[i >> 1] >> 1) | (i & 1 ? L >> 1 : 0);
	}

	void NTT(ll A[], bool type, int tp)
	{
		for (int i = 0; i < L; ++i)
		{
			if (i < r[i])
				swap(A[i], A[r[i]]);
		}
		for (int mid = 1, i = 1; mid < L; mid <<= 1, ++i)
		{
			ll w_n = type ? pw[i][tp] : iv[i][tp];
			for (int j = 0, R = mid << 1; j < L; j += R)
			{
				ll w = 1;
				for (int k = 0; k < mid; ++k)
				{
					ll x = A[j + k], y = A[j + k + mid] * w;
					if (tp == 1)
						y %= P1;
					if (tp == 2)
						y %= P2;
					if (tp == 3)
						y %= P3;
					A[j + k] = x + y;
					if (tp == 1 && A[j + k] >= P1)
						A[j + k] -= P1;
					if (tp == 2 && A[j + k] >= P2)
						A[j + k] -= P2;
					if (tp == 3 && A[j + k] >= P3)
						A[j + k] -= P3;
					A[j + k + mid] = x - y;
					if (tp == 1 && A[j + k + mid] < 0)
						A[j + k + mid] += P1;
					if (tp == 2 && A[j + k + mid] < 0)
						A[j + k + mid] += P2;
					if (tp == 3 && A[j + k + mid] < 0)
						A[j + k + mid] += P3;
					w *= w_n;
					if (tp == 1)
						w %= P1;
					if (tp == 2)
						w %= P2;
					if (tp == 3)
						w %= P3;
				}
			}
		}
		if (!type)
		{
			ll inv = 1;
			if (tp == 1)
				inv = qpow(L, P1 - 2, P1);
			if (tp == 2)
				inv = qpow(L, P2 - 2, P2);
			if (tp == 3)
				inv = qpow(L, P3 - 2, P3);
			for (int i = 0; i < L; ++i)
			{
				A[i] *= inv;
				if (tp == 1)
					A[i] %= P1;
				if (tp == 2)
					A[i] %= P2;
				if (tp == 3)
					A[i] %= P3;
			}
		}
	}

	void mul(ll A[], ll B[], ll C[], int n, int m)
	{
		static ll tmp[N];
		if (min(n, m) <= 32)
		{
			fill(tmp, tmp + n + m - 1, 0);
			for (int i = 0; i < n; ++i)
				for (int j = 0; j < m; ++j)
					(tmp[i + j] += A[i] * B[j] % P) >= P ? tmp[i + j] -= P : 0;
			copy(tmp, tmp + n + m - 1, C);
			return;
		}
		static ll tA1[N], tA2[N], tA3[N], tB1[N], tB2[N], tB3[N];
		calc(n + m - 1);
		for (int i = 0; i < n; ++i)
		{
			tA1[i] = A[i] % P1;
			tA2[i] = A[i] % P2;
			tA3[i] = A[i] % P3;
		}
		for (int i = 0; i < m; ++i)
		{
			tB1[i] = B[i] % P1;
			tB2[i] = B[i] % P2;
			tB3[i] = B[i] % P3;
		}
		fill(tA1 + n, tA1 + L, 0);
		fill(tA2 + n, tA2 + L, 0);
		fill(tA3 + n, tA3 + L, 0);
		fill(tB1 + m, tB1 + L, 0);
		fill(tB2 + m, tB2 + L, 0);
		fill(tB3 + m, tB3 + L, 0);
		NTT(tA1, 1, 1);
		NTT(tA2, 1, 2);
		NTT(tA3, 1, 3);
		NTT(tB1, 1, 1);
		NTT(tB2, 1, 2);
		NTT(tB3, 1, 3);
		for (int i = 0; i < L; ++i)
		{
			tA1[i] = tA1[i] * tB1[i] % P1;
			tA2[i] = tA2[i] * tB2[i] % P2;
			tA3[i] = tA3[i] * tB3[i] % P3;
		}
		NTT(tA1, 0, 1);
		NTT(tA2, 0, 2);
		NTT(tA3, 0, 3);
		lll ab = P1 * P2;
		for (int i = 0; i < n + m - 1; ++i)
		{
			ll t1 = (tA2[i] - tA1[i] + P2) % P2 * inva % P2;
			ll t2 = t1 * P1 + tA1[i];
			ll t3 = (tA3[i] - t2 % P3 + P3) % P3 * invab % P3;
			C[i] = (t2 + t3 * ab) % P;
		}
	}

	void inv(ll A[], ll B[], int n)
	{
		if (n == 1)
		{
			B[0] = qpow(A[0], P - 2, P);
			return;
		}
		int m = (n + 1) >> 1;
		inv(A, B, m);
		fill(B + m, B + n, 0);
		static ll tmp[N];
		mul(A, B, tmp, n, m);
		tmp[0] = (2 - tmp[0] + P) % P;
		for (int i = 1; i < n; ++i)
			tmp[i] = (P - tmp[i]) % P;
		mul(tmp, B, B, n, m);
		fill(B + n, B + n + m - 1, 0);
	}

	void devir(ll A[], ll B[], int n)
	{
		for (int i = 1; i < n; ++i)
			B[i - 1] = i * A[i] % P;
		B[n - 1] = 0;
	}

	void inter(ll A[], ll B[], int n)
	{
		for (int i = 1; i < n; ++i)
			B[i] = A[i - 1] * num[i] % P;
		B[0] = 0;
	}

	void ln(ll A[], ll B[], int n)
	{
		static ll tmp1[N], tmp2[N];
		devir(A, tmp1, n);
		inv(A, tmp2, n);
		mul(tmp1, tmp2, tmp1, n, n);
		inter(tmp1, B, n);
	}

	void exp(ll A[], ll B[], int n)
	{
		if (n == 1)
		{
			B[0] = 1;
			return;
		}
		int m = (n + 1) >> 1;
		exp(A, B, m);
		fill(B + m, B + n, 0);
		static ll tmp[N];
		ln(B, tmp, n);
		tmp[0] = (A[0] + 1 - tmp[0] + P) % P;
		for (int i = 1; i < n; ++i)
			tmp[i] = (A[i] - tmp[i] + P) % P;
		mul(B, tmp, B, m, n);
		fill(B + n, B + n + m - 1, 0);
	}
}

int n, m;
ll f[N], g[N];

void init()
{
	Poly_mod::init();
}

void solve()
{
	cin >> n >> m;
	for (int i = 1; i <= n; ++i)
	{
		ll a;
		cin >> a;
		a = a * i % P;
		for (int j = i; j <= m; j += i)
			(f[j] += a) >= P ? f[j] -= P : 0;
	}
	for (int i = 1; i <= m; ++i)
		f[i] = f[i] * Poly_mod::num[i] % P;
	Poly_mod::exp(f, g, m + 1);
	for (int i = 1; i <= m; ++i)
		cout << g[i] << " \n"[i == m];
}

int main()
{
	ios::sync_with_stdio(false);
	cin.tie(nullptr);
	cout.tie(nullptr);
	int _ = 1;
	// cin >> _;
	init();
	while (_--)
		solve();
	return 0;
}
