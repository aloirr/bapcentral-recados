---
id: R-20261126-180714-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: revisao
prioridade: normal
tarefa: T-0033
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-26T18:07:14-04:00
---
# Pareceres do revisor-codigo: #126 e #127 aprovados

# Pareceres do revisor-codigo: PR #126 e PR #127

Origem: subagente revisor-codigo desta sessão, gravado pelo gerente (decisão 3 A).

## PR #126 (T-0032, correção do celular), head 986c6af
Aprovado. O menu do Exportar abre inteiro a 390 e a 360 px em Entregas, Pedidos (com e sem "Ignorar fora da base") e nas 7 abas do Visita. No PC, 1366 e 700 px ficam iguais ao main. A primeira versão (8e9befb) tinha 🔴, o menu cortado; resolvido.

## PR #127 (T-0033, marca na cobrança), head aa3fc77
Aprovado, sem 🔴 nem 🟡. Só cobranca_whatsapp.py:36 e email_inadimplencia.py:406,433. RELATORIOS/ igual ao main. Nenhum teste cita o texto antigo. 🟢 a suíte regrava RELATORIOS/painel_diretor_hist.json: isolar em tmp (vai ao testes). 🟢 "BAP Auto Parts" ainda em email_parcial.py, email_rota.py, conta_email.py e bap_visual.py (T-0033, outros donos).
