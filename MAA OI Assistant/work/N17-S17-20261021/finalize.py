from pathlib import Path
import json,hashlib
TASK=Path(__file__).resolve().parent
OUT=TASK.parents[1]/'outputs'
data=json.loads((TASK/'stress.json').read_text(encoding='utf-8'))
INFO={
 'N17': [('A_median','中位数','G123911','O(n log n)','n≤2000，直接枚举切分并排序'),('B_tramcar','矿车','G123912','O(n log n)','n≤5000 且 K=0'),('C_connected','连通图','G123913','O(m+n log n)','n≤5，枚举全部候选图'),('D_crystal','水晶','G123914','O(n log n)','n≤500，区间检查与字符串 DP')],
 'S17': [('A_sam','后缀自动机','U2294','O(26(n+q))','n,q≤5000 或询问总长度≤2×10^6'),('B_lis','最长上升子序列','U2295','O(n log n)','n≤5000，平方 DP'),('C_wolf','狼人杀','U2296','O(n log n)','n≤5000，枚举总狼数的平方 DP'),('D_power','二进制拆分','U2297','O(30^4+2^15·30²+30q)','所有询问 n<2^16，完全背包')]
}
VERIFY={
 'N17': '''- 中位数：481 个小数组，枚举全部奇数长度划分，验证“可归并成两段”的结论与程序输出。
- 矿车：160 个小实例，枚举全部预算内填法；用允许反复进出侧线的完整状态 BFS 求最小容量。另与官方 B.cpp 对比 40 个中等规模随机实例。
- 连通图：276 个输入；对 n≤5 枚举全部允许自环的候选图，比较完整奇偶最短距离，求真正的最小边数。另与官方 C.cpp 对比 1200 个随机图实例。
- 水晶：200 个小实例，BFS 枚举全部合法删除结果，与字典序最小值比较。两个原始样例也通过。
- 全部原始样例通过；连通图第二个样例包含的 7 组数据已单独检查。''',
 'S17': '''- 后缀自动机：100 个小字符串，枚举每个区间的全部非空子串，按出现位置计数，与程序逐询问比较。
- 最长上升子序列：933 个排列（包含 n≤6 的全部排列），对每个阈值重建过滤序列，使用平方 LIS 作为独立答案。
- 狼人杀：720 个实例，枚举全部非相邻狼人集合，逐个检查所有村民发言。
- 二进制拆分：12 组权值，包括全部为 1、全部为 P-1；24336 次询问与完全背包比较，312 次高位询问与独立的有理生成函数奇偶抽取算法比较，包含 n=2^30-1。
- 全部原始样例通过。'''
}
for group,rows in INFO.items():
    p=OUT/group
    tid='T3644' if group=='N17' else 'T3624'
    folder='Tf0NfiHZDlFXGId4h5PcwksXnSh' if group=='N17' else 'A0GffH8KklABpLd81DMcQkEandg'
    rd=f'# {group} 参考解答\n\n整理日期：2026-10-21。对应 MXOJ [{tid}](https://www.mxoj.net/training/{tid}) 的四道题。\n\n'
    rd+='| 目录 | 题目 | 标准程序时间 | 部分分程序适用范围 |\n|---|---|---|---|\n'
    for d,title,pid,tc,pc in rows:rd+=f'| `{d}` | [{title}](https://www.mxoj.net/problem/{pid}) | {tc} | {pc} |\n'
    rd+='\n每个题目目录包含 `std.cpp`、`solution.md`、`partial.cpp`。部分分代码是实际受限实现，不等同于完整标准程序；范围外可能超时、越界或结果错误，请按题解标注使用。\n\n'
    rd+='C++17；默认读取原题同名 `.in`，写入 `.out`，加 `-DLOCAL` 改为标准输入输出。示例：\n\n```text\ng++ std.cpp -std=c++17 -O2 -Wall -Wextra -DLOCAL -o std\n```\n\n'
    rd+=f'算法和证明结合题面与[本套官方解析资料库](https://b1bznc26af6.feishu.cn/drive/folder/{folder}) 复核；程序已按统一竞赛风格重写。\n\n'
    rd+='`validation.md` 记录本地编译、独立对拍、样例和规模测试；`manifest.json` 记录本目录其他 14 个文件的字节数与 SHA-256。清单不包含自身。\n\n'
    rd+='交付状态：本地验证通过，未向 MXOJ 提交，不声明官方 AC。所有子任务得分均仅表示根据题面约束推导的覆盖范围。\n'
    if group=='N17':rd+='\n《水晶》完整程序使用双哈希，存在极低的碰撞概率；部分分程序使用完整字符串比较。\n'
    (p/'README.md').write_text(rd,encoding='utf-8')
    vd=f'# {group} 本地验证记录\n\n日期：2026-10-21；随机种子以 20261021 为基础，附加压力用例使用 712021、818、518。\n\n'
    vd+='## 编译与读写\n\n编译器：`C:/TDM-GCC-64/bin/g++.exe`，C++17，参数 `-std=c++17 -O2 -Wall -Wextra`。每题 std/partial 均编译默认文件读写版和 `-DLOCAL` 版；两套总计 32 个编译目标，无警告。\n\n每个程序均实际运行并比较过默认 `.in/.out` 文件读写和 LOCAL 标准输入输出，均通过。文件读写测试仅在本任务 work 子目录进行，未覆盖用户输入。\n\n'
    vd+='## 正确性检查\n\n'+VERIFY[group]+'\n\n'
    vd+='这些测试是对题解证明与实现的补充，不以随机对拍替代证明。没有下载或运行官方完整评测数据，未进行在线提交。\n\n'
    vd+='## 大规模及部分分边界测试\n\n下表为本机单次实测，含进程启动及输入输出；不是评测机时限承诺。峰值为 Windows 进程 PeakWorkingSetSize，和评测机内存统计口径可能不同。“运行完成”只检查退出成功与输出形状，不代表该大用例已有独立正确答案。\n\n'
    vd+='| 题目 | 版本 | 用例 | 秒 | 峰值 MiB | 结果检查 |\n|---|---|---|---:|---:|---|\n'
    for r in data:
        if r.get('group')!=group or 'seconds' not in r:continue
        lab=r['label'].replace('|','/')
        vd+=f"| {r['problem']} | {r['variant']} | {lab} | {r['seconds']:.3f} | {r['peak_working_set_MiB']} | {'与预期答案一致' if r['expected_checked'] else '运行完成，未独立核对该大用例答案'} |\n"
    vd+='\n## 复现材料\n\n本地测试源与详细 JSON 日志保留在项目 `work/N17-S17-20261021/`。验证器使用独立枚举/生成函数算法；标准参考的比较另行标注，没有把与官方源码一致等同于独立证明。\n'
    (p/'validation.md').write_text(vd,encoding='utf-8')
    files=[]
    for f in sorted(p.rglob('*')):
        if not f.is_file() or f.name=='manifest.json':continue
        raw=f.read_bytes();files.append(dict(path=f.relative_to(p).as_posix(),size=len(raw),sha256=hashlib.sha256(raw).hexdigest(),md5=hashlib.md5(raw).hexdigest()))
    assert len(files)==14
    (p/'manifest.json').write_text(json.dumps(dict(group=group,date='2026-10-21',status='locally_verified_not_submitted',files=files),ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
inventory=[]
for group in INFO:
    for f in sorted((OUT/group).rglob('*')):
        if not f.is_file():continue
        raw=f.read_bytes();inventory.append(dict(group=group,path=str(f.resolve()),relative=f.relative_to(OUT/group).as_posix(),size=len(raw),md5=hashlib.md5(raw).hexdigest()))
(TASK/'upload_inventory.json').write_text(json.dumps(inventory,ensure_ascii=False,indent=2),encoding='utf-8')
print('Finalized',len(inventory),'files; 15 per group.')
