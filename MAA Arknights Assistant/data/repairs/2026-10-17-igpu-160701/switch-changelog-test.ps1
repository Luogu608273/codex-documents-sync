param([Parameter(Mandatory)][ValidateSet('Apply','Restore')][string]$Mode)
$ErrorActionPreference = 'Stop'
$target = 'D:\MAA-Arknights-Assistant\data\CHANGELOG.md'
$original = Join-Path $PSScriptRoot 'CHANGELOG.pre-avatar-test.md'
$candidate = Join-Path $PSScriptRoot 'CHANGELOG.link-only.md'
$originalHash = '9E2924248360A61545417D8F89D6CB5B4E906B1A5690F58B1C6020A8E9F19F09'
$candidateHash = '3D5F14C257181F520EC3386EE3D91F3007D0D409AE42E11F6A9CC673855622A6'
if (Get-Process -Name MAA -ErrorAction SilentlyContinue) {
    throw '请先手动完全退出 MAA。脚本不会结束或启动任何程序。'
}
if ((Get-FileHash -LiteralPath $original).Hash -ne $originalHash -or (Get-FileHash -LiteralPath $candidate).Hash -ne $candidateHash) {
    throw '备份或对照版本校验不符，停止替换。'
}
$currentHash = (Get-FileHash -LiteralPath $target).Hash
if ($Mode -eq 'Apply') {
    if ($currentHash -eq $candidateHash) { Write-Output 'Already applied'; exit 0 }
    if ($currentHash -ne $originalHash) { throw '日志已被其他程序更新，停止覆盖。' }
    Copy-Item -LiteralPath $candidate -Destination $target
    $expectedHash = $candidateHash
} else {
    if ($currentHash -eq $originalHash) { Write-Output 'Already original'; exit 0 }
    if ($currentHash -ne $candidateHash) { throw '日志已被其他程序更新，停止覆盖。' }
    Copy-Item -LiteralPath $original -Destination $target
    $expectedHash = $originalHash
}
if ((Get-FileHash -LiteralPath $target).Hash -ne $expectedHash) { throw '写入后的校验失败。' }
Write-Output "$Mode verified; no executable or configuration changed."
