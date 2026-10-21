param([Parameter(Mandatory=$true)][string]$ResultPath)
$ErrorActionPreference='Continue'
$readErrors=@()
$identity=[Security.Principal.WindowsIdentity]::GetCurrent()
$principal=New-Object Security.Principal.WindowsPrincipal($identity)
$report=[ordered]@{CheckedAt=(Get-Date).ToString('o');IsAdministrator=$principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator);Scope='Read graphics failure logs and crash-report file metadata only';Files=@();Events=@();ReadErrors=@()}
foreach($p in @('C:\Windows\LiveKernelReports','C:\ProgramData\Microsoft\Windows\WER\ReportArchive','C:\ProgramData\Microsoft\Windows\WER\ReportQueue')) {
 if(Test-Path -LiteralPath $p){
  $report.Files+=@(Get-ChildItem -LiteralPath $p -File -Recurse -Force -ErrorAction SilentlyContinue -ErrorVariable +readErrors | Sort-Object LastWriteTime -Descending | Select-Object -First 50 FullName,Length,CreationTime,LastWriteTime)
 }
}
$start=(Get-Date).Date
foreach($logName in @('System','Application','Microsoft-Windows-Kernel-PnP/Configuration')){
 $report.Events+=@(Get-WinEvent -FilterHashtable @{LogName=$logName;StartTime=$start} -ErrorAction SilentlyContinue | Where-Object {$_.ProviderName -eq 'Display' -or $_.Message -match 'VEN_1002&DEV_699F|amdwddmg|amdkmdag|LiveKernelEvent|Radeon|AMD Software'} | Select-Object -First 50 TimeCreated,LogName,Id,ProviderName,Message)
}
$report.ReadErrors=@($readErrors | ForEach-Object {$_.Exception.Message})
$report | ConvertTo-Json -Depth 7 | Set-Content -LiteralPath $ResultPath -Encoding UTF8
