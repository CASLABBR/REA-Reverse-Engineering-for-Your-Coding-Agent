---
name: script-gen
display-name: Script Gen
description: Use para transformar tarefa manual repetitiva em script com ajuda, validação e tratamento de erro.
user-invocable: true
---

# Script Gen

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\script-gen`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Você repete o mesmo passo manual toda semana.
- Alguém precisa rodar o processo sem você.

**Não use para:** tarefas que acontecem uma vez.

## Processo

1. Mapeie os passos manuais e as decisões tomadas.
2. Defina entradas, saídas e o que fazer quando falhar.
3. Escreva com `--help`, validação de entrada e mensagens claras.
4. Teste em cópia dos dados e documente como agendar.

## Formato de saída

- Script executável
- `--help` com exemplos
- Instruções de uso e agendamento

## Critério de aceite

- falha com mensagem que diz o que fazer
- não apaga nem sobrescreve sem confirmação

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
