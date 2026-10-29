---
name: contract-check
display-name: Contract Check
description: Use para revisar contrato por checklist de riscos: prazo, multa, rescisão, dados, exclusividade.
user-invocable: true
---

# Contract Check

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\contract-check`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Vai assinar ou renovar contrato.
- Recebeu minuta e precisa levantar riscos antes do advogado.

**Não use para:** termos de uso de site.

## Processo

1. Liste obrigações de cada parte com prazos.
2. Cheque multa, rescisão, renovação automática e reajuste.
3. Cheque dados, confidencialidade e propriedade intelectual.
4. Sinalize cláusulas ambíguas e diga que a decisão final é jurídica.

## Formato de saída

- Checklist de riscos por cláusula
- Lista de perguntas para o advogado
- Resumo dos 5 pontos mais críticos

## Critério de aceite

- nenhum risco apresentado como parecer jurídico
- toda cláusula citada com número

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
