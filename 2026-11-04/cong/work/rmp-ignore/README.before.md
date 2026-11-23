# 手动 Git 同步

双击 `sync.cmd`，选择目录，再选择初始化、查看状态、下载或上传。操作完成（或出错）后按任意键返回，清屏重新显示主菜单；目录和操作菜单均可输入 `0` 退出。命令行带参数调用仍只执行一次。工具通过本机 Git 执行命令，终端会显示错误，不自动修复冲突。

## 同步范围

- **目录 1：文档\Codex**。包括子目录、文件和空文件夹；所有 `.in`、`.exe` 及超过 100 MiB 的其他安装包除外，使用一个仓库。
- **目录 2：用户目录\.codex**。优先使用环境变量 `CODEX_HOME`，否则使用 `%USERPROFILE%\.codex`；使用另一个仓库。
- 两个仓库相互独立。“文档”的其他目录不属于同步目标。文档\\Codex 会包含被 Git 忽略规则排除的普通文件，但所有 `.in`、`.exe` 都不收录；其他超过 100 MiB 的安装包也排除。

`.codex` 默认同步根目录 AGENTS.md、config.toml、hooks.json、history.jsonl、session_index.jsonl 和同步规则，以及 sessions、archived_sessions、attachments、rules、自定义 skills、prompts、instructions、agents、profiles、hooks。聊天同时收录 `.jsonl` 与 `.jsonl.zst`，按原始字节保存。自带 skills/.system、程序缓存、auth.json、cap_sid、SQLite 和未明确收录的应用状态排除。模型/权限/项目/置顶另存为下述小型偏好快照。配置不再按扩展名笼统放行；其他明确由你维护的配置，可在 `.codex/.gitignore` 的 FileSync 区块后逐个添加，例如 `!/settings.yaml`，上传前检查内容。

`memories/` 使用 `.codex/.filesync-memories/` 中的文件快照同步，包含普通记忆文件、自定义技能和摘要；快照排除任何层级的 .git、.system、认证文件及 SQLite。原 memories/.git 保留。下载只更新快照，恢复到实际 memories 必须单独手动执行。

Codex 配置可能包含你手动填写的密钥；使用私有仓库，并自行检查配置内容。日常同步按原始字节备份文件；换电脑后可用主菜单 10 重建本机聊天列表、正文索引和原始标题。数据库仍不跨电脑同步；项目和置顶可用主菜单 11 从偏好快照恢复，用户目录内的项目路径会适配目标电脑。

## 第一台电脑：第一次设置

1. 在 GitHub 新建两个**空私有仓库**，例如 `codex-documents-sync` 和 `codex-state-sync`。不要自动添加 README、许可证或 .gitignore。不要复用非空 fork 或教学用仓库。
2. 双击 `sync.cmd`，选目录 1，再选初始化；粘贴第一个仓库的地址。
3. 再选目录 1、上传，完成首次提交和上传。
4. 在工具里选目录 2、初始化，粘贴第二个仓库地址，然后选目录 2、上传；允许 Codex 在线运行。

文档\Codex 的本地仓库若已经由助手初始化，仍可以选择初始化来填写远程地址。Git 姓名和邮箱沿用你的现有配置；若缺少，按 Git 错误提示设置。

## 日常使用

- 开始工作前：下载需要使用的目录。
- 上传备份允许 Codex 在线运行；最好等当前回复完成后操作。下载、首次导入、恢复记忆或修复正文索引前先退出 Codex；在线备份不受影响。
- 从电脑 A 换到 B：A 上传完，B 再下载。不要同时修改同一条会话。
- Git 删除文件的记录也会同步。文档\Codex 的空文件夹通过 `.filesync-empty-dirs.json` 保存并在下载后重建；它不会删除已存在的空文件夹。
- `.codex` 不保存无内容的空文件夹。
- 初始化不提交、上传文件。上传 = 暂存全部目标内容、必要时提交、正常推送；下载使用 `git pull --ff-only`；仅有未暂存的 config.toml 本机修改时可保留着下载，远程也修改该文件时 Git 会停止。其他本机修改仍需先处理。
- 没有修改时，“上传”仍会重试之前尚未成功推送的提交。

## 第二台电脑：首次接入

先把完整 FileSync 工具目录复制到新电脑。文档目录仍可在目标不存在时克隆（地址和路径换成自己的）：

