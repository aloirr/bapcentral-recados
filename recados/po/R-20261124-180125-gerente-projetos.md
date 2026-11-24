---
id: R-20261124-180125-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:01:25-04:00
---
# Parecer do revisor-codigo: PR #46 head f64ef36 — não aprovado (1 🟡)

> Parecer do revisor-codigo, rodado como subagente do gerente-projetos. O coord.mjs só aceita --de igual à BAP_AGENTE da sessão (gerente-projetos), por isso o gerente grava o texto sem alterar nada.

## Parecer — PR #46 (T-0017) — head f64ef36febb9c9123daa204e9f58bb8abb3d9f6b

Veredito: **não aprovado** — 1 🟡, sem 🔴.

Conferido:
- Correção: `pytest tests/test_T0013_pacote_web.py -q` com 50 passed no head e 50 passed com o `bap_automation.py` de origin/modulo-robo/T-0017-farol-inadimplencia (FAROIS_WEB = ("pl_inadimplencia",)).
- Nenhum teste tirado ou pulado: 37 `def test_` no main e 37 no branch. Os 2 renomeados mantêm o conteúdo, e só existem os importorskip que já havia.
- Donos: `verificar testes --base origin/main` OK, só tests/test_T0013_pacote_web.py. O commit traz `Agente: testes`.
- Sem dado digitado, segredo ou bap_dados no diff.

🟡 tests/test_T0013_pacote_web.py:209-216, 236, 340 e 532-536: o escopo deixou de estar travado. O esperado vem de `ba.FAROIS_WEB`, o próprio módulo testado, então o teste é tautológico. Se alguém puser em FAROIS_WEB um id fora do pedido do Alexandre (por exemplo pl_garantias ou vc_base, com dado de cliente), os 3 testes continuam verdes. Além disso, no estado do robô T-0017 a fixture `_resultados_ficticios()` só traz ids que estão em FAROIS_WEB. Assim, nada prova que um relatório fora da lista é descartado (antes o pl_inadimplencia cumpria esse papel).
  Correção pedida:
  (a) criar uma constante no teste com a lista branca dos 4 faróis autorizados (R-20261124-175008-alexandre: Inadimplência, Pedidos, Entregas, Visita, com os ids reais) e afirmar `set(ba.FAROIS_WEB) <= LISTA_BRANCA`;
  (b) pôr na fixture um relatório que nunca vai ao site (ex.: "pl_garantias" com marcador "NAO-VAI-GARANTIA") e afirmar que ele fica fora de `pacote["relatorios"]` e do texto JSON.

🟢 linha 342-345: o check "linhas/tabelas" olha só o 1º nível do farol. O `NAO-VAI-INAD` no texto já cobre o vazamento de cliente, então isto fica como sugestão.

Revisão nova a cada commit novo.
