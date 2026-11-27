---
id: R-20261127-095858-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: T-0053
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T09:58:58-04:00
---
# T-0053: a visão do estado bate com a TABELA BAP; a visão BAP põe o nome da loja errada (correção em curso)

T-0053, diagnóstico revisto: é defeito do farol, na atribuição do cliente. O detalhe está em `recados/anexos/T-0053/diagnostico.md`.

**Qual visão bate com a TABELA BAP: a do estado (filtro RR).** O pedido é identificado pela filial da nota + número + código do cliente, e o filtro por estado usa a filial da nota, que é o certo.

**Por que a visão BAP mostra outros pedidos com o nome do cliente RR-1:**
- A aba de pedidos da TABELA BAP traz só o código do cliente, sem a loja.
- O cadastro guarda uma loja só por código: a de maior limite.
- Por isso o pedido de outra loja do mesmo código, em outra filial, ganha o nome, a UF, a cidade e o limite do cliente RR-1.
- Na base congelada, 172 códigos têm mais de uma loja, e 58 deles têm lojas em estados diferentes.

**Cartões do topo:**
- Pedidos, R$, Faturar e Volume contam certo, tanto no total da BAP quanto por estado.
- O que sai errado é a quem o pedido é atribuído: nome, UF, cidade e o limite usado na análise de crédito. Isso afeta o "Crédito a analisar".

**A rajada de pedidos iguais** (meu recado das 09h53) pode existir ao mesmo tempo, mas não explica a diferença entre as visões.

**Correção (já em andamento, com simulação antes):**
- O modulo-farois cria a regra "o pedido pega os dados da loja do código cuja UF é a filial do pedido".
- Sem uma loja única nessa UF, o pedido não herda dados de outra loja.
- A regra nova é a RN-GER-019, com teste.
- Mando a simulação (PC e site, dados fictícios) para você aprovar por delegação.
- **A longo prazo:** trazer a loja (`D2_LOJA`) do ERP na aba de pedidos, que é do engenheiro-dados. Fica como tarefa seguinte, se ele aprovar.

**Previsão da simulação:** umas 11h30 de Manaus.

**Conferência opcional (1 minuto, para o Alexandre ou uma assistente):** na TABELA BAP, aba `ftPedidos`, ver a FILIAL dos pedidos 000241 a 000283. Se não for RR, está confirmado.
