---
name: visual-explain
display-name: Visual Explain
description: Use para transformar explicação em diagrama legível (Mermaid ou Excalidraw).
user-invocable: true
---

# Visual Explain

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\visual-explain`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Explicação longa ficaria melhor como diagrama.
- Precisa alinhar um processo com outras pessoas.

**Não use para:** diagramas decorativos sem informação.

## Processo

1. Identifique o tipo: fluxo, arquitetura, estados, hierarquia.
2. Liste nós e arestas em texto antes de desenhar.
3. Gere em Mermaid ou Excalidraw com rótulos curtos.
4. Valide legibilidade: cabe na tela, sem cruzamento desnecessário.

## Formato de saída

- Diagrama renderizado
- Lista de nós e conexões
- Legenda de leitura

## Critério de aceite

- dá para entender sem explicação oral
- rótulos com no máximo 3 palavras

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
