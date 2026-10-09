# N13：四题 solution 与 code

依据用户提供的 U1708.pdf、U1709.pdf、U1710.pdf、U1711.pdf 整理。解法为独立推导，未使用或核对官方题解，未提交在线评测。

## 文件索引

| 题目 | 解法文档 | 完整代码 | 独立部分分代码 |
|---|---|---|---|
| U1708 守望 | U1708_solution.md | U1708_code.cpp | U1708_partial_20.cpp、U1708_partial_40.cpp |
| U1709 合并 | U1709_solution.md | U1709_code.cpp | U1709_partial_14.cpp、U1709_partial_68.cpp |
| U1710 门派 | U1710_solution.md | U1710_code.cpp | U1710_partial_66.cpp |
| U1711 铺砖 | U1711_solution.md | U1711_code.cpp | U1711_partial_20.cpp |

solution 包含题意、各档部分分、完整算法、正确性证明、复杂度与实现注意事项。部分分文件名中的数字是按题面限制分析的预计分值；部分分程序只保证文档列明的数据档，不适用于所有大规模输入。

## 运行方式

所有程序使用 C++17，并按照题面启用文件输入输出：

| 题目 | 输入文件 | 输出文件 |
|---|---|---|
| 守望 | watch.in | watch.out |
| 合并 | merge.in | merge.out |
| 门派 | sect.in | sect.out |
| 铺砖 | tile.in | tile.out |

输入文件应放在程序运行的当前目录。如果所在评测环境要求标准输入输出，删除对应的两行 `freopen` 即可。

## 完整算法复杂度

| 题目 | 时间 | 空间 |
|---|---|---|
| 守望 | O(n) | O(n) |
| 合并 | O(N log N+Q log N) | O(N) |
| 门派 | O(N log N) | O(N log N) |
| 铺砖 | O(N log N) | O(N) |

10 份代码均已编译并通过题面样例和小规模独立对照。完整程序另通过了上限规模数据。测试细节、实际计时与验证范围见 N13_验证说明.md。
