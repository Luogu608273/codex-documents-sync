# S17 参考解答

整理日期：2026-10-21。对应 MXOJ [T3624](https://www.mxoj.net/training/T3624) 的四道题。

| 目录 | 题目 | 标准程序时间 | 部分分程序适用范围 |
|---|---|---|---|
| `A_sam` | [后缀自动机](https://www.mxoj.net/problem/U2294) | O(26(n+q)) | n,q≤5000 或询问总长度≤2×10^6 |
| `B_lis` | [最长上升子序列](https://www.mxoj.net/problem/U2295) | O(n log n) | n≤5000，平方 DP |
| `C_wolf` | [狼人杀](https://www.mxoj.net/problem/U2296) | O(n log n) | n≤5000，枚举总狼数的平方 DP |
| `D_power` | [二进制拆分](https://www.mxoj.net/problem/U2297) | O(30^4+2^15·30²+30q) | 所有询问 n<2^16，完全背包 |

每个题目目录包含 `std.cpp`、`solution.md`、`partial.cpp`。部分分代码是实际受限实现，不等同于完整标准程序；范围外可能超时、越界或结果错误，请按题解标注使用。

C++17；默认读取原题同名 `.in`，写入 `.out`，加 `-DLOCAL` 改为标准输入输出。示例：

```text
g++ std.cpp -std=c++17 -O2 -Wall -Wextra -DLOCAL -o std
```

算法和证明结合题面与[本套官方解析资料库](https://b1bznc26af6.feishu.cn/drive/folder/A0GffH8KklABpLd81DMcQkEandg) 复核；程序已按统一竞赛风格重写。

`validation.md` 记录本地编译、独立对拍、样例和规模测试；`manifest.json` 记录本目录其他 14 个文件的字节数与 SHA-256。清单不包含自身。

交付状态：本地验证通过，未向 MXOJ 提交，不声明官方 AC。所有子任务得分均仅表示根据题面约束推导的覆盖范围。
