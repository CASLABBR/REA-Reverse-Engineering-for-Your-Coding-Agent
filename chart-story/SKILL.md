---
name: chart-story
display-name: Chart Story
description: Use para escolher o gráfico certo e escrever a manchete que o dado conta.
user-invocable: true
---

# Chart Story

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\chart-story`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Precisa mostrar um resultado e não sabe qual gráfico.
- O gráfico atual não comunica nada.

**Não use para:** tabelas de 3 números.

## Processo

1. Defina a mensagem em uma frase antes de escolher o gráfico.
2. Escolha o gráfico pela comparação (evolução, distribuição, composição, relação).
3. Remova ruído: grade, 3D, cores sem significado.
4. Escreva a manchete afirmando o achado, não descrevendo o eixo.

## Formato de saída

- Gráfico pronto
- Manchete do achado
- Nota de fonte e período

## Critério de aceite

- a manchete afirma algo verificável
- eixos e unidades explícitos

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
