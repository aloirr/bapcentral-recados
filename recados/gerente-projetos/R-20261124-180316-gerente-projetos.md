---
id: R-20261124-180316-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:03:16-04:00
---
# Parecer do revisor-codigo: PR #46 head 368fe23 — aprovado

> Parecer do revisor-codigo (subagente do gerente-projetos; gravado pelo gerente sem alteração, pela limitação do --de no coord.mjs).

# Revisão — PR #46 (testes/T-0017-escopo-pacote) — T-0017

- Head revisado: 368fe23c3df3640f2f903d9b7b479d6bee36c35a (parecer anterior: f64ef36, 1 🟡)
- Diff contra origin/main: só tests/test_T0013_pacote_web.py (+57/-9).

## Veredito: APROVADO (sem 🔴, sem 🟡)

## Conferência dos pontos do parecer anterior
- 🟡 escopo não travado → RESOLVIDO. LISTA_FAROIS_WEB fixa (pv_pedidos, vc_visitas,
  pl_entregas, pl_inadimplencia; R-20261124-175008-alexandre) e
  `assert set(_farois_web()) <= LISTA_FAROIS_WEB` (tests/test_T0013_pacote_web.py:360).
  Fixture com relatório fora da lista (pl_garantias, "NAO-VAI-FORA-DA-LISTA")
  provado fora do pacote por chave (:363) e por texto (:371).
- "tabelas" procurada em qualquer nível via _chaves_aninhadas (:226, :369);
  "linhas" só no 1º nível, justificado pelo bloco insights (:367-368).
- RD-0001 → RESOLVIDO: getattr(ba, "FAROIS_WEB", ()) só em _farois_web() (:217-219).
- RD-0002 → RESOLVIDO: assert do escopo saiu do critério 1 (:255); fica só no teste de escopo.

## Testes
- `pytest tests/test_T0013_pacote_web.py -q` no head: 50 passed.
- Mesmo teste com bap_automation.py de origin/modulo-robo/T-0017-farol-inadimplencia
  (FAROIS_WEB = ("pl_inadimplencia",)): 50 passed. Arquivo restaurado depois.
- compileall do arquivo: ok.
- `node scripts/coord.mjs verificar testes --base origin/main`: OK, nenhuma violação.

## Checklist
- Pedido atendido sem mudança a mais: sim (só o arquivo de teste).
- Dados digitados, configs .json, bap_dados.VERSAO, segredos: intocados / nada encontrado.
- Número do Diretor: não se aplica (sem mudança de cálculo). Tela: não se aplica.

## 🟢 Sugestões (não bloqueiam)
- 🟢 tests/test_T0013_pacote_web.py:238-243 — a fixture só traz pl_inadimplencia entre
  os 4 faróis; quando o robô ligar pv_pedidos/vc_visitas/pl_entregas, vale acrescentá-los
  à fixture para o laço da forma "farol" (:364) cobri-los também.
