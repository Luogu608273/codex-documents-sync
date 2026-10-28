#include<bits/stdc++.h>
#define ffor(i,a,b) for(int i=(a);i<=(b);i++)
#define roff(i,a,b) for(int i=(a);i>=(b);i--)
using namespace std;
typedef unsigned int u32;
typedef unsigned long long ull;
typedef long long ll;

/*
	C 狼人游戏（计数版）正解 O(n log n)：扫描 q + 线段树维护转移矩阵乘积。

	【DP】固定狼总数 q：pin(x)= b_x (d_x=L) 或 q-b_x (d_x=R)，φ(x)=pin(x)-x。
		dp[1] = [φ(1)=-1]，dp[2] = [φ(2)=-1] + c1(2)·dp[1]，
		dp[p] = c1(p)·dp[p-1] + c2(p)·dp[p-2]（p>=3），
		c1(p) = [pin(p)=pin(p-1)]，c2(p) = [pin(p)=pin(p-2)-1]；
		答案 = Σ_{p∈{n-1,n}} dp[p]·[φ(p)=q-n]，对 q∈[0,⌊(n+1)/2⌋] 求和（mod 998244353）。

	【关键结构】每个 0/1 判定按两个端点的 d 是否同方向分类：
	  · 同方向：与 q 无关，恒真或恒假；
	  · 不同方向：条件恰为 q = b_i + b_j（gap=1）或 b_i + b_j + 1（gap=2）——只对一个 q 为真。
	首/尾判定同理（R 头、L 尾是单 q；其余 q 无关）。于是全部 q 扫过一遍时，
	「单 q 判定」的翻转总次数 = O(n)：每个在 q=ℓ 开启、q=ℓ+1 关闭。

	【实现】把 p=3..n 的转移写成 2×2 矩阵 M_p=[[c1,c2],[1,0]]（模意义下按 (+,×) 相乘），
	线段树维护按位置左到右的全部乘积 P = M_n ⋯ M_3（合并时右区间乘积左乘左区间乘积），
	扫描 q：先处理 q-1 的关闭、再 q 的开启（均为单点更新），然后
		[dp[n]; dp[n-1]] = P · [dp[2]; dp[1]]，
	配合种子/首尾判定（O(1) 直接求）累加答案(q)。总复杂度 O((Σn)·log n)。

	【变量】d_ 方向；b_ 值；tr 线段树（u32 存模值）；typ/lab 单元类型与标签；
	事件桶 evh/evn（head+nxt 链表，条目编码 id=p*2+t）。
*/

const int MOD=998244353;
const int MAXN=500005;

struct Mat{ u32 a00,a01,a10,a11; };

inline Mat mul(const Mat &X,const Mat &Y){		// 返回 X·Y
	Mat Z;
	Z.a00=(u32)(((ull)X.a00*Y.a00+(ull)X.a01*Y.a10)%MOD);
	Z.a01=(u32)(((ull)X.a00*Y.a01+(ull)X.a01*Y.a11)%MOD);
	Z.a10=(u32)(((ull)X.a10*Y.a00+(ull)X.a11*Y.a10)%MOD);
	Z.a11=(u32)(((ull)X.a10*Y.a01+(ull)X.a11*Y.a11)%MOD);
	return Z;
}

int n,T_;
char d_[MAXN];
int b_[MAXN];

Mat tr[MAXN*4];
int typ_[2][MAXN];			// 0 恒假 1 恒真 2 单 q
int lab_[2][MAXN];
int val_[2][MAXN];			// 当前取值
int evh_act[MAXN], evh_deact[MAXN];
int evn_act[MAXN*2], evn_deact[MAXN*2];
int evs_act[MAXN*2], evs_deact[MAXN*2];

inline void setleaf(int o,int p){
	tr[o].a00=val_[0][p]; tr[o].a01=val_[1][p];
	tr[o].a10=1; tr[o].a11=0;
}
void build(int o,int l,int r){
	if(l==r){ setleaf(o,l); return ; }
	int mid=(l+r)>>1;
	build(o<<1,l,mid); build(o<<1|1,mid+1,r);
	tr[o]=mul(tr[o<<1|1],tr[o<<1]);			// 右区间左乘
}
void upd(int o,int l,int r,int x){
	if(l==r){ setleaf(o,x); return ; }
	int mid=(l+r)>>1;
	if(x<=mid) upd(o<<1,l,mid,x); else upd(o<<1|1,mid+1,r,x);
	tr[o]=mul(tr[o<<1|1],tr[o<<1]);
}

