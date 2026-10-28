$ErrorActionPreference = 'Stop'
$state = Get-Content -LiteralPath (Join-Path $PSScriptRoot 'registry-before.json') -Raw | ConvertFrom-Json
if ($state.Hive -ne 'HKEY_CURRENT_USER' -or $state.SubKey -ne 'Software\Microsoft\Avalon.Graphics' -or $state.ValueName -ne 'DisableHWAcceleration') { throw 'Unexpected backup target; stopped' }
$key = [Microsoft.Win32.Registry]::CurrentUser.OpenSubKey($state.SubKey, $true)
if ($state.ValueExisted) {
    if (-not $key) { $key = [Microsoft.Win32.Registry]::CurrentUser.CreateSubKey($state.SubKey) }
    $kind = [Microsoft.Win32.RegistryValueKind]([Enum]::Parse([Microsoft.Win32.RegistryValueKind], $state.PreviousKind))
    $key.SetValue($state.ValueName, $state.PreviousValue, $kind)
} elseif ($key) {
    $key.DeleteValue($state.ValueName, $false)
}
if ($key) { $key.Dispose() }
Write-Output 'Previous WPF rendering configuration restored. Changes apply to newly started WPF processes.'
