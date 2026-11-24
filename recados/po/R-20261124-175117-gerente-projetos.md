---
id: R-20261124-175117-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: resposta
prioridade: alta
tarefa: T-0017
responde_a: R-20261124-175008-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T17:51:17-04:00
---
# T-0017 começou: ordem, quem faz e previsão da 1ª simulação

## Dados: vêm no pacote do robô?
Não. Hoje o pacote leva só o Painel (resultado e produtividade). Os 4 faróis entram por uma mudança no código do robô (modulo-robo), que é parte da T-0017. Para a SIMULAÇÃO não precisamos do notebook: montamos o farol aqui com as bases congeladas do repositório e desenhamos PC × site com os mesmos dados. Para o NÚMERO REAL no site, sim: depende do robô rodar no notebook (instalação do Alexandre, a mesma espera da T-0013 e da T-0014) e do "instale" do novo bap_automation.py.

## Ordem (um farol por entrega)
1. Inadimplência (leva a base comum: forma "farol" no pacote, desenho genérico no site, menu e perfis) · 2. Pedidos · 3. Entregas · 4. Visita.

## Quem faz (começa agora, em paralelo)
- engenheiro-software: contrato do pacote (forma "farol") e adendo à ADR 0001.
- modulo-robo: o robô separa o farol para o site e manda os cartões por estado prontos.
- modulo-web: site aceita os faróis, desenha cartões/resumo/gráficos (celular 390 px e computador), menu com os 4 itens e perfis novos.
- testes: número PC × pacote (total e um estado, valor × regra). designer-ux: revisão das imagens. revisor-codigo e corretor-redundancias em todos os PRs.

## Previsão (Manaus)
- 1ª simulação (Farol de Inadimplência, PNG PC × site, computador e celular): 25/11 até 12h.
- Pedidos, Entregas e Visita: cerca de 1 dia útil cada depois disso (26, 27 e 30/11).
- Deploy só com "aprovo deploy vX.Y.Z".

## Pendente
As decisões 2, 3 e 4 do R-20261124-174958-gerente-projetos (nomes de vendedor no site, sem tabelas linha a linha, filtro por estado só nos cartões). Sigo com a recomendação "A" nas três, deixando os gráficos com nome de vendedor DESLIGADOS até o "2 A" do Alexandre (liga em 1 linha). Se ele escolher outra opção, ajusto antes da simulação.
