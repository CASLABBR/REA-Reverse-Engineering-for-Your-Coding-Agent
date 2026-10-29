@echo off
chcp 65001 >nul
title OpenHands Agent Canvas Launcher

echo ==========================================
echo OpenHands Agent Canvas - Startup Script
echo ==========================================
echo.

REM 1. Kill processes on conflicting ports
echo [1/4] Limpando portas conflitantes (8000, 18000, 18001)...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000 :18000 :18001"') do (
    taskkill /F /PID %%a >nul 2>&1 && echo   Matou PID %%a
)
echo   Portas liberadas.
echo.

REM 2. Check/Start 9Router on port 20128
echo [2/4] Verificando 9Router na porta 20128...
curl -s http://localhost:20128/api/health >nul 2>&1
if %errorlevel% equ 0 (
    echo   9Router ja esta rodando!
) else (
    echo   9Router nao esta rodando. Tentando iniciar...
    start /b npx @decolua/9router 2>nul
    timeout /t 3 >nul
    curl -s http://localhost:20128/api/health >nul 2>&1
    if %errorlevel% equ 0 (
        echo   9Router iniciado com sucesso!
    ) else (
        echo   AVISO: 9Router nao iniciou. Verifique se esta instalado: npm i -g @decolua/9router
    )
)
echo.

REM 3. Start OpenHands Agent Canvas Electron app
echo [3/4] Iniciando OpenHands Agent Canvas...
set "OPENHANDS_PATH=C:\Users\Home\AppData\Local\Programs\OpenHands Agent Canvas\OpenHands Agent Canvas.exe"
if exist "%OPENHANDS_PATH%" (
    start "" "%OPENHANDS_PATH%"
    echo   App Electron iniciado.
) else (
    echo   ERRO: OpenHands nao encontrado em %OPENHANDS_PATH%
    echo   Verifique se o OpenHands Agent Canvas esta instalado.
)
echo.

REM 4. Wait for backend to be ready
echo [4/4] Aguardando backend subir (portas 8000, 18000, 18001)...
echo   Primeira execucao pode demorar (instala dependencias npm).
echo.
set MAX_WAIT=120
set COUNT=0
:WAIT_LOOP
curl -s http://localhost:8000 >nul 2>&1
if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo SUCESSO! OpenHands disponivel em:
    echo   http://localhost:8000
    echo ==========================================
    goto END
)
set /a COUNT+=5
if %COUNT% geq %MAX_WAIT% (
    echo.
    echo Timeout: backend nao subiu em %MAX_WAIT% segundos.
    echo Verifique o console do Electron para erros.
    goto END
)
timeout /t 5 >nul
goto WAIT_LOOP

:END
echo.