param(
    [ValidateSet('Documents', 'Codex', 'All')][string]$Target = 'Documents',
    [ValidateSet('Menu', 'Init', 'Status', 'Pull', 'Push', 'Sync', 'Prepare', 'RestoreMemory', 'FirstConnect', 'RestoreChats', 'RestorePreferences', 'InferProjects', 'Login')][string]$Action = 'Menu',
    [string]$Root,
    [string]$RemoteUrl,
    [string]$Message,
    [string]$DocumentsRoot,
    [string]$CodexRoot,
    [switch]$NonInteractive,
    [switch]$Log
)

$ErrorActionPreference = 'Stop'
[Console]::OutputEncoding = New-Object System.Text.UTF8Encoding($false)
$OutputEncoding = [Console]::OutputEncoding
$utf8 = New-Object System.Text.UTF8Encoding($false)
$codexIgnore = @'
# FileSync: only configuration, instructions and conversations
/*
!/.gitignore
!/.gitattributes
!/*.toml
!/*.md
!/*.yaml
!/*.yml
!/*.ini
!/*config*.json
!/hooks.json
!/history.jsonl
!/session_index.jsonl
!/sessions/
!/archived_sessions/
!/rules/
!/skills/
!/prompts/
!/instructions/
!/agents/
!/profiles/
!/config/
!/hooks/
!/memories/
auth.json
*.sqlite
*.sqlite-shm
*.sqlite-wal
'@

. (Join-Path $PSScriptRoot 'codex-state.ps1')
. (Join-Path $PSScriptRoot 'first-connect.ps1')

function Invoke-GitProbe {
    param([string[]]$GitArgs)
    # Windows PowerShell 5 drops empty native arguments unless explicitly quoted.
    $nativeArgs = @($GitArgs | ForEach-Object { if ($_ -ceq '' -and $PSVersionTable.PSVersion.Major -lt 7) { '""' } else { $_ } })
    $old = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try { $output = @(& $script:Git -c core.quotePath=false -c core.longpaths=true -C $script:Root @nativeArgs 2>&1); $code = $LASTEXITCODE }
    finally { $ErrorActionPreference = $old }
    $lines = @($output | ForEach-Object { [string]$_ } | Where-Object { $_ -and $_ -ne 'System.Management.Automation.RemoteException' })
    return [pscustomobject]@{ Code = $code; Output = $lines }
}

function Invoke-Git {
    param([string[]]$GitArgs, [switch]$Capture, [int[]]$Allowed = @(0))
    Write-Host ('> git ' + ($GitArgs -join ' ')) -ForegroundColor DarkGray
    $result = Invoke-GitProbe $GitArgs
    $code = $result.Code
    if ($code -notin $Allowed) {
        $result.Output | ForEach-Object { Write-Host $_ }
        throw "Git 返回 $code，请按上面的输出排查。"
    }
    if ($Capture) { return $result.Output }
    $result.Output | ForEach-Object { Write-Host $_ }
}

function Ensure-GitIdentity {
    $author = Invoke-GitProbe @('var', 'GIT_AUTHOR_IDENT')
    $committer = Invoke-GitProbe @('var', 'GIT_COMMITTER_IDENT')
    if ($author.Code -eq 0 -and $committer.Code -eq 0) { return }
    if ($NonInteractive) { throw 'Git 提交者姓名/邮箱未配置或无效；请手动打开 FileSync 选 13 完成设置，再启用定时同步。' }
    Write-Host 'Git 提交者信息尚未配置。这与 GitHub 登录分开；以下只补齐当前 Windows 用户缺少的 Git 姓名/邮箱。' -ForegroundColor Yellow
    $name = [string]((Invoke-GitProbe @('config', '--get', 'user.name')).Output -join '')
    $email = [string]((Invoke-GitProbe @('config', '--get', 'user.email')).Output -join '')
    $setName = -not $name.Trim(); $setEmail = -not $email.Trim()
    if ($setName) { $name = (Read-Host '提交者姓名（可用 GitHub 用户名；留空取消）').Trim() }
    if ($setEmail) { $email = (Read-Host '提交邮箱（可填 GitHub 提供的 noreply 邮箱；留空取消）').Trim() }
    if (-not $name -or $name -match '[<>\r\n]' -or $email -notmatch '^[^<>\s@]+@[^<>\s@]+$') { throw '姓名或邮箱为空/格式无效，未保存；请重新运行 13。' }
    if ($setName) { Invoke-Git @('config', '--global', 'user.name', $name) }
    if ($setEmail) { Invoke-Git @('config', '--global', 'user.email', $email) }
    if ((Invoke-GitProbe @('var', 'GIT_AUTHOR_IDENT')).Code -ne 0 -or (Invoke-GitProbe @('var', 'GIT_COMMITTER_IDENT')).Code -ne 0) {
        throw 'Git 身份仍无效，请检查仓库级 author/committer 配置或相关环境变量。'
    }
}

function Get-GitHubRemote {
    param([string]$Url)
    $uri = $null
    if (-not [Uri]::TryCreate($Url, [UriKind]::Absolute, [ref]$uri) -or $uri.Scheme -ne 'https' -or $uri.Host -ine 'github.com') { return $null }
    if ($uri.UserInfo.Contains(':') -or $uri.Query -or $uri.Fragment) { throw '请将 GitHub 远程地址改为普通 HTTPS 仓库地址，不在 URL 中保存密码、令牌或查询参数。' }
    return $uri
}

function Start-GitHubLogin {
    param([Uri]$Remote)
    if ($NonInteractive) { throw '后台模式不能打开登录窗口。请手动运行主菜单 13。' }
    Write-Host '正在打开 GitHub 浏览器登录，请在浏览器完成授权；关闭或取消后本轮停止。' -ForegroundColor Cyan
    $saved = @{}
    foreach ($key in @('GCM_INTERACTIVE', 'GCM_GUI_PROMPT', 'GIT_TERMINAL_PROMPT')) { $saved[$key] = [Environment]::GetEnvironmentVariable($key, 'Process') }
    try {
        $env:GCM_INTERACTIVE = 'true'; $env:GCM_GUI_PROMPT = 'true'; $env:GIT_TERMINAL_PROMPT = '1'
        $loginArgs = @('-C', $script:Root, 'credential-manager', 'github', 'login', '--url', 'https://github.com', '--browser', '--force')
        if ($Remote.UserInfo) { $loginArgs += @('--username', [Uri]::UnescapeDataString($Remote.UserInfo)) }
        & $script:Git @loginArgs
        if ($LASTEXITCODE -ne 0) { throw 'GitHub 登录未完成或已取消，未继续同步。' }
    } finally {
        foreach ($key in $saved.Keys) { [Environment]::SetEnvironmentVariable($key, $saved[$key], 'Process') }
    }
    # Scope helper selection to this repository and GitHub only; tokens stay in GCM.
    if (Test-Path -LiteralPath (Join-Path $script:Root '.git')) {
        Invoke-Git @('config', '--local', '--replace-all', 'credential.https://github.com.helper', '')
        Invoke-Git @('config', '--local', '--add', 'credential.https://github.com.helper', 'manager')
    } else {
        $script:GitHubUseGcmForClone = $true
    }
}

function Test-RemoteAccess {
    param([string]$Url)
    $saved = @{}
    foreach ($key in @('GCM_INTERACTIVE', 'GIT_TERMINAL_PROMPT')) { $saved[$key] = [Environment]::GetEnvironmentVariable($key, 'Process') }
    try {
        $env:GCM_INTERACTIVE = 'Never'; $env:GIT_TERMINAL_PROMPT = '0'
        $probeArgs = @('-c', 'credential.interactive=false', '-c', 'http.lowSpeedLimit=1', '-c', 'http.lowSpeedTime=20')
        if ($script:GitHubUseGcmForClone) { $probeArgs += @('-c', 'credential.helper=', '-c', 'credential.helper=manager') }
        return (Invoke-GitProbe ($probeArgs + @('ls-remote', '--', $Url, 'HEAD')))
    } finally {
        foreach ($key in $saved.Keys) { [Environment]::SetEnvironmentVariable($key, $saved[$key], 'Process') }
    }
}

function Ensure-GitHubAccess {
    param([string]$Url, [switch]$Login)
    $remote = Get-GitHubRemote $Url
    if ($null -eq $remote) {
        if ($Login) { throw '浏览器登录入口适用于 https://github.com 的远程地址；SSH 地址请使用已配置的 SSH 密钥，其他平台使用原有认证方式。' }
        return
    }
    if ($Login -and $NonInteractive) { throw '后台模式不能打开登录窗口，请手动运行主菜单 13。' }
    $gcm = Invoke-GitProbe @('credential-manager', '--version')
    if ($gcm.Code -ne 0) {
        if ($Login) { throw '未安装 Git Credential Manager。请在 Git for Windows 安装程序中启用它，再运行 13。' }
        Write-Host '未找到 Git Credential Manager，将沿用现有 Git 认证；需要浏览器登录时请安装 GCM 后运行 13。' -ForegroundColor Yellow
        return
    }
    $didLogin = $false
    if (-not $NonInteractive) {
        $accounts = Invoke-GitProbe @('credential-manager', 'github', 'list', '--url', 'https://github.com', '--no-ui')
        if ($accounts.Code -ne 0) { throw '无法读取 GitHub 账号缓存；请检查 Git Credential Manager，未将此错误当作已退出登录。' }
        if ($Login -or $accounts.Output.Count -eq 0) { Start-GitHubLogin $remote; $didLogin = $true }
    }
    $check = Test-RemoteAccess $Url
    if ($check.Code -eq 0) { Write-Host 'GitHub 远程读取检查通过；上传时仍会检查写入权限。'; return }
    $detail = $check.Output -join "`n"
    $authFailure = $detail -match '(?i)authentication failed|invalid username|invalid credentials|could not read (username|password)|terminal prompts disabled|HTTP[^\r\n]*401|unable to get (credential|authentication)'
    if ($authFailure -and -not $NonInteractive -and -not $didLogin) {
        Start-GitHubLogin $remote
        $check = Test-RemoteAccess $Url
        if ($check.Code -eq 0) { Write-Host 'GitHub 登录及远程读取检查通过。'; return }
        $detail = $check.Output -join "`n"
    }
    $check.Output | ForEach-Object { Write-Host $_ }
    if ($NonInteractive) { throw '后台远程检查失败，未弹窗。请检查网络/仓库权限；需要重新登录时手动运行主菜单 13。' }
    if ($detail -match '(?i)repository not found|403|permission denied') { throw '仓库地址或账号权限不匹配；登录成功不代表有此仓库权限，可用 13 更换账号后重试。' }
    throw 'GitHub 远程检查未通过，请检查网络、代理或认证；需要重新登录可运行主菜单 13。'
}

function Require-Repo {
    if (-not (Test-Path -LiteralPath (Join-Path $script:Root '.git'))) { throw '先选择“初始化”，或在第二台电脑克隆仓库到目标目录。' }
    $top = [string](Invoke-Git @('rev-parse', '--show-toplevel') -Capture)
    if ([IO.Path]::GetFullPath($top).TrimEnd('\', '/') -ine $script:Root.TrimEnd('\', '/')) { throw '目标目录不是仓库根目录，请检查 -Root。' }
}

function Update-ExcludedExtensionsIgnore {
    $path = Join-Path $script:Root '.gitignore'
    $old = ''
    if (Test-Path -LiteralPath $path) { $old = [IO.File]::ReadAllText($path) }
    $pattern = '(?ms)^# FileSync: excluded extensions begin\r?\n.*?^# FileSync: excluded extensions end(?:\r?\n|$)'
    $text = [regex]::Replace($old, $pattern, '').TrimEnd([char]13, [char]10)
    if ($text) { $text += "`n`n" }
    $text += "# FileSync: excluded extensions begin`n*.[iI][nN]`n*.[eE][xX][eE]`n# FileSync: excluded extensions end`n"
    if ($text -cne $old) { [IO.File]::WriteAllText($path, $text, $utf8) }
}

function Remove-ExcludedExtensionsFromIndex {
    Invoke-Git @('rm', '-r', '--cached', '--ignore-unmatch', '--', ':(top,icase,glob)**/*.in', ':(top,icase,glob)**/*.exe')
}

function Save-EmptyDirs {
    param([string[]]$Excluded = @())
    $queue = New-Object 'System.Collections.Generic.Queue[string]'
    $empty = New-Object 'System.Collections.Generic.List[string]'
    $queue.Enqueue($script:Root)
    while ($queue.Count) {
        $dir = $queue.Dequeue()
        $items = @(Get-ChildItem -LiteralPath $dir -Force)
        if ($dir -ne $script:Root -and $items.Count -eq 0) { $empty.Add($dir.Substring($script:Root.Length + 1).Replace('\', '/')) }
        foreach ($item in $items) {
            if ($item.Name -eq '.git') {
                if ($dir -ne $script:Root) { throw "有嵌套 Git 仓库：$dir。请先处理，再同步整个目录。" }
                continue
            }
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "目录内有链接：$($item.FullName)。请自行确定如何同步。" }
            if ($item.PSIsContainer) {
                $relative = $item.FullName.Substring($script:Root.Length + 1).Replace('\', '/')
                if (-not (Test-DocumentsExcludedPath -Path $relative -Excluded $Excluded)) { $queue.Enqueue($item.FullName) }
            }
        }
    }
    $json = ConvertTo-Json -InputObject @($empty | Sort-Object) -Compress
    [IO.File]::WriteAllText((Join-Path $script:Root '.filesync-empty-dirs.json'), $json + "`n", $utf8)
}

function Restore-EmptyDirs {
    $manifest = Join-Path $script:Root '.filesync-empty-dirs.json'
    if (-not (Test-Path -LiteralPath $manifest)) { return }
    [string[]]$dirs = ConvertFrom-Json -InputObject (Get-Content -LiteralPath $manifest -Raw -Encoding UTF8)
    foreach ($dir in $dirs) {
        $path = [IO.Path]::GetFullPath((Join-Path $script:Root $dir))
        if (-not $path.StartsWith($script:Root.TrimEnd('\') + '\', [StringComparison]::OrdinalIgnoreCase)) { throw '空目录清单含有目标目录之外的路径。' }
        [IO.Directory]::CreateDirectory($path) | Out-Null
    }
}

function Get-DocumentsExclusions {
    $extensions = @('.msix', '.misx', '.msixbundle', '.appx', '.appxbundle', '.msi', '.msp')
    $queue = New-Object 'System.Collections.Generic.Queue[string]'
    $queue.Enqueue($script:Root)
    while ($queue.Count) {
        foreach ($item in @(Get-ChildItem -LiteralPath $queue.Dequeue() -Force)) {
            if ($item.Name -eq '.git' -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { continue }
            if ($item.PSIsContainer) {
                $relative = $item.FullName.Substring($script:Root.Length + 1).Replace('\', '/')
                if ($relative -match '(^|/)data/repairs/[^/]+/(previous-[^/]+-driver|runtime-[0-9][^/]*)$') { $relative; continue }
                $queue.Enqueue($item.FullName)
            }
            elseif ($item.Length -gt 100MB -and $item.Extension.ToLowerInvariant() -in $extensions) {
                $item.FullName.Substring($script:Root.Length + 1).Replace('\', '/')
            }
        }
    }
}

function Test-DocumentsExcludedPath {
    param([string]$Path, [string[]]$Excluded)
    if ($Path -match '(?i)\.(in|exe)$') { return $true }
    foreach ($entry in $Excluded) {
        if ($Path -ieq $entry -or $Path.StartsWith($entry.TrimEnd('/') + '/', [StringComparison]::OrdinalIgnoreCase)) { return $true }
    }
    return $false
}

function Update-InstallerIgnore {
    param([string[]]$Paths)
    $ignorePath = Join-Path $script:Root '.gitignore'
    $old = ''
    if (Test-Path -LiteralPath $ignorePath) { $old = [IO.File]::ReadAllText($ignorePath) }
    $pattern = '(?ms)^# FileSync: large installers begin\r?\n.*?^# FileSync: large installers end(?:\r?\n|$)'
    $text = [regex]::Replace($old, $pattern, '')
    if ($Paths.Count) {
        if ($text.Length -and -not $text.EndsWith("`n")) { $text += "`n" }
        $lines = @('# FileSync: large installers begin', '# Large installers and repair driver/runtime backups; local files are retained')
        foreach ($path in @($Paths | Sort-Object)) {
            $lines += '/' + [regex]::Replace($path, '([*?\[\]#! ])', '\$1')
        }
        $lines += '# FileSync: large installers end'
        $text += ($lines -join "`n") + "`n"
    }
    if ($text -cne $old) { [IO.File]::WriteAllText($ignorePath, $text, $utf8) }
    Update-ExcludedExtensionsIgnore
}

function Save-Changes {
    Require-Repo
    Ensure-GitIdentity
    $pushUrl = [string](Invoke-Git @('remote', 'get-url', '--push', 'origin') -Capture)
    Ensure-GitHubAccess $pushUrl
    if ($Target -eq 'Codex') {
        $auth = @(Invoke-Git @('ls-files', '--', 'auth.json') -Capture)
        if ($auth.Count) { throw 'auth.json 已被跟踪，请先从仓库和历史中处理登录凭据，再同步。' }
        Update-CodexRules
        Check-CodexConfig
        Export-MemorySnapshot
        Invoke-CodexPreferences export
        Export-FileSyncTool
    } else {
        $installers = @(Get-DocumentsExclusions)
        Update-InstallerIgnore -Paths $installers
        Remove-ExcludedExtensionsFromIndex
        foreach ($path in $installers) {
            Write-Host ("跳过安装包/驱动或运行库备份（保留本地文件）：" + $path) -ForegroundColor Yellow
            Invoke-Git @('rm', '-r', '--cached', '--ignore-unmatch', '--', $path)
        }
        Save-EmptyDirs -Excluded $installers
    }
    $listArgs = @('ls-files', '--cached', '--others')
    if ($Target -eq 'Codex') { $listArgs += '--exclude-standard' }
    $paths = @(Invoke-Git $listArgs -Capture)
    foreach ($path in $paths) {
        if ($Target -eq 'Documents' -and (Test-DocumentsExcludedPath -Path $path -Excluded $installers)) { continue }
        $file = Join-Path $script:Root $path
        if ((Test-Path -LiteralPath $file -PathType Leaf) -and (Get-Item -LiteralPath $file -Force).Length -gt 100MB) { throw "文件超过 GitHub 普通 Git 的 100 MiB 限制：$path。请自行配置 Git LFS。" }
    }
    $addArgs = @('add', '-A')
    if ($Target -eq 'Documents') {
        $addArgs += @('-f', '--', '.')
        $addArgs += @(':(top,icase,glob,exclude)**/*.in', ':(top,icase,glob,exclude)**/*.exe')
        foreach ($path in $installers) { $addArgs += ':(top,literal,exclude)' + $path }
    }
    $stamps = @{}
    if ($Target -eq 'Codex') {
        foreach ($path in $paths) {
            $file = Join-Path $script:Root $path
            if (Test-Path -LiteralPath $file -PathType Leaf) {
                $item = Get-Item -LiteralPath $file -Force
                $stamps[$path] = [string]$item.Length + ':' + $item.LastWriteTimeUtc.Ticks
            }
        }
    }
    Invoke-Git $addArgs
    if ($Target -eq 'Codex') {
        foreach ($path in $stamps.Keys) {
            $file = Join-Path $script:Root $path
            if (-not (Test-Path -LiteralPath $file -PathType Leaf)) { throw '备份期间文件被移走，本轮未提交或上传，请稍后重试。' }
            $item = Get-Item -LiteralPath $file -Force
            $stamp = [string]$item.Length + ':' + $item.LastWriteTimeUtc.Ticks
            if ($stamp -cne $stamps[$path]) { throw '备份期间文件仍在写入，本轮未提交或上传，请稍后重试。' }
        }
    }
    $changed = @(Invoke-Git @('diff', '--cached', '--name-only') -Capture)
    if ($changed.Count) {
        if (-not $Message) { $Message = 'sync ' + $Target + ' ' + (Get-Date -Format 'yyyy-MM-dd HH:mm:ss') }
        Invoke-Git @('commit', '-m', $Message)
    } else { Write-Host '没有新的文件修改；仍会推送之前尚未上传的提交。' }
}

$syncMutex = $null
$mutexHeld = $false
$transcript = $false
try {
    if ($NonInteractive) {
        $env:GIT_TERMINAL_PROMPT = '0'
        $env:GCM_INTERACTIVE = 'Never'
        if (-not $env:GIT_SSH_COMMAND) { $env:GIT_SSH_COMMAND = 'ssh -o BatchMode=yes' }
        if ($Action -in @('Menu', 'Init', 'FirstConnect', 'Login')) { throw '定时模式不接受菜单、初始化或登录；请先手动完成配置和登录。' }
    }
    if ($Log) {
        $logDir = Join-Path $PSScriptRoot 'logs'
        [IO.Directory]::CreateDirectory($logDir) | Out-Null
        Get-ChildItem -LiteralPath $logDir -Filter 'sync-*.txt' | Sort-Object LastWriteTime -Descending | Select-Object -Skip 9 | Remove-Item
        $logPath = Join-Path $logDir ('sync-' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff') + '-' + [Guid]::NewGuid().ToString('N').Substring(0,6) + '.txt')
        Start-Transcript -LiteralPath $logPath | Out-Null
        $transcript = $true
    }
    if ($Action -eq 'Menu') {
        Write-Host '1 = 文档\Codex，2 = 用户目录\.codex'
        Write-Host '3 = 一键同步两个目录，4 = 一键下载两个目录'
        Write-Host '5 = 启用定时同步，6 = 关闭定时同步'
        Write-Host '7 = 升级/准备 .codex 快照，8 = 恢复记忆快照'
        Write-Host '9 = 首次接入 .codex（先备份，以远程为准）'
        Write-Host '10 = 恢复聊天正文、索引和原始标题'
        Write-Host '11 = 恢复模型、权限、项目和置顶快照'
        Write-Host '12 = 旧备份按工作目录重建项目归属（推断，不恢复置顶）'
        Write-Host '13 = 设置 Git 姓名/邮箱并登录 GitHub，0 = 退出'
        $choice = Read-Host '选择（默认 1）'
        if ($choice -eq '0') { exit 2 }
        if ($choice -in @('5', '6')) {
            $mode = 'Enable'
            if ($choice -eq '6') { $mode = 'Disable' }
            & (Join-Path $PSHOME 'powershell.exe') -NoProfile -ExecutionPolicy Bypass -File (Join-Path $PSScriptRoot 'schedule.ps1') -Mode $mode
            exit $LASTEXITCODE
        }
        if ($choice -in @('7', '8', '9', '10', '11', '12')) {
            $Target = 'Codex'
            $Action = 'Prepare'
            if ($choice -eq '8') { $Action = 'RestoreMemory' }
            if ($choice -eq '9') { $Action = 'FirstConnect' }
            if ($choice -eq '10') { $Action = 'RestoreChats' }
            if ($choice -eq '11') { $Action = 'RestorePreferences' }
            if ($choice -eq '12') { $Action = 'InferProjects' }
        } elseif ($choice -eq '13') {
            $Target = 'Documents'
            $Action = 'Login'
        } elseif ($choice -in @('3', '4')) {
            $Target = 'All'
            $Action = 'Sync'
            if ($choice -eq '4') { $Action = 'Pull' }
        } else {
            if ($choice -eq '2') { $Target = 'Codex' } elseif ($choice -notin @('', '1')) { throw '目录选项无效。' }
            Write-Host '选择操作：1 = 初始化，2 = 查看状态，3 = 下载，4 = 上传，5 = 同步，6 = 准备快照（.codex），7 = 恢复记忆（.codex），8 = Git 设置/登录 GitHub，0 = 退出'
            switch (Read-Host '操作') {
                '0' { exit 2 }
                '1' { $Action = 'Init' }
                '2' { $Action = 'Status' }
                '3' { $Action = 'Pull' }
                '4' { $Action = 'Push' }
                '5' { $Action = 'Sync' }
                '6' { $Action = 'Prepare' }
                '7' { $Action = 'RestoreMemory' }
                '8' { $Action = 'Login' }
                default { throw '操作选项无效。' }
            }
        }
    }
    if ($Target -eq 'All') {
        if ($Root -or $Action -in @('Init', 'Prepare', 'RestoreMemory', 'FirstConnect', 'RestoreChats', 'RestorePreferences', 'InferProjects', 'Login')) { throw '此操作请选择单个目录；自定义路径用 -DocumentsRoot 和 -CodexRoot。' }
        $failed = $false
        $summary = New-Object 'System.Collections.Generic.List[string]'
        foreach ($item in @('Documents', 'Codex')) {
            Write-Host ("`n===== " + $item + " =====") -ForegroundColor Cyan
            $childArgs = @('-NoProfile', '-ExecutionPolicy', 'Bypass', '-File', $PSCommandPath, '-Target', $item, '-Action', $Action)
            $childRoot = $DocumentsRoot
            if ($item -eq 'Codex') { $childRoot = $CodexRoot }
            if ($childRoot) { $childArgs += @('-Root', $childRoot) }
            if ($Message) { $childArgs += @('-Message', $Message) }
            if ($NonInteractive) { $childArgs += '-NonInteractive' }
            & (Join-Path $PSHOME 'powershell.exe') @childArgs
            $code = $LASTEXITCODE
            if ($code -eq 0) { $summary.Add($item + '：完成') }
            else { $summary.Add($item + '：失败，请查看上方错误'); $failed = $true }
        }
        Write-Host "`n===== 本轮结果 =====" -ForegroundColor Cyan
        $summary | ForEach-Object { Write-Host $_ }
        if ($failed) { exit 1 }
        exit 0
    }
    if (-not $Root) {
        if ($Target -eq 'Documents') { $Root = Join-Path ([Environment]::GetFolderPath('MyDocuments')) 'Codex' }
        elseif ($env:CODEX_HOME) { $Root = $env:CODEX_HOME }
        else { $Root = Join-Path $env:USERPROFILE '.codex' }
    }
    $script:Root = [IO.Path]::GetFullPath($Root).TrimEnd('\', '/')
    if ($Action -eq 'FirstConnect' -and $Target -eq 'Codex' -and -not $NonInteractive -and -not (Test-Path -LiteralPath $script:Root)) { [IO.Directory]::CreateDirectory($script:Root) | Out-Null }
    if (-not (Test-Path -LiteralPath $script:Root -PathType Container)) { throw "目录不存在：$script:Root" }
    $command = Get-Command git.exe -ErrorAction SilentlyContinue
    if ($command) { $script:Git = $command.Source }
    else {
        $script:Git = @(
            (Join-Path $env:ProgramFiles 'Git\cmd\git.exe'),
            (Join-Path $env:LOCALAPPDATA 'Programs\Git\cmd\git.exe')
        ) | Where-Object { Test-Path -LiteralPath $_ } | Select-Object -First 1
    }
    if (-not $script:Git) { throw '没有找到 Git，请安装 Git 或把 git.exe 加入 PATH。' }
    if ($Action -in @('Prepare', 'RestoreMemory', 'FirstConnect', 'RestoreChats', 'RestorePreferences', 'InferProjects') -and $Target -ne 'Codex') { throw '此操作只用于 .codex。' }
    $liveCodex = Join-Path $env:USERPROFILE '.codex'
    if ($env:CODEX_HOME) { $liveCodex = $env:CODEX_HOME }
    $codexRunning = $false
    if ($Target -eq 'Codex' -and $script:Root -ieq ([IO.Path]::GetFullPath($liveCodex).TrimEnd('\', '/'))) {
        $codexRunning = [bool](Get-Process -Name codex -ErrorAction SilentlyContinue)
    }
    if ($Target -eq 'Codex' -and $Action -in @('Pull', 'RestoreMemory', 'FirstConnect', 'RestoreChats', 'RestorePreferences', 'InferProjects') -and $codexRunning) {
        throw '请先退出 Codex，再下载、首次接入、恢复记忆、偏好或修复正文索引。'
    }
    if ($Target -eq 'Codex' -and $Action -eq 'Sync' -and ($NonInteractive -or $codexRunning)) {
        $Action = 'Push'
        Write-Host '在线备份模式：导出记忆并上传本机文件；本轮不下载或覆盖正在使用的文件。' -ForegroundColor Yellow
    }
    if ($Action -in @('Init', 'Pull', 'Push', 'Sync', 'Prepare', 'RestoreMemory', 'FirstConnect', 'RestoreChats', 'RestorePreferences', 'InferProjects', 'Login')) {
        $sha = [Security.Cryptography.SHA256]::Create()
        $lockId = ([BitConverter]::ToString($sha.ComputeHash($utf8.GetBytes($script:Root.ToLowerInvariant())))).Replace('-', '')
        $sha.Dispose()
        $syncMutex = New-Object Threading.Mutex($false, ('Local\FileSync-' + $lockId))
        $mutexHeld = $syncMutex.WaitOne(0)
        if (-not $mutexHeld) { throw '该目录已有同步操作正在运行，本轮停止。' }
    }
    Write-Host "目录：$script:Root" -ForegroundColor Cyan
    Write-Host "操作：$Action"
    switch ($Action) {
        'Init' {
            if (-not (Test-Path -LiteralPath (Join-Path $script:Root '.git'))) { Invoke-Git @('init', '-b', 'main') }
            Require-Repo
            Invoke-Git @('config', 'core.autocrlf', 'false')
            Invoke-Git @('config', 'pull.ff', 'only')
            $ignore = Join-Path $script:Root '.gitignore'
            if ($Target -eq 'Codex') { Update-CodexRules; Export-MemorySnapshot; Invoke-CodexPreferences export; Export-FileSyncTool }
            $attrs = Join-Path $script:Root '.gitattributes'
            if (-not (Test-Path -LiteralPath $attrs)) { [IO.File]::WriteAllText($attrs, "* -text`n", $utf8) }
            $remotes = @(Invoke-Git @('remote') -Capture)
            if ('origin' -notin $remotes) {
                if (-not $RemoteUrl) { $RemoteUrl = Read-Host '粘贴此目录对应的空私有仓库地址（直接回车暂不设置）' }
                if ($RemoteUrl) { Invoke-Git @('remote', 'add', 'origin', $RemoteUrl.Trim()) }
            } else { Invoke-Git @('remote', '-v') }
            Write-Host '初始化完成。新仓库首次上传选“上传”；.codex 接入已有远程选“下载”或主菜单 9。两个目录使用不同仓库。' -ForegroundColor Green
        }
        'Login' {
            Require-Repo
            Ensure-GitIdentity
            $loginUrl = [string](Invoke-Git @('remote', 'get-url', '--push', 'origin') -Capture)
            Ensure-GitHubAccess -Url $loginUrl -Login
            Write-Host 'Git 身份和 GitHub 登录检查完成；未提交或上传。' -ForegroundColor Green
        }
        'FirstConnect' { Start-CodexFirstConnect }
        'Prepare' {
            Require-Repo
            Update-CodexRules
            Check-CodexConfig
            Export-MemorySnapshot
            Invoke-CodexPreferences export
            Export-FileSyncTool
            Write-Host '规则、记忆、偏好和工具快照已准备；尚未提交或上传。' -ForegroundColor Green
        }
        'RestoreMemory' { Require-Repo; Restore-MemorySnapshot }
        'RestoreChats' { Require-Repo; Restore-ChatIndex }
        'RestorePreferences' { Require-Repo; Invoke-CodexPreferences restore }
        'InferProjects' {
            Require-Repo
            Invoke-CodexPreferences infer-projects
        }
        'Status' { Require-Repo; Invoke-Git @('status', '--short', '--branch'); Invoke-Git @('remote', '-v') }
        'Pull' {
            Require-Repo
            $head = @(Invoke-Git @('rev-parse', '--verify', '--quiet', 'HEAD') -Capture -Allowed @(0,1,128))
            if (-not $head.Count) {
                if ($Target -eq 'Codex') {
                    Write-Host '当前只有初始化，首次下载将先备份本机受管文件，再接入远程仓库。' -ForegroundColor Yellow
                    Start-CodexFirstConnect
                    break
                }
                throw '当前只有初始化、尚无提交。第二台电脑请先将已有文档仓库克隆到文档\Codex 根目录；不要为通过检查而创建本机初始提交。'
            }
            $statusArgs = @('status', '--porcelain')
            if ($Target -eq 'Documents') {
                $statusArgs += @('--ignored', '--', '.')
                $statusArgs += @(':(top,icase,glob,exclude)**/*.in', ':(top,icase,glob,exclude)**/*.exe')
                foreach ($path in @(Get-DocumentsExclusions)) { $statusArgs += ':(top,literal,exclude)' + $path }
            }
            $dirty = @(Invoke-Git $statusArgs -Capture)
            if ($dirty.Count) {
                $onlyLocalConfig = $Target -eq 'Codex' -and $dirty.Count -eq 1 -and $dirty[0] -ceq ' M config.toml'
                if (-not $onlyLocalConfig) { throw '目录内有未提交的修改，请先上传或自行处理，再下载。' }
                Write-Host '检测到本机 config.toml 修改，将保留配置并尝试快进；远程若也修改此文件，Git 会停止以避免覆盖。' -ForegroundColor Yellow
            }
            $fetchUrl = [string](Invoke-Git @('remote', 'get-url', 'origin') -Capture)
            Ensure-GitHubAccess $fetchUrl
            Invoke-Git @('pull', '--ff-only')
            if ($Target -eq 'Documents') { Restore-EmptyDirs }
            if ($Target -eq 'Codex') { Write-Host '下载只更新备份文件；主菜单 8 恢复记忆，10 恢复聊天正文、索引和标题，11 恢复设置、项目和置顶。' -ForegroundColor Yellow }
            Write-Host '下载完成。' -ForegroundColor Green
        }
        'Push' {
            Save-Changes
            Invoke-Git @('push', '-u', 'origin', 'HEAD')
            Write-Host '上传完成。' -ForegroundColor Green
        }
        'Sync' {
            if ($Target -eq 'Documents') { Restore-EmptyDirs }
            Save-Changes
            Invoke-Git @('fetch', 'origin')
            $branch = [string](Invoke-Git @('symbolic-ref', '--short', 'HEAD') -Capture)
            $remoteRef = 'refs/remotes/origin/' + $branch
            $remoteHead = @(Invoke-Git @('rev-parse', '--verify', '--quiet', $remoteRef) -Capture -Allowed @(0,1))
            if ($remoteHead.Count) {
                Invoke-Git @('merge', '--ff-only', $remoteRef)
                if ($Target -eq 'Documents') { Restore-EmptyDirs }
            }
            Invoke-Git @('push', '-u', 'origin', 'HEAD')
            if ($Target -eq 'Codex') { Write-Host '若下载了新快照，请选主菜单 8 恢复记忆、11 恢复设置/项目/置顶后再继续使用。' -ForegroundColor Yellow }
            Write-Host '同步完成。' -ForegroundColor Green
        }
    }
    exit 0
} catch {
    Write-Host ('同步停止：' + $_.Exception.Message) -ForegroundColor Red
    Write-Host '可以在目标目录用 Git Bash 执行 git status 排查。工具不会强推、自动合并冲突或重置你的修改。'
    exit 1
} finally {
    if ($mutexHeld) { $syncMutex.ReleaseMutex() }
    if ($syncMutex) { $syncMutex.Dispose() }
    if ($transcript) { Stop-Transcript | Out-Null }
}
