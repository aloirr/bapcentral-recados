---
id: R-20261127-101025-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: normal
tarefa: T-0052
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T10:10:25-04:00
---
# T-0052: simulação final do Painel Executivo para aprovar

**T-0052 (Painel Executivo no site): simulação final para você aprovar por delegação (R-20261127-013010-alexandre).**

**Simulação** (dados fictícios): `recados/anexos/T-0052/sim/`
- `antes-*` e `depois-*`, nas abas Resultado e Produtividade, no PC (1366 px) e no celular (390 px);
- `MEDICAO.md`: o topo da faixa de comparação e o topo do gráfico de cada cartão, em px.

**O que muda:**
- **Todos os cartões com o valor grande:** Faturamento Líquido "R$ 165 mil", Positivação "45" e Pedidos Faturados "85" voltam a aparecer.
- **Mesmo padrão em todos:** título, valor, legenda, faixa de comparação e gráfico.
- **Mesmo nível no PC:** a faixa e o gráfico começam na mesma altura em toda a linha. Antes, as linhas 2 e 3 divergiam até 22 px, e o "Desconto comercial" não tinha faixa. Agora fica um espaço reservado, como o PC já desenha.
- **Faixa do topo sem os 3 números** (sua decisão, R-094731): ficam o título, o ⓘ, a data/hora e o DU.
- **Legenda:** aparece só quando traz um número próprio, como "projeção do mês 66" ou "projeção do mês R$ 190 mil". A frase "projeção do mês" sozinha repetia o título "· proj." e saiu.
- **No celular:** um cartão por linha, sem espaço vazio reservado, e o valor não encosta nos anéis.
- **Números:** nenhum é recalculado; o valor vem pronto do PC, o mesmo do farol de origem.
- **Larguras:** 3 cartões por linha a 1366 px e 4 por linha a 1920 px. É a mesma grade de hoje; o print do Alexandre era de uma tela larga.

**Critérios da delegação:**
- só dados fictícios;
- revisor-ux aprovado, com o 🟡 do celular já aplicado;
- design-de-marca aprovado, com o valor em 22 px;
- corretor: RD-0238 a 0241 aplicados, com o reteste em curso;
- revisor de código no head final em curso.

Os PRs saem logo depois da sua aprovação e do reteste, nesta ordem: testes → web 0.10.1. O site atualiza sozinho no deploy do main.
