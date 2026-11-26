---
id: R-20261126-181202-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pergunta
prioridade: normal
tarefa: T-0035
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-26T18:12:02-04:00
---
# Status 18h15: T-0024 passa para 00h, T-0035 desenhada e 1 decisão (farol que falha)

# Status 18h15 (Manaus): T-0024 atrasa; T-0035 desenhada; 1 decisão nova

| Frente | Agora | Próxima etapa | Previsão (Manaus) |
|---|---|---|---|
| T-0024 lote 2 (#89, #91, #97) | o designer-ux segurou a simulação: abas que quebram a 1366, Resumo com 12 gráficos que rola, coluna de ação fora da tela, busca com texto errado, aviso de estado contraditório, números fictícios incoerentes; web corrigindo | simulação ao po | **27/11 00h** (era 26/11 22h; motivo: 6 correções antes de mostrar) |
| T-0033 revisão geral | contrato visual BC3 pronto (`.coord/contratos/tela-bc3.md`, branch 04c38e5); web corrigindo marca, grade × popup em todos os faróis, rolagem e celular; botão "Cobrar no WhatsApp" saindo (7 A); PR #127 (marca na cobrança) aprovado pelo revisor, entra junto | simulação ao po | 27/11 03h (mantido) |
| Manual da marca | design-de-marca refazendo sobre o manual do bapajuda (R-20261126-180414) | prancha com as lacunas para você levar ao Alexandre | 26/11 21h |
| T-0035 pacote por farol | ADR 0003 e contrato §10.8 prontos (branch e97761f); web (v0.4.0) e robô começaram | PRs (sem tela, só o selo "Desatualizado" em PNG) | 27/11 14h (mantido) |
| #126 correção do celular | aprovado pelo revisor, CI verde | merge com o seu "ok" (R-20261126-180502) | — |
| #82 e #97 testes | atualizando com o main; a suíte regravava uma base congelada (RELATORIOS/painel_diretor_hist.json) e vazou no #127 (já corrigido); testes isolando | merge | 26/11 20h |

## Decisão nova (ADR 0003, §4.4)
1. Quando o envio de um farol falha na rodada: (A) o site mostra os dados da rodada anterior por até 26 h, com o selo "Desatualizado" no farol; depois disso, o farol mostra "Sem dados" · (B) o site mostra "Sem dados" assim que a rodada falha.
Recomendo A. Resposta pronta: "1 A".
