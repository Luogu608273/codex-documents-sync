$ErrorActionPreference='Stop'
$resultPath='C:\Users\605\Documents\Codex\2026-11-13\d-2\work\memory-20261118\restart-result.json'
function Get-Snapshot {
    $memory=Get-CimInstance Win32_PerfFormattedData_PerfOS_Memory
    $objects=Get-CimInstance Win32_PerfFormattedData_PerfOS_Objects
    $system=Get-CimInstance Win32_PerfFormattedData_PerfOS_System
    $service=Get-CimInstance Win32_Service -Filter "Name='PcaSvc'"
    $handles=0
    if ($service.ProcessId -gt 0) {$handles=(Get-Process -Id $service.ProcessId).HandleCount}
    [pscustomobject]@{Time=(Get-Date -Format o);AvailableMiB=$memory.AvailableMBytes;CommitMiB=[math]::Round($memory.CommittedBytes/1MB);NonpagedMiB=[math]::Round($memory.PoolNonpagedBytes/1MB);ProcessObjects=$objects.Processes;RunningProcesses=$system.Processes;PcaPid=$service.ProcessId;PcaHandles=$handles;PcaState=$service.State}
}
$result=[ordered]@{Before=$null;After=$null;Error=$null}
try {
    $result.Before=Get-Snapshot
    Restart-Service -Name PcaSvc -ErrorAction Stop
    Start-Sleep -Seconds 8
    $result.After=Get-Snapshot
} catch {$result.Error=$_.Exception.Message}
$result | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $resultPath -Encoding UTF8
