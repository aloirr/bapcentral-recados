---
id: R-20261125-175200-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: entrega
prioridade: normal
tarefa: T-0020
responde_a: R-20261125-174000-alexandre
encerra: false
contrato: null
criado_em: 2026-11-25T17:52:00-04:00
---
# T-0020 entregue no PR #79: faróis da web no visual C, sem repetições e com as tabelas de baixo lado a lado

## O que foi feito (só web/, dono modulo-web)
- Visual C: logo e cores da BAP AUTOPARTS, um só estilo de abas e filtros, sem borda pesada, barras nas cores da BAP.
- Juntas lado a lado (Pedidos: Gerar ID CD, Reversa de lojas, Analítico; Entregas: Pendências), rolagem própria de até 420 px.
- Repetições: cartão só com "—", frase do resumo cujos números já estão todos nos cartões, título com a aba, rótulo Estado (farol e Painel), RAZÃO SOCIAL com FANTASIA preenchida, "Baixado do ERP" a até 60 min do pacote, bloco que a web não desenha.
- Testes: 228 passed; revisor-codigo aprovou o head c10cff5 (um 🔴 e dois 🟡 da 1ª rodada corrigidos).
- Pendência anterior: a aba Cobrar no WhatsApp passa 21 px da tela a 390 px (já passava no main).

## Como testar em 5 passos
1. Entre no site (bap-central.onrender.com) depois do deploy do #79.
2. Abra Farol de Pedidos > Pedidos: as três tabelas de baixo aparecem lado a lado (a mais larga desce para a linha de baixo).
3. Confira o cabeçalho com o logo verde da BAP e as abas, filtros e subabas no mesmo estilo cinza-verde.
4. No Resumo de cada farol, veja que nenhuma frase do resumo só repete o número de um cartão e que não sobra cartão com "—".
5. Abra no celular: nada passa da largura da tela, fora a aba Cobrar no WhatsApp (pendência anterior).
