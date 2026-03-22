@echo off
cd /d %~dp0

echo Iniciando PAM API Web...
echo.

.\.venv\Scripts\activate && uvicorn app:app --host 0.0.0.0 --port 10000

pause