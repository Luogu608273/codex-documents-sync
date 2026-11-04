$ErrorActionPreference = 'Stop'
$fixture = Join-Path $PSScriptRoot ('fixture-' + [guid]::NewGuid().ToString('N'))
$null = New-Item -ItemType Directory -Path $fixture
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'codex-state.ps1') -Destination (Join-Path $fixture 'codex-state.ps1')
foreach ($name in @('sync.ps1', 'first-connect.ps1', 'repair-chat-index.py', 'codex-preferences.py', 'schedule.ps1', 'sync.cmd', 'sync-all.cmd')) {
    [IO.File]::WriteAllText((Join-Path $fixture $name), 'test fixture')
}
. (Join-Path $fixture 'codex-state.ps1')
$script:Root = Join-Path $fixture 'without-readme'
Export-FileSyncTool
if (@(Get-ChildItem -LiteralPath (Join-Path $script:Root '.filesync-tool') -File).Count -ne 8) { throw 'Missing README export failed' }
Write-Output 'PASS: missing README does not block export'
[IO.File]::WriteAllText((Join-Path $fixture 'README.md'), 'documentation fixture')
$script:Root = Join-Path $fixture 'with-readme'
Export-FileSyncTool
if ([IO.File]::ReadAllText((Join-Path $script:Root '.filesync-tool\README.md')) -ne 'documentation fixture') { throw 'README not exported' }
Write-Output 'PASS: existing README is exported'
Rename-Item -LiteralPath (Join-Path $fixture 'sync.cmd') -NewName 'sync.cmd.saved'
$script:Root = Join-Path $fixture 'missing-required'
$failed = $false
try { Export-FileSyncTool } catch { $failed = $true }
if (-not $failed -or (Test-Path -LiteralPath (Join-Path $script:Root '.filesync-tool'))) { throw 'Required script check failed' }
Write-Output 'PASS: missing required script stops before copying'
Rename-Item -LiteralPath (Join-Path $fixture 'sync.cmd.saved') -NewName 'sync.cmd'
Rename-Item -LiteralPath (Join-Path $fixture 'README.md') -NewName 'README.saved'
$null = New-Item -ItemType Directory -Path (Join-Path $fixture 'README.md')
$script:Root = Join-Path $fixture 'invalid-readme'
$failed = $false
try { Export-FileSyncTool } catch { $failed = $true }
if (-not $failed) { throw 'Invalid README accepted' }
Write-Output 'PASS: invalid README object is rejected'
