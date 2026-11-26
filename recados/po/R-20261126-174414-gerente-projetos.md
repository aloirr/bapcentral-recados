---
id: R-20261126-174414-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: normal
tarefa: T-0032
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-26T17:44:14-04:00
---
# Retomada 26/11: triagem dos 13 PRs, plano e previsões

# Retomada 26/11 (17h40): plano e previsões do gerente

Lidos os recados de 25 e 26/11 e a passagem completa (R-20261126-173917-po). Conferência dos 33 commits do Cowork (42a020e..c8f6004) com o `verificar --por-commit`: nenhuma violação de dono. Dois squashes juntaram vários donos num PR só (#112 T-0021 e #116 T-0029): registrado, sem ação.

## Triagem dos 13 PRs abertos
| PR | Tarefa | Situação | O que faço |
|---|---|---|---|
| #124 | T-0032 botões das parciais e "Cobrar no WhatsApp" | CI verde, sem conflito, só web | simulação PNG (regra 10) + revisor-codigo + revisor-ux → merge |
| #82 | T-0026 testes das parciais | verde, 22 commits atrás | atualizar com o main → merge |
| #89, #91, #97 | T-0024 faróis do lote 2 (web, robô, testes) | 20 atrás, conflitos pequenos | atualizar com o main; web no BC3 → simulação → merge na ordem robô+testes juntos, web |
| #102, #103, #105, #106 | T-0023 Garantias, Devoluções, NCC | empilhados na T-0021 v1, que nunca entrou (a v4 entrou) | refazer sobre o main (branches -v2) com as decisões de 26/11; fechar os 4 antigos |
| #93, #98, #100, #107 | T-0025 DDR, Campanhas, Expositores | idem; #107 ainda põe TOTAL A PAGAR para vendas (contra a decisão de 26/11) | refazer sobre o main (-v2): diretor só Resumo, TOTAL A PAGAR só admin/gerente/diretor, champions_config.json pela web só admin gravado pelo robô; fechar os 4 antigos |

## Previsões (Manaus)
| Frente | Próxima etapa | Previsão |
|---|---|---|
| #124 T-0032 | PNG antes/depois ao po | 26/11 19h00; merge após o "ok" |
| #82 T-0026 | merge | 26/11 19h00 |
| T-0024 (#89, #91, #97) | simulação BC3 dos 5 faróis do lote 2 | 26/11 21h00; merge após a aprovação |
| Ajuste fino grade × popup por farol (passo 2) | simulação por farol | 26/11 22h30 |
| Painel Executivo e Usuários/Senha no BC3 (passo 3) | simulação | 27/11 01h00 |
| T-0023 e T-0025 refeitos sobre o main (passo 4) | simulação | 27/11 06h00 |
| Fretes (passo 5) | próxima leva | — |
| Quadro e fichas T-0019..T-0032 (o Cowork não atualizou) | PR do gerente | 26/11 19h30 |

Rondas de 20 min reagendadas. Subagentes em Opus 5.5 médio.
