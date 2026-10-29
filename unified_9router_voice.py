#!/usr/bin/env python3
"""
Unified 9Router + Voice Chat Client
Combines REST API (9Router) + WebSocket Realtime (Voice Chat) in one wrapper.
Usage:
    from unified_9router_voice import UnifiedClient
    client = UnifiedClient()

    # REST chat
    response = client.chat("Olá!")

    # Voice chat (full-duplex)
    await client.voice.connect()
    await client.voice.send_text("Oi por texto")
"""

import os
import json
import base64
import asyncio
import requests
import websockets
import pyaudio
import webrtcvad
import numpy as np
from dataclasses import dataclass
from typing import Optional, List, Dict, Any, Generator, Callable
from pathlib import Path


# ========== 9Router REST Client ==========

@dataclass
class Model:
    id: str
    owned_by: str
    kind: Optional[str] = None


class NineRouterREST:
    """9Router REST API client (chat, embeddings, images, web search, TTS/STT)"""

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        timeout: int = 30
    ):
        self.base_url = base_url or os.getenv("NINEROUTER_URL", "http://localhost:20128")
        self.api_key = api_key or os.getenv("NINEROUTER_KEY")
        self.timeout = timeout
        self.session = requests.Session()
        if self.api_key:
            self.session.headers.update({"Authorization": f"Bearer {self.api_key}"})
        self.session.headers.update({"Content-Type": "application/json"})

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}/v1{endpoint}"
        response = self.session.request(method, url, timeout=self.timeout, **kwargs)
        response.raise_for_status()
        return response.json()

    # Health
    def health(self) -> bool:
        try:
            r = self.session.get(f"{self.base_url}/api/health", timeout=5)
            return r.json().get("ok", False)
        except:
            return False

    # Models
    def list_models(self, kind: str = "") -> List[Model]:
        endpoint = f"/models/{kind}" if kind else "/models"
        data = self._request("GET", endpoint)
        return [Model(**m) for m in data.get("data", [])]

    # Chat
    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "auto",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any] | Generator[str, None, None]:
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream
        }
        if max_tokens:
            payload["max_tokens"] = max_tokens

        if stream:
            return self._stream_chat(payload)
        return self._request("POST", "/chat/completions", json=payload)

    def _stream_chat(self, payload: Dict) -> Generator[str, None, None]:
        url = f"{self.base_url}/v1/chat/completions"
        with self.session.post(url, json=payload, stream=True, timeout=self.timeout) as r:
            r.raise_for_status()
            for line in r.iter_lines():
                if line:
                    line = line.decode("utf-8")
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            delta = chunk.get("choices", [{}])[0].get("delta", {})
                            if "content" in delta:
                                yield delta["content"]
                        except json.JSONDecodeError:
                            pass

    def chat_simple(self, prompt: str, model: str = "auto", **kwargs) -> str:
        resp = self.chat([{"role": "user", "content": prompt}], model=model, **kwargs)
        return resp["choices"][0]["message"]["content"]

    # Embeddings
    def embed(self, texts: List[str], model: str = "auto") -> List[List[float]]:
        data = self._request("POST", "/embeddings", json={"model": model, "input": texts})
        return [d["embedding"] for d in data["data"]]

    # Images
    def generate_image(
        self,
        prompt: str,
        model: str = "auto",
        n: int = 1,
        size: str = "1024x1024"
    ) -> List[str]:
        data = self._request("POST", "/images/generations", json={
            "model": model, "prompt": prompt, "n": n, "size": size
        })
        return [d["url"] for d in data["data"]]

    # TTS
    def tts(
        self,
        text: str,
        model: str = "auto",
        voice: str = "alloy",
        format: str = "mp3"
    ) -> bytes:
        url = f"{self.base_url}/v1/audio/speech"
        r = self.session.post(url, json={
            "model": model, "input": text, "voice": voice, "format": format
        }, timeout=self.timeout)
        r.raise_for_status()
        return r.content

    # STT
    def stt(self, audio_file: str, model: str = "auto", language: str = "pt") -> str:
        with open(audio_file, "rb") as f:
            files = {"file": (audio_file, f, "audio/mpeg")}
            data = {"model": model, "language": language}
            r = self.session.post(
                f"{self.base_url}/v1/audio/transcriptions",
                files=files, data=data, timeout=self.timeout
            )
            r.raise_for_status()
            return r.json()["text"]

    # Web Search
    def web_search(self, query: str, model: str = "auto", max_results: int = 10) -> List[Dict]:
        data = self._request("POST", "/web/search", json={
            "model": model, "query": query, "max_results": max_results
        })
        return data.get("results", [])

    # Web Fetch
    def web_fetch(self, urls: List[str], model: str = "auto", max_chars: int = 3000) -> List[Dict]:
        data = self._request("POST", "/web/fetch", json={
            "model": model, "urls": urls, "max_characters": max_chars
        })
        return data.get("results", [])

    # Auto-routing (combo models)
    def auto_chat(self, prompt: str, **kwargs) -> str:
        return self.chat_simple(prompt, model="combo/general", **kwargs)

    def auto_search(self, query: str, **kwargs) -> List[Dict]:
        return self.web_search(query, model="combo/search", **kwargs)


