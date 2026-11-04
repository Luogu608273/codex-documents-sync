# FileSync memory snapshots; never move or delete memories/.git.
$codexIgnoreV2 = @'
# FileSync: codex v2 begin
/*
!/.gitignore
!/.gitattributes
!/AGENTS.md
!/config.toml
!/.filesync-preferences.json
!/hooks.json
!/history.jsonl
!/session_index.jsonl
!/sessions/
!/archived_sessions/
!/attachments/
!/rules/
!/skills/
!/prompts/
!/instructions/
!/agents/
!/profiles/
!/hooks/
!/.filesync-memories/
!/.filesync-memory-archive/
!/generated_images/
!/visualizations/
!/pets/
!/.chatgpt-projects/
/.chatgpt-projects/*
!/.chatgpt-projects/*/
/.chatgpt-projects/*/*
!/.chatgpt-projects/*/AGENTS.md
!/.filesync-tool/
/.filesync-tool/*
!/.filesync-tool/sync.ps1
!/.filesync-tool/codex-state.ps1
!/.filesync-tool/first-connect.ps1
!/.filesync-tool/repair-chat-index.py
!/.filesync-tool/codex-preferences.py
!/.filesync-tool/schedule.ps1
!/.filesync-tool/sync.cmd
!/.filesync-tool/sync-all.cmd
!/.filesync-tool/README.md
/skills/.system/
**/.git/
**/.system/
auth.json
cap_sid
*.sqlite
*.sqlite-wal
*.sqlite-shm
# FileSync: codex v2 end
'@

function Update-CodexRules {
    $sensitive = @(Invoke-Git @('ls-files', '--', 'auth.json', 'cap_sid') -Capture)
    if ($sensitive.Count) { throw '认证文件已被跟踪，需先处理凭据和历史。' }
    $ignore = Join-Path $script:Root '.gitignore'
    $old = ''
    if (Test-Path -LiteralPath $ignore) { $old = [IO.File]::ReadAllText($ignore) }
    $lf = [string][char]10
    $normalized = $old.Replace(([string][char]13 + $lf), $lf)
    $legacy = $codexIgnore.Replace(([string][char]13 + $lf), $lf).Trim()
    if ($normalized.Contains($legacy)) { $normalized = $normalized.Replace($legacy, '').TrimStart([char]13, [char]10) }
    $pattern = '(?ms)^# FileSync: codex v2 begin\r?\n.*?^# FileSync: codex v2 end(?:\r?\n|$)'
    $normalized = [regex]::Replace($normalized, $pattern, '')
    $custom = $normalized.Trim([char]13, [char]10)
    $text = $codexIgnoreV2 + $lf
    if ($custom) { $text += $custom + $lf }
    if ($text -cne $old) { [IO.File]::WriteAllText($ignore, $text, $utf8) }
    Update-ExcludedExtensionsIgnore
    foreach ($path in @(Invoke-Git @('ls-files', '--cached', '--ignored', '--exclude-standard') -Capture)) {
        Invoke-Git @('rm', '--cached', '--ignore-unmatch', '--', $path)
    }
    $links = @(Invoke-Git @('ls-files', '--stage') -Capture | Where-Object { $_ -match '^160000 ' })
    if ($links.Count) { throw '同步范围内仍有嵌套仓库指针，请单独处理：' + ($links -join ', ') }
}

