import json,re,collections,sys
from pathlib import Path
import io_audit as A
sys.stdout.reconfigure(encoding='utf-8')
W=Path(__file__).parent;OUT=W.parent/'outputs'
D=A.D;M={d['path']:d for d in D};I=json.loads((W/'io_audit.json').read_text(encoding='utf-8'));F=json.loads((W/'floyd_verified.json').read_text(encoding='utf-8'))
TY=re.compile(r'\b(?:fropen|freeopen|froepen|freopne|frepoen|feropen|freoper|frozpen|feopen|freout|freclose)\s*\(')
G=collections.defaultdict(dict)
def put(g,p,note=''):
 if p not in G[g]:G[g][p]=[]
 if note and note not in G[g][p]:G[g][p].append(note)
macro_good={'GD-S01445/hub/hub.cpp','GD-S01615/crystal/crystal.cpp','GD-S01615/hub/hub.cpp','GD-S01615/migrate/migrate.cpp','GD-S01615/subway/subway.cpp','GD-S02689/migrate/migrate.cpp','GD-S02689/subway/subway.cpp','GD-S03836/migrate/migrate.cpp'}
special={
 'GD-S00691/subway/subway.cpp':'while(true) 反复松弛，直到没有更新；不能判成单轮顺序错误',
 'GD-S01235/subway/subway.cpp':'先做一轮，再额外做 m 轮；增加了迭代，不能套用单轮结论',
 'GD-S02196/subway/subway.cpp':'两段相同顺序的松弛连续执行',
 'GD-S02335/subway/subway.cpp':'外层 u=1..2，重复两轮并使用 l/die 两张表',
 'GD-S02918/subway/subway.cpp':'外层 t=1..m，完整松弛重复 m 轮；四层循环',
}
for r in I:
 p=r['path'];d=M[p];active,_,_=A.preprocess(A.strip(d['text']));code=A.strip(active,True)
 hascomment=any(re.search(r'\bfreopen\s*\(',c['text']) for c in d['comments'])
 typo=TY.search(code)
 if r['empty']:put('空文件',p)
 elif not r['hasio']:
  if typo:put('只写了拼错的文件函数',p,','.join(sorted(set(m[0].split('(')[0].strip() for m in TY.finditer(code)))))
  elif hascomment:put('文件读写只留在注释中',p)
  else:put('完全未见文件打开代码',p)
 if r['commented']:
  if r['literal_good_pair'] or p in macro_good:put('排除：注释旁保留正确读写',p,'宏封装／字符串拼接' if p in macro_good else '保留对应题目的输入、输出')
  elif r['hasio']:put('有注释且另有读写，需看实际调用',p)
 calls=r['calls']
 # All entries in this list are outside comments and inside the default active preprocessor branch.
 for c in calls:
  if c['fn']!='freopen':continue
  n,m,s=c['name'],c['mode'],c['stream'];line=c['line']
  desc=f'L{line}: {json.dumps(n,ensure_ascii=False)} / {json.dumps(m)} / {s}'
  if (s=='stdin' and m=='w') or (s=='stdout' and m=='r'):put('r 与 w 用反',p,desc)
  if n.endswith('.out') and s=='stdin':put('输出文件接到了 stdin',p,desc)
  if s in ['"stdin"','"stdout"']:put('把 stdin 或 stdout 写成字符串',p,desc)
  if m=='W':put('大写 W 打开模式',p,desc)
  if n.endswith('.ans') and m=='w' and s=='stdout':put('输出写到了 ans 文件',p,desc)
  task=p.split('/')[-2]
  if task in ['crystal','subway','migrate','hub'] and n not in [task+'.in',task+'.out','./'+task+'.in','./'+task+'.out']:
   put('字面文件名不符合本题约定',p,desc)
 # Only count the simple, fully parsed freopen-only form here, avoiding alternate APIs or macros.
 syms=set(re.findall(r'\b\w+\b',code))
 direct=len(re.findall(r'\bfreopen\s*\(',active))
 fre=[c for c in calls if c['fn']=='freopen']
 alternative=bool(re.search(r'\b(?:fopen|freopen_s|freopen64|ifstream|ofstream|fstream|open|open64|dup2)\b',code))
 if direct==len(fre) and fre and not alternative:
  streams={c['stream'] for c in fre}
  if streams=={'stdin'}:put('仅见输入重定向',p,'；'.join(f"L{c['line']} {c['name']}" for c in fre))
  if streams=={'stdout'}:put('仅见输出重定向',p,'；'.join(f"L{c['line']} {c['name']}" for c in fre))
 if typo:put('文件函数拼写变体',p,','.join(sorted(set(m[0].split('(')[0].strip() for m in TY.finditer(code)))))
