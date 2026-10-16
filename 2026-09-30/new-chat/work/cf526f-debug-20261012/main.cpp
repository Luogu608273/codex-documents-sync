#include <bits/stdc++.h>
#define endl '\n'

using namespace std;

using ll = long long;

const ll N = 3e5 + 5;

int n, top1, top2;
ll ans;
struct node
{
	int x, y;
} a[N], st1[N], st2[N];
struct
{
	int l, r, val, tag, cnt;
} t[N << 2];

void maintain(int p)
{
	t[p].val = min(t[p << 1].val, t[p << 1 | 1].val);
	t[p].cnt = 0;
	if (t[p].val == t[p << 1].val)
		t[p].cnt += t[p << 1].cnt;
	if (t[p].val == t[p << 1 | 1].val)
		t[p].cnt += t[p << 1 | 1].cnt;
}

void build(int p = 1, int l = 1, int r = n)
{
	t[p] = {l, r};
	if (l == r)
	{
		t[p].val = l;
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
	t[p << 1].val += t[p].tag;
	t[p << 1 | 1].val += t[p].tag;
	t[p << 1].tag += t[p].tag;
	t[p << 1 | 1].tag += t[p].tag;
	t[p].tag = 0;
}

void modify(int l, int r, int v, int p = 1)
{
	if (l <= t[p].l && t[p].r <= r)
	{
		t[p].val += v;
		t[p].tag += v;
		return;
	}
	int mid = (l + r) >> 1;
	pushdown(p);
	if (l <= mid)
		modify(l, r, v, p << 1);
	if (r > mid)
		modify(l, r, v, p << 1 | 1);
	maintain(p);
}

int query(int l, int r, int p = 1)
{
	if (l <= t[p].l && t[p].r <= r)
		return !t[p].val ? t[p].cnt : 0;
	int mid = (l + r) >> 1, res = 0;
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
		cin >> a[i].x >> a[i].y;
	sort(a + 1, a + n + 1, [](const node &x, const node &y)
		 { return x.x < y.x; });
	build();
	for (int i = 1; i <= n; ++i)
	{
		modify(1, n, -1);
		while (top1 && st1[top1].y < a[i].y)
		{
			modify(st1[top1 - 1].x + 1, st1[top1].x, a[i].y - st1[top1].y);
			--top1;
		}
		st1[++top1] = {i, a[i].y};
		while (top2 && st2[top2].y > a[i].y)
		{
			modify(st2[top2 - 1].x + 1, st2[top2].x, st2[top2].y - a[i].y);
			--top2;
		}
		st2[++top2] = {i, a[i].y};
		ans += query(1, i);
	}
	cout << ans << endl;
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
