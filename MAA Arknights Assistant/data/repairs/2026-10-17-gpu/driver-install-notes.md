# RX 550 驱动排查准备

2026-10-17：用户补充，出现 MAA 更新日志崩溃前，整个桌面和多个程序曾严重花屏、渲染错乱，随后重启。优先排查显卡驱动或硬件；尚未确诊，也未认定更新驱动必然解决 WPF 崩溃。

## 当前环境和准备结果

- H3CDesk X500s 0351，Windows 10 EnterpriseG 21H2，19044.4529。
- 显示器当前由 Radeon RX550/550 Series 驱动，现有驱动 `30.0.15021.11005`，日期 2022-04-28，设备 ID `PCI\VEN_1002&DEV_699F`。
- Intel UHD 770 同时存在，此次没有更改 Intel 驱动。
- 过去两天的所查 System 日志发现一次意外关机事件 6008；没有找到可确认显卡 TDR/WHEA 故障的记录，也未找到 LiveKernelEvent 报告。缺少记录不等于排除驱动或硬件故障。
- 原 AMD 驱动通过 `pnputil /export-driver oem17.inf` 成功导出到 `previous-amd-driver`。159 个文件，包含 `u0379219.inf` 和签名有效的 `U0379219.CAT`，总计 1069157853 字节。
- 已下载 AMD 官方 Adrenalin 26.5.2 for Polaris & Vega，适配 Radeon RX 500 系列，官方说明支持 Windows 10 x64 1809 及以后版本。目标 Driver Store 版本 `31.0.21925.1001`。
- 安装包数字签名 Valid，签名者 Advanced Micro Devices；SHA256：`2E8755B69DDEA92305AC2399102088248C7E2C0F5C7B024A570797EBBBE50E77`。来源和完整路径见 `driver-package.json`。文件名含 win11，但官方说明同时支持 Windows 10。
- 尚未运行安装包、卸载驱动、重启电脑或操控 MAA。

## 用户手动安装与验证

保存工作并退出模拟器等占用显卡的程序，以管理员身份运行本目录中的官方安装包。先使用普通覆盖安装；如提供“仅驱动程序”，可选择此项，不额外启用录屏、叠加层等功能。第一步不使用恢复出厂设置或额外清理工具。安装时显示器可能短暂黑屏或闪烁，按安装器提示完成后手动重启。

重启后先查看桌面与其他程序是否正常，再由用户手动打开 MAA 更新日志。后续助手只读取驱动版本、安装日志和新事件，不自行操控 MAA。若整机仍花屏，再排查显卡硬件、连接与供电等，不能持续盲目换系统设置。

旧版本备份用于必要时在设备管理器中回退或手动选择旧驱动。不要声称 `pnputil /add-driver /install` 一定会强制降级：设备可能继续优先选用较新驱动。

## 系统检查的独立发现

此前 SFC `/verifyonly` 报告 31 项文件不一致，涉及壁纸、电源和磁盘加密工具；所查列表未见字体或文本渲染 DLL，尚未与 MAA 崩溃建立联系。未运行全局 SFC 修复，以免改动定制系统的无关组件。

DISM `/ScanHealth` 返回错误 3，CBS 日志表明无法创建维护会话目录。本机 `C:\Windows\CbsTemp` 实际是一个零字节、只读文件（2024-08-23 建立），占用了本应为目录的路径。用户表示系统安装后即如此、不清楚是否用过精简或更新禁用工具。当前未改动该文件，也未更改系统更新设置；显卡方向优先。

此前 MAA 更新日志文件改动与临时 WPF 软件渲染设置均已撤销。

## 官方依据

- [RX 550 下载页](https://www.amd.com/en/support/downloads/drivers.html/graphics/radeon-600-500-400/radeon-rx-500-series/radeon-rx-550.html)
- [26.5.2 Polaris & Vega 发布说明](https://www.amd.com/en/resources/support-articles/release-notes/RN-RAD-WIN-26-5-2-POLARIS-VEGA.html)
- [AMD 安装说明](https://www.amd.com/en/resources/support-articles/faqs/RSX2-INSTALL.html)
