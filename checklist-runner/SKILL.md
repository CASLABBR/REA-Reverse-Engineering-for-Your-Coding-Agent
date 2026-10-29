---
name: checklist-runner
display-name: Checklist Runner
description: Use para transformar um processo em checklist executável com evidência exigida por item.
user-invocable: true
---

# Checklist Runner

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\checklist-runner`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- O processo sempre esquece um passo.
- Precisa garantir qualidade antes de entregar.

**Não use para:** tarefas de um passo só.

## Processo

1. Quebre o processo em passos verificáveis.
2. Defina evidência para cada item (arquivo, print, número).
3. Execute marcando status: feito, falhou, não se aplica.
4. Registre desvios e o que aprendeu no fim.

## Formato de saída

- Checklist preenchido
- Evidência por item
- Lista de desvios

## Critério de aceite

- nenhum item marcado sem evidência
- desvios com causa

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
