---
id: R-20261124-220929-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T22:09:29-04:00
---
# Faróis: Pedidos, Entregas e Visita começaram agora; #57 e #59 no main; Inadimplência no site sem dado até o robô novo

## Respostas
1. #57 (deploy automático, governança): squash feito com o seu autorizo (20477b1). #59 (rotina diária, T-0018) também no main (e74de94); os testes dela entram pelo #60.
2. Os 3 faróis que faltam (Pedidos, Entregas, Visita): começaram AGORA (22:10), os três juntos — modulo-robo põe os três no pacote; modulo-web desenha os blocos que faltam (tabela de frete por estado das Entregas, cartões em faixa de Pedidos). Eu tinha previsto um farol por entrega (Pedidos 26/11, Entregas 27/11, Visita 30/11) e a entrega 2 da Inadimplência (WhatsApp) entrou na frente; com os três em paralelo, a previsão fica: simulação PNG dos três 25/11 até 12h; PRs no main 25/11 à tarde. As datas antigas ficam como teto.
3. Sim: o Farol de Inadimplência já está no site (v0.2.0, menu dos 4 faróis), mas SEM DADO até o robô novo rodar. O notebook roda o robô da pasta da EMPRESA com o bap_automation antigo, que só manda o Painel. O dado aparece quando a produção estiver na pasta nova com o código do main: rotina diária (T-0018) + migração do robô para a pasta pessoal (plano no R-20261124-215228, 5 decisões do Alexandre pendentes). Se o Alexandre quiser ver dados antes da migração, a opção rápida é instalar só o bap_automation.py do main na pasta da EMPRESA (onde o robô roda) — diga se quer que eu prepare isso.

## Abertos para o seu autorizo (governança)
- #61: regra 11 do CLAUDE.md (instale automático, T-0018), head cdeaec893a500e51b2e9143c78c3e96942940f95 — revisor conferindo; mando quando aprovado.
