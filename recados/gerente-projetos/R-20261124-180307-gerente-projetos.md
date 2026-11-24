---
id: R-20261124-180307-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:03:07-04:00
---
# Parecer do corretor-redundancias: PR #46 head 368fe23 — sem achado em aberto

> Parecer do corretor-redundancias (subagente do gerente-projetos; gravado pelo gerente sem alteração, pela limitação do --de no coord.mjs).

# Parecer de redundâncias — PR #46 (testes/T-0017-escopo-pacote), reteste

Head SHA revisado: 368fe23c3df3640f2f903d9b7b479d6bee36c35a
Escopo: diff contra origin/main, só `tests/test_T0013_pacote_web.py` (+57 −9).

## Veredito: sem achado em aberto

## Reteste dos achados anteriores (head f64ef36)
| ID | Situação | Evidência |
|---|---|---|
| RD-0001 | fechado | `getattr(ba, "FAROIS_WEB", ())` aparece uma vez só, em `_farois_web()` (linha 219). Os usos estão nas linhas 235, 360, 364 e 558 e todos chamam a função. |
| RD-0002 | fechado | `assert set(pacote["relatorios"]) == {"vc_painel"}` saiu do critério 1. O escopo é afirmado só em `test_T0013_escopo_vc_painel_e_farois_web_sem_linhas_cruas` (linhas 361-362, via `_escopo_esperado`). |

## Duplicação nova no head
Nenhuma que segure o lote.
- `_escopo_esperado`, `_chaves_aninhadas`, `LISTA_FAROIS_WEB` e `FORA_DA_LISTA` têm um uso de propósito cada, sem cópia em outro lugar.
- Observação, não é achado: a linha 364 refaz a interseção `set(_farois_web()) & ...` que `_escopo_esperado` já faz. Como a linha 361 garante a igualdade antes, o laço poderia iterar `_escopo_esperado(...) - {"vc_painel"}`. O ganho é marginal e fica a critério do dono.
- O comentário das linhas 355-357 repete a docstring do critério 2 ("só na forma farol"). É baixa e só em comentário de teste, então não segura o lote pela regra de liberação.
