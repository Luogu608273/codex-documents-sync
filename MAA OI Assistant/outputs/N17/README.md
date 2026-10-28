# N17 参考解答

整理日期：2026-10-21。对应 MXOJ [T3644](https://www.mxoj.net/training/T3644) 的四道题。

| 目录 | 题目 | 标准程序时间 | 部分分程序适用范围 |
|---|---|---|---|
| `A_median` | [中位数](https://www.mxoj.net/problem/G123911) | O(n log n) | n≤2000，直接枚举切分并排序 |
| `B_tramcar` | [矿车](https://www.mxoj.net/problem/G123912) | O(n log n) | n≤5000 且 K=0 |
| `C_connected` | [连通图](https://www.mxoj.net/problem/G123913) | O(m+n log n) | n≤5，枚举全部候选图 |
| `D_crystal` | [水晶](https://www.mxoj.net/problem/G123914) | O(n log n) | n≤500，区间检查与字符串 DP |

每个题目目录包含 `std.cpp`、`solution.md`、`partial.cpp`。部分分代码是实际受限实现，不等同于完整标准程序；范围外可能超时、越界或结果错误，请按题解标注使用。

C++17；默认读取原题同名 `.in`，写入 `.out`，加 `-DLOCAL` 改为标准输入输出。示例：

```text
g++ std.cpp -std=c++17 -O2 -Wall -Wextra -DLOCAL -o std
```

算法和证明结合题面与[本套官方解析资料库](https://b1bznc26af6.feishu.cn/drive/folder/Tf0NfiHZDlFXGId4h5PcwksXnSh) 复核；程序已按统一竞赛风格重写。

`validation.md` 记录本地编译、独立对拍、样例和规模测试；`manifest.json` 记录本目录其他 14 个文件的字节数与 SHA-256。清单不包含自身。

交付状态：本地验证通过，未向 MXOJ 提交，不声明官方 AC。所有子任务得分均仅表示根据题面约束推导的覆盖范围。

《水晶》完整程序使用双哈希，存在极低的碰撞概率；部分分程序使用完整字符串比较。
