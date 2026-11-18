@echo off
title PuJiang V0 - Step A - Install WSL Offline
echo ============================================================
echo   Step A - Install Ubuntu 22.04 OFFLINE (bypass Store)
echo   Run this as Administrator.
echo ============================================================
echo.

net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Please RIGHT-CLICK this file and "Run as administrator".
    pause
    exit /b
)

echo [A1/4] Enabling Windows features for WSL (local, no download)...
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

echo.
echo [A2/4] Downloading Ubuntu 22.04 package from Microsoft CDN (~500MB)...
echo         This is a direct link, NOT the Microsoft Store.
powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://aka.ms/wslubuntu2204' -OutFile '%TEMP%\Ubuntu2204.appx' -UseBasicParsing"
if errorlevel 1 goto DL_FAILED
if not exist "%TEMP%\Ubuntu2204.appx" goto DL_FAILED

echo.
echo [A3/4] Downloading WSL2 Linux kernel update...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Invoke-WebRequest -Uri 'https://wslstorestorage.blob.core.windows.net/wslblob/wsl_update_x64.msi' -OutFile '%TEMP%\wsl_update_x64.msi' -UseBasicParsing"
if errorlevel 1 goto KERNEL_FAILED
if not exist "%TEMP%\wsl_update_x64.msi" goto KERNEL_FAILED

echo.
echo [A4/4] Installing WSL2 kernel + Ubuntu package...
msiexec /i "%TEMP%\wsl_update_x64.msi" /quiet /norestart
powershell -NoProfile -ExecutionPolicy Bypass -Command "Add-AppxPackage -Path '%TEMP%\Ubuntu2204.appx'"
if errorlevel 1 goto INSTALL_FAILED

echo.
echo ============================================================
echo   Ubuntu install DONE.
echo   NEXT:
echo     1. REBOOT your PC.
echo     2. After reboot, open "Ubuntu 22.04" from Start menu once,
echo        set a Linux username + password (only once).
echo     3. Then run "OneClickBuild.bat" as administrator to build.
echo ============================================================
pause
exit /b

:DL_FAILED
echo [ERROR] Ubuntu package download failed. Send this to me.
pause
exit /b

:KERNEL_FAILED
echo [ERROR] WSL2 kernel download failed. Send this to me.
pause
exit /b

:INSTALL_FAILED
echo [ERROR] Ubuntu install failed. Send the error lines to me.
pause
exit /b
