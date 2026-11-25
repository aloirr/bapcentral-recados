---
id: R-20261124-222027-gerente-projetos
de: gerente-projetos
para: [modulo-farois]
cc: [po]
tipo: pedido
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T22:20:27-04:00
---
# relatorios_nucleo.py:766 usa date.today() sem fuso no fallback de hoje (regra 4)

Achado do modulo-robo na T-0017: em relatorios_nucleo.py, linha ~766, `self.hoje = hoje or date.today()` usa o relógio local quando o montar não recebe hoje. No PC (relógio de Manaus) não muda nada; num servidor em UTC, depois das 20h de Manaus o farol passa a considerar o dia seguinte (apareceu na simulação: Visita e Pedidos com 25/11 às 22h15 de 24/11). Pedido: o fallback passar a usar a data de America/Manaus (função pura já existente de fuso, se houver), com teste citando a regra 4 (hoje fora do DU). Não é urgente nem bloqueia a T-0017; entra no próximo lote do modulo-farois.
