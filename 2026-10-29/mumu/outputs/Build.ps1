$ErrorActionPreference = 'Stop'
$buildDirectory = 'C:\Users\605\Documents\Output\virtrite 2'
New-Item -ItemType Directory -Force -Path $buildDirectory | Out-Null
$bridgeFile = Join-Path $buildDirectory 'MuMuQtBridge.dll'
& 'C:\TDM-GCC-64\bin\g++.exe' -shared -O2 -static -static-libgcc -static-libstdc++ -o $bridgeFile (Join-Path $PSScriptRoot 'MuMuQtBridge.cpp') -luser32
if ($LASTEXITCODE -ne 0) { throw 'MuMuQtBridge build failed.' }
& 'C:\Windows\Microsoft.NET\Framework64\v4.0.30319\csc.exe' /nologo /target:winexe /platform:x64 /codepage:65001 /r:System.Windows.Forms.dll /r:System.Drawing.dll "/out:$buildDirectory\virtrite 2.exe" (Join-Path $PSScriptRoot 'virtrite 2.cs')
if ($LASTEXITCODE -ne 0) { throw 'virtrite 2 build failed.' }
Copy-Item -LiteralPath $bridgeFile -Destination (Join-Path $PSScriptRoot 'MuMuQtBridge.dll') -Force
Write-Output $buildDirectory
