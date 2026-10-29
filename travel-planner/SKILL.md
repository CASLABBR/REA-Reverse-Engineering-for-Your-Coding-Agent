---
name: travel-planner
display-name: Travel Planner
description: Use para montar roteiro de viagem com logística, custos e plano B.
user-invocable: true
---

# Travel Planner

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\travel-planner`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Vai viajar e quer roteiro realista.
- Precisa equilibrar orçamento e tempo.

**Não use para:** reservas já fechadas sem flexibilidade.

## Processo

1. Defina datas, orçamento e ritmo desejado.
2. Agrupe atrações por proximidade e abra exceções conscientes.
3. Liste reservas críticas e prazos.
4. Crie plano B por dia (chuva, atraso, fechamento).

## Formato de saída

- Roteiro por dia
- Planilha de custos
- Plano B e contatos úteis

## Critério de aceite

- deslocamentos cabem no dia
- custos com margem de 15%

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