```bash
git clone https://github.com/你的用户名/codex-documents-sync.git "$HOME/Documents/Codex"
```

对于已经由应用生成文件的 .codex，使用新入口。若此前只进行了 init、尚无任何本机提交，手动“下载”会自动进入同一首次接入流程，并沿用已有 origin 地址；无需先提交或上传本机自动生成的文件。后台模式不执行首次接入。

首次接入步骤：

1. 先在原电脑用新版工具完成一次上传，确保远程已有 .filesync-memories/manifest.json 和记忆文件。
2. 在新电脑关闭 Codex，双击 sync.cmd，选主菜单 **9 = 首次接入 .codex（先备份，以远程为准）**。
3. 粘贴**已有的 .codex 同步仓库地址**；不是新建空仓库。工具先克隆到临时目录并验证，再自动备份本机受管配置、聊天、附件、技能和记忆。
4. 导入远程受管文件和 Git 历史，并恢复远程记忆。本机仅有的受管聊天和记忆也会从实际目录移走，以远程为准；原内容留在备份。认证、安装程序、数据库和缓存保留，原 memories/.git 始终保留。
5. 检查 config.toml 的本机绝对路径后再启动 Codex；缺少登录状态时重新登录。

新版原文件在 `%USERPROFILE%\.fs-backups\时间戳-标记\files`，旧版备份仍保留在 FileSync/first-connect-backups/时间戳/files；source-path.txt 记录原目录。首次接入使用用户目录下的短临时路径，工具内 Git 操作启用长路径支持，以避免记忆归档在临时目录中超过 Windows 路径限制；原来若有尚无提交的外层 .git，则另存 original-outer-git。备份可能包含旧配置和会话，不会自动上传，请在确认迁移完成后自行决定何时删除。导入中途失败时会尝试还原；若自动还原失败，错误会显示备份路径，可从中手动恢复。

此入口只用于尚无外层 Git 提交历史的新目录，不替换已有同步仓库的历史，也不会执行强推、创建提交或上传。已初始化但尚未提交的空仓库可以接入。远程仍含旧 memories gitlink、认证数据、链接或超出默认白名单的自定义文件时会拒绝导入，先在原电脑处理并上传；额外配置可另行迁移。远程配置含疑似明文凭据时也会停止。

如果已完成接入，日常继续使用一键同步或普通下载。已有本机提交时，除 .codex 仅有未暂存的 config.toml 修改外，普通 pull 仍要求工作区干净，并使用 --ff-only，分叉时停止。config.toml 常被 Codex 自动更新本机程序和插件路径：下载保留这份本机修改，远程同名文件有更新时由 Git 停止以避免覆盖；不会自动提交或上传配置。文档空目录仍在首次下载后重建。

## 命令行用法

在 PowerShell 中（把路径换成工具实际位置）：

```powershell
& "$HOME\Documents\FileSync\sync.cmd" -Target Documents -Action Status
& "$HOME\Documents\FileSync\sync.cmd" -Target Documents -Action Pull
& "$HOME\Documents\FileSync\sync.cmd" -Target Documents -Action Push
& "$HOME\Documents\FileSync\sync.cmd" -Target Codex -Action Init
& "$HOME\Documents\FileSync\sync.cmd" -Target Codex -Action Push
```

`-Root` 可以指定实际目标目录，`-Message` 可以指定提交说明。Git 没加入 PATH 时，工具会尝试标准安装位置 `C:\Program Files\Git\cmd\git.exe`。

## 出错时

进入出错目录，用 Git Bash 查看 `git status`、`git remote -v`。两边历史分叉时，工具会停止；可以自行用 `git pull --no-rebase` 合并、解决冲突，再上传。没有配置上游时，确认远程分支名后执行 `git branch --set-upstream-to=origin/main main`。文档\\Codex 中超过 100 MiB 的安装包（msix、misx、msixbundle、appx、appxbundle、exe、msi、msp，不区分大小写）会自动跳过并写入 .gitignore 的 FileSync 区块，本地文件保留；除 `.exe` 外，小安装包仍同步。所有 `.in`、`.exe` 无论大小都排除。已跟踪的大安装包会停止跟踪，但这一步不删除旧历史中的对象。其他超过 100 MiB 的文件仍会报错，需自行处理或配置 Git LFS。已有 .gitignore 的其他规则保留。

