---
name: image-prompt
display-name: Image Prompt
description: Use para escrever prompts de imagem com estilo consistente, composição e negative prompt.
user-invocable: true
---

# Image Prompt

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\image-prompt`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Precisa gerar imagens coerentes em série.
- O resultado sai aleatório e fora do estilo.

**Não use para:** edição de imagem existente.

## Processo

1. Defina sujeito, ação e ambiente em uma frase.
2. Especifique estilo, luz, lente e composição.
3. Adicione negative prompt e proporção.
4. Gere variações mudando uma variável por vez.

## Formato de saída

- Prompt principal
- Negative prompt
- 3 variações controladas

## Critério de aceite

- estilo reproduzível entre gerações
- uma variável por variação

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