# ========== Voice Chat WebSocket Client ==========

SAMPLE_RATE = 24000
CHANNELS = 1
CHUNK_MS = 20
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_MS / 1000)
FORMAT = pyaudio.paInt16
VAD_AGGRESSIVENESS = 3


@dataclass
class AudioConfig:
    sample_rate: int = SAMPLE_RATE
    channels: int = CHANNELS
    chunk_size: int = CHUNK_SIZE


class VoiceChat:
    """Full-duplex WebSocket voice chat (Gemini Live style)"""

    def __init__(
        self,
        ws_url: Optional[str] = None,
        api_key: Optional[str] = None,
        voice: str = "alloy",
        instructions: str = "Você é um assistente de voz útil e natural. Responda em português do Brasil."
    ):
        self.ws_url = ws_url or os.getenv("NINEROUTER_URL", "http://localhost:20128").replace("http", "ws") + "/v1/realtime"
        self.api_key = api_key or os.getenv("NINEROUTER_KEY")
        self.voice = voice
        self.instructions = instructions

        self.ws: Optional[websockets.WebSocketClientProtocol] = None
        self.running = False

        self.pa = pyaudio.PyAudio()
        self.input_stream = None
        self.output_stream = None
        self.vad = webrtcvad.Vad(VAD_AGGRESSIVENESS)

        self.mic_queue: asyncio.Queue = asyncio.Queue()
        self.playback_queue: asyncio.Queue = asyncio.Queue()

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
        self.on_connected: Optional[Callable[[], None]] = None

    async def connect(self):
        headers = {}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        print(f"🔌 Conectando Voice Chat em {self.ws_url}...")
        try:
            self.ws = await websockets.connect(self.ws_url, extra_headers=headers)
            print("✅ Voice Chat conectado!")

            await self._send({
                "type": "session.update",
                "session": {
                    "type": "realtime",
                    "instructions": self.instructions,
                    "voice": self.voice,
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

            self.running = True
            asyncio.create_task(self._receive_loop())
            asyncio.create_task(self._mic_loop())
            asyncio.create_task(self._playback_loop())

            if self.on_connected:
                self.on_connected()

        except Exception as e:
            print(f"❌ Erro conectando Voice Chat: {e}")
            if self.on_error:
                self.on_error(str(e))
            raise

    async def _send(self, msg: dict):
        if self.ws:
            await self.ws.send(json.dumps(msg))

    async def _receive_loop(self):
        try:
            async for message in self.ws:
                event = json.loads(message)
                await self._handle_event(event)
        except websockets.exceptions.ConnectionClosed:
            print("🔌 Conexão Voice Chat fechada")
        except Exception as e:
            print(f"[Erro receive] {e}")

    async def _handle_event(self, event: dict):
        etype = event.get("type", "")

        if etype == "session.created":
            self.session_id = event.get("session", {}).get("id")
            print(f"📋 Sessão Voice: {self.session_id}")

        elif etype == "session.updated":
            print("⚙️ Sessão Voice configurada")

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
            print(f"❌ Erro Voice: {msg}")
            if self.on_error:
                self.on_error(msg)

    async def _mic_loop(self):
        self.input_stream = self.pa.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE
        )

        print("🎤 Microfone ativo - fale naturalmente (VAD automático)")

        while self.running:
            try:
                data = self.input_stream.read(CHUNK_SIZE, exception_on_overflow=False)
                audio_b64 = base64.b64encode(data).decode()
                await self._send({
                    "type": "input_audio_buffer.append",
                    "audio": audio_b64
                })
                await asyncio.sleep(0.01)
            except Exception as e:
                if self.running:
                    print(f"[Erro mic] {e}")
                break

    async def _playback_loop(self):
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
        """Barge-in: interrompe resposta atual"""
        if self.ws and self.is_speaking:
            asyncio.create_task(self._send({"type": "response.cancel"}))
            print("⏹️ Interrompido!")

    async def send_text(self, text: str):
        """Injeta mensagem de texto na conversa"""
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
        print("👋 Voice Chat desconectado")


# ========== Unified Client ==========

class UnifiedClient:
    """
    Unified 9Router + Voice Chat client.
    Provides both REST (sync) and WebSocket (async) interfaces.
    """

    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        voice: str = "alloy",
        voice_instructions: str = "Você é um assistente de voz útil e natural. Responda em português do Brasil."
    ):
        self.rest = NineRouterREST(base_url, api_key)
        self.voice = VoiceChat(
            ws_url=base_url.replace("http", "ws") + "/v1/realtime" if base_url else None,
            api_key=api_key,
            voice=voice,
            instructions=voice_instructions
        )

    # Delegate REST methods
    def health(self) -> bool:
        return self.rest.health()

    def list_models(self, kind: str = "") -> List[Model]:
        return self.rest.list_models(kind)

    def chat(
        self,
        messages: List[Dict[str, str]],
        model: str = "auto",
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
        stream: bool = False
    ) -> Dict[str, Any] | Generator[str, None, None]:
        return self.rest.chat(messages, model, temperature, max_tokens, stream)

    def chat_simple(self, prompt: str, model: str = "auto", **kwargs) -> str:
        return self.rest.chat_simple(prompt, model, **kwargs)

    def embed(self, texts: List[str], model: str = "auto") -> List[List[float]]:
        return self.rest.embed(texts, model)

    def generate_image(self, prompt: str, model: str = "auto", n: int = 1, size: str = "1024x1024") -> List[str]:
        return self.rest.generate_image(prompt, model, n, size)

    def tts(self, text: str, model: str = "auto", voice: str = "alloy", format: str = "mp3") -> bytes:
        return self.rest.tts(text, model, voice, format)

    def stt(self, audio_file: str, model: str = "auto", language: str = "pt") -> str:
        return self.rest.stt(audio_file, model, language)

    def web_search(self, query: str, model: str = "auto", max_results: int = 10) -> List[Dict]:
        return self.rest.web_search(query, model, max_results)

    def web_fetch(self, urls: List[str], model: str = "auto", max_chars: int = 3000) -> List[Dict]:
        return self.rest.web_fetch(urls, model, max_chars)

    def auto_chat(self, prompt: str, **kwargs) -> str:
        return self.rest.auto_chat(prompt, **kwargs)

    def auto_search(self, query: str, **kwargs) -> List[Dict]:
        return self.rest.auto_search(query, **kwargs)

    # Voice methods (async)
    async def voice_connect(self):
        await self.voice.connect()

    async def voice_send_text(self, text: str):
        await self.voice.send_text(text)

    async def voice_interrupt(self):
        self.voice.interrupt()

    async def voice_close(self):
        await self.voice.close()

    # Convenience: run voice chat with default callbacks
    async def run_voice_chat(self):
        """Run interactive voice chat loop (like voice-chat-realtime.py)"""
        self.voice.on_transcript_delta = lambda d: print(f"   📝 {d}", end="\r")
        self.voice.on_transcript_done = lambda t: print(f"   📝 {t}")
        self.voice.on_response_text_delta = lambda d: print(f"   💬 {d}", end="\r")
        self.voice.on_response_text_done = lambda t: print(f"   💬 {t}")
        self.voice.on_speech_started = lambda: print("   🎙️  [ouvindo...]")
        self.voice.on_speech_stopped = lambda: print("   🤔 [pensando...]")
        self.voice.on_error = lambda e: print(f"   ❌ {e}")

        await self.voice.connect()

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

        try:
            while self.voice.running:
                await asyncio.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Saindo...")
        finally:
            await self.voice.close()


# ========== Convenience Functions ==========

_client: Optional[UnifiedClient] = None


def get_client() -> UnifiedClient:
    global _client
    if _client is None:
        _client = UnifiedClient()
    return _client


def chat(prompt: str, **kwargs) -> str:
    return get_client().auto_chat(prompt, **kwargs)


def search(query: str, **kwargs) -> List[Dict]:
    return get_client().auto_search(query, **kwargs)


def embed(texts: List[str], **kwargs) -> List[List[float]]:
    return get_client().embed(texts, **kwargs)


def generate_image(prompt: str, **kwargs) -> List[str]:
    return get_client().generate_image(prompt, **kwargs)


def tts(text: str, **kwargs) -> bytes:
    return get_client().tts(text, **kwargs)


# ========== Demo / Test ==========

async def demo_voice():
    """Demo voice chat"""
    client = UnifiedClient()
    await client.run_voice_chat()


def demo_rest():
    """Demo REST API"""
    client = UnifiedClient()

    print("=== Unified 9Router + Voice Demo ===\n")
    print(f"Health: {'OK' if client.health() else 'FAIL'}")

    models = client.list_models()
    print(f"\nAvailable models ({len(models)}):")
    for m in models[:5]:
        print(f"  - {m.id} ({m.owned_by})")

    if client.health():
        print("\n--- Chat Test ---")
        try:
            response = client.auto_chat("Olá! Responda em português: qual a capital do Brasil?")
            print(f"Response: {response}")
        except Exception as e:
            print(f"Chat error: {e}")

        print("\n--- Web Search Test ---")
        try:
            results = client.auto_search("GitHub Copilot app download Windows")
            for r in results[:3]:
                print(f"  - {r.get('title', 'N/A')}: {r.get('url', 'N/A')}")
        except Exception as e:
            print(f"Search error: {e}")
    else:
        print("\n9Router not running. Start with: npx @decolua/9router")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1 and sys.argv[1] == "voice":
        asyncio.run(demo_voice())
    else:
        demo_rest()