# Explicit first connection for a Codex directory without outer Git history.
function Invoke-FirstGit {
    param([string]$Directory, [string[]]$GitArgs, [switch]$Capture, [int[]]$Allowed = @(0))
    $old = $ErrorActionPreference
    $ErrorActionPreference = 'Continue'
    try { $output = @(& $script:Git -c core.quotePath=false -c core.longpaths=true -c core.autocrlf=false -C $Directory @GitArgs 2>&1); $code = $LASTEXITCODE }
    finally { $ErrorActionPreference = $old }
    if ($code -notin $Allowed) {
        $output | ForEach-Object { Write-Host $_ }
        throw "首次接入的 Git 操作失败：$($GitArgs[0])，返回 $code。"
    }
    if ($Capture) { return $output | ForEach-Object { [string]$_ } }
}

function Test-FirstManagedPath {
    param([string]$Path)
    if ($Path -match '(^/|\\|:|(^|/)\.\.?(/|$)|(^|/)\.git(/|$)|(^|/)\.system(/|$)|(^|/)(auth\.json|cap_sid)(/|$)|\.sqlite($|-))') { return $false }
    foreach ($part in $Path.Split('/')) {
        if ($part -match '[. ]$|[<>|"*?\x00-\x1f]' -or $part -match '^(CON|PRN|AUX|NUL|COM[1-9]|LPT[1-9])(\.|$)') { return $false }
    }
    if ($Path -in @('.gitignore', '.gitattributes', 'AGENTS.md', 'config.toml', '.filesync-preferences.json', 'hooks.json', 'history.jsonl', 'session_index.jsonl')) { return $true }
    if ($Path -match '^\.chatgpt-projects/[^/]+/AGENTS[.]md$') { return $true }
    if ($Path -match '^\.filesync-tool/([^/]+)$') { return $Matches[1] -in $fileSyncToolFiles }
    return $Path -match '^(\.filesync-memories|\.filesync-memory-archive|sessions|archived_sessions|attachments|rules|skills|prompts|instructions|agents|profiles|hooks|generated_images|visualizations|pets)/'
}

