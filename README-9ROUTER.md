# 9Router - Configuração Completa e Integração Automática

## Visão Geral

Este projeto configura o **9Router** (gateway de IA local/remoto com OpenAI-compatible REST) com integração total:
- Chat automático com fallback entre provedores
- Busca web e fetch de URLs
- Embeddings para RAG/busca semântica
- Geração de imagens
- Text-to-Speech e Speech-to-Text
- Monitoramento em tempo real
- Sincronização automática de dados

---

## Instalação Rápida

### 1. Pré-requisitos
- **Node.js** 18+ instalado
- **Python** 3.10+ (para cliente Python)

### 2. Instalar 9Router
```bash
# Via npx (recomendado - sempre atualizado)
npx @decolua/9router

# Ou instalar globalmente
npm install -g @decolua/9router
9router
```

### 3. Configurar Variáveis de Ambiente
```bash
# Windows PowerShell
$env:NINEROUTER_URL = "http://localhost:20128"
$env:NINEROUTER_KEY = "sk-sua-chave-aqui"  # Opcional se auth desabilitado

# Ou crie arquivo .env (já incluído)
```

### 4. Executar Setup Automático
```powershell
# PowerShell (recomendado)
powershell -ExecutionPolicy Bypass -File setup-9router.ps1

# Ou batch simples
start-9router.bat
```

### 5. Monitoramento Automático (Background)
```powershell
# Inicia 9Router + monitora + reinicia se cair
.\auto-9router.ps1 -Background

# Com intervalo personalizado
.\auto-9router.ps1 -CheckInterval 60 -MaxRetries 5
```

---

## Uso no Python

### Cliente Básico
```python
from 9router_client import NineRouterClient, chat, search, embed

# Cliente completo
client = NineRouterClient()

# Health check
if client.health():
    print("9Router OK!")

# Chat simples
response = client.chat_simple("Olá, tudo bem?")
print(response)

# Chat com modelo específico
response = client.chat([
    {"role": "system", "content": "Você é um assistente útil."},
    {"role": "user", "content": "Explique 9Router"}
], model="openai/gpt-5")

# Auto-chat (combo com fallback)
response = client.auto_chat("Qual a capital da França?")

# Busca web
results = client.auto_search("GitHub Copilot download Windows")
for r in results[:3]:
    print(f"- {r['title']}: {r['url']}")

# Embeddings
vectors = client.embed(["texto 1", "texto 2"])

# Imagens
urls = client.generate_image("um gato cyberpunk")

# TTS
audio = client.tts("Olá mundo!", voice="alloy")
```

### Integração Completa (Auto-messaging, Sync, Monitor)
```python
from 9router_integration import NineRouterIntegration, get_integration

# Instância única
integration = NineRouterIntegration()

# Callbacks para eventos
integration.on("on_message", lambda msg: print(f"Nova msg: {msg.content[:50]}"))
integration.on("on_error", lambda err: print(f"Erro: {err}"))
integration.on("on_status_change", lambda status: print(f"Status: {status}"))
integration.on("on_sync", lambda sync: print(f"Sync: {sync.status}"))

# Chat automático
response = integration.send_auto("Explique RAG em 2 linhas")

# Busca web automática
results = integration.search_web("Python async best practices")

# Busca semântica (RAG)
docs = ["doc 1...", "doc 2...", "doc 3..."]
matches = integration.semantic_search("machine learning", docs, top_k=3)

# Sincronização de dados
integration.sync_data({"users": 100, "status": "active"})

# Monitoramento em background
integration.start_monitoring(interval=30)  # Verifica a cada 30s
# ... seu código ...
integration.stop_monitoring()

# Status completo
print(integration.get_status())
```

---

## Uso no JavaScript/TypeScript

```javascript
import { NineRouterClient, chat, search } from './9router-client.js';

const client = new NineRouterClient();

// Health
const ok = await client.health();

// Chat
const response = await client.autoChat("Olá!");

// Busca
const results = await client.autoSearch("Node.js 20 features");

// Streaming
for await (const chunk of client.streamChat({
    model: 'auto',
    messages: [{ role: 'user', content: 'Conte uma piada' }],
    stream: true
})) {
    process.stdout.write(chunk);
}
```

---

## Estrutura de Arquivos

