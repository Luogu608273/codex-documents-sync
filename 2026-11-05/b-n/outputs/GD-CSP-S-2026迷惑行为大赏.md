# GD CSP-S 2026 迷惑行为大赏

## GD-S00039

### 让我想想

`GD-S00039/migrate/migrate.cpp`，第 124–130 行（注释）。

```cpp
我是不是无意间想到正解了
让我想想 
啊
谈笑间被第二个小样例卡了
让我想想
这也忒阴间了
让我想想这该怎么做
```

## GD-S00150

### Oct31==Dec25?

`GD-S00150/crystal/crystal.cpp`，第 7–8 行。

```cpp
//神秘压缩包密码 `Oct31==Dec25?`
//不尔官方也爱玩梗吗 
```

八进的 31 等于十进制 25，万圣节 = 圣诞节。

## GD-S00159

### d 的作用逐渐增大

`GD-S00159/subway/subway.cpp`，第 103–109 行（注释）。

```cpp
d 到底是啥（  

3:24 p.m. 注意到 d 有滚木作用
只算步行时间，也就是说线路间的边权为 0
但好像也不是缩点（绝对不是因为我不熟 Tarjan）
其实可以直接建个图 然后暴力 floyd 
等一下，发现 d 的作用好像超过了滚木
```

## GD-S00179

### 读取答案

`GD-S00179/subway/subway.cpp`，第 11–20 行。

```cpp
	if(c==0){
		if(n==2&&m==5&&d==20&&q==2){
			cout<<32<<'\n'<<17;
		}else if(n==3&&m==7&&d==20&&q==2)cout<<35<<'\n'<<16;
		else if(n==15&&m==136&&d==20&&q==200){
			freopen("subway3.ans","r",stdin);
			for(ll i=1;i<=q;i++){
				ll x;cin>>x;
				cout<<x<<'\n';
			}
```

## GD-S00192

### 过秦论

`GD-S00192/hub/hub.cpp`，第 38–40 行（注释）。

```cpp
过秦论
贾谊
  秦孝公据崤函之固，拥雍州之地，君臣固守以窥周室，有席卷天下，包举宇内，囊括四海之意，并吞八荒之心。当是时也，商君佐之，内立法度，务耕织，修守战之具，外连衡而斗诸侯。于是秦人拱手而取西河之外。
```

`GD-S00192/hub/hub.cpp`，第 46 行（注释）。

```cpp
默不完了 
```

## GD-S00378

### in.crystal/out.crystal

`GD-S00378/crystal/crystal.cpp`，第 5–6 行。

```cpp
	freopen("in.crystal","r",stdin);
	freopen("out.crystal","w",stdout);
```

## GD-S00428

### 能拖一会儿是一会儿

`GD-S00428/hub/hub.cpp`，第 6–10 行。

```cpp
	int b=0;
	while(1){
		b++;
	}
	//不会，能拖一会儿是一会儿 
```

## GD-S00727

### 诈骗现场

`GD-S00727/subway/subway.cpp`，第 18–22 行。

```cpp
signed main() {
//	freopen("subway.out", "w", stdout); //诶我不小心把 freopen 注释了
	freopen("subway.in", "r", stdin);   //欸还没注释呢
//	freopen("subway.in", "r", stdin);   //欸我又不小心注释了
	freopen("subway.out", "w", stdout); //欸我骗你的 awa
```

## GD-S00846

### freout/freclose

`GD-S00846/subway/subway.cpp`，第 3–16 行。

```cpp
const int N=5*1e5;
int c,n,m,d,q;
int w[N]
int main(){
	freopen("subway.in","D",subway);
	freout("subway.out","D",subway);
	cin>>c>>n>>m>>d>>q;
	for(int i=1;i<=m;i++){
		cin>>w[i];
	}
	cout<<32<<endl;
	cout<<17<<endl;
	freclose("subway.in","D",subway);
	freout("subway.out","D",subway);
```

`freout`、`freclose` 不是这里可用的标准文件函数；模式写成 `"D"`，第三参数直接填 `subway`。本地语法检查还首先遇到了前一行缺分号。

