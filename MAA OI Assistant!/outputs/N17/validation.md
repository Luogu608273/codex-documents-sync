# N17 本地验证记录

日期：2026-10-21；随机种子以 20261021 为基础，附加压力用例使用 712021、818、518。

## 编译与读写

编译器：`C:/TDM-GCC-64/bin/g++.exe`，C++17，参数 `-std=c++17 -O2 -Wall -Wextra`。每题 std/partial 均编译默认文件读写版和 `-DLOCAL` 版；两套总计 32 个编译目标，无警告。

每个程序均实际运行并比较过默认 `.in/.out` 文件读写和 LOCAL 标准输入输出，均通过。文件读写测试仅在本任务 work 子目录进行，未覆盖用户输入。

## 正确性检查

- 中位数：481 个小数组，枚举全部奇数长度划分，验证“可归并成两段”的结论与程序输出。
- 矿车：160 个小实例，枚举全部预算内填法；用允许反复进出侧线的完整状态 BFS 求最小容量。另与官方 B.cpp 对比 40 个中等规模随机实例。
- 连通图：276 个输入；对 n≤5 枚举全部允许自环的候选图，比较完整奇偶最短距离，求真正的最小边数。另与官方 C.cpp 对比 1200 个随机图实例。
- 水晶：200 个小实例，BFS 枚举全部合法删除结果，与字典序最小值比较。两个原始样例也通过。
- 全部原始样例通过；连通图第二个样例包含的 7 组数据已单独检查。

这些测试是对题解证明与实现的补充，不以随机对拍替代证明。没有下载或运行官方完整评测数据，未进行在线提交。

## 大规模及部分分边界测试

下表为本机单次实测，含进程启动及输入输出；不是评测机时限承诺。峰值为 Windows 进程 PeakWorkingSetSize，和评测机内存统计口径可能不同。“运行完成”只检查退出成功与输出形状，不代表该大用例已有独立正确答案。

| 题目 | 版本 | 用例 | 秒 | 峰值 MiB | 结果检查 |
|---|---|---|---:|---:|---|
| A_median | std | n=2e5, strictly increasing | 0.048 | 6.1 | 与预期答案一致 |
| B_tramcar | std | n=3e5, K=0, decreasing | 0.051 | 7.6 | 与预期答案一致 |
| B_tramcar | std | n=3e5, 1.5e5 empty cars, sufficient K | 0.043 | 7.1 | 与预期答案一致 |
| C_connected | std | n=1e5, path | 0.024 | 8.0 | 与预期答案一致 |
| C_connected | std | n=1e5, path and far-end self-loop | 0.049 | 13.8 | 与预期答案一致 |
| D_crystal | std | n=5e5, no deletions | 0.117 | 118.3 | 与预期答案一致 |
| D_crystal | std | n=5e5, all deletable | 0.097 | 120.2 | 与预期答案一致 |
| D_crystal | std | n=5e5, periodic string, cyclic deletion rules | 0.118 | 120.0 | 运行完成，未独立核对该大用例答案 |
| A_median | partial | partial supported upper boundary | 0.016 | 3.0 | 与预期答案一致 |
| B_tramcar | partial | partial supported upper boundary | 0.009 | 3.1 | 与预期答案一致 |
| D_crystal | partial | partial supported upper boundary | 0.005 | 3.4 | 与预期答案一致 |

## 复现材料

本地测试源与详细 JSON 日志保留在项目 `work/N17-S17-20261021/`。验证器使用独立枚举/生成函数算法；标准参考的比较另行标注，没有把与官方源码一致等同于独立证明。
