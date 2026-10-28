$ErrorActionPreference='Stop'
$state=Get-Content -LiteralPath (Join-Path $PSScriptRoot 'graphics-preference-before.json') -Raw | ConvertFrom-Json
if($state.SubKey -ne 'Software\Microsoft\DirectX\UserGpuPreferences'){throw 'Unexpected registry path; stopped'}
$key=[Microsoft.Win32.Registry]::CurrentUser.CreateSubKey($state.SubKey)
try {
    foreach($entry in $state.Entries){
        if($entry.Existed){
            $kind=[Microsoft.Win32.RegistryValueKind]([Enum]::Parse([Microsoft.Win32.RegistryValueKind],$entry.Kind))
            $key.SetValue($entry.Executable,$entry.Value,$kind)
        } else {$key.DeleteValue($entry.Executable,$false)}
    }
} finally {$key.Dispose()}
Write-Output 'Previous per-application graphics preferences restored. Reopen the applications manually to apply.'
