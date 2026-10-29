#!/usr/bin/env python3
"""
9Router Real-Time Voice Chat - Push-to-talk + VAD modes
Como Gemini Live: fala, ouve, interrompe, conversa natural.
"""

import os
import sys
import time
import threading
import queue
import wave
import tempfile
import numpy as np
from pathlib import Path

try:
    import pyaudio
    import webrtcvad
    import requests
except ImportError:
    print("Instalando dependências...")
    os.system(f"{sys.executable} -m pip install pyaudio webrtcvad requests numpy -q")
    import pyaudio
    import webrtcvad
    import requests

from 9router_client import NineRouterClient

# ===== Configuração de Áudio =====
SAMPLE_RATE = 16000
CHANNELS = 1
CHUNK_MS = 30  # 30ms frames para VAD
CHUNK_SIZE = int(SAMPLE_RATE * CHUNK_MS / 1000)
FORMAT = pyaudio.paInt16

# ===== Cliente 9Router =====
client = NineRouterClient()


class VoiceChat:
    def __init__(self, mode="push-to-talk", language="pt"):
        self.mode = mode  # "push-to-talk" ou "vad"
        self.language = language
        self.running = False
        self.audio_queue = queue.Queue()
        self.playback_queue = queue.Queue()

        # VAD (Voice Activity Detection)
        self.vad = webrtcvad.Vad(3)  # Aggressividade 0-3

        # PyAudio
        self.pa = pyaudio.PyAudio()
        self.input_stream = None
        self.output_stream = None

        # Estado
        self.is_speaking = False
        self.is_listening = False
        self.current_audio = []
        self.silence_frames = 0
        self.speech_frames = 0

        # Callbacks
        self.on_transcript = None
        self.on_response = None
        self.on_audio_playing = None

    def start(self):
        """Inicia streams de áudio"""
        self.running = True

        # Input stream (microfone)
        self.input_stream = self.pa.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=SAMPLE_RATE,
            input=True,
            frames_per_buffer=CHUNK_SIZE,
            stream_callback=self._audio_callback
        )

        # Output stream (alto-falante)
        self.output_stream = self.pa.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=SAMPLE_RATE,
            output=True,
            frames_per_buffer=CHUNK_SIZE
        )

        # Thread de processamento
        self.process_thread = threading.Thread(target=self._process_loop, daemon=True)
        self.process_thread.start()

        # Thread de playback
        self.playback_thread = threading.Thread(target=self._playback_loop, daemon=True)
        self.playback_thread.start()

        print(f"🎤 Voice Chat iniciado - Modo: {self.mode}")
        print("   Pressione Ctrl+C para sair")
        print()

    def stop(self):
        """Para tudo"""
        self.running = False
        if self.input_stream:
            self.input_stream.stop_stream()
            self.input_stream.close()
        if self.output_stream:
            self.output_stream.stop_stream()
            self.output_stream.close()
        self.pa.terminate()

    def _audio_callback(self, in_data, frame_count, time_info, status):
        """Callback do PyAudio - recebe áudio do microfone"""
        if self.running:
            self.audio_queue.put(in_data)
        return (None, pyaudio.paContinue)

    def _process_loop(self):
        """Loop principal de processamento"""
        while self.running:
            try:
                if self.mode == "push-to-talk":
                    self._process_push_to_talk()
                else:
                    self._process_vad()
            except Exception as e:
                print(f"[Erro processamento] {e}")
            time.sleep(0.01)

    def _process_push_to_talk(self):
        """Modo push-to-talk: grava enquanto segura tecla"""
        # Neste modo simples, usamos Enter para iniciar/parar
        pass  # Controlado externamente

    def _process_vad(self):
        """Modo VAD: detecta voz automaticamente"""
        try:
            data = self.audio_queue.get(timeout=0.1)
        except queue.Empty:
            return

        is_speech = self.vad.is_speech(data, SAMPLE_RATE)

        if is_speech:
            self.silence_frames = 0
            self.speech_frames += 1
            self.current_audio.append(data)

            if not self.is_listening and self.speech_frames > 3:
                self.is_listening = True
                print("🎙️  Ouvindo...", end="\r")

        else:
            self.silence_frames += 1

            if self.is_listening:
                self.current_audio.append(data)

            # Fim da fala: 1 segundo de silêncio
            if self.is_listening and self.silence_frames > (1000 / CHUNK_MS):
                self._process_speech()

    def _process_speech(self):
        """Processa fala completa: STT -> Chat -> TTS -> Play"""
        if not self.current_audio:
            return

        self.is_listening = False
        self.speech_frames = 0
        print("🤔 Processando...          ")

        # Salva áudio temporário
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_path = f.name
            self._save_wav(f, b"".join(self.current_audio))

        self.current_audio = []

        try:
            # 1. STT (Speech to Text)
            print("📝 Transcrevendo...")
            transcript = client.stt(temp_path, language=self.language)
            print(f"👤 Você: {transcript}")

            if self.on_transcript:
                self.on_transcript(transcript)

            # 2. Chat (LLM)
            print("💭 Pensando...")
            response = client.auto_chat(transcript)
            print(f"🤖 Assistant: {response}")

            if self.on_response:
                self.on_response(response)

            # 3. TTS (Text to Speech)
            print("🔊 Gerando áudio...")
            audio_data = client.tts(response, voice="alloy")

            # 4. Cola na fila de playback
            self.playback_queue.put(audio_data)

        except Exception as e:
            print(f"[Erro] {e}")
        finally:
            # Limpa temp
            try:
                os.unlink(temp_path)
            except:
                pass

    def _save_wav(self, file_obj, audio_data):
        """Salva áudio como WAV"""
        wf = wave.open(file_obj, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(SAMPLE_RATE)
        wf.writeframes(audio_data)
        wf.close()

    def _playback_loop(self):
        """Loop de reprodução de áudio"""
        while self.running:
            try:
                audio_data = self.playback_queue.get(timeout=0.1)
            except queue.Empty:
                continue

            self.is_speaking = True
            if self.on_audio_playing:
                self.on_audio_playing(True)

            print("🔊 Reproduzindo...", end="\r")

            # Reproduz em chunks
            chunk_size = 4096
            for i in range(0, len(audio_data), chunk_size):
                if not self.running:
                    break
                chunk = audio_data[i:i+chunk_size]
                try:
                    self.output_stream.write(chunk)
                except:
                    break

            self.is_speaking = False
            if self.on_audio_playing:
                self.on_audio_playing(False)
            print("✅ Pronto. Fale...        ")

    # ===== Métodos públicos para push-to-talk =====
    def start_recording(self):
        """Inicia gravação (push-to-talk)"""
        self.current_audio = []
        self.is_listening = True
        print("🎙️  Gravando... (solte para enviar)")

    def stop_recording(self):
        """Para gravação e processa"""
        if self.is_listening and self.current_audio:
            self.is_listening = False
            print("🤔 Processando...")
            threading.Thread(target=self._process_push_to_talk_audio, daemon=True).start()

    def _process_push_to_talk_audio(self):
        """Processa áudio gravado no push-to-talk"""
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
            temp_path = f.name
            self._save_wav(f, b"".join(self.current_audio))

        try:
            transcript = client.stt(temp_path, language=self.language)
            print(f"👤 Você: {transcript}")

            response = client.auto_chat(transcript)
            print(f"🤖 Assistant: {response}")

            audio_data = client.tts(response, voice="alloy")
            self.playback_queue.put(audio_data)

        except Exception as e:
            print(f"[Erro] {e}")
        finally:
            try:
                os.unlink(temp_path)
            except:
                pass
            print("✅ Pronto. Segure Enter para falar...")


def main():
    import argparse

    parser = argparse.ArgumentParser(description="9Router Voice Chat - Como Gemini Live")
    parser.add_argument("--mode", choices=["push-to-talk", "vad"], default="push-to-talk",
                        help="Modo: push-to-talk (Enter) ou vad (automático)")
    parser.add_argument("--language", default="pt", help="Idioma STT (pt, en, etc)")
    args = parser.parse_args()

    # Verifica 9Router
    if not client.health():
        print("❌ 9Router não está rodando!")
        print("   Inicie com: npx @decolua/9router")
        return

    print("✅ 9Router conectado")
    print()

    vc = VoiceChat(mode=args.mode, language=args.language)

    # Callbacks bonitos
    vc.on_transcript = lambda t: print(f"   📝 \"{t}\"")
    vc.on_response = lambda r: print(f"   💬 \"{r[:80]}{'...' if len(r)>80 else ''}\"")
    vc.on_audio_playing = lambda p: print(f"   {'🔊 Falando...' if p else '👂 Ouvindo...'}")

    vc.start()

    try:
        if args.mode == "push-to-talk":
            print("📌 MODO PUSH-TO-TALK")
            print("   Segure ENTER para falar, solte para enviar")
            print("   Digite 'sair' + Enter para encerrar")
            print()

            import sys
            import select

            recording = False
            while vc.running:
                # Verifica input sem bloquear
                if sys.stdin in select.select([sys.stdin], [], [], 0.1)[0]:
                    line = sys.stdin.readline().strip()
                    if line.lower() in ('sair', 'exit', 'quit', 'q'):
                        break

                # Simula push-to-talk com teclas (simplificado)
                # Em terminal real, precisaria de library como keyboard ou pynput
                time.sleep(0.1)

        else:
            print("📌 MODO VAD (Voice Activity Detection)")
            print("   Fale naturalmente - detecta voz automaticamente")
            print("   Silêncio de 1s = envia para processamento")
            print("   Ctrl+C para sair")
            print()

            while vc.running:
                time.sleep(1)

    except KeyboardInterrupt:
        print("\n\n👋 Encerrando...")
    finally:
        vc.stop()


if __name__ == "__main__":
    main()