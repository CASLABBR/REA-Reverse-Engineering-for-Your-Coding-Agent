#!/usr/bin/env python3
"""
9Router Realtime Voice Chat - Full-duplex streaming como Gemini Live
Usa WebSocket para streaming contínuo: VAD -> STT -> LLM -> TTS em tempo real
"""

import asyncio
import json
import base64
import wave
import tempfile
import os
import sys
from dataclasses import dataclass
from typing import Optional, Callable
from pathlib import Path

try:
    import pyaudio
    import webrtcvad
    import websockets
    import numpy as np
except ImportError:
    print("Instalando dependências...")
    import subprocess
    subprocess.run([sys.executable, "-m", "pip", "install", "pyaudio", "webrtcvad", "websockets", "numpy", "-q"], capture_output=True, creationflags=subprocess.CREATE_NO_WINDOW)
    import pyaudio
    import webrtcvad
    import websockets
    import numpy as np

# ===== Config =====
SAMPLE_RATE = 24000  # Realtime API usa 24kHz
CHANNELS = 1
CHUNK_MS = 20
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_MS / 1000)
FORMAT = pyaudio.paInt16
VAD_AGGRESSIVENESS = 3

# 9Router base (ajuste se necessário)
NINEROUTER_URL = os.getenv("NINEROUTER_URL", "http://localhost:20128")
WS_URL = NINEROUTER_URL.replace("http", "ws") + "/v1/realtime"


@dataclass
class AudioConfig:
    sample_rate: int = SAMPLE_RATE
    channels: int = CHANNELS
    chunk_size: int = CHUNK_SIZE


