@echo off
chcp 65001 >nul
title Voice Chat Local - speech-to-speech

echo ========================================
echo   Voice Chat Local - Estilo Gemini Live
echo ========================================
echo.

echo Verificando instalacao...
python -c "import speech_to_speech; print('OK: speech-to-speech instalado')" 2>nul || (
    echo Instalando speech-to-speech...
    pip install "speech-to-speech[all]" -q
    pip install "speech-to-speech[nemo]" -q
    pip install "speech-to-speech[kokoro]" -q
    pip install "speech-to-speech[faster-whisper]" -q
)

echo.
echo Escolha o modo:
echo.
echo   1) COMPLETO (Parakeet + Qwen3-TTS) - Melhor qualidade, precisa GPU 6GB+
echo   2) RAPIDO (faster-whisper + Kokoro) - Leve, roda em CPU
echo   3) GGUF (llama.cpp + Kokoro) - CPU only, use llama-server separado
echo.
set /p choice="Opcao [1-3]: "

if "%choice%"=="1" set CONFIG=s2s-local.yaml
if "%choice%"=="2" set CONFIG=s2s-local-fast.yaml
if "%choice%"=="3" set CONFIG=s2s-gguf.yaml

if "%CONFIG%"=="" (
    echo Opcao invalida!
    pause
    exit /b 1
)

echo.
echo Iniciando: %CONFIG%
echo.
echo URL do servidor: ws://localhost:8765/v1/realtime
echo Para conectar cliente: speech-to-speech talk --url ws://localhost:8765/v1/realtime
echo.
echo Pressione Ctrl+C para parar
echo ========================================

start "" speech-to-speech local -f %CONFIG%