## GD-S00883

### remember to write freoepn

`GD-S00883/crystal/crystal.cpp`，第 175 行（注释）。

```cpp
//freopen//freopen//freopen//freopen//freopen,remember to write freoepn
```

最后确实记得写了 `freoepn`。

## GD-S00908

### 提交 checker

`GD-S00908/hub/hub.cpp`，第 3–12 行。

```cpp
string s1,s2;
int main(){
	freopen("D://GD-S00908//subway/subway.out","r",stdin);
	char c;
	while ((c=getchar())!=EOF) s1.push_back(c);
//	s1.pop_back();
	freopen("D://csps-new//down//subway//subway7.ans","r",stdin);
	while ((c=getchar())!=EOF) s2.push_back(c);
	if (s1==s2) cout <<"AC!";
	else cout <<"WA!";
```

## GD-S00953

### 不是我的正解错了，是我的二分错了

`GD-S00953/crystal/crystal.cpp`，第 47–51 行（注释）。

```cpp
ok，我的正解炸了，然后我用二分的写法跟我的正解打对拍发现我的正解错了，我的二分写法应该是没问题的，而且二分的时间复杂度正确。

17：02分，抱歉，是我的二分写错了，继续用上面那份代码继续打对拍！！！

17：10分，拍了1000组没问题，应该过了
```

## GD-S00985

### 本来想写 feropen，后来忍住了

`GD-S00985/hub/hub.cpp`，第 27–29 行（注释）。

```cpp
本来想写个feropen给大家整个活，想了想还是算了
学了3年这个了 上午的J组250+谁能绷住
我最大的愿望就是这个玩意可以上那个每年一度的CSP迷惑行为大赏(还是叫其他什么的)
```

## GD-S00987

### 复杂度自己又升了一次

`GD-S00987/hub/hub.cpp`，第 79–87 行（注释）。

```cpp
n^3 推完了
g_u = max dep
f_{u, d, k, 1/2}
d 是最低连通块深度，k 是不在连通块的子树内的 max dep
不想写 XD
回去让 gpt 教我吧
唉，写一点吧
不对啊
这是 n^4
```

### 做题力竭之后开始排游戏日程

`GD-S00987/migrate/migrate.cpp`，第 99–108 行（注释）。

```cpp
n^2 写了一个半小时
力竭了
好想玩 arknights endfield arcaea phigros milthm
好想出勤，好久没给他们开花一轮信用图灵之迹存货千年了
还想开 xx，可惜一个门都没开
另外感觉小葱不如烧鸟（
考完 csp 回去打阿莱克琉斯。这个镀层好难啊，还是说因为我手法太差了
明天还要下塔露拉和小皇帝
为什么小皇帝是黄毛啊，是白毛的话就是白皇帝了
提醒我了，我还要给他们开白皇帝
```

后面还有长篇内容，自行查看。

## GD-S01126

### T4 看不懂，写个 LCA 庆祝

`GD-S01126/hub/hub.cpp`，第 71–75 行（注释）。

```cpp
5：02 DEV-C++神力，T3成功做到输入RE
 5：20 终于搞好T3输入RE的问题了，我真是太难了，呜呜呜 
 5：40 T3暴力终于写完了，我要崩了
 5：50 T4啥玩意看不懂，写个LCA庆祝一下吧
 6：06 T4RE我也不管了好吧，摸鱼ING... 
```

## GD-S01372

### 地铁站里藏了一位空洞骑士

`GD-S01372/subway/subway.cpp`，第 65–71 行（注释）。

```cpp
你是容器

你是空洞骑士 



去年我就写了这些，真的会有人看到吗？ 
```

## GD-S01444

### 从 freopen 到不要在岩浆里游泳

`GD-S01444/hub/hub.cpp`，第 47–57 行（注释）。

