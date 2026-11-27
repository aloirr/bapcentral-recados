---
id: R-20261127-005628-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: aviso
prioridade: normal
tarefa: T-0024
responde_a: R-20261127-005437-alexandre
encerra: false
contrato: null
criado_em: 2026-11-27T00:56:28-04:00
---
# Recebido 1 A…7 A: T-0024, T-0033 e T-0045 em andamento, com previsões

Resposta de 27/11 00h54 recebida. Previsões no horário de Manaus.

## T-0024 (lote 2)
Os 3 PRs (#89, #91 e #97) estavam atrás do main e conflitavam com o pacote por farol da T-0035. O modulo-web e o modulo-robo já estão trazendo o main para as branches. Depois disso vêm o teste combinado e o reteste do revisor.
- Merge na ordem #89 (web) → #91 (robô) → #97 (testes); o robô nunca entra antes da web.
- Previsão: hoje, 27/11, até 04h.
- A parte do robô chega à produção pela rotina diária (06h30) do dia seguinte ao merge, porque o commit precisa de 2 horas no main.

## T-0033 (revisão geral)
Faltam dois ajustes da revisão do código, que não mudam o que o Alexandre viu:
- com filtro, os cartões da aba saem e fica o aviso, como já é hoje no site;
- o selo vermelho do Entregas passa a fundo claro, conforme o manual. Vou mandar os PNGs de antes e depois para a marca e para o UX.
Depois, o reteste dos 12 retoques e os PRs na ordem pós-venda → rota → robô → contrato → RN-VIS-001 → web → faróis → testes.
- Previsão: PRs no main hoje até 07h. Entro depois da T-0024 para não cruzar as mudanças da web.

## T-0034 (página inicial)
Em correção: 7 🟡 de UX e 6 de redundância. A simulação vem para vocês antes do PR.
- Previsão da simulação: hoje até 05h.

## T-0045 (visitas no Render)
O engenheiro já está fechando a ADR 0004 com as decisões. Ele também prepara:
- a proposta do render.yaml, como PR de governança: o número e o SHA vão para vocês;
- o passo a passo do Alexandre no Render e na Máxima, que mando por recado quando for a hora.
Previsões:
- PR do render.yaml: hoje até 03h;
- código do robô e da web: 28/11, depois que a T-0033 e a T-0034 entrarem;
- antes de ligar a rotina, o diagnóstico real no Render.
