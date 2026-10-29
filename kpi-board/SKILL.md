---
name: kpi-board
display-name: KPI Board
description: Use para definir KPIs, metas e painel de acompanhamento com fonte e frequência.
user-invocable: true
---

# KPI Board

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\kpi-board`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Precisa medir se o trabalho está dando resultado.
- Tem métricas demais e nenhuma decisão.

**Não use para:** métricas de vaidade sem decisão associada.

## Processo

1. Defina qual decisão cada KPI apoia.
2. Especifique fórmula, fonte e frequência.
3. Defina meta e faixa de alerta.
4. Monte painel com 5 a 7 KPIs e uma leitura em 3 linhas.

## Formato de saída

- Tabela de KPIs (fórmula, fonte, meta)
- Painel
- Leitura executiva de 3 linhas

## Critério de aceite

- todo KPI tem dono e decisão
- fórmula reproduzível por outra pessoa

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