function Get-FirstManagedInventory {
    param([string]$Base)
    $map = @{}
    foreach ($name in @('.gitignore', '.gitattributes', 'AGENTS.md', 'config.toml', '.filesync-preferences.json', 'hooks.json', 'history.jsonl', 'session_index.jsonl')) {
        $path = Join-Path $Base $name
        if (Test-Path -LiteralPath $path) {
            $item = Get-Item -LiteralPath $path -Force
            if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw "受管文件路径被目录或链接占用：$name" }
            $map[$name] = (Get-FileHash -LiteralPath $path -Algorithm SHA256).Hash.ToLowerInvariant()
        }
    }
    foreach ($name in @('.filesync-memories', 'sessions', 'archived_sessions', 'attachments', 'rules', 'skills', 'prompts', 'instructions', 'agents', 'profiles', 'hooks', 'generated_images', 'visualizations', 'pets', '.filesync-tool', '.filesync-memory-archive')) {
        $path = Join-Path $Base $name
        if (-not (Test-Path -LiteralPath $path)) { continue }
        if (-not (Test-Path -LiteralPath $path -PathType Container)) { throw "受管目录路径被文件占用：$name" }
        $files = Get-MemoryInventory $path
        foreach ($relative in $files.Keys) {
            $full = $name + '/' + $relative
            if (Test-FirstManagedPath $full) { $map[$full] = $files[$relative] }
        }
    }
    $projects = Join-Path $Base '.chatgpt-projects'
    if (Test-Path -LiteralPath $projects) {
        $parent = Get-Item -LiteralPath $projects -Force
        if (-not $parent.PSIsContainer -or ($parent.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw '项目指令目录不能是链接或文件。' }
        foreach ($project in @(Get-ChildItem -LiteralPath $projects -Force -Directory)) {
            if ($project.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw '项目指令含链接。' }
            $path = Join-Path $project.FullName 'AGENTS.md'
            if (Test-Path -LiteralPath $path) {
                $item = Get-Item -LiteralPath $path -Force
                if ($item.PSIsContainer -or ($item.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw '项目 AGENTS.md 不能是链接或目录。' }
                $relative = '.chatgpt-projects/' + $project.Name + '/AGENTS.md'
                if (Test-FirstManagedPath $relative) { $map[$relative] = (Get-FileHash -LiteralPath $path).Hash.ToLowerInvariant() }
            }
        }
    }
    return $map
}

function Start-CodexFirstConnect {
    if ($NonInteractive) { throw '首次接入只能手动运行，定时任务不能执行。' }
    $live = $script:Root
    if ((Get-Item -LiteralPath $live -Force).Attributes -band [IO.FileAttributes]::ReparsePoint) { throw '首次接入目录不能是链接。' }
    $outerGit = Join-Path $live '.git'
    if (Test-Path -LiteralPath $outerGit) {
        if (-not (Test-Path -LiteralPath $outerGit -PathType Container) -or
            ((Get-Item -LiteralPath $outerGit -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw '首次接入不支持链接或工作树形式的外层 .git。' }
        if (Test-Path -LiteralPath (Join-Path $outerGit 'index.lock')) { throw '目标仓库有 Git 锁，请稍后重试。' }
        $head = @(Invoke-FirstGit $live @('rev-parse', '--verify', '--quiet', 'HEAD') -Capture -Allowed @(0,1,128))
        if ($head.Count) { throw '目标已有外层 Git 提交历史，不能重复首次接入。日常请选择下载或同步；恢复聊天请选择主菜单 10。原仓库保留。' }
    }
    $url = $RemoteUrl
    if (-not $url -and (Test-Path -LiteralPath $outerGit)) {
        $remotes = @(Invoke-FirstGit $live @('remote') -Capture)
        if ('origin' -in $remotes) { $url = [string](Invoke-FirstGit $live @('remote', 'get-url', 'origin') -Capture) }
    }
    if (-not $url) { $url = Read-Host '粘贴已有的 .codex 同步仓库地址（此操作以远程为准，本机受管文件先备份）' }
    if (-not $url) { throw '未填写远程仓库地址，未导入任何文件。' }
    Ensure-GitHubAccess $url.Trim()
    # Keep paths short for Windows PowerShell/.NET as well as Git.
    $stage = Join-Path $env:USERPROFILE ('.fs-' + [Guid]::NewGuid().ToString('N').Substring(0,12))
    $backup = $null
    $changed = $false
    $newGit = $false
    $oldGit = $false
    $incoming = @{}
    $original = @{}
    $memory = @{}
    try {
        Write-Host '正在克隆并验证远程版本，本机文件尚未改动。'
        $cloneArgs = @('clone', '--no-checkout')
        if ($script:GitHubUseGcmForClone) { $cloneArgs += @('--config', 'credential.https://github.com.helper=', '--config', 'credential.https://github.com.helper=manager') }
        Invoke-FirstGit $PSScriptRoot ($cloneArgs + @('--', $url.Trim(), $stage))
        Invoke-FirstGit $stage @('rev-parse', '--verify', 'HEAD')
        $entries = @(Invoke-FirstGit $stage @('ls-tree', '-r', '--full-tree', 'HEAD') -Capture)
        $remotePaths = @()
        foreach ($entry in $entries) {
            if ($entry -notmatch '^([0-9]+) ([a-z]+) [0-9a-f]+\t(.+)$') { throw '远程树存在不支持的条目。' }
            $mode = $Matches[1]
            $path = $Matches[3]
            if ($mode -notin @('100644', '100755') -or -not (Test-FirstManagedPath $path)) {
                throw "远程含超出首次接入范围的文件、链接或 gitlink：$path。请先在原电脑用新版工具上传并检查同步范围。"
            }
            $remotePaths += $path
        }
        if ('.filesync-memories/manifest.json' -notin $remotePaths) { throw '远程尚无新版记忆快照，请先在原电脑用新版工具上传。' }
        Invoke-FirstGit $stage @('read-tree', 'HEAD')
        foreach ($path in $remotePaths) {
            if ((Join-Path $stage $path).Length -ge 260) { throw '首次接入临时路径仍超过 Windows 路径限制，未替换本机文件。请使用更短的用户目录。' }
        }
        Invoke-FirstGit $stage @('checkout-index', '-a')
        $script:Root = $stage
        Update-CodexRules
        Check-CodexConfig
        $snapshot = Read-CheckedSnapshot @{ Snapshot = (Join-Path $stage '.filesync-memories') }
        if ($null -eq $snapshot) { throw '远程记忆快照无效。' }
        $incoming = Get-FirstManagedInventory $stage
        $script:Root = $live
        $original = Get-FirstManagedInventory $live
        $memory = Get-MemoryInventory (Join-Path $live 'memories')
        foreach ($path in $incoming.Keys) {
            $destination = Join-Path $live $path
            if (Test-Path -LiteralPath $destination -PathType Container) { throw "远程文件目标被本机目录占用，未导入：$path" }
        }
        $backup = Join-Path $env:USERPROFILE ('.fs-backups/' + (Get-Date -Format 'yyyyMMdd-HHmmss') + '-' + [Guid]::NewGuid().ToString('N').Substring(0,4))
        foreach ($path in $original.Keys) {
            if ((Join-Path (Join-Path $backup 'files') $path).Length -ge 260) { throw '首次接入备份路径超过 Windows 路径限制，未替换本机文件。' }
        }
        foreach ($path in $memory.Keys) {
            if ((Join-Path (Join-Path $backup 'files/memories') $path).Length -ge 260) { throw '首次接入记忆备份路径超过 Windows 路径限制，未替换本机文件。' }
        }
        [IO.Directory]::CreateDirectory($backup) | Out-Null
        [IO.File]::WriteAllText((Join-Path $backup 'source-path.txt'), $live, $utf8)
        $backupFiles = Join-Path $backup 'files'
        Copy-MemoryFiles $live $backupFiles $original
        Copy-MemoryFiles (Join-Path $live 'memories') (Join-Path $backupFiles 'memories') $memory
        Write-MemoryMap (Join-Path $backup 'managed-manifest.json') $original
        Write-MemoryMap (Join-Path $backup 'memory-manifest.json') $memory
        $saved = Get-FirstManagedInventory $backupFiles
        $savedMemory = Get-MemoryInventory (Join-Path $backupFiles 'memories')
        $current = Get-FirstManagedInventory $live
        $currentMemory = Get-MemoryInventory (Join-Path $live 'memories')
        if ((Get-MapText $saved) -cne (Get-MapText $original) -or
            (Get-MapText $savedMemory) -cne (Get-MapText $memory) -or
            (Get-MapText $current) -cne (Get-MapText $original) -or
            (Get-MapText $currentMemory) -cne (Get-MapText $memory)) { throw '备份校验失败或本机内容仍在变化，未导入远程。' }
        Write-Host ("本机受管文件已备份：" + $backup)
        $changed = $true
        if (Test-Path -LiteralPath $outerGit) {
            [IO.Directory]::Move($outerGit, (Join-Path $backup 'original-outer-git'))
            $oldGit = $true
        }
        foreach ($path in $original.Keys) { Remove-Item -LiteralPath (Join-Path $live $path) -Force }
        [IO.Directory]::Move((Join-Path $stage '.git'), $outerGit)
        $newGit = $true
        Copy-MemoryFiles $stage $live $incoming
        Invoke-Git @('config', 'core.autocrlf', 'false')
        Invoke-Git @('config', 'pull.ff', 'only')
        # Explicit remote-first import: the current memory is already verified in backup.
        Write-MemoryMap (Join-Path $outerGit 'filesync-memories-baseline.json') $memory
        Restore-MemorySnapshot
        Write-Host '首次接入完成：已采用远程历史和受管文件，记忆已恢复；没有创建提交或上传。' -ForegroundColor Green
        Write-Host ("原文件备份：" + $backup)
        Write-Host '本机认证、数据库、缓存和原 memories/.git 保留。使用前请检查 config.toml 的本机路径；回主菜单选 10 恢复聊天正文、索引和标题；11 恢复偏好、项目和置顶。'
    } catch {
        $failure = $_.Exception.Message
        $script:Root = $live
        if ($changed) {
            try {
                foreach ($path in $incoming.Keys) {
                    $target = Join-Path $live $path
                    if (Test-Path -LiteralPath $target -PathType Leaf) { Remove-Item -LiteralPath $target -Force }
                }
                $nowMemory = Get-MemoryInventory (Join-Path $live 'memories')
                foreach ($path in $nowMemory.Keys) { Remove-Item -LiteralPath (Join-Path (Join-Path $live 'memories') $path) -Force }
                Copy-MemoryFiles (Join-Path $backup 'files') $live $original
                Copy-MemoryFiles (Join-Path $backup 'files/memories') (Join-Path $live 'memories') $memory
                if ($newGit) { [IO.Directory]::Move($outerGit, (Join-Path $backup 'failed-import-git')) }
                if ($oldGit) { [IO.Directory]::Move((Join-Path $backup 'original-outer-git'), $outerGit) }
                Write-Host '导入未完成，已还原本机受管文件。' -ForegroundColor Yellow
            } catch { Write-Host ('自动还原未完成，请从备份恢复：' + $backup) -ForegroundColor Red }
        }
        if ($backup) { throw ($failure + '。原文件备份：' + $backup) }
        throw $failure
    } finally {
        $script:Root = $live
        if (Test-Path -LiteralPath $stage) { Remove-Item -LiteralPath $stage -Recurse -Force }
    }
}
