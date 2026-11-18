@echo off
title Upload to GitHub
echo ============================================================
echo   Upload pujiang-v0 to GitHub (for cloud build)
echo ============================================================
echo.

REM ====== 在这里填你的信息 ======
set GH_USER=你的GitHub用户名
set GH_TOKEN=你的Token
set GH_REPO=pujiang-v0
REM ==============================

if "%GH_USER%"=="你的GitHub用户名" (
    echo [ERROR] Please edit this file and set GH_USER and GH_TOKEN first.
    echo   See "GitHub云端编译教程.md" step 2 and 3.
    pause
    exit /b
)

where git >nul 2>&1
if errorlevel 1 (
    echo [ERROR] git not found. Install Git for Windows first.
    pause
    exit /b
)

set "SRC_DIR=%~dp0"

cd /d "%SRC_DIR%"

if exist .git (
    echo [OK] .git exists, skip init.
) else (
    git init
)

git config user.name "%GH_USER%"
git config user.email "%GH_USER%@users.noreply.github.com"

git add -A
git commit -m "pujiang V0 - initial" >nul 2>&1

set "REMOTE=https://%GH_USER%:%GH_TOKEN%@github.com/%GH_USER%/%GH_REPO%.git"

git remote remove origin >nul 2>&1
git remote add origin "%REMOTE%"

echo Pushing to GitHub...
git branch -M main
git push -u origin main --force

echo.
echo ============================================================
echo   DONE. Now open:
echo     https://github.com/%GH_USER%/%GH_REPO%/actions
echo   Click "Build V0 APK" -> "Run workflow".
echo ============================================================
pause
