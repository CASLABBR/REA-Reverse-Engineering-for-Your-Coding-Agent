# Ghost Writer Local — instalação e diagnóstico

Protótipo do MVP. Windows 10/11.

## 1. Modelo e servidor

Baixe um modelo pequeno em GGUF (1.5B–3B instruct, quantização Q4) e suba:

```bash
llama-server -m caminho\modelo.gguf -c 4096 --host 127.0.0.1 --port 8080 --no-webui
```

Teste: `curl http://127.0.0.1:8080/health` deve responder `{"status":"ok"}`.

## 2. Dependências

```bash
pip install uiautomation pynput requests pywin32 pyperclip
```

## 3. Diagnóstico

```bash
python ghostwriter.py --check
```

Esperado:

```
servidor: ok
UIA: ok
clipboard: ok
```

`UIA: indisponível` significa que a leitura de texto não vai funcionar em nenhum app.

## 4. Uso

```bash
python ghostwriter.py --model seu-modelo
```

- Digite em qualquer app.
- `Tab` aceita a sugestão.
- `Esc` descarta (e registra a rejeição).

## 5. Problemas comuns

| Sintoma | Causa provável | Solução |
| --- | --- | --- |
| Nada aparece | app não expõe texto via UIA | testar em Notepad; ver limitações |
| Aparece e some | debounce curto demais | aumentar `DEBOUNCE_S` |
| Sugestão cortada no meio | limite de tokens | aumentar `MAX_TOKENS` |
| Não funciona no app X | app elevado (admin) | rodar o script elevado |
| Latência alta | modelo grande / sem cache | modelo menor, `-c 4096`, GPU offload |

## 6. Privacidade

- Só fala com `127.0.0.1`.
- `perfil.jsonl` guarda apenas a sugestão e se foi aceita. Apague o arquivo para zerar o aprendizado.
- Campos de senha são ignorados antes de qualquer chamada ao modelo.
