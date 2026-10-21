param([string]$OutputDirectory)
$ErrorActionPreference='Stop'
$deviceId='PCI\VEN_1002&DEV_699F&SUBSYS_00001002&REV_C7\4&2BA2138&0&0008'
$report=[ordered]@{Started=(Get-Date).ToString('o');Before=@(Get-CimInstance Win32_VideoController | Select-Object Name,Status,ConfigManagerErrorCode,DriverVersion);DisableOutput=$null;DisableExit=$null;EnableOutput=$null;EnableExit=$null;After=$null;Error=$null}
$resultPath=Join-Path $OutputDirectory 'enable-cycle-result.json'
function Save-Report {$report | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $resultPath -Encoding UTF8}
Save-Report
try {
 $report.DisableOutput=(& "$env:SystemRoot\System32\pnputil.exe" /disable-device $deviceId 2>&1 | Out-String)
 $report.DisableExit=$LASTEXITCODE
 Save-Report
} catch {$report.Error=$_.Exception.Message} finally {
 $report.EnableOutput=(& "$env:SystemRoot\System32\pnputil.exe" /enable-device $deviceId 2>&1 | Out-String)
 $report.EnableExit=$LASTEXITCODE
 Save-Report
}
Start-Sleep -Seconds 6
$report.After=@(Get-CimInstance Win32_VideoController | Select-Object Name,Status,ConfigManagerErrorCode,DriverVersion)
Save-Report
