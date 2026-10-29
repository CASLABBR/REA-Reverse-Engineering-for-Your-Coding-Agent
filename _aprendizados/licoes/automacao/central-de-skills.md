# Central de skills em E:\INTELIGENCIA_ARTIFICIAL\SKILL

- Domínio: automacao
- Criado: 2026-10-28 · Atualizado: 2026-10-28
- Confiança: hipótese
- Usos: 1 · Última aplicação: 2026-10-28
- Tags: skills, instalacao, caminhos, memoria

## Contexto
Criar, instalar ou editar uma skill nova.

## O que funcionou
- Manter a fonte da skill em `E:\INTELIGENCIA_ARTIFICIAL\SKILL\<nome>` e instalar globalmente a partir dessa pasta.
- Manter dados e memória em pasta separada com prefixo `_` (`_aprendizados`), fora do que é reinstalado.

## O que falhou / evitar
- Tentar gravar dentro de `C:\Users\Home\.lmstudio` — é área protegida do aplicativo.
- Guardar memória dentro da pasta da skill: reinstalar sobrescreve o conteúdo.

## Regra prática
> Fonte da skill na central `E:\INTELIGENCIA_ARTIFICIAL\SKILL\<nome>`; memória sempre em `E:\INTELIGENCIA_ARTIFICIAL\SKILL\_aprendizados`.

## Como verificar
A skill nova aparece em `Configurações → Skills` como habilitada e o arquivo-fonte existe na central, com a memória fora da pasta reinstalada.

## Evidências
- 2026-10-28 · criação da skill `learning-map`: gravar em `.lmstudio` foi recusado por ser área protegida do app.