```
E:\INTELIGENCIA_ARTIFICIAL\SKILL\
├── .claude/
│   └── settings.json          # Config Claude Code (env vars, hooks)
├── .env                       # Variáveis de ambiente (criado pelo setup)
├── 9router_client.py          # Cliente Python completo
├── 9router-client.js          # Cliente JS/TS completo
├── 9router-integration.py     # Integração total (auto, sync, monitor)
├── auto-9router.ps1           # Auto-manager PowerShell (background)
├── setup-9router.ps1          # Setup completo PowerShell
├── start-9router.bat          # Iniciador simples Windows
├── 9router-config.json        # Configuração da integração (auto-criado)
└── README-9ROUTER.md          # Este arquivo
```

---

## Modelos Disponíveis

```bash
# Listar todos
curl http://localhost:20128/v1/models

# Por categoria
curl http://localhost:20128/v1/models/chat
curl http://localhost:20128/v1/models/image
curl http://localhost:20128/v1/models/embedding
curl http://localhost:20128/v1/models/web
curl http://localhost:20128/v1/models/tts
curl http://localhost:20128/v1/models/stt
```

**Modelos Combo (Auto-fallback):**
- `combo/general` - Chat geral com fallback
- `combo/search` - Busca web com fallback
- `combo/coding` - Código com fallback
- `combo/creative` - Criativo com fallback

---

## Endpoints API (OpenAI Compatible)

| Funcionalidade | Endpoint |
|----------------|----------|
| Chat | `POST /v1/chat/completions` |
| Embeddings | `POST /v1/embeddings` |
| Imagens | `POST /v1/images/generations` |
| TTS | `POST /v1/audio/speech` |
| STT | `POST /v1/audio/transcriptions` |
| Web Search | `POST /v1/web/search` |
| Web Fetch | `POST /v1/web/fetch` |
| Modelos | `GET /v1/models[/kind]` |
| Health | `GET /api/health` |

---

## Exemplo de Requisição Direta (curl)

```bash
# Chat
curl -X POST http://localhost:20128/v1/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $NINEROUTER_KEY" \
  -d '{
    "model": "combo/general",
    "messages": [{"role": "user", "content": "Olá!"}],
    "temperature": 0.7
  }'

# Busca Web
curl -X POST http://localhost:20128/v1/web/search \
  -H "Content-Type: application/json" \
  -d '{"model": "combo/search", "query": "9Router tutorial", "max_results": 5}'

# Embeddings
curl -X POST http://localhost:20128/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{"model": "auto", "input": ["texto 1", "texto 2"]}'
```

---

## Troubleshooting

| Problema | Solução |
|----------|---------|
| `Connection refused` | Inicie 9Router: `npx @decolua/9router` |
| `401 Unauthorized` | Configure `NINEROUTER_KEY` ou desabilite auth no 9Router |
| `503 All accounts unavailable` | Adicione mais contas de provedores no Dashboard |
| `Invalid model` | Use `GET /v1/models` para ver IDs válidos |
| Python `ModuleNotFoundError` | `pip install requests numpy` |

---

## Recursos Avançados

### RAG (Retrieval-Augmented Generation)
```python
# 1. Indexar documentos
docs = ["doc1.txt", "doc2.pdf", ...]
embeddings = integration.create_embeddings(docs)

# 2. Buscar relevante
results = integration.semantic_search("pergunta do usuário", docs, top_k=5)

# 3. Gerar resposta com contexto
context = "\n".join([r['content'] for r in results])
prompt = f"Contexto:\n{context}\n\nPergunta: {user_question}"
answer = integration.send_auto(prompt)
```

### Pipeline Automático
```python
async def pipeline(pergunta):
    # 1. Busca web se precisar de info atual
    if "atual" in pergunta or "hoje" in pergunta:
        search_results = integration.search_web(pergunta)
        contexto = "\n".join([r['snippet'] for r in search_results[:3]])
        pergunta = f"{contexto}\n\n{pergunta}"

    # 2. Busca semântica na base local
    results = integration.semantic_search(pergunta, base_conhecimento)

    # 3. Resposta final
    return integration.send_auto(pergunta)
```

---

## Licença

MIT - Use livremente para projetos pessoais e comerciais.

---

**Pronto!** Seu 9Router está configurado para comunicação automática, sincronização e monitoramento em tempo real. 🚀