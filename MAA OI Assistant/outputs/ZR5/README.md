# 26 NOIP 十连测 day5：参考解答

根据用户提供的题面 PDF 自行编写，包含四题的完整算法、证明、C++17 参考实现和部分分实现。不是赛事方下发的官方程序；未提交原评测系统，不将本地验证表述为官方 AC。

## 目录

| 题目 | 标准解文件 | 题解文件 | 部分分文件 | 部分分覆盖 |
|---|---|---|---|---:|
| 计数器 counter | `counter/std.cpp` | `counter/solution.md` | `counter/partial.cpp` | 子任务 1--3，78 分 |
| 缓冲 buffer | `buffer/std.cpp` | `buffer/solution.md` | `buffer/partial.cpp` | 子任务 1--3，78 分 |
| 字典 alphabet | `alphabet/std.cpp` | `alphabet/solution.md` | `alphabet/partial.cpp` | 子任务 1--5，62 分 |
| 补贴 subsidy | `subsidy/std.cpp` | `subsidy/solution.md` | `subsidy/partial.cpp` | 子任务 1--5，57 分 |

各项部分分分数按题面子任务范围计算，表示算法设计覆盖，不代表已经在原评测系统取得对应分数。每份 `solution.md` 都包含全部子任务的说明。

## 使用方式

标准编译命令示例：

```text
g++ -std=c++17 -O2 std.cpp -o std
```

默认按题面使用文件输入输出。例如 `counter/std.cpp` 读取当前运行目录的 `counter.in`，写入 `counter.out`。

若使用标准输入输出或 CPH-NG 管道运行，编译时添加 `-DLOCAL`：

```text
g++ -std=c++17 -O2 -DLOCAL std.cpp -o std
```

所有程序均为单组输入，询问彼此独立。模数在需要时为 `998244353`。

## 验证

八份代码使用本项目已有的 TDM-GCC 编译器，以 C++17、`-O2 -Wall -Wextra` 编译检查；样例、独立暴力和边界测试通过。四份标准解还进行了最大规模或最大总长度测试，默认文件输入输出也经过检查。

详细数据、验证方式和实测时间见 `验证记录.md`。随机验证仅辅助发现实现错误；正确性依据各题题解中的证明。
