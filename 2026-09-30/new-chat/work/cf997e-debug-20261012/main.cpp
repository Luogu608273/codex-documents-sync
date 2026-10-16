#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;
using pii = pair<int, int>;

const ll N = 3e5 + 5;

int n, m, a[N], top1, top2;
ll ans[N];
pii st1[N], st2[N];
struct
{
	int l, r, minn, atg, cnt, val, htg;
} t[N << 2];
vector<pii> vec[N];

void maintain(int p)
{
	t[p].minn = min(t[p << 1].minn, t[p << 1 | 1].minn);
	t[p].cnt = 0;
	if (t[p].minn == t[p << 1].minn)
		t[p].cnt += t[p << 1].cnt;
	if (t[p].minn == t[p << 1 | 1].minn)
		t[p].cnt += t[p << 1 | 1].cnt;
}

void build(int p = 1, int l = 1, int r = n)
{
	t[p] = {l, r};
	if (l == r)
	{
		t[p].minn = l;
		t[p].cnt = 1;
		return;
	}
	int mid = (l + r) >> 1;
	build(p << 1, l, mid);
	build(p << 1 | 1, mid + 1, r);
	maintain(p);
}

void pushdown(int p)
{
	if (t[p].atg)
	{
		t[p << 1].minn += t[p].atg;
		t[p << 1 | 1].minn += t[p].atg;
		t[p << 1].atg += t[p].atg;
		t[p << 1 | 1].atg += t[p].atg;
		t[p].atg = 0;
	}
	if (t[p].htg)
	{
		if (t[p << 1].minn == t[p].minn)
		{
			t[p << 1].val += t[p].htg * t[p << 1].cnt;
			t[p << 1].htg += t[p].htg * t[p << 1].cnt;
		}
		if (t[p << 1 | 1].minn == t[p].minn)
		{
			t[p << 1 | 1].val += t[p].htg * t[p << 1].cnt;
			t[p << 1 | 1].htg += t[p].htg * t[p << 1].cnt;
		}
		t[p].htg = 0;
	}
}

void modify(int l, int r, int v, int p = 1)
{
	if (l <= t[p].l && t[p].r <= r)
	{
		t[p].minn += v;
		t[p].atg += v;
		return;
	}
	int mid = (t[p].l + t[p].r) >> 1;
	pushdown(p);
	if (l <= mid)
		modify(l, r, v, p << 1);
	if (r > mid)
		modify(l, r, v, p << 1 | 1);
	maintain(p);
}

void update(int l, int r, int p = 1)
{
	if (l <= t[p].l && t[p].r <= r)
	{
		if (!t[p].minn)
		{
			t[p].val += t[p].cnt;
			++t[p].htg;
		}
		return;
	}
	int mid = (t[p].l + t[p].r) >> 1;
	pushdown(p);
	if (l <= mid)
		update(l, r, p << 1);
	if (r > mid)
		update(l, r, p << 1 | 1);
	maintain(p);
}

int query(int l, int r, int p = 1)
{
	if (l <= t[p].l && t[p].r <= r)
		return t[p].val;
	int mid = (t[p].l + t[p].r) >> 1, res = 0;
	pushdown(p);
	if (l <= mid)
		res += query(l, r, p << 1);
	if (r > mid)
		res += query(l, r, p << 1 | 1);
	return res;
}

void init() {}

void solve()
{
	cin >> n;
	for (int i = 1; i <= n; ++i)
		cin >> a[i];
	cin >> m;
	for (int i = 1, l, r; i <= n; ++i)
	{
		cin >> l >> r;
		vec[r].push_back({l, i});
	}
	build();
	for (int i = 1; i <= n; ++i)
	{
		modify(1, n, -1);
		while (top1 && st1[top1].second < a[i])
		{
			modify(st1[top1 - 1].first + 1, st1[top1].first, a[i] - st1[top1].second);
			--top1;
		}
		st1[++top1] = {i, a[i]};
		while (top2 && st2[top2].second > a[i])
		{
			modify(st2[top2 - 1].first + 1, st2[top2].first, st2[top2].second - a[i]);
			--top2;
		}
		st2[++top2] = {i, a[i]};
		for (auto [x, id] : vec[i])
			ans[id] = query(x, i);
	}
	for (int i = 1; i <= m; ++i)
		cout << ans[i] << endl;
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
