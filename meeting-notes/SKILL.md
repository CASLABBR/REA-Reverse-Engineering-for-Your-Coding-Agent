---
name: meeting-notes
display-name: Meeting Notes
description: Use após reunião ou transcrição para gerar ata com decisões, responsáveis, prazos e pendências.
user-invocable: true
---

# Meeting Notes

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\meeting-notes`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Reunião terminou e ninguém sabe o que foi decidido.
- Transcrição longa e precisa virar registro útil.

**Não use para:** conversas sem decisão ou acompanhamento.

## Processo

1. Separe fatos, opiniões e decisões — não misture.
2. Para cada decisão registre responsável, prazo e critério de pronto.
3. Liste pendências e riscos com dono.
4. Entregue resumo de 5 linhas + ata completa.

## Formato de saída

- Resumo executivo de 5 linhas
- Tabela de decisões (decisão, dono, prazo)
- Lista de pendências e riscos

## Critério de aceite

- toda decisão tem dono e prazo
- nada de opinião apresentada como decisão

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
