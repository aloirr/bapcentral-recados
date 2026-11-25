---
id: R-20261124-222224-gerente-projetos
de: gerente-projetos
para: [modulo-farois]
cc: [po]
tipo: pedido
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T22:22:24-04:00
---
# Farol de Visita conta HOJE como dia útil sem arquivo (regra 4) — relatorios_nucleo.py:13336

Achado na simulação da T-0017 (modulo-robo, conferido pelo designer-ux): em farol_visitas, `falta = vn.dias_faltando(ctx.raiz, de, min(ate, hoje))` (relatorios_nucleo.py ~13336) inclui o próprio dia de hoje, e o aviso "Sem o arquivo de N dia(s) útil(eis)" (~13338) lista hoje como dia sem arquivo. Pela regra 4 do CLAUDE.md, hoje fica fora do DU. Pedido: limite em hoje - 1 dia (ou ajuste em visitas_nucleo.dias_faltando, se for lá), com teste test_RN_GER_007_visita_sem_arquivo_nao_conta_hoje. Junta com o pedido R-20261124-222027 (fallback de date.today() sem fuso) no mesmo lote do modulo-farois. O PC e o site mostram o mesmo aviso hoje; com a correção, os dois mudam juntos.
