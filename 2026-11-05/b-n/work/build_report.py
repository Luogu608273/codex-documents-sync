from pathlib import Path
import json,re,collections
W=Path(__file__).parent;OUT=W.parent/'outputs'
D=json.loads((W/'scan.json').read_text(encoding='utf-8'));M={d['path']:d for d in D}
C=json.loads((W/'comments.json').read_text(encoding='utf-8'))
I=json.loads((W/'io_audit.json').read_text(encoding='utf-8'));IM={r['path']:r for r in I}
F=json.loads((W/'floyd_verified.json').read_text(encoding='utf-8'))
E=[]
def frag(path,a,b):
 ls=M[path]['text'].splitlines();assert 1<=a<=b<=len(ls),(path,a,b,len(ls))
 return {'path':path,'start':a,'end':b,'code':'\n'.join(ls[a-1:b])}
def piece(path,begin,end=None):
 s=M[path]['text'];a=s.index(begin);b=s.index(end,a)+len(end) if end else a+len(begin)
 return frag(path,s.count('\n',0,a)+1,s.count('\n',0,b)+1)
def add(title,note,*frags):
 ids={f['path'].split('/')[0] for f in frags};assert len(ids)==1
 E.append({'id':next(iter(ids)),'title':title,'note':note,'frags':frags})
def com(i,title,note,begin=None,end=None):
 c=C[i];p=c['path']
 if begin:f=piece(p,begin,end)
 else:f=frag(p,c['line'],c['line']+c['text'].count('\n'))
 add(title,note,f)

