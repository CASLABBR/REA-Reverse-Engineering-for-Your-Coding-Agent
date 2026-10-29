---
name: budget-planner
display-name: Budget Planner
description: Use para montar orçamento pessoal com categorias, alertas e projeção de saldo.
user-invocable: true
---

# Budget Planner

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\budget-planner`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- O dinheiro some e você não sabe para onde.
- Precisa planejar os próximos 12 meses.

**Não use para:** controle de gastos diário detalhado.

## Processo

1. Levante renda líquida e gastos fixos.
2. Categorize variáveis com média dos últimos 3 meses.
3. Projete 12 meses com sazonalidade (13º, férias, impostos).
4. Defina alertas e uma revisão mensal de 15 minutos.

## Formato de saída

- Planilha de orçamento
- Projeção de 12 meses
- Regras de alerta

## Critério de aceite

- projeção considera meses atípicos
- toda categoria tem dono e limite

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
