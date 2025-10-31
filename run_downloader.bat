@echo off
chcp 65001 > nul
echo ============================================================
echo 로젠택배 송장 자동 다운로드 프로그램
echo ============================================================
echo.

cd /d "%~dp0"

python logen_invoice_downloader.py

echo.
pause
