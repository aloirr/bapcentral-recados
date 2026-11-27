---
id: R-20261127-095502-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: T-0053
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T09:55:02-04:00
---
# T-0053: nova hipótese (pedidos de outra filial com o nome do cliente RR-1)

Complemento do R-20261127-095245-alexandre recebido. Isso muda a hipótese da T-0053, e o meu diagnóstico das 09h53 (rajada no ERP) fica suspenso.

Como o filtro RR mostra só o pedido 000109 e a visão BAP mostra os 000241 a 000283 para o "mesmo" cliente, a hipótese principal agora é esta: esses pedidos são de outra filial. Na visão BAP, eles ganham o nome do cliente RR-1 por uma junção com o cadastro feita só pelo código do cliente, sem a filial ou a loja.

Se for isso, é defeito do farol, e a visão por estado (filial da nota) é a que bate com a TABELA BAP.

O modulo-farois está conferindo agora:
- qual visão bate com a TABELA BAP, pedido a pedido;
- a causa no código;
- se os cartões estão afetados;
- quantos outros clientes e filiais têm o mesmo problema.

Previsão: umas 10h25 de Manaus. A correção vai com simulação antes.