int main() {
freopen("wolf.in","r",stdin);
    freopen("wolf.out","w",stdout);
	scanf("%d",&T_);
	while(T_--) {
		scanf("%d %s",&n,d_+1);
		ffor(i,1,n) scanf("%d",&b_[i]);
		int Q=(n+1)/2;
		if(n==2) {
			ll ans=0;
			ffor(q,0,1) {
				ll dp1=(d_[1]=='L')?((b_[1]==0)?1:0):((q==b_[1])?1:0);
				ll h2=(d_[2]=='L')?((b_[2]==1)?1:0):((q==b_[2]+1)?1:0);
				ll c12=(d_[1]==d_[2])?((b_[2]==b_[1])?1:0):((q==b_[1]+b_[2])?1:0);
				ll dp2=(h2+c12*dp1)%MOD;
				ll r=0;
				ffor(p,1,2) {
					int phi=(d_[p]=='L')?b_[p]-p:q-b_[p]-p;
					if(phi==q-n) r+= (p==1?dp1:dp2);
				}
				ans=(ans+r)%MOD;
			}
			printf("%lld\n",ans);
			continue;
		}
		// 事件桶初始化
		ffor(q,0,Q) evh_act[q]=evh_deact[q]=-1;
		int ec=0;
		ffor(p,3,n) ffor(t,0,1) {
			int i=(t==0)?p-1:p-2;
			if(d_[i]==d_[p]) {
				if(t==0) typ_[0][p]=(b_[p]==b_[i])?1:0;
				else typ_[1][p]=((d_[p]=='L')?(b_[p]==b_[i]+1):(b_[p]==b_[i]-1))?1:0;
			} else {
				typ_[t][p]=2;
				if(t==0) lab_[0][p]=b_[p]+b_[i];
				else lab_[1][p]=b_[p]+b_[i]+((d_[p]=='R')?1:-1);
			}
			if(typ_[t][p]==2) {
				int id=p*2+t, L=lab_[t][p];
				if(L>=0&&L<=Q) { ec++; evn_act[ec]=evh_act[L]; evh_act[L]=ec; evs_act[ec]=id; }
				if(L+1<=Q) { ec++; evn_deact[ec]=evh_deact[L+1]; evh_deact[L+1]=ec; evs_deact[ec]=id; }
			}
		}
		// 初始：单 q 单元全灭，恒真单元为 1
		ffor(p,3,n) ffor(t,0,1) val_[t][p]=(typ_[t][p]==1)?1:0;
		build(1,3,n);
		ll ans=0;
		ffor(q,0,Q) {
			if(q>=1) {
				for(int e=evh_deact[q];e!=-1;e=evn_deact[e]) {
					int id=evs_deact[e], p=id>>1, t=id&1;
					val_[t][p]=0; upd(1,3,n,p);
				}
			}
			for(int e=evh_act[q];e!=-1;e=evn_act[e]) {
				int id=evs_act[e], p=id>>1, t=id&1;
				val_[t][p]=1; upd(1,3,n,p);
			}
			// 种子
			ll dp1=(d_[1]=='L')?((b_[1]==0)?1:0):((q==b_[1])?1:0);
			ll h2=(d_[2]=='L')?((b_[2]==1)?1:0):((q==b_[2]+1)?1:0);
			ll c12=(d_[1]==d_[2])?((b_[2]==b_[1])?1:0):((q==b_[1]+b_[2])?1:0);
			ll dp2=(h2+c12*dp1)%MOD;
			const Mat &P=tr[1];
			ll dpn=((ull)P.a00*dp2+(ull)P.a01*dp1)%MOD;
			ll dpnm1=((ull)P.a10*dp2+(ull)P.a11*dp1)%MOD;
			// 首尾收集
			ll add=0;
			int pn=n,pn1=n-1;
			{
				int tau=(d_[pn]=='L')?((q==n-pn+b_[pn])?1:0):((b_[pn]==n-pn)?1:0);
				add+=tau*dpn;
			}
			{
				int tau=(d_[pn1]=='L')?((q==n-pn1+b_[pn1])?1:0):((b_[pn1]==n-pn1)?1:0);
				add+=tau*dpnm1;
			}
			ans=(ans+add)%MOD;
		}
		printf("%lld\n",ans);
	}
	return 0;
}
