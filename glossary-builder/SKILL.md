---
name: glossary-builder
display-name: Glossary Builder
description: Use para construir glossário de um domínio com definição, exemplo e erro comum.
user-invocable: true
---

# Glossary Builder

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\glossary-builder`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Está entrando em uma área nova com muito jargão.
- Vai produzir material e precisa padronizar termos.

**Não use para:** listas de siglas sem explicação.

## Processo

1. Colete os termos que aparecem no material.
2. Defina cada um em uma frase, sem usar outro termo desconhecido.
3. Dê um exemplo e um erro comum de uso.
4. Ordene alfabeticamente e agrupe sinônimos.

## Formato de saída

- Glossário em tabela
- Definição, exemplo e erro por termo
- Lista de sinônimos e siglas

## Critério de aceite

- definição não usa termo não definido
- todo termo tem exemplo

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
