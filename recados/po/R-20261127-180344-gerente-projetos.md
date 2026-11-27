---
id: R-20261127-180344-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: T-0060
responde_a: R-20261127-180253-alexandre
encerra: false
contrato: null
criado_em: 2026-11-27T18:03:44-04:00
---
# T-0060 aberta: Painel Executivo × Farol de Pedidos

Autorização: pedido escrito do Alexandre em R-20261127-180253-alexandre.

## Escopo
1. Pedidos: o Painel mostra 80 pedidos projetados e o Farol de Pedidos, 136 pedidos no mês até 27/11. A projeção não pode ficar abaixo do real. Achar o universo ou a contagem que diverge (nota × pedido, filtros, CNPJs internos, conta 000040) e alinhar ao farol de origem.
2. Cartão Resumo: o "Real" (R$ 146.673) conta hoje, mas a projeção (R$ 145.311 = real até 26/11 ÷ 17 DU fechados × 19 DU) não conta. Pela regra 4, o real usado na projeção é o dos DU fechados. O cartão precisa deixar claro, lado a lado, o real até ontem e o de hoje, sem a projeção parecer menor que o real.
3. Os defeitos que a revalidação do Gerente Sênior achar (session_0157qAhjTRckoEzNToBU7oDb), com arquivo e função.
4. Testes com a RN citada; o número do Diretor tem de bater com o farol de origem.

## T-0058 cobre parte?
- Não cobre a divergência principal: o faturado total é o mesmo nos dois (R$ 146.673).
- A T-0058 corrige o faturado por estado (devolução pela vista). Ela só melhora o Painel na quebra por UF, se o Painel usar a mesma função.

## Dono e previsão (Manaus)
- Dono: modulo-farois, na mesma sessão da T-0058, sem sessão nova. Testes no testes. Revisões: revisor-codigo, corretor-redundancias, revisor-ux e design-de-marca (é tela do Diretor).
- Diagnóstico, só leitura: começa agora e cruza com a revalidação do Gerente Sênior às ~19:15.
- Simulação (PNG 1366/390, antes × depois, com valor × regra): 21:00.
- PRs: 22:00. Merge: 22:30, com a aprovação da simulação e o CI verde.
- Instalação: pela rotina das 06h30 de amanhã. Sem "instale", porque só mexe em .py da raiz.
