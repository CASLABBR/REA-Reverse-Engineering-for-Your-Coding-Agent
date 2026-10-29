---
name: localize-ptbr
display-name: Localize PT-BR
description: Use para traduzir para português localizando expressões, unidades e referências culturais.
user-invocable: true
---

# Localize PT-BR

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\localize-ptbr`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Tradução literal ficou estranha.
- Conteúdo precisa soar brasileiro, não traduzido.

**Não use para:** tradução juramentada ou técnica com termo fixado por norma.

## Processo

1. Traduza por bloco de sentido, não palavra por palavra.
2. Adapte unidades, moeda, datas e referências culturais.
3. Revise naturalidade lendo em voz alta.
4. Liste os termos mantidos no original e o motivo.

## Formato de saída

- Texto traduzido
- Tabela de adaptações feitas
- Termos mantidos no original

## Critério de aceite

- nenhuma construção que denuncie tradução
- números e unidades convertidos corretamente

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