```cpp
一定要记得开long long
一定要记得freopen
一定要记得freopen不要写成froepen frepoen feropen等奇怪的写法 不要写错文件名。 
一定，一定要复习，不要像我这样裸考来 虽然我穿了衣服
最后，一定，一定，一定要休息好！
（昨晚获得了6小时30分钟低质睡眠） 
一定要注意身体， 
不要挑食，要多吃蔬菜，少吃点零食，少吃点油炸的东西
不要在没有专业训练的情况下尝试自学女高音！！ 很伤喉咙。 
不要尝试在岩浆里游泳。
不要在没有把握的情况下把校规视为每日任务。
```

## GD-S01500

### 对我来钓鱼的

`GD-S01500/subway/subway.cpp`，第 94–95 行（注释）。

```cpp
ccf CCF csp CSP 114514 514114 //freopen luogu Luogu kkksc03 chen_zhe 
对我来钓鱼的
```

## GD-S01563

### include<chatgptastra6>

`GD-S01563/hub/hub.cpp`，第 1–3 行。

```cpp
#include<>
#include<ostream>
#include<istream>
```

`GD-S01563/hub/hub.cpp`，第 18–32 行。

```cpp
#include<chatgptastra6>
#include<jqQt0220>
#include<Austm>
#include<Ken>
#include<Empty_Dream>
#include<bist//stdc+.h>
#define int unsigned short
#define long unsigned
#define long short
using namespace std;
friend inline const extern and or if for while unsigned long double float short class static delete signed return 
break continue template typename union bool char sizeof xor goto register constexpr operator [{(+-*&^%!/<>:;|~)}] 
int main(){
	fropen("r", "hub.in", stdin);
	fropen("w", "hub.out", stdout);
```

空的 `#include<>` 已足够使预处理失败；后面还有神秘头文件和一整串无法组成合法声明的关键字。本地 GNU++14 语法检查确认失败。

## GD-S01667

### freopen cpp

`GD-S01667/crystal/crystal.cpp`，第 7–10 行。

```cpp
int main(){
	freopen("crystal.cpp","r",stdin);
	freopen("crystal.cpp","w",stdout);
	cin>>n>>m;
```

## GD-S01751

### .pas 里面写 C++

`GD-S01751/crystal/crystal.pas`，第 1–9 行。

**.pas**

```cpp
#include<bits/stdc++.h>
using namespace std;
typedef long long ll;

int main() {
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","w",stdout);
    ios::sync_with_stdio(false);
    cin.tie(nullptr);
```

## GD-S01773

### 连续三年的大赏参赛宣言

`GD-S01773/hub/hub.cpp`，第 116–119 行（注释）。

```cpp
致2026迷惑行为大赏

主要成就:
连续三年当选GD抽象代码 
```

## GD-S01777

### freopen("r","migrate.in",stdin);

`GD-S01777/migrate/migrate.cpp`，第 25–28 行。

```cpp
int main(){
	freopen("r","migrate.in",stdin);
	freopen("w","migrate.out",stdout);
	cin>>c>>t;
```

程序试图打开名为 `r`、`w` 的文件，并把 `migrate.in / migrate.out` 当成打开模式。这不是正确的 `freopen` 参数顺序。

## GD-S01814

### 空调

`GD-S01814/hub/hub.cpp`，第 71–82 行（注释）。

```cpp
 还有0.5h
 要被冷到失去意识了
 监考老师也不会搞空调是什么意思啊
 遗憾离世
 ----
 监考老师发力了
 给空调调高温度了
 活过来了孩子们
 ----
 这个checker程序未免也太简陋了吧
 vscode神力
 bat文件直接用vscode改成猫娘口音了
```

## GD-S01834

### 孩子们，广搜到底能不能用

`GD-S01834/subway/subway.cpp`，第 353–361 行（注释）。

```cpp
15:10开始写T2 
哇，还有专门为我们做特殊数据准备的好东西 
	15:50 不好孩子们，这题东西有点多 
	16:00不好孩子们，这道题不能用广搜 
	16:05好的孩子们，好像可以广搜
	16:23 不好孩子们，数据都存不下
	16:36 孩子们，只能拿部分了 
	16:45 ok,理完思路，开始写 
	18:17 SSL0124在搏斗中倒下了
```