for f in F:
 p=f['path'];order=f['order']
 if p in special:put('Floyd 多轮写法单列',p,f"{order}, L{f['line']}: {special[p]}")
 else:put('Floyd '+order,p,f"L{f['line']}")
R=json.loads((W/'final_compilation.json').read_text(encoding='utf-8')) if (W/'final_compilation.json').exists() else []
for r in R:
 if r['returncode'] in [0,None]:continue
 p=r['path'];diag=r['diagnostics']
 if "'::main' must return 'int'" in diag:put('int 宏影响 main 返回类型',p)
 # Exclude the valid bits/extc++.h family and its platform-specific iconv failure.
 if 'fatal error:' in diag and 'iconv.h' not in diag:
  match=re.search(r'fatal error: ([^\n]+)',diag)
  if match:put('头文件路径错误',p,match[1].replace('C:/TDM-GCC-64/lib/gcc/x86_64-w64-mingw32/10.3.0/include/c++/',''))

order=['完全未见文件打开代码','文件读写只留在注释中','只写了拼错的文件函数','空文件','仅见输入重定向','仅见输出重定向','Floyd ijk','Floyd ikj','Floyd 多轮写法单列','r 与 w 用反','输出文件接到了 stdin','把 stdin 或 stdout 写成字符串','大写 W 打开模式','输出写到了 ans 文件','字面文件名不符合本题约定','文件函数拼写变体','头文件路径错误','int 宏影响 main 返回类型','排除：注释旁保留正确读写','有注释且另有读写，需看实际调用']
def count(g):return len({p.split('/')[0] for p in G[g]}),len(G[g])
notes={
'完全未见文件打开代码':'非空源码中未识别到文件打开操作，也没有被注释的 freopen 调用或本次识别到的文件函数拼写变体。这里的“完全未见”是静态源码结论，不含空文件。',
'文件读写只留在注释中':'源码有被注释的 freopen 调用，但默认预处理分支中未发现其它文件打开操作。包含行注释与块注释；不把保留正确读写的“诈骗”代码列入这里。',
'只写了拼错的文件函数':'没有识别到正确文件 I/O 入口，但写了 fropen、feropen 等拼写变体。单列，避免说成选手根本没尝试文件读写。',
'空文件':'文件为空或只含空白。与非空但没有文件读写的代码分开统计。',
'仅见输入重定向':'仅对已完整识别、未发现其它文件 API 的直接 freopen 写法统计：所有调用都接 stdin，未见输出文件打开。可能与其它类别交叉。',
'仅见输出重定向':'与上一类相同口径：所有直接 freopen 调用都接 stdout，未见输入文件打开。',
'Floyd ijk':'转移中 k 为中转点，嵌套顺序为 i→j→k；不是只搜三个变量名。以一次这样的扫描替代普通 Floyd，一般不能保证最短路正确。下列按源文件去重，多轮结构另列。',
'Floyd ikj':'转移中 k 为中转点，嵌套顺序为 i→k→j。与上一类同样按源文件去重；没有把“用 i 作为中转点的正确写法”误算进来。',
'Floyd 多轮写法单列':'这些源码也出现了 ijk/ikj，但额外重复松弛。尤其“直到不再更新”的版本不能仅凭循环顺序判错；重复 n 轮的版本要另看时间复杂度。因此不混入上面单轮结构的名单，也不作统一 WA 结论。',
'r 与 w 用反':'这里只统计 stdin 配 w，或 stdout 配 r 的直接调用。输入以 w 打开存在截断文件的问题；输出以 r 打开不能按预期写入。',
'输出文件接到了 stdin':'字面文件名以 .out 结尾，第三参数却是 stdin。与上一类可重叠。',
'把 stdin 或 stdout 写成字符串':'第三参数出现 "stdin" 或 "stdout"，而 freopen 需要 FILE*。这是类型错误，不是文件名错误。',
'大写 W 打开模式':'写成 "W"。标准写入模式使用小写 "w"。',
'输出写到了 ans 文件':'stdout 以写模式指向 .ans；本场要求的是 .out。',
'字面文件名不符合本题约定':'列出默认有效分支中的非题目指定字面文件名，包括拼写错误、残留大样例名、其它题名和特殊整活。含样例分支或测试辅助代码，不等于每项都会在所有输入下执行。已排除禁用的 LOCAL/IO 调试分支。',
'文件函数拼写变体':'仅列注释之外识别到的拼写变体；正文里“本来想写 feropen”的注释不算。完整编译可能先在更早的错误处停止。',
'头文件路径错误':'本地 GNU++14 预处理／语法检查中确认的头文件路径错误。没有把有效的 bits/extc++.h 在 Windows 上缺 iconv.h 的环境问题算作选手错误。',
'int 宏影响 main 返回类型':'仅列本地诊断明确为 main 必须返回 int 的文件；不把带 #undef int、signed main 等正常写法列入。',
'排除：注释旁保留正确读写':'这是排除名单，不是错误名单。源码中虽出现 //freopen，仍保留本题正确的输入与输出，或通过核对过的宏／字符串拼接完成读写。正常调试注释与刻意“诈骗”都可能在此，不能统称故意整活。',
'有注释且另有读写，需看实际调用':'这里既有 //freopen，又保留了其它文件读写，但不满足“本题正确的一整对读写”的排除条件。通常为只开一侧、读大样例或复制了其它题的文件名；详情看同一选手在其它表中的记录。'
}
out=['# 重复现象统计与选手名单','',
'对应 [特色案例正文](GD-CSP-S-2026迷惑行为大赏.md)。下列重复现象只统计并列名单，不重复贴源码。各表内均按选手编号升序，同一选手的文件合并到一行。','',
'范围为本地 5,068 个选手目录内的 18,220 份源文件。表中“人数”按编号去重，“文件数”按相对路径去重；类别可能交叉，不能直接相加作为总人数。空文件单列。静态检索覆盖全目录，编译复核仅覆盖疑似语法错误候选，不是全目录官方评测。','',
'文件 I/O 筛查剔除了注释和字符串文字，处理默认条件编译分支，识别 freopen、fopen、文件流及常见宏封装，并对 //freopen 同文件中的替代写法做了复核。注释与有效调用并存时不直接判为漏文件读写。','',
'Floyd 只统计中转点确为 k 的字面 i/j/k 三层循环；未把所有变量重命名、宏循环都强行算入。因此计数表示本次确认的源码结构，不是全体选手错误总数。','',
'## 汇总','', '| 现象 | 人数 | 文件数 |','| --- | ---: | ---: |']
for g in order:
 a,b=count(g);out.append(f'| {g} | {a} | {b} |')
