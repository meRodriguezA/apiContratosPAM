@echo off
cd /d %~dp0

echo Iniciando PAM API Web...
echo.

.\.venv\Scripts\activate && python api.py

pause