---
id: R-20261127-095354-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: T-0053
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T09:53:54-04:00
---
# T-0053: pedidos a mais vêm da TABELA BAP (provável rajada no ERP); proposta de alerta

T-0053, diagnóstico (só leitura de código e das bases congeladas; nada foi mudado). O detalhe está em `recados/anexos/T-0053/diagnostico.md`, sem dado pessoal.

**Resposta curta:** o farol não inventa nem duplica pedido. Ele mostra uma linha para cada número de pedido em aberto que a TABELA BAP traz. Se o site mostra uns 30 pedidos do "cliente RR-1", então a TABELA BAP (aba `ftPedidos`) tem uns 30 números de pedido diferentes desse cliente em 26/11. A diferença para os "2 que subiram" está no ERP, não no caminho até o site.

**Como o farol monta a tabela:**
- A única fonte é a aba `ftPedidos` da TABELA BAP. Cada linha dela é um item.
- O farol agrupa por filial + número do pedido (`NUM_PEDIDO`) e mostra uma linha por pedido.
- Não há junção com outra base, e por isso não há linha duplicada pelo caminho.
- Descartadas: duas fontes juntas e o número tirado de outra coluna.

**De onde vêm os pedidos a mais (hipótese forte):**
- Na base congelada há o mesmo padrão em outros clientes: rajadas de pedidos iguais criados em poucos segundos.
- Exemplo: um cliente do MA, em 04/11, com 13 pedidos entre 21:43:18 e 21:43:27, os mesmos 3 produtos e o mesmo vendedor, com números pulados. Depois foram excluídos no ERP.
- Isso tem cara de envio repetido pelo app ou pela integração: o vendedor manda 2 e o sistema grava vários.
- Na filial RR, o normal é 1 pedido por dia; 3 no máximo.

**Cartões do topo:** sim, estão afetados. Pedidos, R$, Faturar e Volume somam as mesmas linhas da tabela. Se forem duplicatas, os 4 cartões ficam inflados, e hoje esse cliente domina o farol.

**Outros clientes:** podem ter o mesmo. O farol hoje não detecta nem avisa duplicidade.

**Para confirmar o caso de 26/11:** o pacote real fica só no PC e no servidor, e o time não tem acesso a ele. A conferência mais curta, para o Alexandre ou uma assistente, é de 1 minuto:
1. Abrir `TABELA_BAP.xlsx`, aba `ftPedidos`.
2. Filtrar o código do cliente e a data 26/11.
3. Ver se os pedidos 000241 a 000283 têm os mesmos produtos e quantidades e o horário (`C5_XHORA`) no mesmo minuto.
   - Se sim, é rajada: os pedidos estão duplicados no ERP, e quem resolve é o comercial ou a TI do ERP, excluindo os repetidos.
   - Se não, são pedidos pequenos de verdade.

**Proposta (T-0054, com simulação antes):** o farol passa a apontar "pedidos suspeitos de duplicidade" (mesmo cliente, mesmos itens, criados em poucos minutos) na área de alertas, com regra nova no 03-regras e teste citando a RN. Pergunta ao Alexandre, com recomendação:
- **A (recomendada):** os suspeitos continuam nos cartões, porque o ERP diz que existem, e aparece o alerta com a quantidade e o valor suspeitos. Assim o número do farol continua batendo com o ERP.
- **B:** os suspeitos saem dos cartões e da tabela, e ficam só no alerta.

Se ele disser "segue", vou com a A.
