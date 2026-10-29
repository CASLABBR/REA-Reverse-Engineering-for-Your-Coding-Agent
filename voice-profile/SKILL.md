---
name: voice-profile
display-name: Voice Profile
description: Use para capturar seu tom de voz a partir de amostras e aplicá-lo a qualquer texto novo.
user-invocable: true
---

# Voice Profile

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\voice-profile`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Precisa escrever algo que soe como você.
- Vai terceirizar textos recorrentes e quer consistência.

**Não use para:** textos técnicos neutros ou jurídicos.

## Processo

1. Colete 3 a 5 amostras suas do mesmo tipo de texto.
2. Extraia marcadores: ritmo de frase, vocabulário, abertura, fechamento, humor.
3. Escreva `PERFIL-DE-VOZ.md` com regras e 2 exemplos de antes/depois.
4. Aplique em texto novo e compare lado a lado com uma amostra real.

## Formato de saída

- `PERFIL-DE-VOZ.md`
- Texto novo no seu tom
- Comparação antes/depois

## Critério de aceite

- o texto novo passa por leitura cega como seu
- nada de imitar bordão que você não usa

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
