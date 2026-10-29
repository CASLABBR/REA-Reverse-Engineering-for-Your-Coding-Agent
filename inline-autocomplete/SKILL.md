---
name: inline-autocomplete
display-name: Ghost Writer Local
description: Use para instalar, operar ou melhorar o autocompletar local que sugere as próximas palavras em qualquer aplicativo com Tab.
user-invocable: true
---

# Ghost Writer Local

Sugere as próximas palavras enquanto você digita, **em qualquer aplicativo**, 100% no dispositivo. `Tab` aceita, `Esc` descarta.

## Quando usar

- Instalar, rodar, calibrar ou diagnosticar o autocompletar local.
- Escolher modelo, ajustar latência ou modo (prosa, código, curto).

**Não use para:** gerar documentos longos — isso é trabalho do agente com uma skill de conteúdo.

## Arquitetura em 3 peças

1. **Inferência** — `llama-server` local com modelo de 0.5B a 3B quantizado, em `127.0.0.1:8080`, prefix cache ligado.
2. **Contexto** — campo em foco lido via UI Automation no Windows + título da janela; fallback de snapshot de clipboard.
3. **Interface** — ghost text ao lado do cursor; `Tab` insere, `Esc` rejeita; cada decisão vira sinal em `perfil.jsonl`.

## Fluxo de uma sugestão

1. Detecta mudança de texto com debounce de 250–350 ms.
2. Monta o prompt: perfil de estilo + últimos 300–500 caracteres + modo.
3. Pede no máximo 12 tokens e para no primeiro `\n`, `.` ou `,`.
4. Mostra o ghost text; `Tab` insere; `Esc` descarta e registra a rejeição.
5. Aceites e rejeições alimentam o perfil de estilo local.

## Modos

| Modo | Quando | Comportamento |
| --- | --- | --- |
| `prosa` | e-mail, documento, chat | continua a frase no tom do próprio texto |
| `codigo` | editor | fill-in-the-middle, nunca completa credencial |
| `curto` | campos pequenos | no máximo 3 palavras |
| `snippet` | atalho digitado | `;assinatura` expande texto fixo, sem modelo |

Modo automático: título da janela + tipo do campo.

## Segurança e privacidade

- Nenhuma conexão fora de `127.0.0.1`.
- Silêncio total em campo de senha, cartão, banco e saúde (lista de títulos + regex de nome de campo).
- **Nunca sugerir número, valor, data ou nome próprio**: se a sugestão contiver dígito, descarte.
- Perfil salvo local e cifrado com DPAPI; comando para apagar tudo.

## Como subir

1. Baixe um modelo pequeno (1.5B–3B instruct, Q4).
2. `llama-server -m modelo.gguf -c 4096 --host 127.0.0.1 --port 8080 --no-webui`
3. `pip install uiautomation pynput requests pywin32 pyperclip`
4. `python app/ghostwriter.py --model seu-modelo`

Detalhes de instalação e diagnóstico em `app/README.md`. A especificação completa do produto, com as melhorias de projeto, está em `DESIGN.md`.

## Métricas de qualidade

- Latência p95 abaixo de 250 ms até o ghost aparecer.
- Taxa de aceite acima de 25%. Abaixo disso: modelo grande demais, contexto curto ou modo errado.
- Zero sugestão em campo sensível (teste obrigatório).

## Limites honestos

- Apps que não expõem texto via UI Automation (alguns Electron, terminais, jogos) ficam imprecisos — use o fallback e aceite menos qualidade.
- Modelo pequeno erra fato; por isso a regra de não sugerir números e nomes.
- Não substitui corretor ortográfico nem o autocomplete da IDE.