## GD-S01962

### 树不会做，先写行路难

`GD-S01962/hub/hub.cpp`，第 14–16 行（注释）。

```cpp
行路难 李白
金樽清酒斗十千，玉盘珍馐直万钱
停杯投箸不能食，拔剑四顾心茫然
```

## GD-S02215

### 大样例也被搬进注释

`GD-S02215/subway/subway.cpp`，第 18–19 行。

```cpp
//这是subway6.ans:
/*
```

`GD-S02215/subway/subway.cpp`，第 22–28 行。

```cpp
//这是subway6.in
/*
0 480 479521 20 90000
74 11 63 98 34 5 1 19 85 76 61 98 95 48 41 99 3 35 63 26 94 53 69 70 88 13 25 73 71 90  
略90507行(内存超限了)*/

//自己看到9十多万行的时候笑了没 （希望CCF能改，如果是BUG） 
```

## GD-S02465

### 不会

`GD-S02465/hub/hub.cpp`，第 5–6 行。

```cpp
//目测难度：T1:橙 T2:绿 T3:青 T4:不会
//目测算法： T1:贪心+前缀和+二分 T2:全源最短路 T3:dp+分讨 T4：不会
```

## GD-S02638

### 拼写挑战

`GD-S02638/crystal/crystal.cpp`，第 1–9 行。

```cpp
incdule <bits/stdc++.h>
using naamespace std;
const int N=5*le5+10;
int a[N];
int main(){
	froepen("crystal.in","r",stdin);
	froepen("crystal.out","w",studut);
	int n,m;
	int n[1000005];	
```

## GD-S02722

### 有新的注释方式加入哦！

`GD-S02722/crystal/crystal.cpp`，第 5–8 行。

```cpp
int main(){
	//freopen("crystal.in","r",stdin);\
	freopen("crystal.out","w",stdout);
	int n;
```

`GD-S02722/crystal/crystal.cpp`，第 26–28 行。

```cpp
	cout<<maxn;
	return 0;
}.
```

> 文件末尾有多余的句点。

## GD-S02756

### 只有文件读写

`GD-S02756/hub/hub.cpp`，第 1–2 行。

```cpp
freopen("hub.in","r",stdin);
freopen("hub.out","w",stdout);
```

这是 `hub.cpp` **全文**。

那很记得文件读写了。

## GD-S02784

### It's just an example.Remember to delete the // before freopen.

`GD-S02784/subway/subway.cpp`，第 11–13 行。

```cpp
	cout.tie(nullptr);
	//freopen("subway.in","r",stdin);
	//freopen("subway.out","w",stdout);
```

`GD-S02784/subway/subway.cpp`，第 32 行。

```cpp
	if(tesNo==0)cout<<'\n'<<"It's just an example.Remember to delete the // before freopen."<<'\n';
```

## GD-S02874

### Deepseek

`GD-S02874/subway/subway.cpp`，第 90 行（注释）。

```cpp
用户发来了一道题目，看上去是一道信息竞赛题。我需要先理解题意，然后给出题目的完整做法。B 市共有 m 个地铁站，编号为 1 到 m。每个地铁站都有一个站厅，地铁口与站厅
```

## GD-S03017

### 许愿四十二次

`GD-S03017/crystal/crystal.cpp`，第 31–33 行。

```cpp
//评测机请给我100pts
//评测机请给我100pts
//评测机请给我100pts
```

四份源码各有 42 行同样的许愿，共 168 次。

## GD-S03188

### 如果再来一次，还是会打开 C++

`GD-S03188/hub/hub.cpp`，第 45–48 行（注释）。

```cpp
但如果有再来一次的机会
我还是会在12岁的某一天打开c++

因为旅途本身就是意义
```

## GD-S03252

### 不要学这个啥子一直写废话

`GD-S03252/hub/hub.cpp`，第 47–51 行（注释）。

