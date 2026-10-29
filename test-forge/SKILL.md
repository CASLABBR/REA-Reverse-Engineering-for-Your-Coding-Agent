---
name: test-forge
display-name: Test Forge
description: Use para escrever testes com casos de borda, dados de exemplo e critério de falha.
user-invocable: true
---

# Test Forge

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\test-forge`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Código novo sem teste ou teste que só cobre o caminho feliz.
- Precisa provar que a correção funciona.

**Não use para:** testes de interface visual.

## Processo

1. Liste os comportamentos esperados em uma linha cada.
2. Gere casos de borda: vazio, zero, negativo, texto, limite.
3. Crie dados de exemplo realistas e pequenos.
4. Rode os testes antes da correção para confirmar que falham.

## Formato de saída

- Arquivo de testes
- Tabela de casos cobertos
- Saída da execução

## Critério de aceite

- casos de borda presentes
- teste falha quando o código quebra de propósito

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
