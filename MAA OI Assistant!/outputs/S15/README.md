# S15：U2246 / U2247 / U2248

依据用户提供的三份题面 PDF 编写。每题包含完整题解、标准程序和部分分程序；题解给出正确性证明、时间与空间复杂度、部分分适用范围及实现注意事项。

## 目录

```text
S15/
  README.md
  verification.md
  verification.json
  game/
    solution.md
    std.cpp
    partial_enumerate.cpp
  nlp/
    solution.md
    std.cpp
    partial_scan.cpp
  card/
    solution.md
    std.cpp
    partial_pairs.cpp
    partial_scalar.cpp
```

## 程序约定

全部程序使用 C++17。默认遵守原题的文件输入输出：

| 目录 | 输入文件 | 输出文件 |
|---|---|---|
| game | game.in | game.out |
| nlp | nlp.in | nlp.out |
| card | card.in | card.out |

若使用终端或 CPH 的标准输入输出，编译时加 `-DLOCAL`，例如：

```text
g++ -std=c++17 -O2 -DLOCAL std.cpp -o std
```

不加此宏时，从程序运行目录读取 `.in` 并写入 `.out`。

## 部分分范围

| 题目 | 程序 | 题面中适用的测试点 |
|---|---|---|
| U2246 | partial_enumerate.cpp | 1～10、13、14 |
| U2247 | partial_scan.cpp | 1～6 |
| U2248 | partial_pairs.cpp | 1～8 |
| U2248 | partial_scalar.cpp | 1～14 |

部分分程序计算逻辑正确，区别在于最坏运行时间。各点权重未在题面中明确给出，所以没有虚构分数。具体约束和复杂度见各题 `solution.md`。

## 验证状态

已完成编译、原题样例、小数据独立暴力比较和大数据构造测试，具体记录见 `verification.md` 与 `verification.json`。未向原平台提交，不将本地测试表述为官方 AC。

原题面：`U2246.pdf`、`U2247.pdf`、`U2248.pdf`；整理日期：2026-10-13。
