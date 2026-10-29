<#
.SYNOPSIS
    Setup completo speech-to-speech com modelos locais
.DESCRIPTION
    Instala dependências, baixa modelos, configura tudo para rodar 100% local
    Estilo Gemini Live - voz natural, interrupção, streaming
#>

param(
    [string]$Mode = "full",      # full, fast, gguf
    [switch]$DownloadModels,
    [switch]$StartServer
)

$ErrorActionPreference = "Stop"

function Write-Log {
    param([string]$Message, [string]$Level = "INFO")
    $colors = @{ INFO="Cyan"; OK="Green"; WARN="Yellow"; ERR="Red" }
    Write-Host "[$(Get-Date -Format HH:mm:ss)] [$Level] $Message" -ForegroundColor $colors[$Level]
}

function Check-GPU {
    try {
        $nvidia = nvidia-smi --query-gpu=memory.total --format=csv,noheader,nounits 2>$null
        if ($nvidia) {
            $mem = [int]($nvidia.Trim().Split("`n")[0])
            Write-Log "GPU detectada: ${mem}MB VRAM" "OK"
            return $mem
        }
    } catch {}
    Write-Log "Sem GPU NVIDIA - rodará em CPU" "WARN"
    return 0
}

function Install-Dependencies {
    Write-Log "Instalando speech-to-speech..." "INFO"
    pip install "speech-to-speech[all]" -q
    Write-Log "Dependências base instaladas" "OK"

    # Extras opcionais conforme modo
    switch ($Mode) {
        "full" {
            Write-Log "Instalando extras para modo completo (Parakeet, Qwen3-TTS)..." "INFO"
            pip install "speech-to-speech[nemo]" -q
            pip install "speech-to-speech[kokoro]" -q
        }
        "fast" {
            Write-Log "Instalando extras para modo rápido (faster-whisper, Kokoro)..." "INFO"
            pip install "speech-to-speech[faster-whisper]" -q
            pip install "speech-to-speech[kokoro]" -q
        }
        "gguf" {
            Write-Log "Instalando extras para modo GGUF (faster-whisper, Kokoro)..." "INFO"
            pip install "speech-to-speech[faster-whisper]" -q
            pip install "speech-to-speech[kokoro]" -q
        }
    }
}

function Download-Models {
    param([string]$ConfigFile)
    Write-Log "Baixando modelos (primeira execução)..." "INFO"

    # Força download rodando validação
    python -c "
from speech_to_speech.config import load_config, resolve_config
doc = load_config('$ConfigFile')
cfg = resolve_config(doc, include_client=True)
print('Config válida, modelos serão baixados no primeiro run')
"
}

function Start-Server {
    param([string]$ConfigFile)
    Write-Log "Iniciando servidor speech-to-speech..." "OK"
    Write-Log "URL: ws://localhost:8765/v1/realtime" "INFO"
    Write-Log "Pressione Ctrl+C para parar" "WARN"
    speech-to-speech serve -f $ConfigFile
}

function Start-Local {
    param([string]$ConfigFile)
    Write-Log "Iniciando modo local (servidor + cliente loopback)..." "OK"
    speech-to-speech local -f $ConfigFile
}

function Start-Client {
    param([string]$Url = "ws://localhost:8765/v1/realtime")
    Write-Log "Conectando cliente ao $Url ..." "OK"
    speech-to-speech talk --url $Url --voice Aiden --instructions "Você é um assistente de voz útil e natural. Responda em português do Brasil."
}

# ===== MAIN =====
Write-Log "========================================" "INFO"
Write-Log "   speech-to-speech Setup Local" "INFO"
Write-Log "========================================" "INFO"

$gpuMem = Check-GPU

# Seleciona config baseado em GPU e modo
$configFile = switch ($Mode) {
    "fast" { "s2s-local-fast.yaml" }
    "gguf" { "s2s-gguf.yaml" }
    default {
        if ($gpuMem -ge 6000) { "s2s-local.yaml" }  # 6GB+ para Parakeet+Qwen3
        else { "s2s-local-fast.yaml" }
    }
}

$configPath = "E:\INTELIGENCIA_ARTIFICIAL\SKILL\$configFile"
Write-Log "Configuração: $configFile" "INFO"

Install-Dependencies

if ($DownloadModels) {
    Download-Models $configPath
}

if ($StartServer) {
    Start-Server $configPath
    exit
}

# Menu interativo
Write-Log ""
Write-Log "Escolha como executar:" "INFO"
Write-Log "  1) Servidor apenas (para conectar clientes)" "INFO"
Write-Log "  2) Modo local (servidor + microfone/alto-falante)" "INFO"
Write-Log "  3) Cliente apenas (conecta em servidor existente)" "INFO"
Write-Log "  4) Sair" "INFO"

$choice = Read-Host "Opção [1-4]"

switch ($choice) {
    "1" { Start-Server $configPath }
    "2" { Start-Local $configPath }
    "3" { Start-Client }
    default { Write-Log "Saindo..." "INFO" }
}