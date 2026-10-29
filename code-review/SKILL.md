---
name: code-review
display-name: Code Review
description: Use para revisar código com checklist de correção, segurança, legibilidade e testes.
user-invocable: true
---

# Code Review

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\code-review`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Vai aprovar ou rejeitar uma mudança.
- Quer revisão antes de pedir revisão humana.

**Não use para:** revisão de estilo que o formatador resolve.

## Processo

1. Entenda a intenção da mudança antes de olhar linha por linha.
2. Verifique correção e casos de borda.
3. Verifique segurança: entrada, permissão, dados sensíveis.
4. Verifique legibilidade e cobertura de teste; classifique bloqueante x sugestão.

## Formato de saída

- Lista de achados com severidade
- Sugestões de patch
- O que precisa de teste

## Critério de aceite

- todo achado cita arquivo e linha
- separação clara entre bloqueante e opcional

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
