# 后续排查（不重启、不操作 MAA）

用户截图显示 Intel UHD 770 被选为推理加速 GPU；此设置不能单独证明 WPF 界面渲染适配器。读取用户手动打开的 MAA 进程 4320 的模块，确认同时加载 Intel 与 AMD 图形组件、Windows 自带 dwrite/TextShaping、MAA 自带 .NET/WPF 10.0.10；没有发现 MacType/gdipp 等字体替换组件。模块清单见 `maa-loaded-modules.json`。模块在内存不等于对应 GPU 正在执行具体窗口渲染。

发现之前 PowerShell 独立测试实际加载了 PowerShell 自带 WPF 原生 DLL（10.0.11）。因此旧测试不是完整相同运行库的验证；未据此改动 MAA 运行库。

在项目 `runtime-10.0.10` 目录构建独立诊断宿主：复制 PowerShell 宿主，按 MAA.deps.json 的两个 runtimepack 覆盖该副本内的 .NETCore 和 WindowsDesktop 运行时。原 MAA、原 PowerShell/ Codex 运行库均未修改。独立进程报告 CLR 10.0.10，WPF 原生 DLL 与 MAA 相同文件版本。

使用官方 v6.19.0 MdXaml 样式、本地占位图片、113 个头像和昵称组合、中文语言设置、原 MdXaml 控件、嵌套滚动布局、全篇滚动，分别测试 Ideal/Display、异步及预加载图片。均未复现。进一步逐像素扫描 250–650 共 401 个宽度，记录 `width-sweep.log`，全部完成并输出 PASS。软件渲染的这些成功结果不能证明硬件渲染、MAA 加载时序或整个系统正常。

系统排查阶段未继续安装驱动、清理字体缓存、覆盖系统文件或修改系统设置；没有启动、关闭或点击 MAA。

已准备只将贡献者 @名称预链接化的日志缓存对照（114 处），以跳过自动插图和对应合并路径。独立同版本运行库验证此候选完整排版成功，但 MAA 实机结果未知。原文备份 `CHANGELOG.pre-avatar-test.md`，候选 `CHANGELOG.link-only.md`，双向切换脚本 `switch-changelog-test.ps1`；校验哈希并要求 MAA 已由用户手动退出，不操作程序或更改设置。

用户明确确认“允许，MAA 已完全退出”后，已执行 Apply 并校验目标 SHA256 为 `3D5F14C257181F520EC3386EE3D91F3007D0D409AE42E11F6A9CC673855622A6`。仅 `data/CHANGELOG.md` 改变，原文件完整备份 SHA256 为 `9E2924248360A61545417D8F89D6CB5B4E906B1A5690F58B1C6020A8E9F19F09`。

2026-10-17 16:45 用户确认“能正常打开，不再报错”。独立核对：MAA 新进程 24760 于 16:45:24 启动，Responding=True；16:45:47 查询的最新 MAA .NET Runtime 崩溃仍是 16:22:46、记录号 3866，未出现本轮新的同类崩溃。日志哈希保持候选值。

结论：当前日志缓存绕过方案已由用户验证有效，保留当前可用版本。触发范围已缩小到贡献者头像插入及头像昵称组合的复杂排版路径；仍不能据此证明 Windows 文件损坏、显卡硬件正常或 MAA/运行库的唯一根因。未重启电脑，未更改 MAA 程序或设置。本机核显偏好保持此前状态，模拟器随机异常、Endfield 与桌面花屏仍是未完成验证的另一项问题。

后续 MAA 更新可能重新写入日志缓存，此方案不保证跨更新保持。恢复原文需先由用户手动完全退出 MAA，再运行 `switch-changelog-test.ps1 -Mode Restore`；会验证当前文件仍为本候选，遇到新日志则停止覆盖。不要在当前已验证有效的情况下继续无依据地更改驱动、字体或系统设置。

官方源码：
- https://github.com/MaaAssistantArknights/MaaAssistantArknights/blob/v6.19.0/src/MaaWpfGui/Res/Styles/MdXaml.xaml
- https://github.com/MaaAssistantArknights/MaaAssistantArknights/blob/v6.19.0/src/MaaWpfGui/ViewModels/Dialogs/VersionUpdateDialogViewModel.cs
