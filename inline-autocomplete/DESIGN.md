# Ghost Writer Local — especificação

> Ponto de partida: "sugere as próximas palavras em qualquer app, no dispositivo, Tab aceita".
> Este documento vai além disso: o que transforma um autocompletar em **parceiro de escrita**.

## O problema da ideia original

Autocompletar de palavra é útil, mas tem três limites:

1. **Palpite sem contexto** — sem saber o tipo de texto, ele sugere a mesma coisa em um contrato e em uma conversa.
2. **Ruído** — sugestões constantes atrapalham quem digita rápido; o custo de ignorar é maior que o ganho.
3. **Genérico** — não aprende que você escreve curto, sem adjetivo e sem exclamação.

## As 10 melhorias

| # | Melhoria | Por que muda o jogo |
| --- | --- | --- |
| 1 | **Três níveis de Tab** — `Tab` aceita a palavra, `Tab Tab` a frase inteira, `Esc` rejeita | Controle fino sem tirar a mão do teclado |
| 2 | **Perfil de estilo local** — aprende com aceites e rejeições, não com nuvem | A sugestão passa a soar como você, não como o modelo |
| 3 | **Modo automático por janela** — e-mail, chat, código, documento | Mesmo motor, comportamento certo em cada contexto |
| 4 | **Nunca inventa fato** — nenhuma sugestão com número, data, valor ou nome próprio | Elimina a pior falha possível: dado errado com cara de certo |
| 5 | **Silêncio em campo sensível** — senha, banco, saúde, documentos | Privacidade como padrão, não como opção |
| 6 | **Modo foco** — só sugere após X palavras digitadas ou após pausa real | Reduz ruído; sugestão vira evento, não perseguição |
| 7 | **"Por que sugeriu isso?"** — atalho mostra o contexto usado | Confiança: você vê o que o modelo leu |
| 8 | **Reescrita sob demanda** — seleciona e pede "mais curto", "mais formal" | Sai do "próxima palavra" para "próxima versão" |
| 9 | **Snippets + variáveis** — `;data`, `;assinatura`, `;saudacao` | O que é fixo não passa pelo modelo: instantâneo e sempre igual |
| 10 | **Integração com o `learning-map`** — rejeições viram preferência registrada | O sistema aprende uma vez e não repete o erro em outra skill |

## Decisões de arquitetura

- **Local, sempre.** `llama-server` em `127.0.0.1`. Nenhum byte sai da máquina. Sem telemetria, sem "melhorar o serviço".
- **Modelo pequeno e especializado.** 1.5B–3B quantizado ganha de 7B em latência, e latência é tudo aqui: acima de 250 ms a sugestão chega depois do dedo.
- **Cache de prefixo é obrigatório.** Reaproveitar o KV do texto já processado é o que faz a diferença entre 40 ms e 400 ms.
- **Overlay, não janela.** Ghost text desenhado por cima, sem foco, sem roubar clique.
- **Falha silenciosa.** Se o app não expõe texto ou o servidor cai, o programa simplesmente não sugere. Nunca travar a digitação.

## Métricas que definem sucesso

| Métrica | Meta | Como medir |
| --- | --- | --- |
| Latência p95 | < 250 ms | log de tempo por sugestão |
| Taxa de aceite | > 25% | aceites ÷ sugestões mostradas |
| Rejeição imediata (`Esc` em < 1 s) | < 15% | log de rejeição |
| Sugestão com dígito | 0 | teste automatizado no sanitizador |
| Sugestão em campo sensível | 0 | teste com formulário de mentira |

## Riscos e mitigação

| Risco | Mitigação |
| --- | --- |
| App não expõe texto (Electron, terminal) | fallback por clipboard; marcar o app como "modo degradado" |
| Modelo "alucina" continuação plausível | regra de não sugerir fato; limite de 12 tokens |
| Cansaço visual | modo foco + opacidade configurável + atalho para desligar |
| Perfil virar vigilância | arquivo local cifrado, rotação a cada 30 dias, botão "apagar perfil" |
| UAC / apps elevados | documento de limitação: rodar elevado ou não usar nesses apps |

## Roadmap

1. **MVP (1 semana)** — prosa + `Tab`/`Esc` + perfil mínimo + métricas no log.
2. **v0.2** — modos automáticos, snippets, sanitizador de fatos.
3. **v0.3** — `Tab Tab` por frase, reescrita de seleção, "por que sugeriu".
4. **v1.0** — perfil de estilo treinado localmente (few-shot + adapter leve), integração com `learning-map`.

## O que eu não faria

- Enviar texto para API na nuvem: destrói a proposta inteira.
- Sugerir parágrafos inteiros: vira geração de texto, não escrita sua.
- Esconder que é IA: o valor é velocidade, não passar por humano.
