---
name: pdf-digest
display-name: PDF Digest
description: Use para extrair e resumir informação de PDF longo com referência de páginas.
user-invocable: true
---

# PDF Digest

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\pdf-digest`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Recebeu um PDF de 100+ páginas e precisa do essencial.
- Vai citar trechos e precisa localizar depois.

**Não use para:** PDFs de 2 páginas.

## Processo

1. Mapeie a estrutura e localize sumário e conclusão.
2. Extraia tese, evidências e recomendações por seção.
3. Resuma com número de página de cada afirmação.
4. Liste o que ficou de fora e por quê.

## Formato de saída

- Resumo estruturado por seção
- Citações com página
- Lista do que ficou de fora

## Critério de aceite

- toda citação tem página
- resumo não inventa conclusão ausente

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
