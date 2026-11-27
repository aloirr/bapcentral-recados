---
id: R-20261127-044440-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: pergunta
prioridade: normal
tarefa: T-0023
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T04:44:40-04:00
---
# T-0023: o % de devoluções do Painel do Diretor muda (4,7% → 4,9% em nov) pela RN-GER-002; aprovar por delegação?

Pedido de aprovação, por delegação (R-20261127-013010-alexandre), de uma mudança no número do Diretor. Pela regra 10, número do Diretor só muda com simulação.

## O que muda
O "% do faturado" das Devoluções passa a usar o faturado líquido de devolução (VND − DEV, pela data da NF), como manda a RN-GER-002. Hoje ele divide pelo faturado bruto. O valor das devoluções em R$ não muda.

| Mês | Painel Executivo, cartão Devoluções (antes → depois) |
|---|---|
| SET/26 | R$ 28.569 · 10,7% → 12,0% |
| OUT/26 | R$ 1.667 · 1,1% → 1,1% |
| NOV/26 | R$ 5.552 · 4,7% → 4,9% |

- Nos dias em que a devolução passa da venda, o percentual mostra "—". Por exemplo, em 06/10 hoje aparece 106,51% e passa a "—". Nunca sai número negativo.
- Também muda na aba "Por vendedor (12 meses)": a coluna "% DEVOLVIDO" passa a ser calculada sobre o líquido, e a coluna "FATURADO 12M" também.
- O "D.U. S/ MOV." da NCC deixa de contar o dia de hoje (RN-GER-007).

## Conferência
- Os números vêm das bases congeladas, com hoje = 24/11, e batem com o farol de origem.
- Tabela completa: `recados/anexos/T-0023/antes-depois-devolucoes.md`.
- O revisor de código pediu exatamente esta conferência antes do merge.

## Decisão
(A) aprovar · (B) manter a conta atual (bruto) só no Painel.

Recomendo A: é a RN-GER-002.
