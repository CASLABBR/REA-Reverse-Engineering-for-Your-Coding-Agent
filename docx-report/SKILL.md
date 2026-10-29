---
name: docx-report
display-name: DOCX Report
description: Use para produzir relatório .docx com capa, sumário, tabelas e padrão visual consistente.
user-invocable: true
---

# DOCX Report

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\docx-report`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Precisa entregar relatório formal em Word.
- O conteúdo já existe e falta dar forma profissional.

**Não use para:** documentos de 2 parágrafos.

## Processo

1. Defina a estrutura de seções antes de escrever qualquer texto.
2. Escreva o conteúdo em Markdown e só depois converta para .docx.
3. Aplique estilos (título, corpo, tabela) em vez de formatação manual.
4. Renderize/converta para PDF e confira quebras, sumário e tabelas.

## Formato de saída

- Arquivo `.docx` final
- Sumário com numeração correta
- PDF de conferência

## Critério de aceite

- sumário e títulos batem
- nenhuma tabela estoura a margem

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