class RealtimeVoiceChat:
    """
    Voice Chat full-duplex estilo Gemini Live:
    - Streaming contínuo de áudio
    - Interrupção natural (barge-in)
    - VAD no cliente + servidor
    - Transcrição ao vivo
    """

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("NINEROUTER_KEY")
        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.running = False

        # Áudio
        self.pa = pyaudio.PyAudio()
        self.input_stream = None
        self.output_stream = None
        self.vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)

        # Filas
        self.mic_queue: asyncio.Queue = asyncio.Queue()
        self.playback_queue: asyncio.Queue = asyncio.Queue()

        # Estado
        self.session_id = None
        self.is_speaking = False
        self.is_listening = False

        # Callbacks
        self.on_transcript_delta: Optional[Callable[[str], None]] = None
        self.on_transcript_done: Optional[Callable[[str], None]] = None
        self.on_response_text_delta: Optional[Callable[[str], None]] = None
        self.on_response_text_done: Optional[Callable[[str], None]] = None
        self.on_response_audio_delta: Optional[Callable[[bytes], None]] = None
        self.on_speech_started: Optional[Callable[[], None]] = None
        self.on_speech_stopped: Optional[Callable[[], None]] = None
        self.on_error: Optional[Callable[[str], None]] = None

    async def connect(self):
        """Conecta ao WebSocket Realtime"""
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        print(f"🔌 Conectando em {WS_URL}...")
        try:
            self.ws = await websockets.connect(WS_URL, extra_headers=headers)
            print("✅ Conectado!")

            # Configura sessão
            await self._send({
                "type": "session.update",
                "session": {
                    "type": "realtime",
                    "instructions": "Você é um assistente de voz útil e natural. Responda em português do Brasil.",
                    "voice": "alloy",
                    "turn_detection": {
                        "type": "server_vad",
                        "threshold": 0.5,
                        "prefix_padding_ms": 300,
                        "silence_duration_ms": 500,
                        "interrupt_response": True
                    },
                    "input_audio_format": "pcm16",
                    "output_audio_format": "pcm16",
                    "input_audio_transcription": {
                        "model": "whisper-1",
                        "language": "pt"
                    }
                }
            })

            # Inicia loops
            self.running = True
            asyncio.create_task(self._receive_loop())
            asyncio.create_task(self._mic_loop())
            asyncio.create_task(self._playback_loop())

        except Exception as e:
            print(f"❌ Erro conectando: {e}")
            if self.on_error:
                self.on_error(str(e))
            raise

    async def _send(self, msg: dict):
        """Envia mensagem JSON"""
        if self.ws:
            await self.ws.send(json.dumps(msg))

    async def _receive_loop(self):
        """Loop de recebimento de eventos do servidor"""
        try:
            async for message in self.ws:
                event = json.loads(message)
                await self._handle_event(event)
        except websockets.exceptions.ConnectionClosed:
            print("🔌 Conexão fechada")
        except Exception as e:
            print(f"[Erro receive] {e}")

    async def _handle_event(self, event: dict):
        """Processa eventos do servidor"""
        etype = event.get("type", "")

        if etype == "session.created":
            self.session_id = event.get("session", {}).get("id")
            print(f"📋 Sessão: {self.session_id}")

        elif etype == "session.updated":
            print("⚙️ Sessão configurada")

        elif etype == "input_audio_buffer.speech_started":
            self.is_listening = True
            if self.on_speech_started:
                self.on_speech_started()
            print("🎙️  Você começou a falar...")

        elif etype == "input_audio_buffer.speech_stopped":
            self.is_listening = False
            if self.on_speech_stopped:
                self.on_speech_stopped()
            print("🤔 Processando...")

        elif etype == "conversation.item.input_audio_transcription.delta":
            delta = event.get("delta", "")
            if self.on_transcript_delta:
                self.on_transcript_delta(delta)

        elif etype == "conversation.item.input_audio_transcription.completed":
            transcript = event.get("transcript", "")
            if self.on_transcript_done:
                self.on_transcript_done(transcript)
            print(f"👤 Você: {transcript}")

        elif etype == "response.created":
            print("🤖 Gerando resposta...")

        elif etype == "response.output_audio.delta":
            # Áudio base64 do TTS
            audio_b64 = event.get("delta", "")
            if audio_b64:
                audio_bytes = base64.b64decode(audio_b64)
                await self.playback_queue.put(audio_bytes)
                if self.on_response_audio_delta:
                    self.on_response_audio_delta(audio_bytes)

        elif etype == "response.output_audio_transcript.delta":
            delta = event.get("delta", "")
            if self.on_response_text_delta:
                self.on_response_text_delta(delta)

        elif etype == "response.output_audio_transcript.done":
            text = event.get("transcript", "")
            if self.on_response_text_done:
                self.on_response_text_done(text)
            print(f"🤖 Assistant: {text}")

        elif etype == "response.done":
            status = event.get("response", {}).get("status", "")
            print(f"✅ Resposta: {status}")

        elif etype == "error":
            err = event.get("error", {})
            msg = f"{err.get('code', '')}: {err.get('message', '')}"
            print(f"❌ Erro: {msg}")
            if self.on_error:
                self.on_error(msg)

    async def _mic_loop(self):
        """Loop de captura do microfone"""
        self.input_stream = self.pa.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE
        )

        print("🎤 Microfone ativo - fale naturalmente")
        print("   (VAD automático detecta sua voz)")

        while self.running:
            try:
                data = self.input_stream.read(CHUNK_SIZE, exception_on_overflow=False)

                # VAD local opcional (para economia de banda)
                is_speech = self.vad.is_speech(data, SAMPLE_RATE)

                # Envia tudo (servidor também faz VAD)
                audio_b64 = base64.b64encode(data).decode()
                await self._send({
                    "type": "input_audio_buffer.append",
                    "audio": audio_b64
                })

                # Pequeno delay para não saturar
                await asyncio.sleep(0.01)

            except Exception as e:
                if self.running:
                    print(f"[Erro mic] {e}")
                break

    async def _playback_loop(self):
        """Loop de reprodução de áudio"""
        self.output_stream = self.pa.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=SAMPLE_RATE,
            output=True,
            frames_per_buffer=CHUNK_SIZE
        )

        while self.running:
            try:
                audio_data = await asyncio.wait_for(self.playback_queue.get(), timeout=0.1)

                self.is_speaking = True
                # Reproduz em chunks menores
                for i in range(0, len(audio_data), 1024):
                    if not self.running:
                        break
                    chunk = audio_data[i:i+1024]
                    self.output_stream.write(chunk)

                self.is_speaking = False

            except asyncio.TimeoutError:
                continue
            except Exception as e:
                if self.running:
                    print(f"[Erro playback] {e}")

    def interrupt(self):
        """Interrompe resposta atual (barge-in)"""
        if self.ws and self.is_speaking:
            asyncio.create_task(self._send({
                "type": "response.cancel"
            }))
            print("⏹️ Interrompido!")

    async def send_text(self, text: str):
        """Envia mensagem de texto (injeta na conversa)"""
        await self._send({
            "type": "conversation.item.create",
            "item": {
                "type": "message",
                "role": "user",
                "content": [{"type": "input_text", "text": text}]
            }
        })
        await self._send({"type": "response.create"})

    async def close(self):
        """Encerra conexão"""
        self.running = False
        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()
        if self.output_stream:
            self.output_stream.stop_stream()
            self.output_stream.close()
        if self.ws:
            await self.ws.close()
        self.pa.terminate()
        print("👋 Desconectado")


