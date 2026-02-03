@echo off
REM ============================================================
REM SR Email Processor - Fetch Emails from Outlook (GSSUTSMAIL)
REM Downloads today's Excel attachments and uploads to Linux server
REM TARGET: inoscmm2222.corp.amdocs.com
REM ============================================================

echo ================================================================
echo    SR Email Processor - Fetch from Outlook
echo    TARGET SERVER: inoscmm2222
echo ================================================================
echo.

REM Configuration - MODIFY THESE SETTINGS
set "LINUX_SERVER=inoscmm2222.corp.amdocs.com"
set "LINUX_USER=rke"
set "LINUX_PATH=/ossusers1/oss/users/rke/sr-analyzer/semantic-resolution/input"
set "LOCAL_DOWNLOAD_FOLDER=%~dp0downloads"
set "SENDER_EMAIL=GSSUTSMail@amdocs.com"

echo [1/4] Setting up local download folder...
if not exist "%LOCAL_DOWNLOAD_FOLDER%" mkdir "%LOCAL_DOWNLOAD_FOLDER%"

REM Clear old files to ensure only today's files are uploaded
echo       Clearing old files from downloads folder...
del /q "%LOCAL_DOWNLOAD_FOLDER%\*.xls" 2>nul
del /q "%LOCAL_DOWNLOAD_FOLDER%\*.xlsx" 2>nul
echo       Folder: %LOCAL_DOWNLOAD_FOLDER%
echo.

echo [2/4] Fetching today's emails from Outlook (FROM: %SENDER_EMAIL%)...
powershell -ExecutionPolicy Bypass -File "%~dp0fetch_outlook_attachments.ps1" -DownloadFolder "%LOCAL_DOWNLOAD_FOLDER%" -SenderEmail "%SENDER_EMAIL%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Failed to fetch emails from Outlook!
    echo         Make sure Outlook is running and you have emails from %SENDER_EMAIL%
    pause
    exit /b 1
)
echo.

echo [3/4] Checking for downloaded files...
set "FILE_COUNT=0"
for %%f in ("%LOCAL_DOWNLOAD_FOLDER%\*.xls" "%LOCAL_DOWNLOAD_FOLDER%\*.xlsx") do set /a FILE_COUNT+=1

if %FILE_COUNT% EQU 0 (
    echo       No Excel files found for today.
    echo.
    pause
    exit /b 0
)
echo       Found %FILE_COUNT% Excel file(s)
echo.

echo [4/4] Uploading to Linux server...
echo       Server: %LINUX_USER%@%LINUX_SERVER%:%LINUX_PATH%
echo.

REM Try SCP first (if OpenSSH is available)
where scp >nul 2>&1
if %ERRORLEVEL% EQU 0 (
    echo       Using SCP for upload...
    for %%f in ("%LOCAL_DOWNLOAD_FOLDER%\*.xls" "%LOCAL_DOWNLOAD_FOLDER%\*.xlsx") do (
        echo       Uploading: %%~nxf
        scp "%%f" "%LINUX_USER%@%LINUX_SERVER%:%LINUX_PATH%/"
    )
) else (
    echo [WARN] SCP not found. Please install OpenSSH or manually copy files.
    echo        Files are in: %LOCAL_DOWNLOAD_FOLDER%
    echo.
    echo        Manual upload command:
    echo        scp "%LOCAL_DOWNLOAD_FOLDER%\*.xlsx" %LINUX_USER%@%LINUX_SERVER%:%LINUX_PATH%/
)

echo.
echo ================================================================
echo    COMPLETE! Files uploaded to inoscmm2222
echo ================================================================
echo.
echo Next steps:
echo   1. Go to https://%LINUX_SERVER%:5000/admin
echo   2. Click "Process Uploaded Files" or "Fetch from Outlook"
echo.
pause

