---
id: R-20261125-034226-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: aviso
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-25T03:42:26-04:00
---
# Pausa confirmada (25/11 03h50): passagem do gerente para a outra conta

# Passagem do gerente-projetos (pausa de 25/11 03h50, Manaus) — para o gerente da outra conta

Pedido: R-20261125-034012-alexandre ("Pause e deixe recado vou continuar da outra conta"). Complementa a passagem do po (R-20261125-034013-po).

## Ponto seguro
- Nada instalado em PC. Nenhum merge pela metade. Rondas do gerente apagadas. Subagentes parados (não houve sessão filha para arquivar).
- PR aberto: **#68** (só quadro e ficha da T-0017, sem código). Se o CI estiver verde, o gerente da outra conta faz o squash; se não, o merge fica para ele.
- main: `ae1d6e2` (#67). Site v0.2.0 no ar, deploy automático a cada merge.

## T-0017 — abas de Pedidos, Entregas e Visita no site (pronto em branch, sem PR)
| Branch | Head | Dono |
|---|---|---|
| engenheiro-software/T-0017-abas-tres-farois | 1b3d902 | contrato §10.7 e adendo 5 da ADR 0001 |
| modulo-farois/T-0017-hoje-fora-du | 6adc32d | funções puras (RN-GER-011) e hoje fora do DU |
| modulo-robo/T-0017-tres-farois | 189bb4d | tabelas no pacote web |
| modulo-web/T-0017-tres-farois | b791a43 | web v0.3.0 |
| testes/T-0017-testes-tres-farois | 72e45a5 | testes e conferência valor × regra |
| gerente-projetos/T-0017-rn-ger-011 | 730643e | RN-GER-011 no doc 03 |

- Provas: suíte combinada (as 6 juntas) 682 ok / 0 falha; pacote real das bases congeladas aceito pela web (1,76 MB; 0 CPF/CNPJ/e-mail); 25 cartões iguais ao PC; Entregas por UF iguais ao PC.
- Simulação sim6: R-20261125-025823-gerente-projetos, PNGs em `recados/anexos/T-0017/abas/` (dados fictícios). designer-ux sem 🔴 no reteste.
- Desenho e pareceres (revisão prévia, RD-0017 a RD-0031, UX): `recados/anexos/T-0017/abas/pareceres/`.

## Próximos passos (na ordem)
1. Alexandre: simulação sim6 + D1–D6 (R-20261125-021827). Resposta pronta: "1 A; D1 A, D2 A, D3 A, D4 A, D5 A, D6 A". Se vier B/C em algum D, ajustar antes.
2. Reteste do revisor-codigo e do corretor-redundancias nos heads acima (estava em curso; foi interrompido pela pausa). designer-ux confere o total fixo e o aviso "Cartões sem filtro. Com filtro, veja as linhas na tabela."
3. PRs (um por dono), merge na ordem: contrato → farois → testes → web → robô, mais a RN-GER-011. Robô antes da web derruba o pacote inteiro. A web v0.3.0 vai ao ar sozinha no merge; o robô novo só chega à produção pela rotina diária (T-0018).
4. Tarefas à parte: cobrança usar `relatorios_nucleo.sem_documento` (modulo-posvenda); tela do PC usar `solicitacao_bap.tipos_colunas` (modulo-farois); RD-0030; RD-0031; RD-0014.

## T-0018
Aguarda as 5 decisões do plano de migração para a pasta pessoal (R-20261124-215228-gerente-projetos). Nada instalado.

## Cuidados para o gerente da outra conta
- As branches dos subagentes já estão no origin; não dependem desta sessão. A pasta temporária desta sessão se perde: o que importa está nos recados e nas branches.
- Pareceres de subagente: o `coord.mjs` só aceita `--de` igual ao BAP_AGENTE; o gerente grava com nota de origem (3 A).
- send_message ao po não funciona desta sessão; o canal é o recado.
- Sobre a pendência citada na passagem do po (nomes de clientes no R-20261124-212002): a linha foi trocada no commit acc7525 do repositório de recados (2 A, sem reescrever histórico). Conferir.
