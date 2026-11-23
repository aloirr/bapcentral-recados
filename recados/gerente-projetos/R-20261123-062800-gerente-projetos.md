---
id: R-20261123-062800-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: aviso
prioridade: normal
tarefa: T-0010
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-23T06:28:00-04:00
---
# T-0010: fim do lote no Cowork — #14, #23 e #13 no main; falta só o "instale"

Sessão BAPCentral - Cowork (gerente-projetos), 23/11/2026. Sem os guardiões do Claude Code (ver R-20261122-182900-alexandre e R-20261122-183000-alexandre).

## PRs (squash, nesta ordem)
| PR | Dono | Head revisado | Commit no main | O que muda |
|---|---|---|---|---|
| #14 | engenheiro-dados | a2a3d48 | 646ff3ca5773ab2e74e820f1ce33cd483c3bb0b3 | `bap_dados._bloco_base` grava `visita_semanal` em cada visita; marca do bloco "base" b4 → b5; VERSAO 27 |
| #23 (novo) | modulo-farois | a5d8766 | ce93876b19ac30ceae1b415e6d17ca15a0b14167 | `relatorios_nucleo._exportar_protheus_da_rota` passa `VISITA_SEMANAL` ao gerador: o semanal exportado pelo Farol sai com periodicidade 7 (critério 4 da T-0010, que estava aberto: o #14 gravava o campo, mas ninguém o lia) |
| #13 | testes | aa5d44f | b45b9d84afe7362e29bef8d2d200eec46d8b1eeb | testes da exportação sem o skipif (🟡 resolvido) e teste novo `test_RN_ROT_001_farol_repassa_visita_semanal_com_7` (falha sem o #23) |

Pareceres: R-20261123-062351-revisor-codigo (os três aprovados no head). CI `conferir` verde nos três heads. `verificar` e `governanca` OK nos três.

## Testes rodados (cópia na nuvem, Python 3.12)
- `compileall` ok; `pytest tests/` no main b45b9d8: 51 passed.
- `smoke_relatorios.py`: sem FALHA; para nos contatos (falta `contatos_vcf.py`, conhecida).
- `smoke_processos.py`: 4 falhas, iguais às do main db187d8 (antes deste lote): ftPedidos (conhecida) e 3 da rota fora da lista de conhecidas. Pedido ao testes no R-20261123-062830-gerente-projetos.
- Só no CI: nada a mais (o CI não roda pytest; T-0004).

## O que falta
- T-0010 fica em `aguardando_alexandre`: o "instale" no PC (pasta "Regionais - Leandro"), que depende do instalador da T-0003 (PRs #20 e #21, próximo lote).
- Quadro e `.coord/tarefas/T-0010.md`: vão no PR do gerente-projetos deste período (junto com a T-0003, para economizar Actions, R-20261120-101025-alexandre).
- `docs/revisao/T-0010.md`: o parecer está no recado; o arquivo vai num PR do revisor-codigo no fim da sessão.
- Título "[PRONTO PARA MERGE]": não usado, porque o merge foi feito logo depois do parecer, pela mesma sessão.
