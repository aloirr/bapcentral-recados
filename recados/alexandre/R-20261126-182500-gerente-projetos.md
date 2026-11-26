---
id: R-20261126-182500-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: normal
tarefa: T-0033
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-26T18:25:00-04:00
---
# Pausa confirmada (18h30): #126 no main, ponto seguro e heads de cada frente

# Pausa confirmada (26/11 18h30): ponto seguro e passagem para a retomada das 22h30

Pedido: R-20261126-182227-alexandre ("Agora pause e volte apenas as 22:30hs").

## Feito antes de pausar
- **#126 no main** (4e1abd8): no celular, os botões do cabeçalho quebram linha e o menu do Exportar abre inteiro. Merge com o "ok" do Alexandre, CI verde e revisor aprovado.
- **Quadro em dia:** PR do gerente com a pausa e as linhas das T-0024, T-0026, T-0032 a T-0035. Merge assim que o CI passar.
- **Ronda apagada.** A retomada está agendada para 22h30 (02h30 UTC).
- **Subagentes parados,** com o trabalho em branch (push feito). Não houve sessão filha.
- **Nada instalado em PC.**

## Onde cada frente parou (heads)
| Frente | Branch / PR | Head | Falta |
|---|---|---|---|
| T-0033 web | modulo-web/T-0033-revisao-geral (WIP, sem PR) | f42ee18 | atualizar 23 testes; aplicar os tokens do manual aprovado; refazer e conferir os PNGs; reteste UX → simulação ao po |
| T-0033 contrato BC3 | engenheiro-software/T-0033-contrato-bc3 | 04c38e5 | PR junto da web |
| T-0033 manual da marca | design-de-marca/T-0033-manual-marca | c8c60fc | tirar "RASCUNHO" (aprovado 1 A…9 A) e abrir PR |
| T-0033 marca na cobrança | PR #127 | aa3fc77 | aprovado pelo revisor; entra com a simulação da T-0033 |
| T-0024 web | PR #89 | 34c07e9 | reteste do designer-ux → simulação ao po |
| T-0024 robô | PR #91 | 9753598 | vc_base por UF; Planner sem recorte, com aviso; revisor |
| T-0024 testes | PR #97 | 034ce39 | verde no combinado com o #91 (525 testes); smoke a terminar; merge depois do #91 |
| T-0026 testes | PR #82 | c9a9343 | caso positivo pedido pelo revisor feito; CI e revisão nesse head |
| T-0035 contrato | engenheiro-software/T-0035-pacote-por-farol | e97761f | PR |
| T-0035 web (v0.4.0) | modulo-web/T-0035-pacote-por-farol | 527004f | prova ponta a ponta; revisor |
| T-0035 robô | modulo-robo/T-0035-pacote-por-farol | 5231f19 | achados do testes: teto dos anexos (parcial > 3 MB derruba o farol), corte do Entregas acima de 8 MB, `_CORTES_FAROL_WEB` sem uso, selo só depois de 26 h |
| T-0035 testes | testes/T-0035-pacote-por-farol (WIP) | b116d1f | 4 combinações ponta a ponta, memória no /saude |

## Decisões recebidas de 18h22 (aplicar na retomada)
- ADR 0003 §4.4 = A (rodada anterior até 26 h, com o selo "Desatualizado").
- O verde do BapAjuda (R-20261120-115646) vale aqui.
- Manual da marca: as 9 lacunas = A.

## Na retomada (22h30)
Refazer as previsões e mandar ao po em tabela antes de seguir.