out+=['',f'直接出现行注释形式 `//freopen(...)` 的文件共 **{sum(r["commented"] for r in I)}** 份。这个原始命中数不是错误数：其中 **{count("排除：注释旁保留正确读写")[1]}** 份已确认保留正确读写并排除，其他情况按表分开。','',
'文件位置统一相对于 `C:/Users/605/Downloads/answers/选手编号/`。`L数字` 为统一换行后的源码行号。表格中的参数顺序为“文件名 / 模式 / 第三参数”。','']
for g in order:
 a,b=count(g);out+=['## '+g,'',f'**{a} 人，{b} 份文件。** '+notes[g],'','| 选手编号 | 文件与定位 |','| --- | --- |']
 byid=collections.defaultdict(list)
 for p,info in sorted(G[g].items()):
  sid,rel=p.split('/',1);detail='；'.join(info)
  val=f'`{rel}`'+('：'+detail if detail else '')
  byid[sid].append(val.replace('|','\\|').replace('\n',' '))
 for sid,vals in sorted(byid.items()):out.append(f'| {sid} | '+ '<br>'.join(vals)+' |')
 out.append('')
out+=['## 核验说明','',
f'按 UTF-8 优先、GB18030 兼容 GB2312／GBK 的方式解码。3 份文件仍含不能完整解码的字节，未把其乱码作为特色内容；ASCII 范围的代码筛查不依赖乱码解释。原文件未修改。','',
'编译器为本地 TDM-GCC 10.3.0，GNU++14 语法检查；正文称“确认失败”的文件均有对应诊断。编译器环境差异项另行剔除。没有执行选手程序，也没有使用官方测试数据推断得分。','',
'输入输出文件名依据：[crystal](https://www.luogu.com.cn/problem/P17831)、[subway](https://www.luogu.com.cn/problem/P17832)、[migrate](https://www.luogu.com.cn/problem/P17833)、[hub](https://www.luogu.com.cn/problem/P17834)。','']
(OUT/'重复现象统计与选手名单.md').write_text('\n'.join(out),encoding='utf-8')
(W/'stats.json').write_text(json.dumps({g:{'players':count(g)[0],'files':count(g)[1],'records':G[g]} for g in order},ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({g:count(g) for g in order},ensure_ascii=False,indent=2))
