# S15 本地验证记录

日期：2026-10-13。编译器：TDM-GCC 10.3.0，C++17，`-O2 -Wall -Wextra`。

七份 C++ 程序均编译通过。标准输入输出测试使用 `-DLOCAL`；另将七份程序全部不带该宏编译，用原题的 `.in` / `.out` 文件核对原题第一组样例，全部一致。NLP 的第二组样例也已单独核对。

## 独立小数据检查

| 题目 | 检查组数 | 独立判断方法 | 比较程序 |
|---|---:|---|---|
| game | 900 | A,B∈[1,30]，逐个枚举最终 a,b 至 70 | std、partial_enumerate |
| nlp | 1760 | 每轮先枚举规则，再从左到右枚举位置 | std、partial_scan |
| card | 1343 | 枚举区间、损坏位、人对，检查剩余位能否全部取同值 | std、partial_pairs、partial_scalar |

随机种子：20261013。NLP 包含二值序列穷举及随机多规则，校园卡包含两人三种集合的小范围穷举、随机集合、n=1 和 63/64/65/127/128/129 人的字边界检查。所有比较一致。

## 大数据构造

以下为本机从启动程序到收集输出的单次墙钟时间，含进程与输入输出开销；它不是评测机耗时保证。预期输出由构造的简单性质独立计算。

| 题目/程序 | 构造 | 秒 |
|---|---|---:|
| nlp/std | n=m=10^6，重复规则，全合并 | 0.436 |
| nlp/std | n=m=10^6，逆序互异规则，全合并 | 0.496 |
| card/std | n=1000,m=2000，所有集合相同 | 0.433 |
| card/std | n=1000,m=2000，各人互不相交 | 0.459 |
| card/std | n=1000,m=2000，仅末两人无法区分 | 0.441 |
| card/std | n=1000,m=2000，交替区分位 | 0.482 |
| card/std | n=2,m=200000，所有集合相同 | 0.061 |
| card/std | n=2,m=200000，每一位可区分 | 0.061 |
| card/std | n=2,m=200000，交替区分位 | 0.062 |
| card/std | n=1,m=200000，所有区间合法 | 0.030 |
| card/partial_scalar | n=200,m=1000，各人互不相交 | 0.064 |
| game/std | T=10^5，每组 1 和 10^6 | 0.083 |
| card/std | n=200,m=1000,K=200万，每集合10元素 | 0.186 |
| card/partial_scalar | n=200,m=1000,K=200万，每集合10元素 | 0.200 |
| card/std | n=1000,m=1,K=200万，集合逆序输入 | 0.231 |

## 空间与结论边界

校园卡标准程序采用压缩上三角位集。n=1000 时每列 8664 个 64 位字；此时输入总量限制推出 m≤2000，两大矩阵总计 277,248,000 字节，约 264.40 MiB。另有输入、当前列排序记录和小型工作位集，低于 512 MiB 限制。此处为按实现计算的存储上界，未把它伪称为进程峰值测量。

有限穷举、随机比较及压力测试用于检验实现，不能替代全范围正确性证明。证明见各题 solution.md。没有向原平台提交，没有官方 AC 记录；部分分范围依据题面约束和程序复杂度判断。

## 文件校验

下面 SHA-256 对应交付的 C++ 和题解原文件，可用于下载后核对。

```text
ed6e88e509596e92353e819570b2727ae10038ba2d19b762e42a3318669e1de4  card/partial_pairs.cpp
b494ea05d005618263473112f1cb6a6b9bbfb33d34320d289e61cd4f7d1eb69d  card/partial_scalar.cpp
abbb15c4b23eff3bfc7b2c8f15864c4f4e95bf7e0b66da6ea6f259d197a49dde  card/solution.md
7ef9f0a70ccca47a1ff8cfb9aa84dcf640b42f7ddc597ee3af9566cf5feb57e7  card/std.cpp
28a7f97d626aa2df046deaaecc50abc275e335dec38289c1c87bc6e0bd290efc  game/partial_enumerate.cpp
a05acd303551cac983abbd9265781ab9fadf72a8b415957bd0ceac5caaa50cd7  game/solution.md
c1310fb24325dae9ff64336add50bfc4ddb59b4a10bc56a19edd6d237631d8bc  game/std.cpp
61ab8df6f6cf00062a3aad09e5bf066901443530c4ae8724c89d8b7277e33868  nlp/partial_scan.cpp
e2767ee557d1f8decdb810b8e55b237d385e277691fb870ddcbcceaeff8e8bb4  nlp/solution.md
7e0b25c11476d049a610c37473865ac0740cdfd312933ea959fcf3d565066d2c  nlp/std.cpp
```
