# Vitrite Fixed

这是独立重写的 Vitrite 替代程序，适用于 64 位 Windows 10 / 11。

## 使用

1. 右键原版 Vitrite 的托盘图标，选择 Exit。
2. 双击 `Vitrite Fixed.exe`。程序在系统托盘运行。
3. 点击需要调整的窗口，再使用快捷键。
4. 结束使用时，右键本程序的托盘图标，选择“退出”。

| 快捷键 | 作用 |
| --- | --- |
| Ctrl + Shift + 1～9 | 设置为 10%～90% 不透明度 |
| Ctrl + Shift + 0 | 恢复为 100% 不透明 |
| Ctrl + Alt + 0 | 备用恢复快捷键 |
| Ctrl + Shift + 加号所在键 | 切换窗口置顶 |

数字键使用主键盘上方的一排。

## 改动

原版的 0 键会移除 WS_EX_LAYERED 属性；本程序对已透明窗口直接设置 Alpha=255，保留该属性。Windows 定义 Alpha=255 为完全不透明。这样绕过原版恢复操作的处理路径；并不代表已确定 Milthm 中原快捷键失效的根因。

使用低级键盘钩子，在本程序内监听上述快捷键，不注入其他程序，不记录按键内容。窗口更改在键盘回调返回后执行。程序不修改游戏文件，也不设置自动启动。退出不会自动恢复此前调整过的窗口。

对以管理员身份运行的窗口，普通权限可能无法更改其属性；需要时可将本程序以管理员身份运行。受保护窗口及特殊全屏渲染窗口仍可能不支持透明度调整。

## 验证范围

本地验证快捷键识别、备用恢复键、长按过滤、1～9 各级不透明度及恢复后的原生属性读回、窗口置顶和取消置顶。Milthm 的直接恢复路径另行实测。完整物理快捷键在 Milthm 中的效果，需要退出原版后实际按键确认。

## 来源

- 原版行为参考：https://github.com/ryanvm/vitrite/blob/master/src/VitriDLL/VitriDLL.c
- 完全不透明的定义：https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setlayeredwindowattributes
- 键盘钩子说明：https://learn.microsoft.com/en-us/windows/win32/winmsg/lowlevelkeyboardproc

源代码为同目录下的 `Vitrite Fixed.cs`，为独立实现。
