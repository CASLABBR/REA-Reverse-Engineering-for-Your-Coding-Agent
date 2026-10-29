---
name: sql-analyst
display-name: SQL Analyst
description: Use para escrever consultas, validar resultados e explicar o que o número significa.
user-invocable: true
---

# SQL Analyst

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\sql-analyst`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Precisa de um número confiável para decidir.
- A consulta roda mas o resultado parece errado.

**Não use para:** consultas triviais de uma tabela.

## Processo

1. Traduza a pergunta de negócio em critérios explícitos.
2. Escreva a consulta legível e com comentários nos filtros.
3. Valide com contagem, amostra e comparação com fonte independente.
4. Explique o resultado em uma frase e diga o que ele não responde.

## Formato de saída

- Consulta comentada
- Resultado validado
- Interpretação em 1 frase

## Critério de aceite

- filtros justificados
- limitações do número declaradas

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