升级时会把已跟踪但现已排除的文件从外层 Git 索引移除，保留本地文件；memories 的 gitlink 也仅从外层索引移除。旧提交中的缓存不会因此立即消失。若 auth.json 或 cap_sid 已被跟踪，工具会停止，需另外清理凭据和历史。config.toml 的常见明文凭据字段会拦截上传，但这不是完整的秘密检测，请自行检查自定义配置。

## 一键同步与定时运行

双击 `sync-all.cmd`，或在主菜单输入 **3**，会依次同步两个目录，并汇总各自完成、跳过或失败的状态。单独一个目录的操作菜单也新增 **5 = 同步**。主菜单 **4** 可以一次下载两个目录。

“同步”执行：保存本地修改并创建提交 → 获取远程更新 → 可以快进时更新本地 → 正常上传。空远程也支持首次上传。本地和远程都有独立提交时会停止，保留本地提交；需你手动合并。两个目录独立处理，一个失败仍会尝试另一个，不保证两个仓库同时成功。

### 设置定时同步

1. 先手动“一键同步”成功，确保两个远程仓库和 GitHub 登录均正常。
2. 在主菜单选择 **5 = 启用定时同步**，输入每天的时间，格式为 24 小时制 `HH:mm`，例如 `22:00`。
3. 需要停止时，选 **6 = 关闭定时同步**。

这是本机 Windows 任务计划程序，按电脑本地时间每天运行一次。首次从下一个所填时间开始；如果今天已过该时间，首次是明天。电脑需开机、联网、当前用户已登录；关机期间不会运行，错过后 Windows 会在条件恢复时补跑。再次选择 5 会替换原任务的时间（也会替换旧的间隔任务）。程序不会要求你输入或保存 Windows 密码，也不会在本次制作工具时自动启用。

后台会记录 `FileSync\logs\sync-*.txt`，最多保留最近 10 份。不会弹出登录提示；登录失效、冲突或网络错误会写入日志，需要你手动排查。

定时任务的 .codex 操作现为在线备份：即使 Codex 正在运行，也会导出记忆快照、暂存并上传；不下载远程文件、不恢复记忆。手动“一键同步”检测到本机 Codex 进程运行时，.codex 同样只上传。检测到暂存期间文件长度或修改时间变化时，本轮停止提交和上传，保留本地文件及暂存状态，下一次备份会重新暂存。其他客户端可能不使用 codex.exe 进程，请自行在下载和恢复前关闭正在写这些文件的应用。

若另一台电脑已上传新提交，在线备份的正常推送可能被拒绝。这时先退出 Codex，手动处理下载或历史分叉，再继续备份；工具不会强推。文档目录仍按原来的双向同步执行。

同一目录的并发同步会停止后来的操作；定时任务也不会重叠执行。未改动时不会新建提交；文档目录仍检查远程更新，后台 .codex 仅重试正常推送。任务运行超过 30 分钟会由 Windows 停止。启用后请保留工具所在路径，搬动工具后需重新启用。

