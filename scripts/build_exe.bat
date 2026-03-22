@echo off
cd /d %~dp0\..

.\.venv\Scripts\python.exe -m PyInstaller --onefile --name PAM_GeneradorDocs ^
  --add-data "plantillas;plantillas" ^
  --add-data "conf;conf" ^
  GenerarDocs.py

pause