```cpp
我时间到底怎么分配到竟沦落到如此地步（划掉
哦原来是注释写太多了
精石后入：不要写太多注释和废话
当然如果真不会了可以打点暴力什么的
不要学这个啥子一直写废话
```

### 很期待到时候翻我代码的人发现我注释是代码长度的数倍的时候会有什么感想

`GD-S03252/migrate/migrate.cpp`，第 196–198 行（注释）。

```cpp
很期待到时候翻我代码的人发现我注释是代码长度的数倍的时候会有什么感想
会觉得我像Deepseek吗？或者是别的什么LLM？
感觉我好吵
```

## GD-S03295

### 中文输入法

`GD-S03295/migrate/migrate.cpp`，第 6–9 行。

```cpp
井include 《bits、stdc++。h>
uisng namesapce std;
int mian() {
	froepen("migrate.in", "r", stdin)， freopen("migrate.out", "w", stdout)
```

`GD-S03295/migrate/migrate.cpp`，第 11–13 行。

```cpp
	crystal, subway, migrate, hub
	retturn 0；
}
```

## GD-S03359

### 程序放在选手目录 & cystal

`GD-S03359/cystal.cpp`，第 1–4 行。

**GD-S03359/cystal.cpp**

```cpp
#include <bits/c++.h>
using namespace std;

int main(){
```

`GD-S03359/cystal.cpp`，第 16–17 行。

```cpp
	reture 0;
} 
```

## GD-S03473

### 请支持_____喵!!!

`GD-S03473/hub/hub.cpp`，第 61–70 行。

```cpp
//CCF
//love
//你 被 骗 了
//我要上GD迷惑行为大赏OvO
//my luogu ID:1241325，去看看我的游记呀 
//请支持飞行雪绒喵!!!
//请支持明日方舟喵!!!请支持阿米娅喵!!!
//请支持星尘infinity喵!!! 
//请支持超时空辉夜姬喵!!!
// AFO... 
```

## GD-S03595

### .cout

`GD-S03595/hub/hub.cpp`，第 7 行。

```cpp
	freopen("hub.cout","w",stdout);
```

`GD-S03595/migrate/migrate.cpp`，第 7 行。

```cpp
	freopen("migrate.cout","w",stdout);
```

`GD-S03595/subway/subway.cpp`，第 7 行。

```cpp
	freopen("subway.cout","w",stdout);
```

## GD-S03636

### 复制试卷

`GD-S03636/crystal/crystal.cpp`，第 39 行（注释）。

```cpp
2026 CCF 非专业级软件能力认证CSP-J/S 2026 第二轮提高组时间：2026 年 10 月 31 日 14:30 ∼ 18:30题目名称 能量水晶 地铁 迁徙 研发基地题目类型 传统型 传统型 传统型 传统型目录 crystal subway migrate hub可执行文件名 crystal subway migrate hub输入文件名 crystal.in subway.in …
```

原行较长，此处截取前 200 字符，省略号为后加。

## GD-S03759

### 究竟是哪种人会把排序前的前缀和拿去用然后检查一个小时才检查出来

`GD-S03759/crystal/crystal.cpp`，第 32 行（注释）。

```cpp
究竟是哪种人会把排序前的前缀和拿去用然后检查一个小时才检查出来，一开始就知道咋做结果15:37才做完 
```

## GD-S03760

### 迷惑行为大赏能帮我看看GD-J04204的代码有没有加reutrn 0吗 

`GD-S03760/crystal/crystal.cpp`，第 40–43 行（注释）。

```cpp
/*
估分：100+44+?+15 
我是GD-J04204，迷惑行为大赏能帮我看看GD-J04204的代码有没有加reutrn 0吗 
*/
```

只扫描了 S 的文件，没有看 J，不知道有没有（

## GD-S03763

### 打开模式进入 g 档

`GD-S03763/crystal/crystal.cpp`，第 4–5 行。

```cpp
	freopen("crystal.in","r",stdin);
	freopen("crystal.out","g",stdout);
```

四题的输出模式都写成了 `"g"`。

## GD-S04295

