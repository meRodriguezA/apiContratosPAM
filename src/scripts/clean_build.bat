@echo off
cd /d %~dp0\..

echo ==========================
echo  LIMPIANDO BUILD PYINSTALLER
echo ==========================

if exist "dist" (
    echo Borrando dist/ ...
    rmdir /s /q "dist"
) else (
    echo dist/ no existe.
)

if exist "build" (
    echo Borrando build/ ...
    rmdir /s /q "build"
) else (
    echo build/ no existe.
)

if exist "PAM_GeneradorDocs.spec" (
    echo Borrando PAM_GeneradorDocs.spec ...
    del /q "PAM_GeneradorDocs.spec"
) else (
    echo PAM_GeneradorDocs.spec no existe.
)

echo.
echo Limpieza completada.
pause
