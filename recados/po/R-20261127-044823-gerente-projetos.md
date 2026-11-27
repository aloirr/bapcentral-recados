---
id: R-20261127-044823-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: pergunta
prioridade: normal
tarefa: T-0045
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T04:48:23-04:00
---
# Simulação da T-0045 (tela Atualizar visitas) para aprovar por delegação

Simulação da T-0045 para aprovação por delegação (R-20261127-013010-alexandre). A tela nova é "Atualizar visitas", dentro do Farol de Visita. As imagens estão em `recados/anexos/T-0045/sim/`, no PC a 1366 e no celular, com dados fictícios e em pt-BR.

| Arquivo | O que mostra |
|---|---|
| 1-admin-agenda-desligada | O admin vê a "Situação" em palavras simples, a última rodada, o botão "Atualizar visitas" e o "Ligar a agenda". O diagnóstico vem fechado. |
| 2-gerente | O gerente vê só o botão "Atualizar visitas" e a situação (4 A). |
| 3-pausa-por-codigo | Quando a Máxima pede confirmação ou captcha, as rodadas pausam. A tela diz o que fazer, mostra o código pequeno "para o suporte" e só o admin vê o "Retomar". Não há print (6 B). |
| 4-cabecalho-farol-visita | O link "Atualizar visitas" no cabeçalho do farol, só para admin e gerente. |

## Condições da delegação
- PNGs no PC e no celular com dados fictícios: sim.
- revisor-ux e marca sem 🔴 nem 🟡 em aberto: `recados/anexos/T-0045/reteste-ux-marca.md`.
- Cores e logo do manual: sim.
- Nenhum documento, telefone ou e-mail na tela, e o lote é recusado se trouxer algum: sim.
- Esta tela não mostra número do Diretor.

## Ainda falta
- O reteste final de código e de redundância, que está em curso.
- O teste que confere se o núcleo e o site decidem igual quem ganha no empate de hora.

Depois disso, os PRs entram na ordem: contrato → rota → web 0.6.0 → testes.

O site só passa a baixar sozinho quando:
1. o Alexandre fizer os passos da Máxima e do Render;
2. o PR de governança do render.yaml e do donos.json for autorizado;
3. a parte do robô (`nuvem/`) estiver pronta.

## Custo
O normal fica entre US$ 1 e 3 por mês. O pior caso, com 8 logins por dia todos os dias, fica em cerca de US$ 7 por mês (ADR 0004 §4). Isso vai ao Alexandre como informe.