function Get-MemoryInventory {
    param([string]$Base)
    $result = @{}
    if (-not (Test-Path -LiteralPath $Base)) { return $result }
    $queue = New-Object 'System.Collections.Generic.Queue[string]'
    $queue.Enqueue($Base)
    while ($queue.Count) {
        $dir = Get-Item -LiteralPath $queue.Dequeue() -Force
        if ($dir.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "记忆目录含链接：$($dir.FullName)" }
        foreach ($item in @(Get-ChildItem -LiteralPath $dir.FullName -Force)) {
            if ($item.Name -in @('.git', '.system', 'auth.json', 'cap_sid') -or $item.Name -like '*.sqlite*') { continue }
            if (-not $item.PSIsContainer -and $item.Extension -in @('.in', '.exe')) { continue }
            if ($item.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw "记忆内容含链接：$($item.FullName)" }
            if ($item.PSIsContainer) { $queue.Enqueue($item.FullName); continue }
            $length = $item.Length
            $stamp = $item.LastWriteTimeUtc.Ticks
            $hash = (Get-FileHash -LiteralPath $item.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
            $after = Get-Item -LiteralPath $item.FullName -Force
            if ($length -ne $after.Length -or $stamp -ne $after.LastWriteTimeUtc.Ticks) { throw '记忆正在写入，请稍后重试。' }
            $result[$item.FullName.Substring($Base.Length + 1).Replace('\', '/')] = $hash
        }
    }
    return $result
}

function Get-MapText {
    param([hashtable]$Map)
    $ordered = [ordered]@{}
    foreach ($key in @($Map.Keys | Sort-Object)) { $ordered[$key] = $Map[$key] }
    return (ConvertTo-Json -InputObject $ordered -Compress -Depth 8)
}

function Read-MemoryMap {
    param([string]$Path)
    if (-not (Test-Path -LiteralPath $Path)) { return $null }
    $data = Get-Content -LiteralPath $Path -Raw -Encoding UTF8 | ConvertFrom-Json
    if ($data.Format -ne 1 -or $null -eq $data.Files) { throw "记忆清单格式不支持：$Path" }
    $map = @{}
    foreach ($property in $data.Files.PSObject.Properties) {
        $relative = $property.Name
        if ($relative.Split('/') | Where-Object { $_ -match '[. ]$' -or $_ -match '[<>|"*?]' }) { throw '记忆路径包含 Windows 不安全名称。' }
        if ($relative -match '(^/|\\|:|(^|/)\.\.?(/|$)|(^|/)\.git(/|$)|(^|/)\.system(/|$))' -or
            $property.Value -notmatch '^[0-9a-f]{64}$') { throw '记忆清单存在不安全的路径或哈希。' }
        if ($relative -match '(?i)\.(in|exe)$') { continue }
        $map[$relative] = [string]$property.Value
    }
    return $map
}

function Write-MemoryMap {
    param([string]$Path, [hashtable]$Map)
    $text = '{"Format":1,"Files":' + (Get-MapText $Map) + '}'
    [IO.File]::WriteAllText($Path, $text + [char]10, $utf8)
}

function Get-MemoryPaths {
    $gitDir = [string](Invoke-Git @('rev-parse', '--absolute-git-dir') -Capture)
    return @{
        Live = (Join-Path $script:Root 'memories')
        Snapshot = (Join-Path $script:Root '.filesync-memories')
        Baseline = (Join-Path $gitDir 'filesync-memories-baseline.json')
        GitDir = $gitDir
    }
}

function Read-CheckedSnapshot {
    param([hashtable]$Paths)
    if ((Test-Path -LiteralPath $Paths.Snapshot) -and ((Get-Item -LiteralPath $Paths.Snapshot -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw '快照目录不能是链接。' }
    $map = Read-MemoryMap (Join-Path $Paths.Snapshot 'manifest.json')
    if ($null -eq $map) {
        if (Test-Path -LiteralPath $Paths.Snapshot) { throw '快照目录缺少清单，请检查 .filesync-memories。' }
        return $null
    }
    $actual = Get-MemoryInventory (Join-Path $Paths.Snapshot 'files')
    if ((Get-MapText $actual) -cne (Get-MapText $map)) { throw '记忆快照与清单不一致，停止操作。' }
    return $map
}

function Copy-MemoryFiles {
    param([string]$Source, [string]$Destination, [hashtable]$Map)
    [IO.Directory]::CreateDirectory($Destination) | Out-Null
    foreach ($relative in $Map.Keys) {
        $target = Join-Path $Destination $relative
        [IO.Directory]::CreateDirectory([IO.Path]::GetDirectoryName($target)) | Out-Null
        [IO.File]::Copy((Join-Path $Source $relative), $target, $true)
    }
}

function Export-MemorySnapshot {
    $p = Get-MemoryPaths
    $current = Get-MemoryInventory $p.Live
    $snapshot = Read-CheckedSnapshot $p
    $baseline = Read-MemoryMap $p.Baseline
    if ($null -ne $snapshot) {
        $incoming = $null -eq $baseline -or (Get-MapText $snapshot) -cne (Get-MapText $baseline)
        if ($incoming -and (Get-MapText $current) -cne (Get-MapText $snapshot)) {
            throw '已有下载的记忆快照尚未恢复。请选择“恢复记忆快照”，处理本机冲突后再上传，避免覆盖远程记忆。'
        }
    }
    if ($null -ne $snapshot) { Save-PreviousMemoryFiles -Source (Join-Path $p.Snapshot 'files') -Previous $snapshot -Current $current -GitDir $p.GitDir }
    $temp = Join-Path $p.GitDir ('filesync-memory-export-' + [Guid]::NewGuid().ToString('N'))
    [IO.Directory]::CreateDirectory($temp) | Out-Null
    try {
        Copy-MemoryFiles $p.Live (Join-Path $temp 'files') $current
        $copied = Get-MemoryInventory (Join-Path $temp 'files')
        $after = Get-MemoryInventory $p.Live
        if ((Get-MapText $copied) -cne (Get-MapText $current) -or (Get-MapText $after) -cne (Get-MapText $current)) { throw '导出期间记忆发生变化，请重试。' }
        Write-MemoryMap (Join-Path $temp 'manifest.json') $current
        $oldSnapshot = Join-Path $p.GitDir ('filesync-memory-old-' + [Guid]::NewGuid().ToString('N'))
        if (Test-Path -LiteralPath $p.Snapshot) { [IO.Directory]::Move($p.Snapshot, $oldSnapshot) }
        try { [IO.Directory]::Move($temp, $p.Snapshot) }
        catch {
            if (Test-Path -LiteralPath $oldSnapshot) { [IO.Directory]::Move($oldSnapshot, $p.Snapshot) }
            throw
        }
        if (Test-Path -LiteralPath $oldSnapshot) { Remove-Item -LiteralPath $oldSnapshot -Recurse -Force }
        Write-MemoryMap $p.Baseline $current
        Write-Host ("已导出记忆快照：" + $current.Count + " 个文件；原 memories/.git 保留。")
    } finally {
        if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Recurse -Force }
    }
}

# Retain replaced/removed memory material without reactivating it in memories/.
function Save-PreviousMemoryFiles {
    param([string]$Source, [hashtable]$Previous, [hashtable]$Current, [string]$GitDir)
    $retained = @{}
    foreach ($key in $Previous.Keys) {
        if ($Previous[$key] -cne $Current[$key]) { $retained[$key] = $Previous[$key] }
    }
    if (-not $retained.Count) { return }
    $archive = Join-Path $script:Root '.filesync-memory-archive'
    if (Test-Path -LiteralPath $archive) { $null = Get-MemoryInventory $archive }
    $sha = [Security.Cryptography.SHA256]::Create()
    try { $key = ([BitConverter]::ToString($sha.ComputeHash($utf8.GetBytes((Get-MapText $retained))))).Replace('-', '').ToLowerInvariant() }
    finally { $sha.Dispose() }
    $destination = Join-Path $archive $key
    if (Test-Path -LiteralPath $destination) {
        $saved = Read-CheckedSnapshot @{ Snapshot = $destination }
        if ((Get-MapText $saved) -cne (Get-MapText $retained)) { throw '历史记忆备份校验失败。' }
        return
    }
    $temp = Join-Path $GitDir ('filesync-memory-archive-' + [Guid]::NewGuid().ToString('N'))
    try {
        Copy-MemoryFiles $Source (Join-Path $temp 'files') $retained
        Write-MemoryMap (Join-Path $temp 'manifest.json') $retained
        $null = Read-CheckedSnapshot @{ Snapshot = $temp }
        [IO.Directory]::CreateDirectory($archive) | Out-Null
        [IO.Directory]::Move($temp, $destination)
        Write-Host ("已另存历史记忆：" + $retained.Count + " 个文件；不会恢复到正在使用的记忆。")
    } finally {
        if (Test-Path -LiteralPath $temp) { Remove-Item -LiteralPath $temp -Recurse -Force }
    }
}

$fileSyncToolFiles = @('sync.ps1', 'codex-state.ps1', 'first-connect.ps1', 'repair-chat-index.py', 'codex-preferences.py', 'schedule.ps1', 'sync.cmd', 'sync-all.cmd', 'README.md')
function Export-FileSyncTool {
    $destination = Join-Path $script:Root '.filesync-tool'
    if (Test-Path -LiteralPath $destination) { $null = Get-MemoryInventory $destination }
    foreach ($name in $fileSyncToolFiles) {
        $source = Get-Item -LiteralPath (Join-Path $PSScriptRoot $name) -Force
        if ($source.PSIsContainer -or ($source.Attributes -band [IO.FileAttributes]::ReparsePoint)) { throw "工具文件无效：$name" }
    }
    [IO.Directory]::CreateDirectory($destination) | Out-Null
    foreach ($name in $fileSyncToolFiles) {
        $source = Join-Path $PSScriptRoot $name
        $target = Join-Path $destination $name
        if (-not (Test-Path -LiteralPath $target) -or
            (Get-FileHash -LiteralPath $source).Hash -cne (Get-FileHash -LiteralPath $target).Hash) { [IO.File]::Copy($source, $target, $true) }
    }
}

function Get-FileSyncPython {
    $python = Get-Command python.exe -ErrorAction SilentlyContinue
    if ($python -and $python.Source -notlike '*WindowsApps*') { return $python.Source }
    $path = Get-ChildItem -Path (Join-Path $env:LOCALAPPDATA 'Programs\Python\Python*\python.exe') -ErrorAction SilentlyContinue |
        Sort-Object FullName -Descending | Select-Object -First 1 -ExpandProperty FullName
    if (-not $path) { throw '聊天恢复和偏好快照需要 Python 3.8 或以上，请先安装 Python。' }
    return $path
}

function Invoke-CodexPreferences {
    param([ValidateSet('export', 'restore', 'infer-projects')][string]$Mode)
    if ($Mode -ne 'export' -and $NonInteractive) { throw '偏好恢复请手动运行。' }
    $pythonPath = Get-FileSyncPython
    & $pythonPath (Join-Path $PSScriptRoot 'codex-preferences.py') --root $script:Root ('--' + $Mode)
    if ($LASTEXITCODE -ne 0) { throw '偏好快照操作未完成，请查看上方提示。' }
    if ($Mode -eq 'export') { Write-Host '模型、权限、项目归属和置顶快照已更新。' }
    else { Write-Host '偏好/项目恢复完成，请重新打开 Codex；原文件备份在 .filesync-preferences-backups。' -ForegroundColor Green }
}

function Restore-ChatIndex {
    if ($NonInteractive) { throw '聊天索引恢复请手动运行。' }
    $pythonPath = Get-FileSyncPython
    & $pythonPath (Join-Path $PSScriptRoot 'repair-chat-index.py') --root $script:Root
    if ($LASTEXITCODE -ne 0) { throw '聊天索引恢复未完成，请查看上方提示和备份。' }
    Write-Host '如已下载偏好快照，请继续选主菜单 11 恢复设置、项目和置顶。' -ForegroundColor Yellow
}

function Restore-MemorySnapshot {
    if ($NonInteractive) { throw '恢复记忆只能由你手动运行。' }
    $p = Get-MemoryPaths
    $snapshot = Read-CheckedSnapshot $p
    if ($null -eq $snapshot) { throw '没有记忆快照，请先从已升级的电脑上传，再下载。' }
    $current = Get-MemoryInventory $p.Live
    $baseline = Read-MemoryMap $p.Baseline
    if ($null -eq $baseline) { $baseline = @{} }
    $conflicts = @()
    foreach ($key in @(@($current.Keys) + @($baseline.Keys) + @($snapshot.Keys) | Sort-Object -Unique)) {
        if ($current[$key] -cne $baseline[$key] -and $current[$key] -cne $snapshot[$key]) { $conflicts += $key }
    }
    if ($conflicts.Count) { throw "本机记忆有冲突，未恢复任何文件。请先另存并手动处理：$($conflicts -join ', ')" }
    $backup = Join-Path $p.GitDir ('filesync-memory-backups/' + (Get-Date -Format 'yyyyMMdd-HHmmss-fff'))
    Copy-MemoryFiles $p.Live (Join-Path $backup 'files') $current
    Write-MemoryMap (Join-Path $backup 'manifest.json') $current
    $again = Get-MemoryInventory $p.Live
    if ((Get-MapText $again) -cne (Get-MapText $current)) { throw '恢复前记忆发生变化，停止操作。' }
    Copy-MemoryFiles (Join-Path $p.Snapshot 'files') $p.Live $snapshot
    foreach ($key in $baseline.Keys) {
        if (-not $snapshot.ContainsKey($key) -and $current.ContainsKey($key)) { Remove-Item -LiteralPath (Join-Path $p.Live $key) -Force }
    }
    $restored = Get-MemoryInventory $p.Live
    if ((Get-MapText $restored) -cne (Get-MapText $snapshot)) { throw "恢复校验失败，原文件备份在 $backup" }
    Write-MemoryMap $p.Baseline $snapshot
    Write-Host ("记忆已恢复，原文件备份在：" + $backup) -ForegroundColor Green
}

function Check-CodexConfig {
    $path = Join-Path $script:Root 'config.toml'
    if (Test-Path -LiteralPath $path) {
        foreach ($line in [IO.File]::ReadAllLines($path)) {
            if ($line -match '^\s*(api[_-]?key|access[_-]?token|refresh[_-]?token|password|secret)\s*=\s*["''][^"'']+["'']') {
                throw 'config.toml 含疑似明文凭据字段，请改用环境变量或手动排除此配置；未显示字段值。'
            }
        }
    }
}