命令行示例（后台模式没有 pause）：

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$HOME\\Documents\\FileSync\\sync.ps1" -Target All -Action Sync
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "$HOME\\Documents\\FileSync\\sync.ps1" -Target All -Action Sync -NonInteractive -Log
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "$HOME\\Documents\\FileSync\\schedule.ps1" -Mode Enable -DailyTime "22:00"
```

`-DocumentsRoot` 和 `-CodexRoot` 可用于一键操作时指定两个自定义目录；单目录仍使用 `-Root`。默认定时任务使用 Windows 的文档路径与 CODEX_HOME/用户目录，不保存这两个自定义参数。

## 记忆快照升级与恢复（v2）

本机工具升级后，主菜单 **7 = 升级/准备 .codex 快照** 会更新规则、解除外层 memories 版本指针、移除自带技能的跟踪，并导出完整记忆快照。不会创建提交或上传；随后选 **3 = 一键同步** 完成提交与上传。原 memories/.git 和记忆内容保持原样。已有每日定时任务会继续调用同一路径的新版脚本。

日常上传 .codex 时会自动更新规则并导出快照；原始文件没有改动时不会新增提交。附件若超过普通 Git 的 100 MiB 限制，工具会报错，需另行备份或自行使用 LFS。

换电脑时：先退出 Codex，再下载，选主菜单 **8 = 恢复记忆快照**。恢复前逐文件对照 SHA-256 基线；本机存在尚未备份的不同内容时，整次恢复在写入前停止。恢复会应用快照中相对基线的文件删除；原文件另存到外层 Git 目录的 filesync-memory-backups/时间戳/files，原 memories/.git 始终保留。备份不上传，可在确认无需回退后自行删除。

下载了尚未恢复的新快照时，后续上传会停止，避免把本机旧记忆重新覆盖到快照。若两台机器都修改了内容，先另存本机记忆，再手动比较处理；工具不强制覆盖，也不自动合并。纯下载后实际 memories 不变；它内部的 .git 状态在恢复后可能显示修改，需由原来的记忆管理流程处理。

命令行：
```powershell
& "$HOME\Documents\FileSync\sync.cmd" -Target Codex -Action Prepare
& "$HOME\Documents\FileSync\sync.cmd" -Target Codex -Action RestoreMemory
```

此方案备份文件和选择性导出的偏好；不跨电脑覆盖 SQLite 或应用完整状态。聊天正文先用主菜单 10 重建，再用 11 恢复设置、项目和置顶。


首次接入的命令行形式（先退出 Codex，已有外层提交历史时会拒绝）：

```powershell
& "$HOME\Documents\FileSync\sync.cmd" -Target Codex -Action FirstConnect -RemoteUrl "https://github.com/你的用户名/codex-state-sync.git"
```


## 2026-10-17 补充同步范围

- `.chatgpt-projects/*/AGENTS.md`：保留项目指令；项目定义和聊天归属由偏好快照单独收录，不复制整份本机元数据。
- `generated_images/`、`visualizations/`、`pets/`：保留作品、自定义资源。空目录不增加上传流量；单文件超过 100 MiB 仍会停止并提示，不悄悄漏掉文件。
- `.filesync-tool/`：自动保存本工具的 8 个运行脚本，以及存在时的 `README.md`；缺少说明书不会阻止同步，缺少运行脚本仍会停止。不含日志、测试目录和本机备份。换电脑后可从这里复制完整工具到文档/FileSync；下载不会自动执行或覆盖已安装脚本。
- `.filesync-memory-archive/`：更新记忆快照前，将被替换或移除的旧文件另存为带哈希清单的历史备份。它参与 Git 同步，但不会自动恢复到 `memories/`，避免旧指令重新生效。未改变的内容不会重复生成备份。

原有聊天、归档、附件、自定义技能仍同步；`.jsonl.zst` 压缩记录原本就在范围内。认证数据、程序和插件缓存、运行中的数据库继续排除。这里只备份插件自定义技能和独立保存的源码，不同步插件安装缓存。超过 100 MiB 安装包的跳过规则不变。

### 换电脑后恢复聊天正文、列表和标题

完成下载或首次接入后，在主菜单选择 **10 = 恢复聊天正文、索引和原始标题**。这个操作需要 Python 3.8 或以上、新版 Git 和可运行的 Codex 引擎；应用应已安装并创建 state 数据库；正文数据库尚不存在、聊天索引为空时，工具会在隔离副本中首次建库并验证，再备份和回填本机索引，不需要先新建或发送对话。修复本机正文索引前请退出 Codex；`--check-only` 隔离检查允许在线进行。新版 .codex 偏好快照也需要 Python 3.8 或以上；文档目录同步只需要 Git 和 PowerShell。

恢复时会显示所用引擎路径，优先使用新版桌面安装位置 `%LOCALAPPDATA%/Programs/Codex/app/resources/codex.exe`，再兼容旧安装位置与 PATH；也可用 `--codex-exe` 显式指定。旧引擎可能无法解析新版记录（例如 `unknown variant modelNotFound`）；工具现在保留 RPC 的具体错误，并显示失败的历史片段和会话 ID，便于定位。

它会在隔离副本中，按依赖顺序逐个重放普通、压缩和归档记录的全部祖先片段，再重放最新片段；不能只读取最新片段，否则可能只剩最后几轮。验证以原始日志引用的精确字节范围为准，逐条核对用户与助手消息的 ID、正文及附件引用，而不是仅比较两次接口读取结果。当前片段没有消息时也会继续恢复其引用的祖先历史。验证通过后，先用 SQLite 一致性备份保存本机数据库，再只修复索引，并从 `session_index.jsonl` 恢复标题。不会发送新提示词或运行模型；本机原始聊天文件、会话 ID 和归档状态保留，不上传数据库。备份及 `report.json` 保存在 `.codex/.filesync-chat-backups/时间戳/`，这部分不上传。

扫描期间原文发生变化，或本机已有消息与恢复结果不同的会话会跳过；写入期间再次变化则事务回滚。它只能恢复现有原始日志包含的内容，不会补写缺失的对话。完成后重新打开会话刷新显示，若仍显示旧缓存，可退出再打开 Codex。排查时可单独运行 `repair-chat-index.py --root "$HOME\.codex" --check-only`，只验证隔离副本，不修改本机索引。

这是针对当前本机数据库结构的修复工具，不等同于完整迁移。历史引用缺失、原生重放失败或原文核对不一致时，会停止本次修复，不回填未通过检查的正文；缺少原始标题时保留客户端提取的标题，不编造原名。客户端将来变更接口或数据库结构时，工具可能停止并保留备份。

命令行：
```powershell
& "$HOME\Documents\FileSync\sync.cmd" -Target Codex -Action RestoreChats
```


## 驱动与运行库备份排除

文档/Codex 中 `*/data/repairs/*/previous-*-driver/` 和 `*/data/repairs/*/runtime-数字*/` 属于可重新安装的驱动、运行库备份，现按目录排除；本地文件保留，修复记录、脚本和普通项目文件继续同步。超过 100 MiB 安装包仍按原规则跳过。这些排除同时用于上传和下载前的状态检查，不受强制暂存普通文档的参数影响。

只停止跟踪不会移除旧提交中的文件。清理历史后，其他电脑不要直接合并旧历史，否则可能重新带回大对象；先备份未上传文件，再重新克隆清理后的文档仓库，并复制自己的新文件。`.codex` 仓库不受这次文档历史清理影响。


## 模型、权限、项目和置顶（v7）

此前只有 `config.toml` 和聊天日志，未备份桌面应用的偏好与聊天组织信息。新版上传、准备快照或初始化 .codex 时，会自动生成 `.filesync-preferences.json`，日常上传仍允许 Codex 在线运行。这部分需要 Python 3.8 或以上；无变化时内容保持一致，不为时间戳制造新提交。

快照收录：config.toml 根级的默认模型、推理强度、回复详细度、服务档位和权限偏好；应用中的完全访问显示开关、本机权限模式、最近模型选择和项目侧栏排序；本机项目名称/根目录/顺序；每个已导入聊天的项目、置顶、分组和顺序。不会复制认证、远程主机连接、MCP 命令、安装路径、提示词草稿、应用数据库或整份 `.codex-global-state.json`。快照包含聊天 ID、项目路径和名称，请继续使用私有仓库。

换电脑时：原电脑用新版工具上传 → 新电脑退出 Codex 后下载 → 主菜单 **10** 恢复聊天正文 → **11 = 恢复模型、权限、项目和置顶快照**。已有本机聊天时也可直接执行 11。恢复先备份到 `.codex/.filesync-preferences-backups/时间戳/`，匹配已有项目根目录，重建目标电脑的 ID 关联；未知应用字段和本机程序/插件路径保留。用户目录内的项目路径用目标电脑用户目录展开；用户目录外的绝对路径保留，目录结构不同需手动调整项目根目录。不会启动模型或发送消息。

恢复覆盖快照所含聊天的这几项组织信息，以及快照明确记录的设置；目标电脑独有的聊天和项目保留。快照中的部分聊天尚未导入时，先恢复已有聊天并报告待恢复 ID；待恢复条目继续保留在快照及本机基线中，不会阻止其他条目，也不会被之后的导出或菜单 12 丢弃。即使聊天之后才导入，导出也不会用其空偏好覆盖待恢复内容；可再次运行 11，或在已恢复快照后运行 12 应用这些内容。项目路径重复或 ID 冲突时仍停止，不猜测映射。已下载但从未恢复的快照会阻止后续上传，避免新电脑自动生成的空置顶/项目覆盖原备份。恢复需关闭 Codex，在线导出不受影响。数据库结构将来变化时可能停止，应保留备份排查。

**旧备份的限制：**旧版本未保存的置顶和偏好不能从对话文本精确还原。请在原电脑运行新版工具上传一次，再在新电脑下载并用 11 恢复。原电脑不可用时，主菜单 **12 = 旧备份按工作目录重建项目归属** 可将尚无归属的聊天分配给唯一匹配的现有项目；按最长目录前缀匹配，歧义跳过。这是推断，会保留已有归属，不猜测置顶。从原电脑下载了新版偏好快照时，请优先使用 11；尚未恢复的快照会阻止 12，以免推断覆盖原归属。可以先只检查结果：

```powershell
python "$HOME\Documents\FileSync\codex-preferences.py" --root "$HOME\.codex" --infer-projects --check-only
python "$HOME\Documents\FileSync\codex-preferences.py" --root "$HOME\.codex" --restore --check-only
& "$HOME\Documents\FileSync\sync.cmd" -Target Codex -Action RestorePreferences
```

仅有旧备份时，先运行 12 再上传。12 会同时更新本机归属、偏好快照及其基线，再运行 11 也不会用旧快照撤销刚重建的归属；失败时一起回滚。旧版在 12 后直接运行 11 会被旧快照撤销，已在 v7.1 修复。恢复不改变聊天正文、标题或归档状态，也不会关闭原 memories/.git。


## Git 姓名/邮箱与 GitHub 登录（v7.2）

`Author identity unknown`、`unable to auto-detect email address` 表示缺少 Git 提交者姓名/邮箱，与 GitHub 登录分开。新版手动上传/同步会先检测提交身份，提示填写缺少的姓名或邮箱，保存到当前 Windows 用户的 Git 全局配置；已有信息不覆盖。邮箱可使用 GitHub 邮箱设置中提供的 `noreply` 地址，请自行填写，不根据 Windows 用户名编造。

主菜单 **13 = 设置 Git 姓名/邮箱并登录 GitHub**，默认使用文档/Codex 的远程地址。也可在单目录操作菜单选 **8**，或运行 `sync.cmd -Target Codex -Action Login`。完成缺少的身份设置后，会用 Git for Windows 自带的 Git Credential Manager（GCM）打开浏览器授权；即使已有账号，也可用此入口重新登录。账号凭据由 GCM 保存在 Windows 的凭据存储中，不写入 FileSync、同步快照或 Git 仓库。此入口本身不提交、下载或上传文件。

对于 `https://github.com/...`：手动上传、下载和首次接入前，会检查 GCM 账号缓存及远程可读性。没有缓存账号时打开登录；明确的认证失效会重新登录并只重试一次。缓存存在不等于账号有效，因此还会执行只读取远程 HEAD 的检查，不下载仓库正文。读取成功也不保证有推送权限，写入权限由实际上传检查。网络/代理故障、错误仓库地址和权限不足不会触发反复登录。取消登录会停止本轮操作。

