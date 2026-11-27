---
id: R-20261127-105222-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0052
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T10:52:22-04:00
---
# T-0052 entregue: Painel Executivo com o valor em todos os cartões (web 0.10.1)

**T-0052 entregue: o Painel Executivo no site, com o valor grande em todos os cartões, no mesmo padrão e no mesmo nível.** O merge foi feito (#181, testes, 66b0d95; #182, web 0.10.1, a86aa85). O site atualiza sozinho com o deploy do main, em poucos minutos. Na ronda, eu confiro se o /saude dá 0.10.1.

**O que mudou:**
- O Faturamento Líquido, a Positivação e os Pedidos Faturados voltam a mostrar o valor grande no cartão.
- Todos os cartões seguem a mesma estrutura: título, valor, legenda, faixa de comparação e gráfico. No PC, a faixa e o gráfico começam na mesma altura em toda a linha.
- A faixa do topo fica sem os 3 números. Ficam o título, o ⓘ, a data e o DU.
- A legenda só aparece quando tem número próprio, como "projeção do mês 66".
- No celular, um cartão por linha, sem espaço vazio.

**Como testar em 5 passos:**
1. Abra o site e entre (qualquer perfil que veja o Painel Executivo).
2. Na aba **Resultado**, confira se o Faturamento Líquido, a Positivação e os Pedidos Faturados mostram o valor grande.
3. Compare os números com o Painel Executivo do PC (mesmo horário de dados). Eles têm de bater, porque a web não recalcula nada.
4. Na mesma linha de cartões, confira se as faixas "out / set / jul" e o começo dos gráficos estão na mesma altura. Faça o mesmo na aba **Produtividade**.
5. No celular, abra o Painel: um cartão por linha, sem espaço verde vazio, com o valor sem encostar nos anéis.

**Revisões no head final:**
- revisor de código sem 🔴 nem 🟡 de código;
- revisor-ux reconfirmado no 73dbbbe;
- design-de-marca aprovado (22 px, só tokens);
- corretor: RD-0238 a 0241 fechados.

**Fica para depois (🟢):** no recorte por estado no PC, o cartão ainda estica até encher a tela.
