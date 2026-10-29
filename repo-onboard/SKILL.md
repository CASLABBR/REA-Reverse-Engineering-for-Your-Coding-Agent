---
name: repo-onboard
display-name: Repo Onboard
description: Use para entender repositório desconhecido: stack, entrypoints, testes, riscos e mapa de pastas.
user-invocable: true
---

# Repo Onboard

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\repo-onboard`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Caiu em um repositório que não conhece.
- Precisa mexer em código legado sem quebrar.

**Não use para:** repositórios de um único arquivo.

## Processo

1. Mapeie pastas, linguagens e dependências.
2. Ache entrypoints e comandos de build, teste e execução.
3. Identifique riscos: código morto, segredos, testes frágeis.
4. Escreva `MAPA-DO-REPO.md` com o caminho de uma mudança típica.

## Formato de saída

- `MAPA-DO-REPO.md`
- Comandos para rodar e testar
- Lista de riscos encontrados

## Critério de aceite

- dá para rodar o projeto seguindo só o mapa
- riscos citam arquivo e linha

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
