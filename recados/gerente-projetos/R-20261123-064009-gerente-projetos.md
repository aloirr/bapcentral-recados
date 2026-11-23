---
id: R-20261123-064009-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: aviso
prioridade: normal
tarefa: T-0003
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-23T06:40:09-04:00
---
# T-0003: fim do lote no Cowork — #20 e #21 no main, tarefa concluída; quadro atualizado (#24)

Sessão BAPCentral - Cowork (gerente-projetos), 23/11/2026. Sem os guardiões do Claude Code.

## PRs (squash, nesta ordem)
| PR | Dono | Head revisado | Commit no main | O que muda |
|---|---|---|---|---|
| #20 | engenheiro-software | 1020bdc | cf4eca6bc77bb3594b66704d869ab2bee8907062 | `ATUALIZAR_DO_GITHUB.bat` + `atualizar_do_github.py` (zip do main ou `--origem`; backup `ANTES_<ASSUNTO>_<MÊS><ANO>` por hash; troca atômica só de `.py`/`.bat` da raiz; trava "instalado por fora"; `--simular`) e `docs/desenho/T-0003.md` (vindo do branch ba12136, com o status atualizado; commit novo neste lote) |
| #21 | testes | 7abe5e9 | d0a518bcc75e064bed5ca0799170f431eeb8618e | 19 testes `test_T0003_*` em pasta de mentira |
| #24 | gerente-projetos | 62ad1c2 | d32a454f7e0409c420b19aada1efc66e7a4dda3a | quadro, T-0003 (concluída), T-0010 (aguardando o "instale") e diário |

Pareceres: R-20261123-063245-revisor-codigo (#20 e #21, aprovados com 3 🟢) e R-20261123-063910-revisor-codigo (#24, aprovado). CI `conferir` verde nos três heads; `verificar` e `governanca` OK.

## Testes rodados (cópia na nuvem, Python 3.12)
- `compileall` ok; `pytest tests/` no main d0a518b: 90 passed; doctest do `atualizar_do_github.py` ok.
- Ensaio do instalador numa pasta de mentira (cópia do main db187d8 como produção): `--simular` lista 2 alterados e 2 novos sem gravar; a execução real faz o backup `ANTES_T0010_NOV2026` e troca 4 arquivos com o hash conferido; a segunda simulação diz "Nada a fazer".
- Só no CI: nada a mais (o CI não roda pytest; T-0004).

## O que falta
- Primeiro uso no PC: só com o "instale" do Alexandre, depois de um `--simular` na pasta de produção ("Regionais - Leandro"), que ainda não está ligada a esta sessão. Ler a lista: se aparecer `.bat` alterado só por final de linha (🟢 1 do parecer), decidir antes de trocar.
- O "instale" leva junto a T-0010 (`bap_dados.py` e `relatorios_nucleo.py`).
