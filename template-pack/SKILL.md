---
name: template-pack
display-name: Template Pack
description: Use para criar templates reutilizáveis de documentos com campos marcados e instruções de uso.
user-invocable: true
---

# Template Pack

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\template-pack`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Repete o mesmo documento toda semana.
- Quer padronizar o que a equipe produz.

**Não use para:** documentos usados uma única vez.

## Processo

1. Identifique campos variáveis e partes fixas.
2. Crie o template com marcadores claros ({{campo}}).
3. Escreva instruções de preenchimento no topo.
4. Teste preenchendo um caso real e ajuste o que confundir.

## Formato de saída

- Template em Markdown ou DOCX
- Instruções de preenchimento
- Exemplo preenchido

## Critério de aceite

- preenche sem dúvida olhando só as instruções
- marcadores fáceis de localizar

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
