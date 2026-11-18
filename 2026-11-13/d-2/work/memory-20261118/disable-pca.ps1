$ErrorActionPreference='Stop'
$resultPath='C:\Users\605\Documents\Codex\2026-11-13\d-2\work\memory-20261118\disable-result.json'
$result=[ordered]@{Before=$null;After=$null;Error=$null}
try {
    $result.Before=Get-CimInstance Win32_Service -Filter "Name='PcaSvc'" | Select-Object Name,State,StartMode,ProcessId
    Set-Service -Name PcaSvc -StartupType Disabled -ErrorAction Stop
    Stop-Service -Name PcaSvc -ErrorAction Stop
    (Get-Service -Name PcaSvc).WaitForStatus([System.ServiceProcess.ServiceControllerStatus]::Stopped,[TimeSpan]::FromSeconds(30))
    $result.After=Get-CimInstance Win32_Service -Filter "Name='PcaSvc'" | Select-Object Name,State,StartMode,ProcessId
} catch {$result.Error=$_.Exception.Message}
$result | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $resultPath -Encoding UTF8
