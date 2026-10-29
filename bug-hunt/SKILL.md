---
name: bug-hunt
display-name: Bug Hunt
description: Use para depurar de forma sistemática: reproduzir, hipótese, experimento e conclusão.
user-invocable: true
---

# Bug Hunt

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\bug-hunt`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Algo quebrou e a causa não é óbvia.
- Já tentou consertar no chute e piorou.

**Não use para:** erros com mensagem que aponta a linha exata.

## Processo

1. Reproduza com o menor passo possível e registre o ambiente.
2. Formule 3 hipóteses e ordene por probabilidade.
3. Teste uma hipótese por vez, mudando só uma variável.
4. Corrija a causa raiz e escreva teste de regressão.

## Formato de saída

- Causa raiz explicada
- Correção aplicada
- Teste que falha sem a correção

## Critério de aceite

- explica por que o bug acontecia
- não introduz correção defensiva sem teste

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
