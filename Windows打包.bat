@echo off
title PuJiang V0 - Build APK (Windows Native)
echo ============================================================
echo   PuJiang Agent - V0 Windows Native Build
echo   No WSL / No Docker / No Microsoft Store needed.
echo ============================================================
echo.

REM --- use the same Python that WorkBuddy ships (3.13, on PATH) ---
where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found on PATH.
    echo   Install Python 3.10+ from https://www.python.org/downloads/
    pause
    exit /b
)

echo [OK] Python found.
echo.
echo This script will download and build everything locally:
echo   - JDK 17        (Tsinghua mirror)
echo   - Android SDK   (dl.google.com, verified reachable)
echo   - python-for-android (Tsinghua pypi)
echo.
echo First run downloads ~1-2GB and takes 30-60 minutes.
echo Please wait, do NOT close this window.
echo.

python "%~dp0build_apk.py"
if errorlevel 1 goto FAILED

echo.
echo ============================================================
echo   DONE. APK is in v0-kivy-test\dist\ folder.
echo ============================================================
pause
exit /b

:FAILED
echo.
echo [ERROR] Build failed. Screenshot the error lines and send to me.
pause
