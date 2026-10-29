---
name: explain-levels
display-name: Explain Levels
description: Use para explicar o mesmo conceito em três níveis: criança, leigo e técnico.
user-invocable: true
---

# Explain Levels

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\explain-levels`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Precisa explicar algo para públicos diferentes.
- Você mesmo quer testar se entendeu de verdade.

**Não use para:** conceitos que só fazem sentido em nível técnico.

## Processo

1. Escreva a versão criança com analogia do cotidiano.
2. Escreva a versão leigo sem jargão e com exemplo prático.
3. Escreva a versão técnica com precisão e limites.
4. Aponte onde a analogia deixa de valer.

## Formato de saída

- Três explicações encadeadas
- Analogia central
- Onde a simplificação quebra

## Critério de aceite

- a versão técnica não contradiz as outras
- limites da analogia declarados

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
