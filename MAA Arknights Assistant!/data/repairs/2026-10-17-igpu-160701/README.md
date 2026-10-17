# MAA 更新日志崩溃：已验证的绕过方案

2026-10-17 16:45，用户手动重新打开 MAA，确认更新日志正常打开，不再报错。本轮没有重启电脑，没有操作 MAA 界面。

仅替换 `D:\MAA-Arknights-Assistant\data\CHANGELOG.md`：将 114 处贡献者名称预先写成 GitHub 文字链接，保留正文，避免 MAA 自动插入头像及合并头像昵称。未替换程序、运行库、配置、干员数据或作业。

- 原件：`CHANGELOG.pre-avatar-test.md`
- 当前有效候选：`CHANGELOG.link-only.md`
- 应用/恢复：`switch-changelog-test.ps1`
- 完整排查及局限：`investigation-continued.md`

若要恢复，先手动完全退出 MAA，然后在此目录运行：

```powershell
.\switch-changelog-test.ps1 -Mode Restore
```

恢复脚本校验哈希；如果日志已被 MAA 更新，不会覆盖新内容。MAA 后续更新可能覆盖本次缓存绕过，出现复发时需按新日志重新生成候选，不能直接覆盖旧候选。

这解决了当前更新日志窗口的触发问题；不能据此认定模拟器随机崩溃、桌面和 Endfield 花屏已经修复，也不能确定问题只来自应用、WPF、系统或驱动中的某一方。
