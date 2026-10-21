param([Parameter(Mandatory=$true)][string]$OutputDirectory)
$ErrorActionPreference='Stop'
$deviceId='PCI\VEN_1002&DEV_699F&SUBSYS_00001002&REV_C7\4&2BA2138&0&0008'
$identity=[Security.Principal.WindowsIdentity]::GetCurrent()
$principal=New-Object Security.Principal.WindowsPrincipal($identity)
if(-not $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)){throw 'Administrator authorization was not granted.'}
function Read-GpuState {
 [ordered]@{Time=(Get-Date).ToString('o');Devices=@(Get-CimInstance Win32_VideoController | Select-Object Name,Status,ConfigManagerErrorCode,DriverVersion);AMDProperties=@(Get-PnpDeviceProperty -InstanceId $deviceId -KeyName 'DEVPKEY_Device_ProblemCode','DEVPKEY_Device_ProblemStatus','DEVPKEY_Device_DriverInfPath' | Select-Object KeyName,Data)}
}
$report=[ordered]@{StartedAt=(Get-Date).ToString('o');Action='Restart only the RX550 device with pnputil, without /reboot';Before=(Read-GpuState);SavedDumps=@();RestartExitCode=$null;RestartOutput=$null;After4Seconds=$null;After16Seconds=$null;Error=$null}
$resultPath=Join-Path $OutputDirectory 'recovery-result.json'
function Save-Report {$report | ConvertTo-Json -Depth 8 | Set-Content -LiteralPath $resultPath -Encoding UTF8}
Save-Report
try {
 $dumpDir=Join-Path $OutputDirectory 'evidence'
 New-Item -ItemType Directory -Path $dumpDir -Force | Out-Null
 $dumps=@(Get-ChildItem -LiteralPath 'C:\Windows\LiveKernelReports' -File -Filter '*.dmp' -Recurse -Force -ErrorAction SilentlyContinue | Where-Object {$_.LastWriteTime -ge (Get-Date).Date -and $_.Name -like 'WATCHDOG*' -and $_.Length -lt 20MB} | Sort-Object LastWriteTime -Descending | Select-Object -First 10)
 foreach($dump in $dumps){
  $destination=Join-Path $dumpDir $dump.Name
  Copy-Item -LiteralPath $dump.FullName -Destination $destination -ErrorAction Stop
  $report.SavedDumps+=@([ordered]@{Source=$dump.FullName;SavedTo=$destination;Length=$dump.Length;LastWriteTime=$dump.LastWriteTime.ToString('o')})
 }
 Save-Report
 $report.RestartOutput=(& "$env:SystemRoot\System32\pnputil.exe" /restart-device $deviceId 2>&1 | Out-String)
 $report.RestartExitCode=$LASTEXITCODE
 Save-Report
 Start-Sleep -Seconds 4
 $report.After4Seconds=Read-GpuState
 Save-Report
 Start-Sleep -Seconds 12
 $report.After16Seconds=Read-GpuState
 Save-Report
} catch {
 $report.Error=$_.Exception.Message
 Save-Report
}
