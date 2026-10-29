---
name: purchase-advisor
display-name: Purchase Advisor
description: Use para decidir compra comparando custo total, durabilidade e critérios ponderados.
user-invocable: true
---

# Purchase Advisor

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\purchase-advisor`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Compra relevante e muitas opções parecidas.
- Preço baixo agora pode custar caro depois.

**Não use para:** compras de baixo valor.

## Processo

1. Defina uso real e vida útil esperada.
2. Compare custo total (compra, manutenção, consumo, revenda).
3. Cheque garantia, assistência e disponibilidade de peças.
4. Decida com critérios ponderados e diga o risco da escolha.

## Formato de saída

- Tabela comparativa com custo total
- Recomendação justificada
- Riscos da escolha

## Critério de aceite

- custo total, não só preço
- recomendação indica quando não comprar

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
