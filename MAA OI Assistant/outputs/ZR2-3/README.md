# 26 NOIP 二十连测 day3 参考交付

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
