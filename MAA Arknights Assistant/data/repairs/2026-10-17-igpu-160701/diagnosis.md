# 无需重启电脑的核显偏好验证

用户限制：现在不能重启电脑；不要操控 MAA；优先排查 Windows 环境。未重启或关闭任何程序。

用户确认模拟器和重启前的 Endfield 都出现花屏、黑块或贴图颜色错乱，而不仅是 MAA 更新日志崩溃。新驱动安装后，MAA 的事件仍为 `TextParaClient.RenderSimpleLines -> Invariant.FailFast`；不能据此确认它与其他花屏共用一个根因。

模拟器当前启动日志明确记录 Radeon RX550/550 Series、Direct3D11、驱动 `31.0.21925.1001`。因此至少模拟器的新会话已经加载新 AMD 驱动，不能把所有问题简单归结为没有重启、仍使用旧版本。

本机 Intel UHD 770 与 RX550 的设备状态均为 OK。Windows 状态 OK 不证明显卡硬件或显存健康。当前未查到 TDR/WHEA/内存耗尽事件；约 2.9 GiB 物理内存可用，不能因此完全排除资源压力。

已备份当前用户注册表 `Software\Microsoft\DirectX\UserGpuPreferences` 的三个应用条目，然后设置 `GpuPreference=1;`，保留其他已有偏好字段。目标为实际存在的 MuMuPlayer.exe、MuMuVMMHeadless.exe、MAA.exe。原值记录在 `graphics-preference-before.json`，恢复脚本为 `restore-graphics-preferences.ps1`。未改程序文件、未改全局显卡驱动选项、未改系统更新设置。

这是 Windows 的节能 GPU 选择偏好，可能被程序自己的适配器选择覆盖。用户重新打开模拟器后，必须读取新的 `shell.log` 中 `[Renderer::start] info:` 的 NativeAdapter / NativeAdapterDriverDesc 字段确认实际选择；不要仅凭注册表写入成功声称已经使用 Intel。

待验证：实际 GPU 是否变为 Intel、花屏是否改善、MAA 报错是否仍发生。不能将此项写成已修复。

参考：[AMD 关于 Windows 10 程序显卡偏好的说明](https://www.amd.com/en/resources/support-articles/faqs/GPU-110.html)，节能模式选择核显，设置在下次启动应用时生效。