com(0,'让我想想','把思考过程实时写进注释：刚觉得摸到了正解，下一刻就被小样例送回起点。','我是不是无意间想到正解了','让我想想这该怎么做')
add('解压密码也能玩梗','注释开始研究密码：八进制的 31 等于十进制的 25，Oct / Dec 又恰好能让人想到十月和十二月。',frag('GD-S00150/crystal/crystal.cpp',7,8))
com(15,'d 的作用逐渐增大','从“d 到底是啥”到发现它有用，读题过程直接连载在源码末尾。','d 到底是啥','等一下，发现 d 的作用好像超过了滚木')
add('大样例通过方法：打开答案','先判断样例参数，再尝试从 `subway3.ans` 读取并输出答案；这是对样例文件的依赖，不是求解过程。',frag('GD-S00179/subway/subway.cpp',11,20))
add('研发基地改上语文课','`hub.cpp` 的块注释里默写《过秦论》，最后以“默不完了”收尾。',piece('GD-S00192/hub/hub.cpp','过秦论','君臣固守以窥周室'),piece('GD-S00192/hub/hub.cpp','默不完了'))
add('文件名前后缀交换位置','把文件名写成 `in.crystal / out.crystal`，前后缀交换了位置。',piece('GD-S00378/crystal/crystal.cpp','freopen("in.crystal"','freopen("out.crystal"'))
add('能拖一会儿是一会儿','循环只管增加 `b`，没有求解或输出。注释把写法解释得明明白白。',frag('GD-S00428/hub/hub.cpp',6,10))
add('freopen 诈骗现场','两条被注释的重定向旁边，各有一条正确且未被注释的重定向。这里文件读写没有因为 `//freopen` 而缺失，不能算进“忘取消注释”。',frag('GD-S00727/subway/subway.cpp',18,22))
add('自行发明文件函数','`freout`、`freclose` 不是这里可用的标准文件函数；模式写成 `"D"`，第三参数直接填 `subway`。本地语法检查还首先遇到了前一行缺分号。',frag('GD-S00846/subway/subway.cpp',3,16))
com(68,'提醒自己别忘文件读写，提醒里先拼错','最后写的是 `freoepn`。这段在注释里，所以只算整活，不把它当成实际编译错误。','//freopen//freopen//freopen//freopen//freopen,remember to write freoepn')
add('把比较器交成了第四题','`hub.cpp` 实际上在比较 B 题输出和大样例答案，最后打印 `AC! / WA!`。两个读取路径都固定到了考场的 D 盘。',frag('GD-S00908/hub/hub.cpp',3,12))
com(73,'不是我的正解错了，是我的二分错了','同一段调试记录经历了两次翻案。注释里的“不能用 signed main”也是选手自己的误解：`signed main()` 合法。','ok，我的正解炸了','拍了1000组没问题，应该过了')
com(77,'本来想写 feropen，后来忍住了','此处的 `feropen` 只出现在整活计划里，不能算 CE。','本来想写个feropen','CSP迷惑行为大赏(还是叫其他什么的)')
com(79,'复杂度自己又升了一次','刚宣布推完 `n^3`，检查状态后又发现要记录已选点数，于是变成了自己所说的 `n^4`。这是注释中的自述。','n^3 推完了','这是 n^4')
com(80,'做题力竭之后开始排游戏日程','T3 的注释先安排了音游和方舟行程，后面还接了长篇内容；这里只摘游戏日程。','n^2 写了一个半小时','提醒我了，我还要给他们开白皇帝')
com(84,'T4 看不懂，写个 LCA 庆祝','前面还在和输入 RE 搏斗，到了第四题，LCA 已经承担起了庆祝功能。','5：02 DEV-C++神力','6：06 T4RE我也不管了好吧，摸鱼ING...')
com(99,'地铁站里藏了一位空洞骑士','B 题末尾的注释变成了游戏台词，并向翻代码的人询问“真的会有人看到吗”。','你是容器','去年我就写了这些，真的会有人看到吗？')
com(109,'从 freopen 讲到不要在岩浆里游泳','考后建议从程序检查一路扩展到了饮食、声乐和校园生活。','一定要记得开long long','不要在没有把握的情况下把校规视为每日任务。')
com(125,'搜索关键词投喂大赏','把常见检索词写成一串，后面直接承认“对我来钓鱼的”。','ccf CCF csp CSP','对我来钓鱼的')
add('头文件请来了 ChatGPT，关键字开起了会','空的 `#include<>` 已足够使预处理失败；后面还有神秘头文件和一整串无法组成合法声明的关键字。本地 GNU++14 语法检查确认失败。',frag('GD-S01563/hub/hub.cpp',1,3),frag('GD-S01563/hub/hub.cpp',18,32))
add('四题都对自己的源码动手','四份代码都把输入、输出指向同名 `.cpp`。若当前目录有可写的该源码文件，第二句以 `w` 打开会将它截断。这里只检查源码，没有运行这些程序。',frag('GD-S01667/crystal/crystal.cpp',7,10))
add('扩展名是 Pascal，里面是 C++','该选手四份源文件都是 `.pas`，内容却是 C++。按扩展名选择语言或按题目指定文件名收取时都会出问题；不把这等同于 C++ 代码本身语法错误。',frag('GD-S01751/crystal/crystal.pas',1,9))
com(133,'连续三年的大赏参赛宣言','选手自报“连续三年当选”，并向今年的大赏投来参赛宣言。','致2026迷惑行为大赏','连续三年当选GD抽象代码')
add('文件名和模式互换岗位','程序试图打开名为 `r`、`w` 的文件，并把 `migrate.in / migrate.out` 当成打开模式。这不是正确的 `freopen` 参数顺序。',frag('GD-S01777/migrate/migrate.cpp',25,28))
com(136,'空调才是第五题','注释连载了“太冷—老师调空调—活过来了”的全过程，后面还记下把检查脚本改成猫娘口音。','还有0.5h','bat文件直接用vscode改成猫娘口音了')
com(141,'孩子们，广搜到底能不能用','一连串时间戳记录了从广搜自信到数据存不下的过程。','15:10开始写T2','18:17 SSL0124在搏斗中倒下了')
com(150,'树不会做，先写行路难','D 题注释里出现了李白《行路难》。只摘标题和开头。','行路难 李白','停杯投箸不能食，拔剑四顾心茫然')
add('大样例也被搬进注释','B 题末尾标出 `subway6.ans` 和 `subway6.in`，又写下“略90507行”。这里只展示可确认的文字，不复制那段很长的乱码状内容，也不将其归因于选手编码错误。',frag('GD-S02215/subway/subway.cpp',18,19),frag('GD-S02215/subway/subway.cpp',22,28))
add('算法栏和难度栏一起投降','前三题还能写算法和颜色，第四题两栏都直接填“不会”。',frag('GD-S02465/hub/hub.cpp',5,6))
add('第一行就开始拼写挑战','`incdule` 少了 `#` 且拼错，`naamespace` 多了字母，`1e5` 写成 `le5`，后面还有 `froepen / studut`。本地语法检查确认失败。',frag('GD-S02638/crystal/crystal.cpp',1,9))
add('没注释的下一行，也可能被注释掉','第一行末尾的反斜杠触发行拼接，所以第二行也落进了 `//` 注释。看起来有一条没加 `//` 的输出重定向，预处理后却同样消失；此外文件末尾还有多余的句点。',frag('GD-S02722/crystal/crystal.cpp',5,8),frag('GD-S02722/crystal/crystal.cpp',26,28))
add('只记得文件读写，忘了整个程序','这是 `hub.cpp` 全文。没有头文件和 `main`，只留下两条不能这样放在全局作用域的函数调用。本地语法检查确认失败。',frag('GD-S02756/hub/hub.cpp',1,2))
add('程序提醒删掉斜杠，但源码没删','样例分支会打印“记得删掉 freopen 前面的 //”，而源文件里两条重定向确实仍被注释。',frag('GD-S02784/subway/subway.cpp',11,13),piece('GD-S02784/subway/subway.cpp','if(tesNo==0)'))
com(218,'注释里开始模拟模型思考','把模型思考过程的口吻搬进考场，连题意复述都安排上了。','用户发来了一道题目','地铁口与站厅')
add('四题各许愿四十二次','四份源码各有 42 行同样的许愿，共 168 次。这里展示三行；重复内容不展开。',frag('GD-S03017/crystal/crystal.cpp',31,33))
com(407,'如果再来一次，还是会打开 C++','这一条留给考场里的回忆：一段写在 `hub.cpp` 里的告别。','但如果有再来一次的机会','因为旅途本身就是意义')
com(414,'反省注释太多的方式是再写一段注释','从“时间怎么没了”查到了“注释写太多了”，随后继续在注释里反省。','我时间到底怎么分配到竟沦落到如此地步','不要学这个啥子一直写废话')
com(422,'提前预告翻代码人的感想','选手已经设想好了别人发现注释长度远超代码时的反应。','很期待到时候翻我代码的人','感觉我好吵')
add('中文输入法接管 C++','`井include`、书名号、顿号、中文句号，加上 `uisng namesapce / mian / retturn`。本地语法检查确认失败；包含私人信息的变量行未收录。',frag('GD-S03295/migrate/migrate.cpp',6,9),frag('GD-S03295/migrate/migrate.cpp',11,13))
add('程序放在选手目录，crystal 还少了一个 r','四份源文件直接位于选手目录，未分入四题子目录，第一题文件名是 `cystal.cpp`；该文件还使用不存在的 `bits/c++.h` 并写了 `reture`。',frag('GD-S03359/cystal.cpp',1,4),frag('GD-S03359/cystal.cpp',16,17))
add('从 CCF 转场到阿米娅','一开始是 `CCF / love`，接着“你被骗了”，最后变成了游戏和角色推荐。',frag('GD-S03473/hub/hub.cpp',61,70))
add('输出文件的后缀叫 cout','`hub / migrate / subway` 都使用了 `.cout` 后缀。`cout` 是输出流的名字，不是题目要求的文件扩展名。',piece('GD-S03595/hub/hub.cpp','freopen("hub.cout"'),piece('GD-S03595/migrate/migrate.cpp','freopen("migrate.cout"'),piece('GD-S03595/subway/subway.cpp','freopen("subway.cout"'))
exam_fragment=piece('GD-S03636/crystal/crystal.cpp','2026 CCF')
exam_fragment['code']=exam_fragment['code'][:200]+'…'
exam_fragment['editorial']='原行较长，此处截取前 200 字符，省略号由整理者添加。'
add('把整份试卷复制四遍','四题末尾都有同一段约 1 万字符的块注释，包含试卷抬头、四题题面和数据说明。这里只摘其中一份的开头，原文是一条长行。',exam_fragment)
com(477,'前缀和比排序先到了一步','选手自述：一直在使用排序前的前缀和，检查一小时才发现。这里不据此判定最终提交仍有同样错误。','究竟是哪种人会把排序前的前缀和拿去用','15:37才做完')
com(478,'大赏兼职失物招领','四题都留了同一句请求，让大赏帮忙检查上午 J 组有没有写 `return 0`，留言本身写成了 `reutrn 0`。顺带说，C++ 的 `main` 正常执行到末尾会隐式返回 0。')
add('打开模式进入 g 档','四题的输出模式都写成了 `"g"`，不是标准的写入模式 `"w"`。这类错误不一定引起 CE，而是在打开文件时出问题。',frag('GD-S03763/crystal/crystal.cpp',4,5))
add('先打开输入，再用答案文件覆盖输入','第二句又重定向了 `stdin`，文件名还是 `hub.ans`；随后按读到的次数输出随机数，没有打开 `hub.out`。',frag('GD-S04295/hub/hub.cpp',10,16))
add('游戏名也能套命名空间','`库洛::崩坏::星穹铁道` 出现在注释里，所以不会真的去查找这些命名空间。',frag('GD-S04373/crystal/crystal.cpp',49,49))
add('stdin 被拆成 std.in','四题都写了 `std.in / std.out`。这不是标准流对象，也不是合法的命名空间成员访问写法；本地语法检查确认失败。',frag('GD-S04492/crystal/crystal.cpp',5,7))
add('文件函数和逗号一起消失','`"r"stdin` 中间缺逗号，下一句又写成 `feopen`，并继续把输出目标写成 `.in`。本地语法检查确认失败。',frag('GD-S04572/crystal/crystal.cpp',8,11))
com(544,'宿舍预言家也没躲过调试','从“我三天前出过这个题”到“先拿部分分”，时间线非常完整。')
add('模式写得很直观，但接口不认','`crystal / migrate / subway` 使用 `"in" / "out"` 作为打开模式。`freopen` 的输入、输出模式应分别使用 `"r" / "w"`。',frag('GD-S04796/crystal/crystal.cpp',5,6))
com(556,'最后用一首小诗收场','D 题程序之后是一段告别式诗文，作为这份摘录的结尾。')

