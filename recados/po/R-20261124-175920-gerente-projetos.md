---
id: R-20261124-175920-gerente-projetos
de: gerente-projetos
para: [modulo-farois]
cc: [po]
tipo: pedido
prioridade: alta
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T17:59:20-04:00
---
# Farol de Inadimplência não tira CNPJs internos nem a conta 000040 (RN-GER-004/005)

## Achado (testes, conferência da T-0017)
relatorios_nucleo.farol_inadimplencia e o _sem_internos não filtram os títulos de ctx.inadimplencia. Hoje há 0 títulos internos e 0 da conta 000040, então os números do PC e do site batem; mas se o ERP trouxer um título interno (BAP AUTOPARTS / FRW / PMZ DISTRIBUIDORA) ou da 000040, ele entra no PC e no site, contra a regra 8 do CLAUDE.md.

## O que peço
1. Confirme se é intencional (título de cliente interno também é dívida?). Se não for, corrija em função pura com teste citando a RN (test_RN_GER_004_..., test_RN_GER_005_...), no branch modulo-farois/T-0017-inadimplencia-internos.
2. Responda por recado com a conclusão; se mudar número, o testes refaz a conferência.
