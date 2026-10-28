#include<bits/stdc++.h>
#define ffor(i,a,b) for(int i=(a);i<=(b);i++)
#define roff(i,a,b) for(int i=(a);i>=(b);i--)
using namespace std;
typedef unsigned int u32;
typedef unsigned long long u64;

/*
	D 二进制拆分

	【转化】S_n = 值域 [0,29]、和为 n 的 2 的幂多重集的权值积之和。
	记 dp[n][l][r] = 值取自 [l,r]、最大值恰为 r、和为 n 的权值和；
	空集记账约定 dp[0][l][o]=[l==o]（让拆分参数 o 唯一）。

	【拆分引理】k=⌊log2 n⌋：按值从大到小逐层累加，层 c 的部分和都是 2^c 的倍数，
	从 <2^k 跨到 >=2^k 必恰经过 2^k，故存在唯一的「大头后缀」和为 2^k。于是
		dp[n][l][r] = Σ_o dp[n-2^k][l][o] · dp[2^k][o][r]。
	2 的幂是原子：n=2^k 时前半为空 ⇔ o=l。

	【原子表】D_t[l][r]=dp[2^t][l][r]：r>t 全 0；r=t 恰为 w_t（只能 {t}）；
	r<t 用引理（对 2^t 取 k=t-1）得 D_t = D_{t-1}^2 再把第 t 列（行 l<=t）覆盖成 w_t。

	【查询链】n 的二进制位 b_1<...<b_m（小位先乘）：
	dp[n][0][*] = e_0 · D_{b_1} · ... · D_{b_m}，S_n = 行向量求和。

	【meet in the middle】位 0..14 低位、15..29 高位：
	  vlo[m][*] = e_0 · Π_{m 的位 b} D_b          （行向量；递推 vlo[m]=vlo[m^(1<<hb)]·D_hb）
	  whi[m][*] = Π_{m 的位 b} D_{b+15} · 𝟙       （列向量；递推 whi[m]=D_{lb+15}·whi[m^(1<<lb)]）
	  S_n = Σ_i vlo[n&32767][i] · whi[n>>15][i]
	（高位掩码的第 b 位对应真实位 b+15，别丢偏移。）

	【复杂度】时间 O(30^4 + 2^16·900 + q·30)，空间 2·2^15·30·4B ≈ 7.9MB。
	【变量】w 权值；D[30] 张 30x30 原子矩阵；vlo/whi 两张 mitm 表；ibuf/obuf 快读快写缓冲。
*/

const int MOD=998244353,B=15,SZ=1<<B;

int w[30];
u32 D[30][30][30];			// D[t]：原子矩阵 D_t[l][r] = dp[2^t][l][r]
u32 vlo[SZ][30],whi[SZ][30];		// vlo：低位行向量表；whi：高位列向量表（均 mod p）

static char ibuf[1<<24]; int ipos,ilen;
static char obuf[1<<24]; int opos;

int rd(){				// 快读非负整数（跳过所有非数字字符）
	while(ipos<ilen&&(ibuf[ipos]<'0'||ibuf[ipos]>'9')) ipos++;
	if(ipos>=ilen) return -1;
	int x=0;
	while(ipos<ilen&&ibuf[ipos]>='0'&&ibuf[ipos]<='9') x=x*10+(ibuf[ipos++]-'0');
	return x;
}
void wr(u32 x){				// 快写
	char tmp[12]; int t=0;
	if(!x) tmp[t++]='0';
	while(x) tmp[t++]='0'+x%10,x/=10;
	while(t) obuf[opos++]=tmp[--t];
}

void matsq(u32 A[30][30],u32 R[30][30]){	// R = A^2（mod p 普通矩阵乘，8 项一取模防溢出）
	ffor(l,0,29) ffor(r,0,29){
		u64 s=0; int cnt=0;
		ffor(o,0,29){ s+=(u64)A[l][o]*A[o][r]; if((++cnt&7)==0) s%=MOD; }
		R[l][r]=s%MOD;
	}
}
void mulvm(u32* v,const u32 M[30][30]){		// v <- v·M（行向量乘矩阵）
	static u64 acc[30];
	ffor(r,0,29) acc[r]=0;
	int used=0;
	ffor(o,0,29){
		if(!v[o]) continue ;
		u64 vo=v[o];
		ffor(r,0,29) acc[r]+=vo*M[o][r];
		if((++used&7)==0) ffor(r,0,29) acc[r]%=MOD;
	}
	ffor(r,0,29) v[r]=acc[r]%MOD;
}

int main(){
freopen("power.in","r",stdin);
    freopen("power.out","w",stdout);
	ilen=(int)fread(ibuf,1,sizeof ibuf,stdin),ipos=0;
	ffor(i,0,29) w[i]=rd();
	int q=rd();
	memset(D,0,sizeof D);
	D[0][0][0]=w[0];			// D_0：dp[1] 只有 {0}
	ffor(t,1,29){
		matsq(D[t-1],D[t]);		// r<t 部分：D_t = D_{t-1}^2
		ffor(l,0,t) D[t][l][t]=w[t];	// r=t 覆盖为 w_t（只能 {t}）
	}
	vlo[0][0]=1;				// e_0
	ffor(m,1,SZ-1){
		int hb=31-__builtin_clz(m);
		ffor(r,0,29) vlo[m][r]=vlo[m^(1<<hb)][r];
		mulvm(vlo[m],D[hb]);
	}
	ffor(r,0,29) whi[0][r]=1;		// 𝟙
	ffor(m,1,SZ-1){
		int lb=__builtin_ctz(m),src=m^(1<<lb);
		const u32 (*M)[30]=D[lb+B];	// 高位掩码第 b 位 = 真实位 b+15
		ffor(l,0,29){
			u64 s=0; int cnt=0;
			ffor(o,0,29){ s+=(u64)M[l][o]*whi[src][o]; if((++cnt&7)==0) s%=MOD; }
			whi[m][l]=s%MOD;
		}
	}
	opos=0;
	ffor(i,1,q){
		u32 n=rd();
		const u32* a=vlo[n&(SZ-1)]; const u32* b=whi[n>>B];
		u64 s=0; int cnt=0;
		ffor(j,0,29){ s+=(u64)a[j]*b[j]; if((++cnt&7)==0) s%=MOD; }
		if(i>1) obuf[opos++]=' ';
		wr(s%MOD);
	}
	obuf[opos++]='\n';
	fwrite(obuf,1,opos,stdout);
	return 0;
}
