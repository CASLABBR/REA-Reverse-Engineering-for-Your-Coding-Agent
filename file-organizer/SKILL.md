---
name: file-organizer
display-name: File Organizer
description: Use para organizar pasta bagunçada com regra de nomes, categorias e índice do que mudou.
user-invocable: true
---

# File Organizer

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\file-organizer`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- A pasta de downloads ou do projeto virou caos.
- Precisa encontrar arquivos por data e tema.

**Não use para:** pastas já organizadas.

## Processo

1. Inventarie arquivos, duplicatas e órfãos.
2. Defina esquema de nome: `AAAA-MM-DD_tema_versao.ext`.
3. Mova em lotes, confirmando antes de apagar qualquer coisa.
4. Gere `INDICE.md` com o que mudou e onde ficou.

## Formato de saída

- Pasta reorganizada
- `INDICE.md`
- Lista de duplicatas e sugestões de exclusão

## Critério de aceite

- nada é apagado sem confirmação
- nome novo permite ordenar por data

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