E.sort(key=lambda e:(e['id'],e['frags'][0]['path'],e['frags'][0]['start']))
main=['# GD CSP-S 2026 迷惑行为大赏','',
'按选手编号升序整理。正文只放较有特点的代码和注释；重复出现的文件读写、Floyd 循环顺序等，统一见 [重复现象统计与选手名单](重复现象统计与选手名单.md)。','',
f'材料来自本地 `answers`：5,068 个选手目录、18,220 份源文件。本篇收录 **{len(set(e["id"] for e in E))} 位选手、{len(E)} 个特色条目**。源码按 UTF-8 或兼容 GB2312／GBK 的编码分别读取，本文统一为 UTF-8。','',
'代码保留原拼写与内容；长注释只摘相关片段。行号按统一 CRLF／LF 后的文本计数，路径相对于 `C:/Users/605/Downloads/answers/`。注释里的估分、AC、退役或往年入选经历均为选手自述。编译结论仅指本地 GNU++14 检查，不代表官方成绩。','']
last=None
for e in E:
 if e['id']!=last:main+=['## '+e['id'],''];last=e['id']
 main+=['### '+e['title'],'']
 for f in e['frags']:
  loc=str(f['start']) if f['start']==f['end'] else f"{f['start']}–{f['end']}"
  inside=any(c['line']<=f['start'] and c['line']+c['text'].count('\n')>=f['end'] and c['text'].startswith('/*') for c in M[f['path']]['comments'])
  label='（块注释节选）' if inside else ''
  main+=[f"`{f['path']}`，第 {loc} 行{label}。",'','```cpp',f['code'],'```','']
  if f.get('editorial'):main+=[f['editorial'],'']
 main+=[e['note'],'']
main+=['## 参考','',
'编排参考了 [HA CSP 迷惑行为大赏](https://www.luogu.com.cn/article/bsf69p78)、[ZJ NOIP 2024 迷惑行为大赏](https://www.luogu.com.cn/article/3vbhuccy) 和 [NOIP 2024 NM 迷惑行为大赏](https://www.luogu.com.cn/article/p58zmqm0) 的“编号、源码、短评”形式；本篇案例均取自本地文件，没有把往年案例混入今年。','',
'题目及文件名核对：[A 能量水晶](https://www.luogu.com.cn/problem/P17831)、[B 地铁](https://www.luogu.com.cn/problem/P17832)、[C 迁徙](https://www.luogu.com.cn/problem/P17833)、[D 研发基地](https://www.luogu.com.cn/problem/P17834)。','']
(OUT/'GD-CSP-S-2026迷惑行为大赏.md').write_text('\n'.join(main),encoding='utf-8')
(W/'selected.json').write_text(json.dumps(E,ensure_ascii=False,indent=2),encoding='utf-8')
print('main',len(E),len(set(e['id'] for e in E)))
