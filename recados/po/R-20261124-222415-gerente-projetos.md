---
id: R-20261124-222415-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: alta
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T22:24:15-04:00
---
# T-0017: simulação dos Faróis de Pedidos, Entregas e Visita no site (dados fictícios) — aprovação

## Simulação ("Simule" = mostrar antes)
12 imagens em recados/anexos/T-0017/tres-farois/ — sim5-pedidos, sim5-entregas, sim5-visita; -pc (computador) e -cel (celular), tela inicial e -inteira (página toda). Dados FICTÍCIOS (Vendedor NN), conferidos pelo designer-ux e por varredura automática; nada passa da largura da tela no celular.
- Pedidos: cartões em faixa como no PC, Resumo e gráficos; filtro por estado (filial da nota). Sem autorização de venda no site.
- Entregas: cartões, gráficos e a tabela de frete por estado (UF, notas, valor, frete R$, % sobre a nota), com total; filtro por estado pela UF do cliente (RN-GER-006). Sem edição no site.
- Visita: cartões e gráficos (horários em hh:mm, tempos em min); sem filtro por estado (a base de visitas não traz a UF do cliente), com o aviso "Sem filtro por estado: os cartões mostram a BAP inteira."
- Os 3 com "Baixado do ERP em", no horário de Manaus.

## Junto
- Correção da regra 4 no PC e no site: o Farol de Visita deixa de contar HOJE como dia útil sem arquivo; e a data de hoje passa a ser a de Manaus mesmo fora do PC.
- Conferência PC × pacote (número bate com o farol do PC, valor × regra) com o testes em seguida, antes dos PRs.

## Decisão para o Alexandre (resposta pronta "N X")
1. Simulação dos 3 faróis: (A) aprovada, abrir os PRs (robô, site, faróis, testes); (B) ajustar antes (diga o quê). Recomendo A. Resposta: "1 A".

## Depois do 1 A
PRs no main 25/11 até 12h; o site publica sozinho no merge; os números aparecem quando o robô novo rodar na pasta de produção (T-0018).
