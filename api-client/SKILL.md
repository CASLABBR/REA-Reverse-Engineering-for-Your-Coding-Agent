---
name: api-client
display-name: API Client
description: Use para integrar API com autenticação, paginação, retry e tratamento de erros.
user-invocable: true
---

# API Client

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\api-client`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Precisa consumir uma API de terceiros.
- A integração falha de forma intermitente.

**Não use para:** scripts de uma chamada só.

## Processo

1. Mapeie endpoints, auth e limites de uso.
2. Implemente paginação e retry com backoff.
3. Trate erros por classe: 4xx, 5xx, timeout, rate limit.
4. Registre log com contexto e esconda credenciais.

## Formato de saída

- Módulo cliente
- Tabela de erros tratados
- Exemplo de uso

## Critério de aceite

- credencial nunca aparece em log
- rate limit respeitado

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
