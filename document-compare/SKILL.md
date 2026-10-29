---
name: document-compare
display-name: Document Compare
description: Use para comparar duas versões de um documento e listar só as mudanças materiais.
user-invocable: true
---

# Document Compare

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\document-compare`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Recebeu v2 de um contrato, proposta ou texto.
- Precisa saber o que mudou sem reler tudo.

**Não use para:** documentos totalmente diferentes.

## Processo

1. Normalize formatação para comparar conteúdo, não estilo.
2. Alinhe por seção e parágrafo correspondente.
3. Liste mudanças materiais com impacto prático.
4. Ignore ruído cosmético; diga quando só houve formatação.

## Formato de saída

- Tabela de mudanças (antes, depois, impacto)
- Lista de mudanças de risco
- Resumo em 5 linhas

## Critério de aceite

- nenhuma mudança material omitida
- impacto explicado, não só transcrito

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
