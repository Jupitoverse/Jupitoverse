@echo off
cd /d "%~dp0"
title Push to GitHub - Data-Annotation

echo ============================================
echo  Push AI Project to Jupitoverse/Data-Annotation
echo ============================================
echo.

echo [1/4] Adding all files...
git add -A
if errorlevel 1 ( echo ERROR: git add failed. & pause & exit /b 1 )
echo Done.
echo.

echo [2/4] Committing...
git commit -m "Data Annotation Platform: Planning, V3 demo, batch scripts, presentation"
if errorlevel 1 (
    echo No changes to commit or already committed. Continuing...
) else (
    echo Done.
)
echo.

echo [3/4] Setting remote origin...
git remote remove origin 2>nul
git remote add origin https://github.com/Jupitoverse/Data-Annotation.git
if errorlevel 1 ( echo ERROR: remote add failed. & pause & exit /b 1 )
git branch -M main 2>nul
echo Done.
echo.

echo [4/4] Pushing to GitHub...
echo If prompted, use your GitHub username and a Personal Access Token as password.
echo.
git push -u origin main
if errorlevel 1 (
    echo.
    echo PUSH FAILED: Check your internet and GitHub login.
    echo Use a Personal Access Token at: https://github.com/settings/tokens
    pause
    exit /b 1
)

echo.
echo ============================================
echo  Success. Repo: https://github.com/Jupitoverse/Data-Annotation
echo ============================================
pause
