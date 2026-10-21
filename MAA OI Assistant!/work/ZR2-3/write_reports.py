from pathlib import Path
import json,hashlib,time
from validate import ROOT,run
out=Path('outputs/ZR2-3')
data='3\n4\n3 2 3\n3 4 5\n3 6 7\n3 -1 -1\n3\n1 10 100\n2 1 100000\n3 10000 1000\n1\n2 -1234567 7654321\n'
ans='2\n6\n12\n19\n100\n101\n100101\n-1234567'
run('brackets','partial',data,ans)
run('brackets','partial',data,ans,file=True)
t=time.perf_counter()
run('brackets','partial','1\n2000\n'+'3 10000000 10000000\n'*2000,'\n'.join(str(i*10**7) for i in range(1,2001)))
partial_time=round(time.perf_counter()-t,3)
common='''# 本地验证记录

验证日期：2026-10-21。随机种子：20261021。

## 环境和证据范围

- 编译器：`C:/TDM-GCC-64/bin/g++.exe`，C++17。
- 参数：`-std=c++17 -O2 -Wall -Wextra`；标准程序、部分分程序均分别编译默认文件输入输出版和 `-DLOCAL` 标准输入输出版，无编译警告。
- 完整题面样例同时检查两种输入输出方式。部分分只在注明的支持范围内验证。
- 下列时间是本机运行耗时，包含进程启动和输入输出，不是评测机耗时，也不构成官方 AC 或正式得分。
- 正确性证明见 `solution.md`，不以对拍通过替代证明。

'''
details={
'color':'''## 已完成检查

- PDF 的三组样例，输出分别为 3、2、3；两份程序及两种输入输出方式均通过。
- 984 组独立检查：包含长度 1~3 的全部 584 个八字符颜色串，以及 400 个长度不超过 8 的随机串。
- 参照程序对每种原色枚举全部合法笔划区间，用位置位集做最小覆盖 DP；标准、部分分输出全部一致。
- 标准程序：T=20，每组 N=100000、全部为 A，每组答案 3，合计约 0.015 秒。
- 部分分：T=20，每组 N=1000、全部为 A，覆盖其二次 DP 的最长连续段情况，每组答案 3，合计约 0.021 秒。

部分分支持 N<=1000；按题面覆盖 30%，未声称获得正式 30 分。
''',
'greedy':'''## 已完成检查

- PDF 的三组样例输出 21、11、220，标准程序和部分分均一致；默认文件输入输出也已检查。
- 240 组 N<=8 的随机输入，与独立枚举全部排列、直接模拟购买的暴力一致；两份程序均通过。
- 40 组 N=9~150、A=B 的随机输入，与独立 0/1 背包一致；两份程序均通过。
- 标准程序：N=A=B=150，所有商品价格 1，Ui=Vi=10^9，答案 300000000000，约 0.202 秒。
- 标准程序：N=150、A=149、B=150，价格随机取 1~10、价值取 1~10^9 的密集状态输入，约 0.208 秒。该项仅验证运行与耗时，没有独立最优值，未算作正确性对拍。

## 原比赛公开数据本地核对

从 [JAG 官方数据归档](https://jag-icpc.org/files/summer-camp-2026-day2-data.zip) 的 C.zip 读取 63 组输入。原题与用户 PDF 的范围不同，只运行其中符合 N、A、B、Ci<=150 的 22 组，全部与配套答案一致。

其余 41 组超出当前 PDF 的约束，未运行，未声称通过原比赛完整数据集。具体通过名单：

```text
00-sample-001 ~ 003
01-hand-small-001 ~ 010
02-boundary-001 ~ 003
03-random-small-001 ~ 006
```

部分分支持 N<=8 或 A=B，按题面覆盖 35%，未声称正式得分。
''',
'brackets':f'''## 已完成检查

- PDF 的完整样例，8 行输出全部吻合。最终两份程序的默认文件输入输出与标准输入输出均已检查。
- 标准程序：1000 组混合插入测试，共 37989 次询问，与独立括号余额 DP 的最优值完全一致。
- 最终部分分程序：其中后 500 组，共 24910 次询问，同样与余额 DP 一致；包含随机负权、三种插入类型和接近 10^7 的权值。
- 标准程序：Q=400000，全部右端插入、所有权值 10^7，第 i 次答案 i*10^7，约 0.345 秒。
- 标准程序：Q=400000，随机混合三类插入、所有权值 -10^7，第 i 次答案 -i*10^7，约 0.395 秒。覆盖相等权值、结构交换和负答案。
- 部分分：Q=2000 的全正相同权值输入，逐项核对答案，约 {partial_time} 秒；另检查两端各加一个的 Q=2000 输入。

参照 DP 状态为“扫描到当前位置、未匹配左括号数量”的最大得分：选左括号余额加一并增加权值，选右括号要求余额大于零。最终取余额为零，未使用堆贪心作为参照。

部分分支持 sum Q<=2000，按题面覆盖 40%，未声称正式得分。
''',
'noise':'''## 已完成检查

- PDF 的第一组完整样例答案 4，标准程序和部分分、默认文件输入输出和标准输入输出均通过。
- PDF 第二组样例标为 N=20，但页面横向裁切后只保留前 16 个数；该不完整样例未测试，也未补造缺失内容。
- 1626 组独立三重枚举对拍：包括长度 1~9 的全部 1022 个正负 1 序列、600 个长度不超过 50 的随机序列，以及 4 个全正序列。两份程序输出均与逐区间、逐元素的暴力一致。
- 标准程序：T=3、每组 N=500000 的交替正负 1 序列，每组答案 31250125000；三组合计约 0.837 秒。
- 标准程序：N=500000 全为 1，答案 0，约 0.211 秒。
- 标准程序：N=500000，随机正负号及完整值域，约 0.165 秒。该项仅作性能及运行检查，没有独立最优值，未计入正确性对拍。
- 部分分：N=2000 的交替序列，答案 500500，约 0.007 秒。

上述交替序列答案由独立公式 k(N+1)-2k^2 得到，其中 k=ceil(floor(N/2)/2)。静态数组总量约 91.6 MiB，未把这一静态计算值称作进程峰值实测。

部分分支持 N<=2000，按题面覆盖 40%，未声称正式得分。
'''}
for name,body in details.items():
    rows=['\n## 本次最终源文件 SHA-256\n','| 文件 | SHA-256 |','|---|---|']
    for kind in ['std','partial']:
        p=out/name/(kind+'.cpp')
        rows.append(f'| {p.name} | `{hashlib.sha256(p.read_bytes()).hexdigest()}` |')
    (out/name/'validation.md').write_text(common+body+'\n'.join(rows)+'\n',encoding='utf-8')
