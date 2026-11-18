@echo off
title PuJiang V0 - One Click Build
echo ============================================================
echo   PuJiang Agent - V0 One Click APK Build
echo   Run as Administrator.
echo ============================================================
echo.

net session >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Please RIGHT-CLICK this file and "Run as administrator".
    pause
    exit /b
)

set "PROJ_DIR=%~dp0"
set "OUT_DIR=%PROJ_DIR%.."

REM ---------- check Ubuntu installed ----------
wsl -l -q 2>nul | findstr /i "Ubuntu" >nul
if errorlevel 1 goto NO_UBUNTU
goto HAVE_UBUNTU

:NO_UBUNTU
echo [ERROR] Ubuntu not installed yet.
echo   First run "StepA_InstallWSL_Offline.bat" as administrator,
echo   reboot, open Ubuntu once to set username, then run this again.
pause
exit /b

:HAVE_UBUNTU
echo [OK] Ubuntu detected.

REM ---------- convert Windows paths to WSL paths ----------
for /f "usebackq delims=" %%i in (`wsl -d Ubuntu-22.04 -- wslpath -a "%PROJ_DIR%"`) do set "PROJ_UNIX=%%i"
for /f "usebackq delims=" %%i in (`wsl -d Ubuntu-22.04 -- wslpath -a "%OUT_DIR%"`) do set "OUT_UNIX=%%i"

if "%PROJ_UNIX%"=="" (
    echo [ERROR] Path conversion failed.
    echo   Open Ubuntu once from Start menu to finish setup, then retry.
    pause
    exit /b
)

echo [STEP 2/3] Building APK inside Ubuntu.
echo             First build downloads ~1-2GB, takes 20-50 minutes.
echo             Please wait, do NOT close this window.
echo.

wsl -d Ubuntu-22.04 -- bash -c "rm -rf ~/pujiang_v0; cp -r '%PROJ_UNIX%' ~/pujiang_v0; cd ~/pujiang_v0 && bash build_in_wsl.sh '%OUT_UNIX%'"

if errorlevel 1 goto BUILD_FAILED

echo.
echo ============================================================
echo   [STEP 3/3] BUILD DONE. APK copied to parent folder:
echo   pujiang-agent\pujiang_v0-0.1-arm64-v8a-debug.apk
echo   Follow README to install it on your phone via Zhuoyitong.
echo ============================================================
echo.
pause
exit /b

:BUILD_FAILED
echo.
echo ============================================================
echo   [ERROR] Build failed. Screenshot the lines near ERROR and
echo   send to me so I can fix the script or switch the mirror.
echo ============================================================
pause
