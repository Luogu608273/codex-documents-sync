param([Parameter(Mandatory=$true)][string]$SyncScript,[string]$Git='C:\Program Files\Git\cmd\git.exe')
$ErrorActionPreference='Stop'
$utf8=New-Object Text.UTF8Encoding($false)
$tokens=$null;$errors=$null
$ast=[Management.Automation.Language.Parser]::ParseFile($SyncScript,[ref]$tokens,[ref]$errors)
if($errors.Count){throw ($errors | Out-String)}
foreach($node in $ast.FindAll({param($n) $n -is [Management.Automation.Language.FunctionDefinitionAst]},$false)){. ([scriptblock]::Create($node.Extent.Text))}
foreach($node in $ast.FindAll({param($n) $n -is [Management.Automation.Language.AssignmentStatementAst] -and $n.Left.Extent.Text -eq '$codexIgnore'},$false)){. ([scriptblock]::Create($node.Extent.Text))}
. (Join-Path (Split-Path $SyncScript) 'codex-state.ps1')
. (Join-Path (Split-Path $SyncScript) 'first-connect.ps1')
$script:Git=$Git
$base=Join-Path 'C:\Users\605\Documents\Output' ('FileSync-exclusion-tests-'+[Guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $base -Force | Out-Null
$saved=@{}
foreach($key in @('GIT_CONFIG_GLOBAL','GIT_CONFIG_NOSYSTEM','GIT_AUTHOR_NAME','GIT_AUTHOR_EMAIL','GIT_COMMITTER_NAME','GIT_COMMITTER_EMAIL','EMAIL')){
 $saved[$key]=[Environment]::GetEnvironmentVariable($key,'Process');[Environment]::SetEnvironmentVariable($key,$null,'Process')
}
$env:GIT_CONFIG_GLOBAL=Join-Path $base 'isolated-config';$env:GIT_CONFIG_NOSYSTEM='1'
function Assert($Condition,$Message){if(-not $Condition){throw $Message}}
try {
 $script:Root=Join-Path $base 'Documents';New-Item -ItemType Directory -Path $script:Root | Out-Null
 New-Item -ItemType Directory -Path (Join-Path $script:Root 'nested') | Out-Null
 $names=@('sample.in','upper.IN','tool.exe','nested/mixed.ExE','nested/source.cpp','memory.rmp','nested/UPPER.RMP','keep.out','hidden.ignore')
 foreach($name in $names){[IO.File]::WriteAllText((Join-Path $script:Root $name),('fixture '+$name),$utf8)}
 [IO.File]::WriteAllText((Join-Path $script:Root '.gitignore'),"*.ignore`n!*.exe`n",$utf8)
 Invoke-Git @('init','-q','-b','main')
 Invoke-Git @('config','user.name','Fixture');Invoke-Git @('config','user.email','fixture@example.invalid')
 Invoke-Git @('config','commit.gpgsign','false')
 Invoke-Git @('add','-f','--','.')
 Invoke-Git @('commit','-qm','fixture before exclusions')
 Assert ((@(Get-DocumentsExclusions)).Count -eq 2) 'RAMMap snapshots not excluded'
 $localHashes=@{};foreach($name in $names){$localHashes[$name]=(Get-FileHash -LiteralPath (Join-Path $script:Root $name)).Hash}
 Invoke-Git @('remote','add','origin',$base)
 $Target='Documents';$Message='fixture exclusion update';$NonInteractive=$true
 Save-Changes
 $tracked=@(Invoke-Git @('ls-files') -Capture)
 Assert (-not @($tracked | Where-Object {$_ -match '(?i)\.(in|exe|rmp)$'}).Count) 'forced add retained excluded extension'
 foreach($name in $names){Assert ((Get-FileHash -LiteralPath (Join-Path $script:Root $name)).Hash -ceq $localHashes[$name]) ('local file changed: '+$name)}
 Assert ('nested/source.cpp' -in $tracked -and 'hidden.ignore' -in $tracked) 'ordinary forced-add scope changed'
 $ignore=[IO.File]::ReadAllText((Join-Path $script:Root '.gitignore'))
 Update-InstallerIgnore -Paths @(Get-DocumentsExclusions)
 Assert ($ignore -ceq [IO.File]::ReadAllText((Join-Path $script:Root '.gitignore'))) 'ignore block is not stable'
 [IO.File]::WriteAllText((Join-Path $script:Root 'new.IN'),'new ignored input',$utf8)
 [IO.File]::WriteAllText((Join-Path $script:Root 'nested/new.EXE'),'new ignored binary',$utf8)
 $paths=@('status','--porcelain','--ignored','--','.',':(top,icase,glob,exclude)**/*.in',':(top,icase,glob,exclude)**/*.exe')
 foreach($excluded in @(Get-DocumentsExclusions)){$paths += ':(top,literal,exclude)'+$excluded}
 Assert (-not @(Invoke-Git $paths -Capture).Count) 'excluded files block pull status'
 Assert (Test-DocumentsExcludedPath 'missing/deleted.EXE' @()) 'deleted tracked extension not excluded'
 Write-Output 'PASS Documents tracked removal, forced add, local preservation, case-insensitivity and pull status'

 $script:Root=Join-Path $base 'Codex';New-Item -ItemType Directory -Path $script:Root | Out-Null
 Invoke-Git @('init','-q','-b','main')
 New-Item -ItemType Directory -Path (Join-Path $script:Root 'skills/custom') -Force | Out-Null
 New-Item -ItemType Directory -Path (Join-Path $script:Root 'memories') -Force | Out-Null
 [IO.File]::WriteAllText((Join-Path $script:Root 'skills/custom/runner.EXE'),'binary fixture',$utf8)
 [IO.File]::WriteAllText((Join-Path $script:Root 'skills/custom/test.in'),'input fixture',$utf8)
 [IO.File]::WriteAllText((Join-Path $script:Root 'skills/custom/SKILL.md'),'skill fixture',$utf8)
 [IO.File]::WriteAllText((Join-Path $script:Root 'memories/a.in'),'input fixture',$utf8)
 [IO.File]::WriteAllText((Join-Path $script:Root 'memories/b.EXE'),'binary fixture',$utf8)
 [IO.File]::WriteAllText((Join-Path $script:Root 'memories/keep.md'),'memory fixture',$utf8)
 Invoke-Git @('add','-f','--','skills')
 Update-CodexRules
 Assert (-not @(Invoke-Git @('ls-files','--',':(top,icase,glob)**/*.in',':(top,icase,glob)**/*.exe') -Capture).Count) 'Codex excluded extensions remain tracked'
 $inventory=Get-MemoryInventory (Join-Path $script:Root 'memories')
 Assert ($inventory.Count -eq 1 -and $inventory.ContainsKey('keep.md')) 'memory inventory includes excluded files'
 $legacy=@{'a.in'='0'*64;'b.EXE'='1'*64;'keep.md'=$inventory['keep.md']}
 $manifest=Join-Path $base 'legacy-manifest.json';Write-MemoryMap $manifest $legacy
 $map=Read-MemoryMap $manifest
 Assert ($map.Count -eq 1 -and $map['keep.md'] -ceq $inventory['keep.md']) 'legacy memory manifest incompatible'
 Assert (-not (Test-FirstManagedPath 'attachments/test.IN')) 'first connection admits excluded extension'
 Assert (-not (Test-FirstManagedPath 'skills/custom/tool.exe')) 'first connection admits binary'
 Assert (Test-FirstManagedPath 'skills/custom/SKILL.md') 'first connection excludes unrelated content'
 Invoke-Git @('add','-A')
 Assert (-not @(Invoke-Git @('ls-files','--',':(top,icase,glob)**/*.in',':(top,icase,glob)**/*.exe') -Capture).Count) 'Codex add reintroduced excluded files'
 Write-Output 'PASS Codex skills, memory inventory, old snapshot manifests and first connection exclusions'
 Write-Output 'ExclusionRegression=PASS'
} finally {
 foreach($key in $saved.Keys){[Environment]::SetEnvironmentVariable($key,$saved[$key],'Process')}
 $resolved=[IO.Path]::GetFullPath($base)
 if([IO.Path]::GetDirectoryName($resolved) -ne 'C:\Users\605\Documents\Output' -or [IO.Path]::GetFileName($resolved) -notlike 'FileSync-exclusion-tests-*'){throw 'Unexpected fixture path'}
 Remove-Item -LiteralPath $resolved -Recurse -Force
}
