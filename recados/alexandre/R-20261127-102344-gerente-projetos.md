---
id: R-20261127-102344-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: normal
tarefa: T-0053
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T10:23:44-04:00
---
# T-0053: simulação da correção (cliente certo no pedido) para aprovar + P1 do crédito

**T-0053 (Farol de Pedidos): simulação da correção para você aprovar por delegação.**

**Simulação** (dados fictícios: o código 900001 tem a loja RR, com limite de 20 mil, e a loja AM, com 80 mil): `recados/anexos/T-0053/sim/`
- `pc_antes_visao_BAP.png`: o pedido da filial Boa Vista aparece como a "LOJA AM", com AM, Manaus, limite 80.000 e saldo 60.000. É o defeito do print.
- `pc_depois_visao_BAP.png`: o mesmo pedido aparece como a "LOJA RR", com RR, Boa Vista e limite 20.000. Os pedidos das filiais de Manaus continuam como a "LOJA AM".
- `pc_*_recorte_RR.png`: no recorte RR, o número de linhas é o mesmo; só o cliente certo aparece.
- O site mostra as mesmas células do pacote, então herda a correção sem código novo.

**A regra (RN-GER-019, texto no PR de regras):**
- No pedido, nome, UF, cidade, limite e saldo vêm da loja do código cuja UF é a da filial do pedido.
- Código com uma loja só usa essa loja, mesmo quando compra em outra filial. Assim o cliente de AM que compra em RR não perde nome e limite.
- Sem uma loja única na UF da filial, o pedido não herda dados de outra loja. A UF é a da filial, e o nome vira "(loja não identificada)" se as lojas daquela UF tiverem nomes diferentes.
- **Os cartões e o filtro por estado não mudam:** contam pela filial do pedido.

**Pergunta ao Alexandre, com recomendação (o padrão vale até a resposta):**
- **P1:** hoje o robô só traz o saldo e o atraso da loja de maior limite de cada código. Para as outras lojas, o que a análise de crédito mostra?
  - **A (recomendada e padrão):** "Crédito não apurado", que entra em "Crédito a analisar". É honesto: não afirma "Sem Limite" nem herda o crédito de outra loja. Na base congelada, isso atinge só os códigos com mais de uma loja (172 de 4.154).
  - **B:** como hoje, com o saldo da loja de maior limite. É mais "limpo" na tela, mas pode liberar crédito com o saldo de outra loja.

**Próximo passo, de dados (tarefa à parte, engenheiro-dados):** o robô passar a trazer a loja do pedido (`D2_LOJA`) e o saldo por loja. Aí acaba a adivinhação pela UF e o "Crédito não apurado".

**Critérios da delegação:** dados fictícios ✅. Revisões de código e de redundância e os testes da RN estão rodando agora. Os PRs saem depois da sua aprovação, nesta ordem: regras → testes → faróis.
