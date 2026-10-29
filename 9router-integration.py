"""
9Router Full Integration - Auto messaging, data sync, real-time monitoring
Tudo em português, automático e integrado.
"""

import os
import json
import time
import asyncio
import threading
from datetime import datetime
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, asdict
from pathlib import Path

# Import our client
from 9router_client import NineRouterClient, get_client, chat, search, embed, generate_image, tts


@dataclass
class Message:
    """Estrutura de mensagem para comunicação automática"""
    id: str
    role: str  # user, assistant, system
    content: str
    timestamp: str
    metadata: Dict[str, Any]


@dataclass
class SyncStatus:
    """Status de sincronização de dados"""
    last_sync: str
    items_synced: int
    status: str  # ok, error, pending
    details: str


class NineRouterIntegration:
    """
    Integração completa com 9Router:
    - Chat automático com fallback
    - Busca web e fetch
    - Embeddings para RAG
    - Geração de imagens
    - TTS/STT
    - Monitoramento em tempo real
    - Sincronização de dados
    """

    def __init__(self, config_path: str = "9router-config.json"):
        self.config_path = Path(config_path)
        self.client = get_client()
        self.running = False
        self.monitor_thread: Optional[threading.Thread] = None
        self.message_queue: List[Message] = []
        self.sync_status = SyncStatus(
            last_sync="never",
            items_synced=0,
            status="pending",
            details="Not started"
        )
        self.callbacks: Dict[str, List[Callable]] = {
            "on_message": [],
            "on_sync": [],
            "on_error": [],
            "on_status_change": []
        }
        self._load_config()

    def _load_config(self):
        """Carrega configuração do arquivo"""
        default_config = {
            "router_url": "http://localhost:20128",
            "api_key": "",
            "auto_start": True,
            "monitor_interval": 30,
            "max_retries": 3,
            "default_model": "combo/general",
            "search_model": "combo/search",
            "sync_interval": 300,  # 5 min
            "message_history_limit": 100,
            "enable_tts": True,
            "enable_web_search": True,
            "language": "pt-BR"
        }

        if self.config_path.exists():
            with open(self.config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
                default_config.update(config)

        self.config = default_config
        self._save_config()

    def _save_config(self):
        """Salva configuração no arquivo"""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, indent=2, ensure_ascii=False)

    def on(self, event: str, callback: Callable):
        """Registra callback para eventos"""
        if event in self.callbacks:
            self.callbacks[event].append(callback)

    def _emit(self, event: str, data: Any):
        """Dispara callbacks registrados"""
        for cb in self.callbacks.get(event, []):
            try:
                cb(data)
            except Exception as e:
                print(f"[Callback Error] {event}: {e}")

    # ===== Chat Automático =====
    def send_message(self, content: str, role: str = "user", **kwargs) -> Message:
        """Envia mensagem e retorna resposta automática"""
        msg_id = f"msg_{int(time.time() * 1000)}"
        user_msg = Message(
            id=msg_id,
            role=role,
            content=content,
            timestamp=datetime.now().isoformat(),
            metadata=kwargs
        )
        self.message_queue.append(user_msg)
        self._trim_history()

        # Obter resposta do 9Router
        try:
            model = kwargs.get("model", self.config["default_model"])
            response_text = self.client.chat_simple(content, model=model)

            assistant_msg = Message(
                id=f"msg_{int(time.time() * 1000)}",
                role="assistant",
                content=response_text,
                timestamp=datetime.now().isoformat(),
                metadata={"model": model, "in_response_to": msg_id}
            )
            self.message_queue.append(assistant_msg)
            self._trim_history()

            self._emit("on_message", assistant_msg)
            return assistant_msg

        except Exception as e:
            error_msg = Message(
                id=f"err_{int(time.time() * 1000)}",
                role="system",
                content=f"Erro: {str(e)}",
                timestamp=datetime.now().isoformat(),
                metadata={"error": str(e), "original_id": msg_id}
            )
            self._emit("on_error", error_msg)
            return error_msg

    def send_auto(self, prompt: str, **kwargs) -> str:
        """Envio simples com modelo combo (auto-fallback)"""
        return self.client.auto_chat(prompt, **kwargs)

    # ===== Busca Web Automática =====
    def search_web(self, query: str, **kwargs) -> List[Dict]:
        """Busca web com fallback automático"""
        try:
            model = kwargs.get("model", self.config["search_model"])
            results = self.client.web_search(query, model=model, max_results=kwargs.get("max_results", 10))
            self._emit("on_message", {"type": "search", "query": query, "results": len(results)})
            return results
        except Exception as e:
            self._emit("on_error", {"type": "search", "query": query, "error": str(e)})
            return []

    def fetch_urls(self, urls: List[str], **kwargs) -> List[Dict]:
        """Busca conteúdo de URLs"""
        try:
            results = self.client.web_fetch(urls, model=kwargs.get("model", "auto"))
            return results
        except Exception as e:
            self._emit("on_error", {"type": "fetch", "urls": urls, "error": str(e)})
            return []

    # ===== Embeddings & RAG =====
    def create_embeddings(self, texts: List[str]) -> List[List[float]]:
        """Cria embeddings para RAG/busca semântica"""
        return self.client.embed(texts)

    def semantic_search(self, query: str, documents: List[str], top_k: int = 5) -> List[Dict]:
        """Busca semântica simples usando embeddings"""
        import numpy as np

        query_emb = self.create_embeddings([query])[0]
        doc_embs = self.create_embeddings(documents)

        # Similaridade cosseno
        similarities = []
        for i, doc_emb in enumerate(doc_embs):
            sim = np.dot(query_emb, doc_emb) / (np.linalg.norm(query_emb) * np.linalg.norm(doc_emb))
            similarities.append((i, sim))

        similarities.sort(key=lambda x: x[1], reverse=True)
        return [
            {"index": idx, "score": score, "content": documents[idx]}
            for idx, score in similarities[:top_k]
        ]

    # ===== Geração de Mídia =====
    def generate_image_auto(self, prompt: str, **kwargs) -> List[str]:
        """Gera imagem com modelo automático"""
        return self.client.generate_image(prompt, model=kwargs.get("model", "auto"))

    def text_to_speech(self, text: str, **kwargs) -> bytes:
        """Converte texto em áudio"""
        return self.client.tts(text, voice=kwargs.get("voice", "alloy"))

    # ===== Sincronização de Dados =====
    def sync_data(self, data: Dict[str, Any], target: str = "local") -> SyncStatus:
        """Sincroniza dados (local, remoto, cloud)"""
        self.sync_status = SyncStatus(
            last_sync=datetime.now().isoformat(),
            items_synced=len(data),
            status="pending",
            details=f"Syncing to {target}..."
        )
        self._emit("on_sync", self.sync_status)

        try:
            # Aqui você implementa a sincronização real
            # Ex: salvar em arquivo, enviar para API, database, etc.
            sync_file = Path("data/sync") / f"sync_{int(time.time())}.json"
            sync_file.parent.mkdir(parents=True, exist_ok=True)
            with open(sync_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)

            self.sync_status.status = "ok"
            self.sync_status.details = f"Synced {len(data)} items to {sync_file}"
        except Exception as e:
            self.sync_status.status = "error"
            self.sync_status.details = str(e)

        self._emit("on_sync", self.sync_status)
        return self.sync_status

    # ===== Monitoramento em Tempo Real =====
    def start_monitoring(self, interval: Optional[int] = None):
        """Inicia monitoramento em background"""
        if self.running:
            return

        self.running = True
        interval = interval or self.config["monitor_interval"]

        def monitor_loop():
            while self.running:
                try:
                    healthy = self.client.health()
                    status = "healthy" if healthy else "unhealthy"
                    self._emit("on_status_change", {
                        "status": status,
                        "timestamp": datetime.now().isoformat(),
                        "url": self.config["router_url"]
                    })

                    # Auto-sync periódico
                    if hasattr(self, '_last_sync'):
                        if time.time() - self._last_sync > self.config["sync_interval"]:
                            self.sync_data({"messages": [asdict(m) for m in self.message_queue]})
                            self._last_sync = time.time()
                    else:
                        self._last_sync = time.time()

                except Exception as e:
                    self._emit("on_error", {"type": "monitor", "error": str(e)})

                time.sleep(interval)

        self.monitor_thread = threading.Thread(target=monitor_loop, daemon=True)
        self.monitor_thread.start()
        self._emit("on_status_change", {"status": "monitoring_started"})

    def stop_monitoring(self):
        """Para monitoramento"""
        self.running = False
        if self.monitor_thread:
            self.monitor_thread.join(timeout=5)
        self._emit("on_status_change", {"status": "monitoring_stopped"})

    # ===== Utilitários =====
    def _trim_history(self):
        limit = self.config["message_history_limit"]
        if len(self.message_queue) > limit:
            self.message_queue = self.message_queue[-limit:]

    def get_history(self, limit: Optional[int] = None) -> List[Message]:
        """Retorna histórico de mensagens"""
        if limit:
            return self.message_queue[-limit:]
        return self.message_queue

    def get_status(self) -> Dict[str, Any]:
        """Retorna status completo do sistema"""
        return {
            "healthy": self.client.health(),
            "monitoring": self.running,
            "message_count": len(self.message_queue),
            "sync_status": asdict(self.sync_status),
            "config": self.config
        }

    def export_session(self, path: str):
        """Exporta sessão completa"""
        session = {
            "timestamp": datetime.now().isoformat(),
            "messages": [asdict(m) for m in self.message_queue],
            "sync_status": asdict(self.sync_status),
            "config": self.config
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(session, f, indent=2, ensure_ascii=False)


# ===== Instância Global (Singleton) =====
_integration: Optional[NineRouterIntegration] = None

def get_integration() -> NineRouterIntegration:
    global _integration
    if _integration is None:
        _integration = NineRouterIntegration()
    return _integration


# ===== Funções de Conveniência =====
def ask(prompt: str, **kwargs) -> str:
    """Pergunta rápida ao 9Router"""
    return get_integration().send_auto(prompt, **kwargs)

def search_web(query: str, **kwargs) -> List[Dict]:
    """Busca web rápida"""
    return get_integration().search_web(query, **kwargs)

def sync_now(data: Dict[str, Any]) -> SyncStatus:
    """Sincronização rápida"""
    return get_integration().sync_data(data)

def start_monitor(interval: int = 30):
    """Inicia monitoramento"""
    get_integration().start_monitoring(interval)

def stop_monitor():
    """Para monitoramento"""
    get_integration().stop_monitoring()


# ===== Demo / Teste =====
if __name__ == "__main__":
    print("=== 9Router Full Integration Demo ===\n")

    integration = NineRouterIntegration()

    # Callbacks para demonstração
    integration.on("on_message", lambda m: print(f"[MSG] {m.role}: {m.content[:80]}..."))
    integration.on("on_error", lambda e: print(f"[ERR] {e}"))
    integration.on("on_status_change", lambda s: print(f"[STATUS] {s}"))
    integration.on("on_sync", lambda s: print(f"[SYNC] {s.status}: {s.details}"))

    # Teste de saúde
    print(f"Health: {'OK' if integration.client.health() else 'FAIL'}")

    if integration.client.health():
        # Chat automático
        print("\n--- Chat Auto ---")
        response = integration.send_auto("Explique o que é 9Router em 2 frases, em português.")
        print(f"Resposta: {response}")

        # Busca web
        print("\n--- Busca Web ---")
        results = integration.search_web("GitHub Copilot app Windows download")
        for r in results[:3]:
            print(f"  - {r.get('title', 'N/A')}: {r.get('url', 'N/A')}")

        # Embeddings
        print("\n--- Embeddings ---")
        docs = ["9Router é um gateway de IA", "Permite múltiplos provedores", "Tem fallback automático"]
        results = integration.semantic_search("gateway IA", docs)
        for r in results:
            print(f"  Score: {r['score']:.3f} - {r['content']}")

        # Sincronização
        print("\n--- Sync ---")
        integration.sync_data({"test": "data", "timestamp": datetime.now().isoformat()})

        # Monitoramento (rodar por 10s)
        print("\n--- Monitor (10s) ---")
        integration.start_monitoring(interval=3)
        time.sleep(10)
        integration.stop_monitoring()

        print("\n--- Status Final ---")
        print(json.dumps(integration.get_status(), indent=2, ensure_ascii=False))
    else:
        print("\n9Router não está rodando. Inicie com: npx @decolua/9router")