登录时仅为所选仓库的 GitHub 地址设置 GCM 凭据助手；其他仓库/平台的助手配置保留。首次接入尚无仓库时，GCM 设置应用于新克隆的仓库。SSH 地址继续使用原来的 SSH 密钥，不自动转换协议；其他 Git 平台沿用原有认证。未安装 GCM 时普通同步沿用现有 Git 认证并提示，浏览器登录入口会说明需要在 Git for Windows 安装程序中启用 GCM。

定时/`-NonInteractive` 模式不会询问姓名邮箱或弹出登录窗口；身份缺失或认证失败会记录明确提示并停止。请先手动运行 13 完成设置，再使用一键同步或定时备份。若文档仓库不在默认位置，可用 `-Target Documents -Root "实际路径" -Action Login`。


## 排除输入文件与可执行文件（v7.3）

所有同步范围排除 `.in` 和 `.exe`，包括大写/混合大小写扩展名。文档/Codex 的强制暂存、上传大小检查、下载前状态检查均使用相同排除规则；.codex 的附件、自定义技能、记忆快照和历史记忆快照也排除这两类文件。首次接入的远程仍包含它们时会提示超出范围，先在原电脑用新版工具解除跟踪并上传，再接入。

本地文件保留。以后生成的 `.in`、`.exe` 按全局指令放在 `C:/Users/605/Documents/Output`，不要放进文档/Codex。文档同步会将已跟踪的两类文件从 Git 索引解除，其他修改保留；下一次上传提交这些移除记录后，远程的最新版本才会去掉它们。其他电脑更新前请自行保留所需的旧文件，因为 Git 的删除记录也会同步。

这是同步排除规则，不改写已有提交历史。已有提交中的文件对象仍可能占用 .git 空间；不直接删除 pack、index、HEAD 或 refs。中断操作留下且确认无进程使用的临时文件可以单独清理，历史瘦身需要另行处理。记忆快照读取旧清单时也过滤这两类文件，避免升级后因为旧清单仍列着它们而校验失败。
