# 2026-10-17 后续验证

状态：未修复。用户反馈模拟器属于随机异常，无法据此判定改善；MAA 打开更新日志仍报错。

最新 .NET Runtime 1025 事件为 16:17:17（此前为 16:15:32），MAA 的堆栈仍包含 `TextParaClient.RenderSimpleLines -> Invariant.FailFast`。模拟器最新 `[Renderer::start] info:` 仍为 16:01:08，记录 AMD RX550、新驱动 31.0.21925.1001，没有核显偏好设置之后的新启动记录。因此不能声称模拟器已经使用 Intel，也不能将随机花屏与 MAA 的确定性文字排版错误认定为同一原因。

完成独立、无窗口、仅软件渲染的 WPF 测试；没有启动或操控 MAA，没有改 MAA 文件。脚本 `test-text-layout.ps1` 只读 MAA 自带 WPF/MdXaml 依赖、原始日志及本地头像占位缓存。分别验证普通中英文、原始 Markdown、纯文本、加入本地头像、按官方源码结构合并头像和昵称；每种均在 560、540、580 像素宽度排版并渲染成功。最后一项实际合并了 113 个头像和昵称组合。

限制：测试宿主为 PowerShell/.NET 10.0.11，而 MAA 为 .NET 10.0.10；没有完整复制 MAA 的主题、窗口、异步加载时序。这些成功结果仅说明测试没有复现，不能证明 MAA 程序正常或系统正常，也不能据此确认字体、显卡、运行时哪一个是根因。

本轮没有继续修改 Windows 设置。三项核显偏好仍保留，恢复脚本为 `restore-graphics-preferences.ps1`；模拟器实际选择与随机稳定性仍待观察。此前全局 WPF 软件渲染试验无效，已经撤销，不应反复应用。

创建 `changelog-safe.html` 供浏览器阅读相同日志，内容经过 HTML 转义，不执行日志内标签，不访问网络。这是临时阅读入口，不是修复 MAA 崩溃。原始日志 SHA256 仍为 9E2924248360A61545417D8F89D6CB5B4E906B1A5690F58B1C6020A8E9F19F09。

源码依据：https://github.com/MaaAssistantArknights/MaaAssistantArknights/blob/v6.19.0/src/MaaWpfGui/ViewModels/Dialogs/VersionUpdateDialogViewModel.cs

后续不应仅因错误框标题含 Hard Error 就断言硬盘、显卡或系统文件损坏；不应在没有证据时清空系统字体缓存、改 TDR、禁用显卡、覆盖系统 DLL，或再次安装驱动。不重启且不修改 MAA 的限制下，目前没有已验证有效的修复方案。
