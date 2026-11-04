@echo off
chcp 65001 >nul
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync.ps1" -Target All -Action Sync
set "sync_exit=%errorlevel%"
echo.
pause
exit /b %sync_exit%