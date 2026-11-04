@echo off
chcp 65001 >nul
if not "%~1"=="" goto one_shot

:main
cls
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync.ps1"
if "%errorlevel%"=="2" exit /b 0
echo.
pause
goto main

:one_shot
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0sync.ps1" %*
set "sync_exit=%errorlevel%"
echo.
pause
exit /b %sync_exit%
