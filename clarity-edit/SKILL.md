---
name: clarity-edit
display-name: Clarity Edit
description: Use para cortar gordura, simplificar frases e manter o sentido de um texto.
user-invocable: true
---

# Clarity Edit

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\clarity-edit`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Texto longo, confuso ou cheio de jargão.
- Precisa caber em menos espaço sem perder conteúdo.

**Não use para:** textos literários onde o estilo é o ponto.

## Processo

1. Marque frases com mais de 25 palavras e voz passiva sem agente.
2. Corte redundância, advérbios vazios e preâmbulos.
3. Reescreva na ordem sujeito-verbo-objeto.
4. Releia em voz alta e informe a redução de palavras.

## Formato de saída

- Texto revisado
- Lista das 5 mudanças mais importantes
- Percentual de redução

## Critério de aceite

- sentido preservado
- redução de pelo menos 15% ou justificativa

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
