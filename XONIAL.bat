@echo off
title XONIAL 2026 - Monitoreo de Servicio Social
color 0A

:: ============================================================
:: SOLICITAR PERMISOS DE ADMINISTRADOR
:: ============================================================
:: Verificar si ya tiene permisos de administrador
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Solicitando permisos de administrador...
    echo.
    :: Crear script VBS para solicitar elevacion
    echo Set UAC = CreateObject^("Shell.Application"^) > "%temp%\getadmin.vbs"
    echo UAC.ShellExecute "%~s0", "", "", "runas", 1 >> "%temp%\getadmin.vbs"
    "%temp%\getadmin.vbs"
    del "%temp%\getadmin.vbs"
    exit /B
)

:: ============================================================
:: EJECUTAR start.py CON PERMISOS DE ADMINISTRADOR
:: ============================================================
cls
echo ============================================================
echo              XONIAL 2026 - Monitoreo de Servicio Social
echo              (Modo Administrador)
echo ============================================================
echo.
echo [OK] Permisos de administrador obtenidos
echo.
echo Iniciando XONIAL...
echo.
echo [INFO] Credenciales por defecto: xonial / xonial123
echo [INFO] Accede a: http://127.0.0.1:5000/login
echo.
echo Presiona Ctrl+C para detener el servidor
echo ============================================================
echo.

:: Ejecutar start.py
python start.py

:: Pausa si el programa se cierra
pause
