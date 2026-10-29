---
name: source-audit
display-name: Source Audit
description: Use quando precisar saber se uma fonte é confiável: autor, data, interesse, evidência e o que ela não prova.
user-invocable: true
---

# Source Audit

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\source-audit`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Encontrou uma estatística impactante e quer usá-la.
- Duas fontes dizem coisas opostas sobre o mesmo fato.

**Não use para:** fontes primárias oficiais já verificadas.

## Processo

1. Identifique autor, veículo, data e financiamento.
2. Cheque se a evidência citada sustenta a manchete.
3. Procure a fonte primária (estudo, lei, dataset).
4. Classifique: confiável, usar com ressalva ou descartar — e diga o que ela não prova.

## Formato de saída

- Ficha da fonte em 6 linhas
- Classificação de confiabilidade
- Limites do que a fonte permite afirmar

## Critério de aceite

- a classificação vem com justificativa
- aponta o que a fonte não prova

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
