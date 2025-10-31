@echo off
chcp 65001 > nul
cd /d "%~dp0"

echo ============================================================
echo 로젠택배 비밀번호 업데이트
echo ============================================================
echo.

python update_password.py

echo.
pause
