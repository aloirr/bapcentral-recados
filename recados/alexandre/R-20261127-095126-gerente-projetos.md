---
id: R-20261127-095126-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: T-0053
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T09:51:26-04:00
---
# T-0053: pedidos a mais no Farol de Pedidos, diagnóstico em andamento

T-0053 aberta: os pedidos a mais do "cliente RR-1" no Farol de Pedidos do site. Recebi o R-20261127-095026-alexandre.

**Em andamento:** o modulo-farois investiga, só lendo o código e as bases congeladas. Vai responder:
1. De onde o farol tira as linhas e o número do pedido. Uma linha é um pedido ou um item? Há alguma junção que multiplica linhas?
2. As hipóteses:
   - o ERP quebra um pedido em vários números;
   - duas fontes juntadas (ex.: pedido + TABELA BAP);
   - o número sai de outra coluna;
   - entram pedidos que não são venda (bonificação, troca ou garantia).
3. Como cruzar com a TABELA BAP, pedido a pedido.
4. Se os cartões do topo (Pedidos, R$, Faturar, Volume) ficam inflados.
5. Se outros clientes têm o mesmo padrão.

**Limite:** o pacote real das 09h39 está só no servidor do site, e o time não acessa dado real de lá. A comparação pedido a pedido com a TABELA BAP do mesmo horário talvez precise de um passo do robô ou de um print do Alexandre (sem nome do cliente). Se for o caso, o diagnóstico diz exatamente qual é o passo, com o mínimo de trabalho para ele.

**Previsão do diagnóstico:** umas 10h40 de Manaus. Se precisar mudar código, faço simulação antes (regra 10) e peço a sua aprovação por delegação.
