@echo off
setlocal
rem Read-only Windows component checks. Run manually as administrator.
rem This script never starts, stops, or modifies MAA.
"%SystemRoot%\System32\fltmc.exe" >nul 2>&1
if errorlevel 1 (
    echo Administrator rights are required. Right-click this file and choose Run as administrator.
    pause
    exit /b 5
)
set "reportDir=%~dp0health-results"
if not exist "%reportDir%" mkdir "%reportDir%"
if not exist "%reportDir%" exit /b 3
echo Checking the Windows component store. This may take several minutes...
"%SystemRoot%\System32\Dism.exe" /Online /Cleanup-Image /ScanHealth /LogPath:"%reportDir%\dism-detail.log" >"%reportDir%\dism-scan.txt" 2>&1
set "dismResult=%errorlevel%"
echo Verifying protected Windows files. No repair is requested...
"%SystemRoot%\System32\sfc.exe" /verifyonly >"%reportDir%\sfc-verify.txt" 2>&1
set "sfcResult=%errorlevel%"
>"%reportDir%\exit-codes.txt" echo DISM=%dismResult%
>>"%reportDir%\exit-codes.txt" echo SFC=%sfcResult%
echo Checks finished. Results are saved in:
echo "%reportDir%"
echo These checks did not request component repair or font-cache deletion.
pause
exit /b 0
