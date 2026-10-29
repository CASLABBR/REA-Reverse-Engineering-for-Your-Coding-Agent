# Voice Chat Local - speech-to-speech (Estilo Gemini Live)

## Instalação Rápida

```bash
# 1. Instala tudo
pip install "speech-to-speech[all]" -q
pip install "speech-to-speech[nemo]" -q
pip install "speech-to-speech[kokoro]" -q
pip install "speech-to-speech[faster-whisper]" -q

# 2. Roda modo local (servidor + microfone/auto-falante)
speech-to-speech local -f s2s-local.yaml
```

## 3 Modos de Configuração

| Arquivo | STT | LLM | TTS | Requisitos | Qualidade |
|---------|-----|-----|-----|------------|-----------|
| `s2s-local.yaml` | Parakeet TDT | Qwen2.5-3B | Qwen3-TTS | GPU 6GB+ | ⭐⭐⭐ Melhor |
| `s2s-local-fast.yaml` | faster-whisper | Phi-3.5-mini | Kokoro | CPU / 4GB RAM | ⭐⭐ Boa |
| `s2s-gguf.yaml` | faster-whisper | llama.cpp (GGUF) | Kokoro | CPU only | ⭐⭐ Boa |

## Como Usar

### Opção 1: Script Automático (Windows)
```cmd
start-voice-chat.bat
```

### Opção 2: PowerShell Completo
```powershell
# Instala + baixa modelos + menu interativo
.\setup-speech-to-speech.ps1 -Mode full -DownloadModels

# Ou direto servidor
.\setup-speech-to-speech.ps1 -Mode fast -StartServer
```

### Opção 3: Comandos Diretos
```bash
# Servidor (roda em background)
speech-to-speech serve -f s2s-local.yaml

# Cliente conecta no servidor (outro terminal)
speech-to-speech talk --url ws://localhost:8765/v1/realtime --voice Aiden

# Modo local tudo-em-um (microfone + speaker)
speech-to-speech local -f s2s-local.yaml
```

## Modelos Locais Suportados

### STT (Speech-to-Text)
| Backend | Modelo | Comando Extra |
|---------|--------|---------------|
| `parakeet-tdt` | `nvidia/parakeet-tdt-0.6b-v2` | `pip install "speech-to-speech[nemo]"` |
| `faster-whisper` | `tiny/base/small/medium/large-v3` | `pip install "speech-to-speech[faster-whisper]"` |
| `whisper` | OpenAI Whisper local | `pip install "speech-to-speech[whisper]"` |
| `mlx-audio-whisper` | MLX Whisper (Apple Silicon) | `pip install "speech-to-speech[whisper-mlx]"` |

### LLM (Local)
| Backend | Modelos Recomendados PT-BR |
|---------|----------------------------|
| `transformers` | `Qwen/Qwen2.5-3B-Instruct`, `microsoft/Phi-3.5-mini-instruct`, `meta-llama/Llama-3.2-3B-Instruct` |
| `mlx-lm` | Mesmo acima (Apple Silicon) |
| `chat-completions` | Qualquer via llama.cpp / vLLM / Ollama |

### TTS (Text-to-Speech)
| Backend | Modelo | Vozes | Extra |
|---------|--------|-------|-------|
| `qwen3` | `Qwen/Qwen3-TTS-12Hz-1.7B-CustomVoice` | Aiden, Ethan, Liam, Noah... | - |
| `kokoro` | `hexgrad/Kokoro-82M` | pf_dora, pm_alex, pf_bella... | `pip install "speech-to-speech[kokoro]"` |
| `chatTTS` | ChatTTS | Múltiplas | `pip install "speech-to-speech[chattts]"` |

## Exemplo YAML Customizado

```yaml
schema_version: 1
runtime:
  server:
    host: "0.0.0.0"
    port: 8765
  client:
    voice: "Aiden"
    instructions: "Responda em português do Brasil, seja natural e conversacional."

blocks:
  vad_meu:
    kind: vad
    backend: silero
    settings:
      vad: silero
      threshold: 0.5
  
  stt_meu:
    kind: stt
    backend: faster-whisper
    settings:
      faster_whisper_stt_model_name: "small"
      faster_whisper_stt_device: "cpu"
      faster_whisper_stt_compute_type: "int8"
      faster_whisper_stt_language: "pt"
  
  llm_meu:
    kind: llm
    backend: transformers
    settings:
      llm_model_name: "Qwen/Qwen2.5-3B-Instruct"
      llm_device: "auto"
      llm_max_new_tokens: 512
      llm_temperature: 0.7
  
  tts_meu:
    kind: tts
    backend: kokoro
    settings:
      kokoro_model_name: "hexgrad/Kokoro-82M"
      kokoro_voice: "pf_dora"
      kokoro_language: "pt"

pipelines:
  meu_pipeline:
    stages:
      vad: vad_meu
      stt: stt_meu
      llm: llm_meu
      tts: tts_meu
    num_pipelines: 1
    options:
      enable_live_transcription: true
```

## Troubleshooting

| Problema | Solução |
|----------|---------|
| `ModuleNotFoundError: nemo` | `pip install "speech-to-speech[nemo]"` |
| `CUDA out of memory` | Use `s2s-local-fast.yaml` ou `llm_dtype: "int8"` |
| `No audio device` | Verifique `--input-device` / `--output-device` em `talk` |
| `Connection refused` | Inicie `serve` antes do `talk` |
| Latência alta | Reduza `playback_buffer_ms`, use `faster-whisper` tiny |

## Integração com 9Router

O speech-to-speech expõe endpoint **OpenAI Realtime API compatível**:
- URL: `ws://localhost:8765/v1/realtime`
- Use qualquer cliente OpenAI Realtime (web, Python, JS)
- Funciona com `voice-chat-realtime.py` que já criamos

## Referências
- GitHub: https://github.com/keenableai/keenable-s2s
- PyPI: `speech-to-speech`
- Modelos: Hugging Face (NVIDIA, Qwen, Microsoft, hexgrad)