readme='''# 26 NOIP 二十连测 day3 参考交付

日期：2026-10-21。依据用户提供的 7 页题面 PDF 编写。

每题目录包含 `solution.md`（完整中文题解、证明、复杂度和部分分说明）、`std.cpp`（完整数据参考程序）、`partial.cpp`（部分分程序）、`validation.md`（实际本地验证记录）。

| 目录 | 标准程序时间 | 部分分支持范围 | 按题面覆盖 |
|---|---|---|---|
| color | O(sum N) | N<=1000 | 30% |
| greedy | O(N*min(A,B)*A*B) | N<=8 或 A=B | 35% |
| brackets | O(sum Q log Q) | sum Q<=2000 | 40% |
| noise | O(sum N log N) | N<=2000 | 40% |

表中省略了复杂度的 +1 边界项，精确说明见各题题解。覆盖比例只来自题面测试点划分，不是正式评测成绩。部分分输入超出注明范围时可能以退出码 1 结束，不承诺完整数据。

## 编译和输入输出

所有程序使用竞赛风格 C++17，默认读取题目代号的 `.in`，写入同代号的 `.out`：

```text
color.in / color.out
greedy.in / greedy.out
brackets.in / brackets.out
noise.in / noise.out
```

在标准输入输出环境编译时增加 `-DLOCAL`。本地验证使用 TDM-GCC 和参数 `-std=c++17 -O2 -Wall -Wextra`，两种输入输出版本均编译和运行检查。

## 验证结果及限制

四题标准程序、部分分程序在支持范围内均通过样例与独立对拍。额外检查完整规模的运行、64 位答案、重复元素和负权值等情况。greedy 还核对了符合本 PDF 约束的 22 组原比赛公开数据。

noise 第二组样例在原 PDF 中横向截断，缺少后 4 个元素，没有补造该样例，也未声称验证。完整第一组样例、1626 组独立暴力对拍以及最大规模已检查。

当前没有本次正式提交记录，不把本地检查写成官方 AC。各题 `validation.md` 明确区分有参照答案的检查与仅作运行、性能检查的数据。

## 云端目录

- [color](https://drive.google.com/drive/folders/1l00DEHUzabecyyyKNkrE2VIvSUDMpBl3)
- [greedy](https://drive.google.com/drive/folders/1oPZwQcXO_QS5hfsa5p7M217Ql_XwJ3cf)
- [brackets](https://drive.google.com/drive/folders/1T4MFyJ8_XFxB7LXz5e4oIazUvYcHNvv6)
- [noise](https://drive.google.com/drive/folders/1LcJNl-3m6T6gteAfkmml0B3bZFk32TNl)

greedy、brackets 的官方讲解来源已分别列在对应题解末尾；本次实现、证明细节及验证以交付内容为准。
'''
(out/'README.md').write_text(readme,encoding='utf-8')
print('17 deliverable files ready; brackets partial Q=2000 seconds:',partial_time)
