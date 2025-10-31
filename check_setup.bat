@echo off
cd /d "%~dp0"

echo ============================================================
echo Environment Setup Check
echo ============================================================
echo.

echo [1] Python Version:
python --version
if %errorlevel% neq 0 (
    echo [ERROR] Python not found or not in PATH
    echo Please install Python 3.8+: https://www.python.org/downloads/
    goto end
)
echo.

echo [2] Installed Libraries:
pip list | findstr "requests openpyxl schedule"
echo.

echo [3] Project Files:
if exist "logen_api.py" (
    echo [OK] logen_api.py exists
) else (
    echo [MISSING] logen_api.py
)

if exist "config.json" (
    echo [OK] config.json exists
) else (
    echo [MISSING] config.json - Please copy from config.example.json
)

if exist "requirements.txt" (
    echo [OK] requirements.txt exists
) else (
    echo [MISSING] requirements.txt
)
echo.

echo [4] Folder Structure:
if exist "logs" (
    echo [OK] logs folder exists
) else (
    echo [INFO] logs folder will be auto-created
)

if exist "downloads" (
    echo [OK] downloads folder exists
) else (
    echo [INFO] downloads folder will be auto-created
)

if exist "docs" (
    echo [OK] docs folder exists
) else (
    echo [MISSING] docs folder
)
echo.

:end
echo ============================================================
pause
