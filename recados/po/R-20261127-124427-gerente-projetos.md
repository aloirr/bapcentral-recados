---
id: R-20261127-124427-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0053
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T12:44:27-04:00
---
# T-0053 entregue: Farol de Pedidos com o cliente da loja certa (RN-GER-019)

**No main:** #180 (RN-GER-019, a042d7c), #186 (faróis, 1ca269b), #188 (testes, dca49a7). Revisor de código e corretor aprovados em cada head; CI verde. Fretes, Entregas, Devoluções e Saldo saem idênticos ao main de antes. Sem tela nova (UX e marca aprovados antes).

**Como testar em 5 passos:**
1. No PC, abrir o Farol de Pedidos (depois do "instale" ou da rotina das 06h30 com o código novo).
2. Escolher um pedido de cliente com loja em mais de uma filial: nome, fantasia, cidade e crédito vêm da loja da filial do pedido.
3. Um pedido de cliente sem cadastro na filial aparece como antes e, sem crédito apurado, entra em "crédito a analisar" como "Saldo Não Apurado" (P1 A).
4. Conferir os cartões e o filtro por estado: os números não mudam.
5. Abrir Fretes, Entregas, Devoluções e Saldo: tudo igual ao de antes.

**Para depois (🟢, sem pressa):** a aba "Por cliente" dos excluídos agrupa por "código - nome"; a consulta de pedido passou a mostrar o nome da loja também em Entregas, Fretes e Devoluções. O po confirma se está ok.
