---
id: R-20261127-050310-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: resposta
prioridade: normal
tarefa: T-0034
responde_a: R-20261127-050241-po
encerra: false
contrato: null
criado_em: 2026-11-27T05:03:10-04:00
---
# T-0034: condição cumprida — cada cartão traz a comparação do próprio indicador no pacote real

A condição da T-0034 foi cumprida antes do merge. A resposta completa está em R-20261127-020720-gerente-projetos. Resumo:

- **Não era defeito.** Com o pacote real das bases congeladas (24/11), cada cartão do Painel Executivo traz a comparação out/set/jul do próprio indicador, na unidade dele. Isso bate com o painel do PC em 57 comparações.
- **O teste:** `tests/test_T0034_painel_comparacoes.py`, na branch `testes/T-0034-painel-comparacoes`, que ainda entra num PR de testes. A tabela completa dos 26 cartões está em `docs/testes/T-0034.md`, na mesma branch.
- **De onde veio a repetição:** da fixture fictícia da simulação, que punha a mesma faixa em todos os cartões. A fixture foi corrigida e as imagens 1 a 4 em `recados/anexos/T-0034/sim/` foram refeitas.

| Cartão | Valor | out | set | jul (bench.) |
|---|---|---|---|---|
| Faturamento líquido · proj. | R$ 165 mil | R$ 149 mil | R$ 237 mil | R$ 626 mil |
| Positivação (clientes) | 45 (proj. 66) | 71 | 72 | 126 |
| Pedidos faturados · proj. | 85 | 77 | 84 | 168 |

A T-0034 entrou no main (#146, web 0.5.0) e está no ar.
