---
name: xlsx-model
display-name: XLSX Model
description: Use para criar planilha .xlsx com fórmulas, validações, formatação e aba de instruções.
user-invocable: true
---

# XLSX Model

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\xlsx-model`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Precisa de cálculo confiável, não de tabela manual.
- Outra pessoa vai usar e precisa entender sem perguntar.

**Não use para:** listas simples de 5 linhas.

## Processo

1. Separe abas: `dados`, `calculo`, `painel` e `como-usar`.
2. Coloque entrada em célula destacada e nunca digite número dentro de fórmula.
3. Use validação de dados, formatação condicional e proteção das fórmulas.
4. Teste com casos extremos (zero, negativo, texto) e registre o resultado.

## Formato de saída

- Arquivo `.xlsx`
- Aba `como-usar` com passo a passo
- Lista de testes executados

## Critério de aceite

- nenhuma fórmula quebra com entrada vazia
- quem abre entende sem ajuda externa

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
