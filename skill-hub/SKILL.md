---
name: skill-hub
display-name: Central de Skills
description: Use quando a tarefa corresponder a um fluxo catalogado na central de skills, para localizar e seguir a skill específica.
user-invocable: true
---

# Central de Skills

Biblioteca com 51 skills em `E:\INTELIGENCIA_ARTIFICIAL\SKILL`. Esta skill faz o roteamento: encontra a skill certa e segue o processo dela.

## Quando usar

- A tarefa combina com alguma linha do `_indice.md`.
- O usuário diz "usa a skill de X", "tem skill pra isso?" ou pede um entregável que já existe na central.

**Não use para:** conversa simples, dúvida pontual ou tarefa que nenhuma skill cobre.

## Passo 1 — Rotear

1. Leia `E:\INTELIGENCIA_ARTIFICIAL\SKILL\_indice.md`.
2. Escolha a skill mais específica. Empate? Prefira a de escopo menor.
3. Nenhuma correspondência clara? Não force: faça a tarefa normalmente e diga que não havia skill.

## Passo 2 — Carregar

1. Leia `E:\INTELIGENCIA_ARTIFICIAL\SKILL\<nome>\SKILL.md` inteiro.
2. Leia `assets\` e `referencias\` só se o `SKILL.md` pedir.
3. Siga o processo e o formato de saída à risca. A skill manda mais que seu estilo padrão.

## Passo 3 — Fechar

1. Cumpra o critério de aceite antes de entregar.
2. Registre no `learning-map`: linha no `LOG.md` e lição se houve aprendizado reutilizável.
3. Se precisou improvisar além da skill, registre a lacuna — é candidata a melhoria da própria skill.

## Regras

- Nunca invente skill que não está no índice.
- Se a skill exigir arquivo que não existe, diga e ofereça criar.
- Não instale nem edite skill sem pedir.
- Ao final, uma linha: `Skill usada: <nome>`.