### 先打开输入，再用答案文件覆盖输入

`GD-S04295/hub/hub.cpp`，第 10–16 行。

```cpp
	//呜呜呜我是毛毛虫[80,100]+0+0+0=[80,100] 
	freopen("hub.in","r",stdin);
	freopen("hub.ans","r",stdin);
	srand(time(0));
	int t;
	cin>>t;
	while (t--) cout<<rand()<<'\n';
```

第二句又重定向了 `stdin`，文件名还是 `hub.ans`；随后按读到的次数输出随机数，没有打开 `hub.out`。

## GD-S04373

### 游戏名也能套命名空间

`GD-S04373/crystal/crystal.cpp`，第 49 行。

```cpp
//鸣朝神了 库洛::崩坏::星穹铁道nb
```

`库洛::崩坏::星穹铁道` 出现在注释里，所以不会真的去查找这些命名空间。

## GD-S04492

### std.in std.out

`GD-S04492/crystal/crystal.cpp`，第 5–7 行。

```cpp
int main(){
	freopen("crystal.in","r",std.in);
	freopen("crystal.out","w",std.out);
```

四题都写了 `std.in / std.out`。这不是标准流对象，也不是合法的命名空间成员访问写法；本地语法检查确认失败。

## GD-S04572

### feopen 与小时的都好

`GD-S04572/crystal/crystal.cpp`，第 8–11 行。

```cpp
	ios::sync_with_stdio(false);
	cin>>m>>n;
	freopen("crystal.in","r"stdin);
	feopen("crystal.in","w"stdout);
```

`"r"stdin` 中间缺逗号，下一句又写成 `feopen`，并继续把输出目标写成 `.in`。本地语法检查确认失败。

## GD-S04686

### 宿舍预言家也没躲过调试

`GD-S04686/subway/subway.cpp`，第 58–67 行（注释）。

```cpp
/*
14:54我的天，我在10.28的宿舍卧谈会出过这个题
14:55其实还是有点不同，难道我是预言家？ 
15:01好乱，让我注释一下 
15:21没啥思路呢，但好像换乘站数量不会很大？
15:26并非 
15:36先拿部分分吧
16:01好难调啊先看下一题吧
18:13又回来了，不想写了，这不仅模拟还算法，难难？！ 
*/
```

从“我三天前出过这个题”到“先拿部分分”，时间线非常完整。

## GD-S04796

### 模式写得很直观，但接口不认

`GD-S04796/crystal/crystal.cpp`，第 5–6 行。

```cpp
	freopen("crystal.in", "in", stdin);
	freopen("crystal.out", "out", stdout);
```

`crystal / migrate / subway` 使用 `"in" / "out"` 作为打开模式。`freopen` 的输入、输出模式应分别使用 `"r" / "w"`。

## GD-S04990

### 最后用一首小诗收场

`GD-S04990/hub/hub.cpp`，第 12–22 行（注释）。

```cpp
/*
常忆年少时，意气风发，
谈笑写出唯一解。
却轻易别离，三载时光，
退役满是憾与茫。

今有幸，复回赛场，
不复当年。
终曲散，夜时回想，
人在何方？ 
*/
```

D 题程序之后是一段告别式诗文，作为这份摘录的结尾。

## 参考

编排参考了 [HA CSP 迷惑行为大赏](https://www.luogu.com.cn/article/bsf69p78)、[ZJ NOIP 2024 迷惑行为大赏](https://www.luogu.com.cn/article/3vbhuccy) 和 [NOIP 2024 NM 迷惑行为大赏](https://www.luogu.com.cn/article/p58zmqm0) 的“编号、源码、短评”形式；本篇案例均取自本地文件，没有把往年案例混入今年。

题目及文件名核对：[A 能量水晶](https://www.luogu.com.cn/problem/P17831)、[B 地铁](https://www.luogu.com.cn/problem/P17832)、[C 迁徙](https://www.luogu.com.cn/problem/P17833)、[D 研发基地](https://www.luogu.com.cn/problem/P17834)。
