$ErrorActionPreference='Stop'
$resultPath='C:\Users\605\Documents\Codex\2026-11-13\d-2\work\memory-20261118\wpn-result.json'
function Get-Snapshot {
    $service=Get-CimInstance Win32_Service -Filter "Name='WpnUserService_bede8'"
    $process=Get-CimInstance Win32_PerfFormattedData_PerfProc_Process | Where-Object {$_.IDProcess -eq $service.ProcessId -and $service.ProcessId -gt 0} | Select-Object -First 1
    $memory=Get-CimInstance Win32_PerfFormattedData_PerfOS_Memory
    $objects=Get-CimInstance Win32_PerfFormattedData_PerfOS_Objects
    [pscustomobject]@{Time=Get-Date -Format o;ServiceState=$service.State;StartMode=$service.StartMode;ProcessId=$service.ProcessId;Handles=$process.HandleCount;PrivateWSMiB=[math]::Round($process.WorkingSetPrivate/1MB,1);CommitMiB=[math]::Round($process.PrivateBytes/1MB,1);AvailableMiB=$memory.AvailableMBytes;PagedPoolMiB=[math]::Round($memory.PoolPagedBytes/1MB,1);NonpagedPoolMiB=[math]::Round($memory.PoolNonpagedBytes/1MB,1);Events=$objects.Events}
}
$result=[ordered]@{Before=$null;After=$null;Later=$null;Error=$null}
try {
    $result.Before=Get-Snapshot
    Restart-Service -Name WpnUserService_bede8 -ErrorAction Stop
    Start-Sleep -Seconds 5
    $result.After=Get-Snapshot
    $result | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $resultPath -Encoding UTF8
    Start-Sleep -Seconds 25
    $result.Later=Get-Snapshot
} catch {$result.Error=$_.Exception.Message}
$result | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $resultPath -Encoding UTF8
