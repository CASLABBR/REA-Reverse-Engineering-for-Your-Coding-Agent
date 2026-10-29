---
name: health-prep
display-name: Health Prep
description: Use para organizar sintomas, exames e perguntas para a consulta médica, sem diagnosticar.
user-invocable: true
---

# Health Prep

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\health-prep`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Consulta chegando e você esquece o que ia falar.
- Sintomas espalhados em anotações.

**Não use para:** diagnóstico, prescrição ou interpretação de exame.

## Processo

1. Liste sintomas com data de início, duração e intensidade.
2. Organize exames, medicamentos e alergias em ordem cronológica.
3. Escreva 5 perguntas objetivas para o médico.
4. Reforce que o material organiza informação e não substitui avaliação médica.

## Formato de saída

- Resumo cronológico para levar
- Lista de medicamentos e exames
- 5 perguntas para o médico

## Critério de aceite

- nenhuma conclusão diagnóstica
- informação datada e objetiva

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
