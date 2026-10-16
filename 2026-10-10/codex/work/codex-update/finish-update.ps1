$ErrorActionPreference = 'Stop'
$taskName = 'CodexClientUpdate-20261010'
$logPath = Join-Path $PSScriptRoot 'finish-update.log'
$packagePath = Join-Path $PSScriptRoot 'ChatGPT-x64.msix'
$expectedVersion = [version]'26.1007.2314.0'
function Write-UpdateLog([string]$message) {
    Add-Content -LiteralPath $logPath -Value ((Get-Date -Format 'yyyy-MM-dd HH:mm:ss') + ' ' + $message)
}
try {
    Write-UpdateLog 'Waiting for client exit.'
    $deadline = (Get-Date).AddMinutes(15)
    do {
        $clientProcesses = @(Get-Process -Name ChatGPT -ErrorAction SilentlyContinue | Where-Object {
            $_.Path -like 'C:\Program Files\WindowsApps\OpenAI.Codex_*\app\ChatGPT.exe'
        })
        if ($clientProcesses.Count -eq 0) { break }
        if ((Get-Date) -gt $deadline) { throw 'Timed out waiting for client exit; no applications were closed.' }
        Start-Sleep -Seconds 1
    } while ($true)
    Write-UpdateLog 'Client exited; checking update signature.'
    $signature = Get-AuthenticodeSignature -LiteralPath $packagePath
    if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -ne 'CN=50BDFD77-8903-4850-9FFE-6E8522F64D5B') {
        throw 'The update signature did not match the installed publisher.'
    }
    Write-UpdateLog 'Applying update.'
    Add-AppxPackage -Path $packagePath -ForceApplicationShutdown -ErrorAction Stop
    $installed = Get-AppxPackage -Name OpenAI.Codex
    if ([version]$installed.Version -lt $expectedVersion) { throw ('Unexpected installed version: ' + $installed.Version) }
    Write-UpdateLog ('SUCCESS installed version ' + $installed.Version)
    Start-Process -FilePath explorer.exe -ArgumentList 'shell:AppsFolder\OpenAI.Codex_2p2nqsd0c76g0!App'
} catch {
    Write-UpdateLog ('FAILED ' + $_.Exception.Message)
    exit 1
} finally {
    Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue
}
