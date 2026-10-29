---
name: prompt-forge
display-name: Prompt Forge
description: Use quando o pedido for vago ou grande demais, para transformá-lo em prompt com papel, contexto, formato e critério de aceite.
user-invocable: true
---

# Prompt Forge

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\prompt-forge`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- O pedido chega como "faz um texto sobre X" e não se sabe o formato.
- A tarefa é grande e o modelo tende a entregar algo genérico.

**Não use para:** perguntas simples que já têm resposta direta.

## Processo

1. Reescreva o pedido em uma frase de resultado esperado.
2. Faça no máximo 3 perguntas de clarificação: público, restrição e formato.
3. Monte o prompt com papel, contexto, tarefa, formato de saída e critérios de aceite.
4. Teste o prompt em um caso pequeno antes de entregar; ajuste o que falhou.

## Formato de saída

- Prompt final pronto para colar
- Perguntas de clarificação (se houver)
- Suposições assumidas

## Critério de aceite

- o prompt tem formato de saída verificável
- não passa de 400 palavras

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
