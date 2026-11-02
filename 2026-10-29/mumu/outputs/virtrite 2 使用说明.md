# virtrite 2

先退出旧版 Vitrite / Vitrite Fixed，再双击“启动 virtrite 2”快捷方式。程序只显示托盘图标，不打开主窗口，也不切换到 MuMu。

点击需要调节的窗口后，使用主键盘数字键：

| 快捷键 | 操作 |
| --- | --- |
| Ctrl + Shift + 1～9 | 设为 10%～90% 不透明度 |
| Ctrl + Shift + 0 | 设为 100% 不透明 |
| Ctrl + Alt + 0 | 备用的 100% 不透明快捷键 |
| Ctrl + Shift + 加号所在键 | 切换置顶 |

MuMu 可以直接使用上述快捷键，也可以在其他窗口中使用下面的后台快捷键：

| 快捷键 | 操作 |
| --- | --- |
| Ctrl + Alt + Shift + 1～9 | 调节全部 MuMu 的不透明度 |
| Ctrl + Alt + Shift + 0 | 全部 MuMu 设为 100% 不透明 |

“MuMu 设为 50%”快捷方式可在后台启动程序并调节 MuMu；“全部恢复不透明”和“恢复并退出”快捷方式可直接恢复。右键托盘图标也能操作。

普通窗口的恢复操作明确写入 Alpha=255，保留 WS_EX_LAYERED，不使用切换/移除透明样式的办法。MuMu 则通过它使用的 Qt 接口设置不透明度，避免被 MuMu 自身重置而无效或闪屏；Qt 在 100% 时自行移除样式属于正常行为。

适配已在本机 MuMu 模拟器 12、Qt 5.15.6 上实测：半透明、游戏刷新正常、不闪屏。使用 MuMu 自带老板键隐藏、再恢复窗口时，会保留最后设置的透明度；用户已确认恢复时直接半透明显示，不会先闪出不透明画面。Ctrl+Shift+0 会解除半透明保持并恢复 100% 不透明。

其他 MuMu/Qt 版本若接口不匹配会提示失败，不会启用反复移除、增加窗口透明样式的方式。工具向 MuMuPlayer 的界面线程加载桥接 DLL，在运行期间处理窗口显示和样式变化；恢复并退出时清除保持状态并卸载相关钩子。不改游戏/虚拟机进程，不修改 MuMu 安装文件。

可执行程序与运行所需的 DLL 位于 `C:\Users\605\Documents\Output\virtrite 2`，本目录的快捷方式指向该目录。移动程序时，应将 `virtrite 2.exe` 与 `MuMuQtBridge.dll` 一起移动并重新创建快捷方式。源码和构建脚本保存在本目录。

运行错误记录在 `%LOCALAPPDATA%\virtrite 2\virtrite 2.log`。若目标窗口权限更高，程序会提示拒绝访问，需手动以相同权限重启工具。

开发依据：[Qt 窗口不透明度接口](https://doc.qt.io/qt-6/qwidget.html#windowOpacity-prop)、[Windows 窗口不透明度接口](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setlayeredwindowattributes)。
