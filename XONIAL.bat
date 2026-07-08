@echo off
title XONIAL 2026 - Monitoreo de Servicio Social
color 0A

cd /d "%~dp0"

:: ============================================================
:: SOLICITAR PERMISOS DE ADMINISTRADOR
:: ============================================================
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permisos de administrador...
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)

:: ============================================================
:: VERIFICAR QUE start.py EXISTE
:: ============================================================
if not exist "%~dp0start.py" (
    echo [ERROR] No se encuentra start.py en esta carpeta
    echo Asegúrate de que el archivo start.py esté en el mismo directorio.
    pause
    exit /B
)

:: ============================================================
:: MOSTRAR BANNER Y EJECUTAR
:: ============================================================
cls
echo ============================================================
echo          XONIAL 2026 - Monitoreo de Servicio Social
echo              (Modo Administrador)
echo ============================================================
echo.
echo [OK] Permisos de administrador obtenidos
echo [INFO] Directorio de trabajo: %~dp0
echo.
echo Iniciando XONIAL...
echo [INFO] Accede a: http://localhost:5000
echo [INFO] Desde tu red local: http://<TU-IP>:5000
echo.
echo [INFO] Credenciales por defecto: xonial / xonial123
echo.
echo Presiona Ctrl+C para detener el servidor
echo ============================================================
echo.

python start.py

pause