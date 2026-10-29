---
name: decision-matrix
display-name: Decision Matrix
description: Use para decidir entre opções com critérios ponderados e teste de sensibilidade.
user-invocable: true
---

# Decision Matrix

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\decision-matrix`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Precisa escolher entre 2 a 5 alternativas.
- A decisão está travada por opinião.

**Não use para:** decisões com um único critério.

## Processo

1. Liste opções e critérios que realmente importam.
2. Atribua pesos somando 100%.
3. Pontue cada opção com evidência, não com impressão.
4. Teste a sensibilidade: a resposta muda se o peso mudar 20%?

## Formato de saída

- Matriz pontuada
- Ranking com justificativa
- Teste de sensibilidade

## Critério de aceite

- cada nota tem evidência
- conclusão resiste a variação de peso

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
