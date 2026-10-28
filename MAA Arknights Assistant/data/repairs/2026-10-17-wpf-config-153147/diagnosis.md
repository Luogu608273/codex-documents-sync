# 2026-10-17 Windows / WPF 排查记录

## 当前结论

尚未修复；不再操控 MAA，按用户要求排查 Windows 环境。

- 原先对 `D:\MAA-Arknights-Assistant\data\CHANGELOG.md` 的作者链接改动已撤销。原始 SHA256 为 `9e2924248360a61545417d8f89d6cb5b4e906b1a5690f58b1c6020a8e9f19f09`，恢复后已验证一致。
- 临时创建当前用户 `Software\Microsoft\Avalon.Graphics\DisableHWAcceleration=1` 后，用户手动重启并测试，仍然报错。因此已运行 `restore-wpf.ps1` 撤销该值，恢复原来的无此值状态。没有把此项当作修复。
- 应用程序日志的 .NET Runtime 事件 1025：原记录 3781、3782、3785、3786；软件渲染测试后新记录 3790（2026-10-17 15:32:31）。关键栈均为 `Invariant.FailFast -> TextParaClient.RenderSimpleLines`，运行时 .NET 10.0.10。
- 对应版本 WPF 源码在 RenderSimpleLines 中会检查文本行的实际长度是否与布局阶段一致；这里的失败表明文本排版不一致，不能单凭这个堆栈认定硬盘、显卡或 MAA 本体损坏。
- Windows 10 EnterpriseG（神州网信政府版），21H2，19044.4529；本机列出的最新系统补丁安装日期为 2024-06-27。两块显卡驱动日期在 2022 年。这里只记录环境，未证实是根因。
- 未发现额外字体替换、MAA 的 Windows 兼容模式或异常文本缩放；AppliedDPI=96。常用字体的注册表映射指向实际存在的系统字体。
- dwrite.dll、TextShaping.dll、MAA 使用的 PresentationFramework.dll 和 PresentationNative_cor3.dll 的签名检查为 Valid。签名正常不等价于完整系统健康证明。
- 当前会话不具有管理员权限；系统 FontCache 目录访问被拒绝，未清理该目录，未停止字体服务。

## 下一步：管理员只读检查

用户可右键同目录的 `check-windows-health.cmd`，选择“以管理员身份运行”。它只运行 DISM `/ScanHealth` 与 SFC `/verifyonly`，不运行 RestoreHealth 或 scannow，不更改 MAA，不删除字体缓存，也不自动提权。

结果保存在同目录的 `health-results`，可由后续会话直接读取，不需要用户上传。用户已于 2026-10-17 15:38 完成管理员检查：DISM 返回错误 3，CBS 记录显示 `C:\Windows\CbsTemp` 被零字节只读文件占用，无法创建维护会话目录；SFC 报告 31 项文件不一致，涉及壁纸、电源和磁盘加密工具，所查列表未见字体或文本渲染组件。暂未更改这些系统文件或更新设置。

随后用户补充，重启前整个桌面和多个程序都曾严重花屏。排查优先转向显卡，已准备官方 AMD 驱动及当前驱动备份，尚未安装；后续读取相邻 `../2026-10-17-gpu/driver-install-notes.md`。

## 参考

- [微软 WPF 软件渲染排查设置](https://learn.microsoft.com/en-us/dotnet/desktop/wpf/graphics-multimedia/graphics-rendering-registry-settings)：软件渲染是诊断手段；此机器测试无效，已撤销。
- [WPF v10.0.10 TextParaClient 源码](https://github.com/dotnet/wpf/blob/v10.0.10/src/Microsoft.DotNet.Wpf/src/PresentationFramework/MS/Internal/PtsHost/TextParaClient.cs)：RenderSimpleLines 的行长度一致性断言。

不要将只是在其他问题中出现相近关键词的 TextBox/IME 问题当成此机器已确诊原因；不要继续随机更改全局配置。
