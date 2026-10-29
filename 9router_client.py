"""
9Router Python Client - Auto-integration for chat, images, embeddings, web search, TTS/STT
Usage:
    from 9router_client import NineRouterClient
    client = NineRouterClient()
    response = client.chat("Hello, world!")
"""

import os
import requests
import json
from typing import Optional, List, Dict, Any, Generator
from dataclasses import dataclass

@dataclass
class Model:
    id: str
    owned_by: str
    kind: Optional[str] = None

class NineRouterClient:
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

    # ===== Health =====
    def health(self) -> bool:
        try:
            r = self.session.get(f"{self.base_url}/api/health", timeout=5)
            return r.json().get("ok", False)
        except:
            return False

    # ===== Models =====
    def list_models(self, kind: str = "") -> List[Model]:
        endpoint = f"/models/{kind}" if kind else "/models"
        data = self._request("GET", endpoint)
        return [Model(**m) for m in data.get("data", [])]

    # ===== Chat =====
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
        """Simple one-shot chat returning just the text."""
        resp = self.chat([{"role": "user", "content": prompt}], model=model, **kwargs)
        return resp["choices"][0]["message"]["content"]

    # ===== Embeddings =====
    def embed(self, texts: List[str], model: str = "auto") -> List[List[float]]:
        data = self._request("POST", "/embeddings", json={"model": model, "input": texts})
        return [d["embedding"] for d in data["data"]]

    # ===== Image Generation =====
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

    # ===== Text-to-Speech =====
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

    # ===== Speech-to-Text =====
    def stt(self, audio_file: str, model: str = "auto", language: str = "pt") -> str:
        with open(audio_file, "rb") as f:
            files = {"file": (audio_file, f, "audio/mpeg")}
            data = {"model": model, "language": language}
            r = self.session.post(f"{self.base_url}/v1/audio/transcriptions", files=files, data=data, timeout=self.timeout)
            r.raise_for_status()
            return r.json()["text"]

    # ===== Web Search =====
    def web_search(self, query: str, model: str = "auto", max_results: int = 10) -> List[Dict]:
        data = self._request("POST", "/web/search", json={
            "model": model, "query": query, "max_results": max_results
        })
        return data.get("results", [])

    # ===== Web Fetch =====
    def web_fetch(self, urls: List[str], model: str = "auto", max_chars: int = 3000) -> List[Dict]:
        data = self._request("POST", "/web/fetch", json={
            "model": model, "urls": urls, "max_characters": max_chars
        })
        return data.get("results", [])

    # ===== Auto-Routing (Combo Models) =====
    def auto_chat(self, prompt: str, **kwargs) -> str:
        """Uses combo model for auto-provider fallback."""
        return self.chat_simple(prompt, model="combo/general", **kwargs)

    def auto_search(self, query: str, **kwargs) -> List[Dict]:
        """Uses combo model for web search with fallback."""
        return self.web_search(query, model="combo/search", **kwargs)


# ===== Convenience Functions =====
_client: Optional[NineRouterClient] = None

def get_client() -> NineRouterClient:
    global _client
    if _client is None:
        _client = NineRouterClient()
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


# ===== Demo / Test =====
if __name__ == "__main__":
    client = NineRouterClient()

    print("=== 9Router Client Demo ===\n")

    # Health check
    print(f"Health: {'OK' if client.health() else 'FAIL'}")

    # List models
    models = client.list_models()
    print(f"\nAvailable models ({len(models)}):")
    for m in models[:5]:
        print(f"  - {m.id} ({m.owned_by})")

    # Test chat (only if running)
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