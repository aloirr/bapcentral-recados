---
id: R-20261127-003955-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: aviso
prioridade: normal
tarefa: T-0033
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T00:39:55-04:00
---
# T-0033: revisão final do código sem 🔴, com 6 🟡 de cor e texto em correção

Parecer do revisor-codigo, registrado pelo gerente-projetos (subagente sem recado próprio, decisão 3 A). Texto: recados/anexos/T-0033/revisao-codigo-final.md.

- Combinado das 8 branches: 609 testes ok + 2 xpassed na suíte geral e 343 ok na web, zero falha.
- RN-VIS-001 é a mesma no PC, no robô e no site, com as bordas 49,99, 50, 79,99 e 80 testadas.
- Aprovados sem achado: RN-VIS-001 (#135), rota, robô, pós-venda (#127) e testes.
- 6 🟡, nenhum 🔴, em correção agora (previsão: hoje até 02h):
  1. o verde-claro #E5F3DF sai do site, do PC e do contrato, e entra o #F0F7EC do manual;
  2. o título da aba do navegador passa a terminar em "BAP AUTOPARTS";
  3. com filtro de estado, o cartão que mostra o número da BAP inteira passa a dizer "BAP inteira".
- Nada disso muda a simulação já enviada (R-20261126-232717). A resposta "1 A" continua valendo.
- Ordem de merge confirmada: pós-venda → rota → robô → contrato → RN-VIS-001 → web → faróis → testes. Os faróis nunca entram antes da web, senão o site recusa o pacote do Farol de Visita.

T-0034, a página inicial: pronta na branch e em revisão de UX e de redundância. A simulação vem a seguir.
