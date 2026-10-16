# ADB 连接与低频观察

依据：[Android 官方 ADB 文档](https://developer.android.com/tools/adb?hl=zh-cn)，以及 2026-10-10 对本机 ADB 的实际调用。

## 连接顺序

本机 ADB 不在 PATH，使用已核实的完整路径；地址来自现有连接，不扫描或猜测其他实例端口。

```powershell
$arkAdb = 'C:\Program Files\YXArkNights-12.0\shell\adb.exe'
& $arkAdb version
& $arkAdb devices -l
& $arkAdb -s '127.0.0.1:16384' get-state
& $arkAdb -s '127.0.0.1:16384' shell pidof com.hypergryph.arknights
```

已显示目标 `device` 就复用。目标不在列表且已核实模拟器打开、地址正确时，运行 `& $arkAdb connect '127.0.0.1:16384'`，再检查列表；别把 `offline`、`unauthorized` 当已连接。多设备时每条设备命令都明确 `-s`，不使用默认设备。

只读观察可使用 `shell dumpsys window windows`、`shell dumpsys activity activities` 了解焦点，用 `shell wm size` 辅助了解尺寸。不同 Android 版本输出字段不同，筛不到 `mCurrentFocus` 不等于游戏退出；进程存在也不等于前台显示，用实际截图核实。

当前 MuMu 原始 `wm size` 为 720×1280，但横屏截图是 1280×720。未来若需要本次已授权的点击，先读取新图和实际尺寸、旋转与缩放，再定位；不能把格子坐标或旧画面坐标直接用于 tap。

## 截图方法与频率

使用 `adb -s SERIAL exec-out screencap -p`，由 Python `subprocess.run([...], capture_output=True)` 获取二进制 PNG 并写文件。避免依赖 PowerShell 文本管道/重定向保存图片，以免版本差异损坏字节。无需在模拟器内保存截图再 pull。

项目助手 `../scripts/adb_observe.py`：

```powershell
python .agents/skills/maa-battle/scripts/adb_observe.py status
python .agents/skills/maa-battle/scripts/adb_observe.py screenshot --output data/observations/phase-01.png --interval 60
```

- `status` 不截图、不点击。`screenshot` 每次只取一张 PNG，校验签名和尺寸，拒绝覆盖现有文件。
- 默认间隔 30 秒，可调长。按设备的时间戳与锁保存在本机临时目录 `maa-adb-observation`，跨调用生效；`skipped` 表示没有获取新截图。异常中断留下锁时先检查是否仍有截图任务，仅清理确认过的该设备锁。
- 使用同一观察状态目录，避免多实例竞相截图。优先初始、状态变更、异常和结果节点；普通观察间隔 30–60 秒或更久。不为展示进度连续刷新，也不新建录屏或后台截图循环。
- 降低的是助手主动观察频率，不改 MAA 内部识别帧率。作战运行时主要跟踪回调与日志，只有需要理解画面时才取图。
- 截图后用图片查看工具实际读取保存文件，不能仅凭路径存在声称看见了画面。

本次验证只拍了一张 `data/observations/arknights-2026-10-10.png`，观察到终端页面，未发送 tap/swipe/keyevent 或启动作战。截图是历史证据，不能当作后续会话的实时画面。

连接检查不需要 kill-server、disconnect 全部设备、root、安装应用或修改模拟器设置。输入操作与游戏导航属于后续实际任务范围，按当前任务授权进行。
