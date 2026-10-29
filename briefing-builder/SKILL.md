---
name: briefing-builder
display-name: Briefing Builder
description: Use ao iniciar projeto ou chat novo para montar um briefing reutilizável com objetivo, público, restrições e padrões.
user-invocable: true
---

# Briefing Builder

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\briefing-builder`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Cada sessão nova começa do zero e o contexto se perde.
- O trabalho tem padrões de estilo e decisões que precisam sobreviver.

**Não use para:** tarefas de uma única pergunta.

## Processo

1. Extraia objetivo, público, restrições e prazo do que já foi dito.
2. Liste as decisões já tomadas e o porquê de cada uma.
3. Liste arquivos-chave, padrões de formato e o que nunca deve ser feito.
4. Salve `BRIEFING.md` e releia no início de toda sessão do projeto.

## Formato de saída

- `BRIEFING.md` com no máximo 1 página
- Lista de decisões fechadas
- Lista de pontos ainda em aberto

## Critério de aceite

- cabe em 1 página
- qualquer pessoa entende o projeto só lendo ele

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
