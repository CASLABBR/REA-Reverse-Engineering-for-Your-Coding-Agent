---
name: data-clean
display-name: Data Clean
description: Use para limpar e padronizar dados com registro do que foi alterado e por quê.
user-invocable: true
---

# Data Clean

Fonte: `E:\INTELIGENCIA_ARTIFICIAL\SKILL\data-clean`. Pertence à central de skills; use junto com `learning-map`.

## Quando usar

- Planilha ou base com nulos, duplicatas e formatos misturados.
- Vai analisar dados e precisa confiar neles.

**Não use para:** dados já tratados e documentados.

## Processo

1. Perfile: nulos, duplicatas, tipos, outliers.
2. Defina a regra de cada transformação antes de aplicar.
3. Registre cada mudança (linhas afetadas, regra, motivo).
4. Compare antes/depois com contagens e amostras.

## Formato de saída

- Base limpa
- Log de transformações
- Relatório antes/depois

## Critério de aceite

- toda transformação tem regra escrita
- nada foi excluído sem registro

## Regras gerais

- Não invente dado, número ou citação. Faltou informação? Pergunte (máx. 3 perguntas) ou declare a suposição.
- Quando o formato permitir, entregue arquivo, não só texto no chat.
- Se o pedido fugir do escopo desta skill, diga isso e faça o trabalho normalmente.
- Ao terminar, registre o resultado no `LOG.md` do `learning-map`.
