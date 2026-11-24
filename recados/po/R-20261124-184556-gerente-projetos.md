---
id: R-20261124-184556-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:45:56-04:00
---
# Pareceres: PR #50 a88209b aprovado (RD-0016 fechado); PR #52 95c1cd5 aprovado

> Pareceres do revisor-codigo, com a checagem de redundância (subagente do gerente-projetos; gravados pelo gerente sem alteração, pela limitação do --de no coord.mjs).

# Revisão 3 — PR #50 — T-0017 Farol de Inadimplência sem CNPJs internos
- Branch: modulo-farois/T-0017-inadimplencia-internos
- Head SHA revisado: a88209b8b9ae0c763a2f1ae14fa7a3762dfb3196 (antes 5ef155b; base origin/main 0605f8b)
- Revisor: revisor-codigo (também a checagem do corretor-redundancias) · 24/11/2026

## Veredito: APROVADO (sem 🔴 nem 🟡)

Conferido:
- A correção: o diff contra o main é só `relatorios_nucleo.py` (+3 linhas). O ramo `"inadimplencia"` do `_sem_internos` (linhas 743-745) chama `bd.titulos_sem_internos(bloco.get("titulos"))`. A cópia local foi apagada, e `git grep` acha só uma `def titulos_sem_internos`, a de `bap_dados.py:1427`.
- O 000040 não é filtrado: a fonte única usa só `_interno(nome, fantasia)`. O teste `test_RN_GER_005_cliente_000040_continua_no_farol` passa.
- RN-GER-004: os CNPJs internos (BAP AUTOPARTS / FRW / PMZ DISTRIBUIDORA) saem por `bd._interno`. O filtro roda depois do cache.
- `bap_dados.VERSAO = 27`: o PR não toca no `bap_dados.py` e não muda o cache, então não precisa de marca nova.
- Testes no head: `pytest tests/ -q` dá 153 passed. O teste do scratchpad `test_T0017_inadimplencia_internos.py`, copiado para uma pasta temporária, dá 3 passed. O `compileall` passa.
- `verificar modulo-farois --base origin/main`, rodado num worktree do head: OK, 1 arquivo (`relatorios_nucleo.py`), nenhuma violação.
- Dados digitados e configs: intocados. Nenhum segredo no diff.

## Redundância (corretor-redundancias)
- RD-0016: fechado. Não ficou cópia da função: a regra mora só em `bap_dados.titulos_sem_internos`, usada nas fotos (`bap_dados.py:1473`) e no farol (`relatorios_nucleo.py:744`).
- Nenhuma duplicação nova: o ramo novo segue o padrão dos ramos vizinhos do `_sem_internos`.

## 🟢 Sugestões
1. O merge commit `c8d096f` ("Merge origin/main em T-0017") está sem o trailer `Agente: modulo-farois`. Os outros 3 commits têm o trailer, e o squash resolve no merge.
2. Continua a 🟢 anterior: hoje o interno é detectado só pelo `E1_NOMCLI`. Se um dia for reusar os códigos de `bloco["internos"]`, fazer na fonte única.

---
# Revisão — PR #52 — T-0017 web v0.2.0
- Branch: modulo-web/T-0017-versao-0.2.0
- Head SHA revisado: 95c1cd578920d18fbb0b042cb523da25bc6168c2 (base origin/main 0605f8b)
- Revisor: revisor-codigo (também a checagem do corretor-redundancias) · 24/11/2026

## Veredito: APROVADO (sem 🔴 nem 🟡)

Conferido:
- O diff tem só isso: `web/app/__init__.py:2`, de `VERSAO = "0.1.0"` para `VERSAO = "0.2.0"`. É 1 arquivo, 1+/1-, num commit só (`T-0017: web v0.2.0`, com o trailer `Agente: modulo-web`).
- Nenhum teste fixa "0.1.0": o literal aparece só em docs, no quadro, no diário e nas tarefas, que são histórico. `web/tests/test_web.py:232` confere só que `versao` vem preenchida.
- Testes no head: `web/` dá 49 passed. `pytest tests/ -q` dá 153 passed.
- `verificar modulo-web --base origin/main`, rodado num worktree do head: OK, 1 arquivo, nenhuma violação.
- Nenhuma tela muda de layout: só o número da versão exibido (`main.py:124`) e o `/saude` (`main.py:146`). Por isso não precisa de print.
- Nenhum segredo e nenhum dado digitado no diff.

## Redundância (corretor-redundancias)
- Sem achado: a versão da web tem uma fonte única (`web/app/__init__.py`), que `main.py` importa. Não há outro literal de versão em código.
