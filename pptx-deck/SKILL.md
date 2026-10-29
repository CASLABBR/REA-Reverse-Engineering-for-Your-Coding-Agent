---
name: pptx-deck
display-name: PPTX Deck
description: Use para montar apresentação .pptx com narrativa, uma ideia por slide e consistência visual.
user-invocable: true
---

# PPTX Deck

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\pptx-deck`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Precisa apresentar resultado para cliente, chefe ou banca.
- Tem conteúdo demais e precisa virar narrativa.

**Não use para:** slides de uma única imagem.

## Processo

1. Escreva a mensagem central em uma frase; tudo serve a ela.
2. Faça o storyboard: 1 ideia por slide, com título que afirma algo.
3. Gere com python-pptx usando paleta e tipografia fixas (fonte mínima 18pt).
4. Valide convertendo para PDF/imagens e corrigindo overflow.

## Formato de saída

- Arquivo `.pptx`
- Storyboard em texto
- PDF de conferência

## Critério de aceite

- cada slide tem 1 ideia
- texto legível a 2 metros; sem overflow

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