async def main():
    import argparse

    parser = argparse.ArgumentParser(description="9Router Realtime Voice Chat - Estilo Gemini Live")
    parser.add_argument("--key", help="API Key (ou use NINEROUTER_KEY env)")
    args = parser.parse_args()

    # Verifica se 9Router suporta Realtime
    print("🔍 Verificando suporte Realtime...")
    import requests
    try:
        # Tenta endpoint realtime
        r = requests.get(f"{NINEROUTER_URL}/v1/models", timeout=5)
        models = r.json().get("data", [])
        realtime_models = [m for m in models if m.get("kind") == "realtime" or "realtime" in m.get("id", "")]
        if realtime_models:
            print(f"✅ Modelos Realtime: {[m['id'] for m in realtime_models]}")
        else:
            print("⚠️  9Router pode não ter endpoint /v1/realtime")
            print("   Este script precisa de servidor compatível OpenAI Realtime API")
            print("   Alternativas: speech-to-speech (keenableai), OpenGPT Live, vowel engine")
    except:
        print("⚠️  Não foi possível verificar")

    chat = RealtimeVoiceChat(api_key=args.key)

    # Callbacks visuais
    chat.on_transcript_delta = lambda d: print(f"   📝 {d}", end="\r")
    chat.on_transcript_done = lambda t: print(f"   📝 {t}")
    chat.on_response_text_delta = lambda d: print(f"   💬 {d}", end="\r")
    chat.on_response_text_done = lambda t: print(f"   💬 {t}")
    chat.on_speech_started = lambda: print("   🎙️  [ouvindo...]")
    chat.on_speech_stopped = lambda: print("   🤔 [pensando...]")
    chat.on_error = lambda e: print(f"   ❌ {e}")

    try:
        await chat.connect()

        print("""
╔══════════════════════════════════════════╗
║  🎙️  VOICE CHAT ATIVO - GEMINI LIVE      ║
║                                         ║
║  • Fale naturalmente                    ║
║  • VAD detecta sua voz automaticamente  ║
║  • Interrompa falando a qualquer hora   ║
║  • Ctrl+C para sair                     ║
╚══════════════════════════════════════════╝
        """)

        # Loop principal
        while chat.running:
            await asyncio.sleep(1)

    except KeyboardInterrupt:
        print("\n👋 Saindo...")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
    finally:
        await chat.close()


if __name__ == "__main__":
    asyncio.run(main())