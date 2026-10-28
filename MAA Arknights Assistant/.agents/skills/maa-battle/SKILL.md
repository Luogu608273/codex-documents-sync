---
name: maa-battle
description: 在本项目使用 MAA Arknights Assistant 的 Python SDK 执行或排查自动战斗、Copilot 作业和 Fight 代理刷关，并通过 ADB 连接 MuMu、低频观察明日方舟画面。适用于 MAA 接口学习、连接检查、作业运行和作战结果复核。
---

# MAA 自动战斗与低频观察

## 选择任务

- 查找作业、匹配干员时使用相邻的 [arknights-homework](../arknights-homework/SKILL.md)。拿到的是作业详情时，解析其中的 `content` 为作战 JSON，保存后再交给 MAA。
- `Copilot` 根据 JSON 自动部署、撤退、放技能，用于抄作业；`Fight` 使用游戏内代理刷关，需要已有可用代理。保全和悖论分别使用 `SSSCopilot`、`ParadoxCopilot`，不能直接套普通 Copilot 参数。
- 学习接口、检查环境或观察画面只需只读检查。用户要求执行作战时，按已授权的关卡、次数、模式、助战和消耗范围操作；信息足够就继续，无需逐步重复确认。缺少会影响消耗或作业正确性的必要信息时才澄清。

## 本项目环境

2026-10-10 实机核实，后续先检查路径和设备是否仍有效：

| 项目 | 已验证值 |
| --- | --- |
| MAA 安装目录 | `D:\MAA-Arknights-Assistant` |
| 核心 / Python 包 | `MaaCore.dll` / `Python\asst\asst.py` |
| SDK 核心版本 | `v6.18.0`，通过 `get_version()` 读取 |
| Python | 本机 Python 3.12，64 位进程需与 DLL 架构匹配 |
| ADB | `C:\Program Files\YXArkNights-12.0\shell\adb.exe` |
| 模拟器序列号 | `127.0.0.1:16384`，`devices -l` 为 `device` |
| 游戏包名 | `com.hypergryph.arknights`，国服官服 |
| 实际截图 | PNG 1280×720；`wm size` 的竖屏数值不能直接当横屏坐标 |

启动执行前避免 MAA GUI、独立 Python 实例和手动 ADB 输入同时控制一个游戏。`asst.running()` 只表示自己的实例状态，不能据此断言 GUI 空闲。观察截图和设备状态可在 GUI 存在时进行。

## Python 作战

读取 [Python SDK 与自动战斗](references/python-and-copilot.md)，包含本机接口、任务参数、回调、执行示例及完成判定。

- 使用安装目录自带 `asst`，不替换为其他同名包或 MaaFramework。
- `Asst.load()` 加载资源时给独立 `user_dir`，避免覆盖 GUI 的调试输出。
- 先核对作业关卡和难度、阵容技能模组、版本与作者说明，再连接、添加任务和启动。`formation=true` 会改动编队，按本次任务指定栏位使用；`ignore_requirements` 保持 `false`。
- 官方要求自动战斗有稳定至少 60 帧游戏帧率，并使用 Minitouch、MaaTouch 或 MuMu 触控增强；执行前核对实际设置。本次只读学习未验证帧率和触控性能。
- 明确指定有限次数；`Fight.times` 默认极大，不能遗漏。未要求额外补充理智时，药、临期药和源石均关闭。不要顺带运行官方示例中的更新、基建、招募、购物任务。
- 结合回调和结算判定结果，不能把 `start()` 成功、`running()==False` 或“全部任务完成”当作三星通关。失败时保留诊断，不盲目重复消耗理智。

只验证 SDK 加载（不连接设备、不添加任务）：

```powershell
python .agents/skills/maa-battle/scripts/maa_probe.py --user-dir data/maa-probe
```

## ADB 与截图频率

读取 [ADB 连接与低频观察](references/adb-observation.md)。用户要求截图不要频繁：优先在初始页面、关键状态改变、异常和最终结果截图；状态没变时通常隔 30–60 秒以上观察一次，也可更久。先用 MAA 回调和日志了解进度，避免轮询截图。

这个频率用于助手主动观察，**不调整 MAA 内部的截图识别循环**，否则可能错过部署和技能时机。

```powershell
python .agents/skills/maa-battle/scripts/adb_observe.py status
python .agents/skills/maa-battle/scripts/adb_observe.py screenshot --output data/observations/current.png
```

截图助手每次只取一张，跨调用按设备记录至少 30 秒冷却，文件存在则不覆盖；需要新观察时换新文件名。冷却返回 `skipped` 就等待状态或时间变化，不轮换状态目录绕过。先读取返回的图片再判断画面；游戏进程存在不表示它在前台或准备完成。

## 验证边界

已实际验证：SDK 加载及版本、ADB 设备状态、游戏进程、一次截图及查看。验证截图位于项目 `data/observations/arknights-2026-10-10.png`，当时是终端页面。自动战斗流程通过官方文档、本机 Python 包和对应版本核心源码核实；本次学习没有执行作战，也未验证具体作业实战成功。
