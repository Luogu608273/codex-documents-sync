$ErrorActionPreference='Stop'
$resultPath='C:\Users\605\Documents\Codex\2026-11-13\d-2\work\memory-20261121\capture-result.json'
try {
    $existing=Get-Process -Id 23164 -ErrorAction SilentlyContinue
    if ($existing -and $existing.ProcessName -eq 'rammap64') {Stop-Process -Id $existing.Id -ErrorAction Stop}
    $capture=Start-Process -FilePath 'C:\Users\605\Downloads\RAMMap\RAMMap.exe' -ArgumentList @('"C:\Users\605\Documents\Codex\2026-11-13\d-2\work\memory-20261121\memory.rmp"') -WindowStyle Hidden -PassThru
    if (-not $capture.WaitForExit(45000)) {throw 'RAMMap snapshot process is still running after 45 seconds'}
    [pscustomobject]@{ExitCode=$capture.ExitCode;Error=$null} | ConvertTo-Json | Set-Content -LiteralPath $resultPath -Encoding UTF8
} catch {[pscustomobject]@{Error=$_.Exception.Message} | ConvertTo-Json | Set-Content -LiteralPath $resultPath -Encoding UTF8}
