param(
    [ValidateSet('Enable', 'Disable', 'Preview')][string]$Mode = 'Enable',
    [string]$DailyTime = ''
)
$ErrorActionPreference = 'Stop'
try {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent()
    $taskName = 'FileSync-' + $identity.User.Value
    if ($Mode -eq 'Disable') {
        if (Get-ScheduledTask -TaskName $taskName -ErrorAction SilentlyContinue) {
            Unregister-ScheduledTask -TaskName $taskName -Confirm:$false
            Write-Host '定时同步已关闭。' -ForegroundColor Green
        } else { Write-Host '当前没有此工具的定时任务。' }
        exit 0
    }
    if (-not $DailyTime) {
        if ($Mode -eq 'Preview') { throw '预览请提供 -DailyTime HH:mm。' }
        $DailyTime = Read-Host '每天几点同步？输入 24 小时制 HH:mm（例如 22:00）'
    }
    $DailyTime = $DailyTime.Trim()
    if ($DailyTime -notmatch '^(?:[01][0-9]|2[0-3]):[0-5][0-9]$') {
        throw '时间必须是 HH:mm，例如 09:30 或 22:00。'
    }
    $parts = $DailyTime.Split(':')
    $now = Get-Date
    $startAt = $now.Date.AddHours([int]$parts[0]).AddMinutes([int]$parts[1])
    if ($startAt -le $now) { $startAt = $startAt.AddDays(1) }
    $sync = Join-Path $PSScriptRoot 'sync.ps1'
    if (-not (Test-Path -LiteralPath $sync)) { throw '没有找到 sync.ps1。' }
    $arguments = '-NoProfile -NonInteractive -ExecutionPolicy Bypass -WindowStyle Hidden -File "' + $sync + '" -Target All -Action Sync -NonInteractive -Log'
    $action = New-ScheduledTaskAction -Execute (Join-Path $PSHOME 'powershell.exe') -Argument $arguments -WorkingDirectory $PSScriptRoot
    $trigger = New-ScheduledTaskTrigger -Daily -At $startAt
    $principal = New-ScheduledTaskPrincipal -UserId $identity.Name -LogonType Interactive -RunLevel Limited
    $settings = New-ScheduledTaskSettingsSet -MultipleInstances IgnoreNew -StartWhenAvailable -RunOnlyIfNetworkAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 30) -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries
    if ($Mode -eq 'Preview') {
        [PSCustomObject]@{ TaskName=$taskName; DailyTime=$DailyTime; DaysInterval=$trigger.DaysInterval; Arguments=$arguments; StartAt=$trigger.StartBoundary; RepetitionInterval=$trigger.Repetition.Interval; RepetitionDuration=$trigger.Repetition.Duration; LogonType=[string]$principal.LogonType; RunLevel=[string]$principal.RunLevel; MultipleInstances=[string]$settings.MultipleInstances; RunOnlyIfNetworkAvailable=$settings.RunOnlyIfNetworkAvailable } | ConvertTo-Json
        exit 0
    }
    Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Description 'FileSync: synchronize Documents/Codex and Codex state' -Force | Out-Null
    Write-Host ("已启用：每天 " + $DailyTime + " 同步两个目录（本机时间）。") -ForegroundColor Green
    Write-Host '电脑开机、联网且当前用户已登录时运行；错过时 Windows 会在可用后补跑。日志在 FileSync\logs。'
    Write-Host '请先手动同步成功，确保两个仓库和 GitHub 登录都已配置。'
    exit 0
} catch {
    Write-Host ('定时设置失败：' + $_.Exception.Message) -ForegroundColor Red
    exit 1
}