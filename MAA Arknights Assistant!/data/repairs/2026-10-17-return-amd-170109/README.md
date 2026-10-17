# 按用户要求切回 AMD 独显

用户明确暂停此前卡顿、作业预检等问题的排查，要求 MAA 切回独立显卡，原因是核显推理过慢。

Windows 界面工具未返回可操作的 MAA 窗口，因此没有进行界面操作。先请用户退出 MAA；随后进程检查确认为已退出，脚本再次检查 `MAA.exe` 不存在后才写配置。

已完成并校验：

- `D:\MAA-Arknights-Assistant\config\gui.new.json` 中 `Gui.Performance.UseGpu=true`、`GpuDescription="Radeon RX550/550 Series"`、`GpuInstancePath=""`。按官方 v6.19.0 GPU 选择代码，实例路径未指定时按唯一显卡描述匹配，避免误用 PNP 标识代替显示适配器接口路径。
- 当前用户 Windows `UserGpuPreferences` 中，仅 MAA.exe 一项从 `GpuPreference=1;` 改为 `GpuPreference=2;`。
- 其他 MAA 配置经过解析比较确认未改变；模拟器配置和显卡偏好未动；未启动 MAA 或作业，未重启电脑、未安装驱动。

备份原值为 `before.json`，实际写入前后的设置与校验值为 `applied.json`。`select-amd.py` 包含退出检查、变更范围检查和写后校验，`--dry-run` 可只预览。

配置在 MAA 下次启动生效；实际 GPU 仍需在用户手动重开 MAA 后通过日志确认。当前文档不代表已验证启动后的实际选择。

源码依据：https://github.com/MaaAssistantArknights/MaaAssistantArknights/blob/v6.19.0/src/MaaWpfGui/Helper/GpuOption.cs
