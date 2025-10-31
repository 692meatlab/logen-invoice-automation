@echo off
cd /d "%~dp0"

echo ============================================================
echo Installing Python Libraries
echo ============================================================
echo.

pip install -r requirements.txt

echo.
if %errorlevel% equ 0 (
    echo ============================================================
    echo Installation Complete!
    echo ============================================================
) else (
    echo ============================================================
    echo Installation Failed! Check error messages above.
    echo ============================================================
)
echo.
pause
