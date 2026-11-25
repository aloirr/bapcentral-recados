---
id: R-20261124-220325-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0018
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T22:03:25-04:00
---
# Parecer do revisor-codigo: PR #59 head 38a262e — 🟡 1 e 2 fechados; 🟡 3 (testes em tests/) com o testes

> Parecer do revisor-codigo (subagente do gerente-projetos; gravado pelo gerente sem alteração).

# Revisão T-0018 (2ª rodada): PR #59

- **Branch:** `engenheiro-software/T-0018-rotina-diaria` · **head revisado:** `38a262e` (anterior: `46f6ee2`)
- **Parecer:** **não aprovado ainda**. Não há 🔴. Os 🟡 1 e 2 caíram. O 🟡 3 caiu em parte: falta só levar os testes para `tests/`, o que é do agente testes.
- Commit novo exige revisão nova.

## O que foi conferido no head `38a262e`
- `compileall` ok.
- Testes do rascunho contra o head numa cópia temporária: **63 passed**.
- `pytest tests/ -q`: **184 passed**.
- `verificar engenheiro-software --base origin/main` e `verificar --base origin/main`: **OK**, sem violação (5 arquivos).

## Situação dos achados da 1ª rodada
| Achado | Situação |
|---|---|
| 🟡 1: `pr_de_origem` aceitava outro PR | **Resolvido**. `atualizar_do_github.py:248` devolve `None` sem PR cujo `merge_commit_sha` seja o SHA; o `--diario` sai 11. Teste novo: `test_limite_2_pr_de_outro_commit_nao_vale`. |
| 🟡 2: zip sem SHA passava | **Resolvido**. `:882` compara `info.get("sha") != sha`: sem comentário ou com outro SHA, sai 1. Teste novo: `test_diario_zip_de_outro_commit_ou_sem_comentario`. |
| 🟡 3: testes fora do CI | **Em parte**. Os casos que faltavam foram criados: `test_diario_api_fora_do_ar` (15), o teste do zip (1) e `test_diario_falha_na_troca_restaura` (4). Os 63 casos ainda estão só no rascunho e o CI do head não roda nenhum. Pronto quando o agente testes levar o arquivo para `tests/` (antes do merge ou no mesmo lote) e o CI ficar verde. |
| 🟢 simular grava log | **Resolvido**. `fim` não grava com `simular`, e o `--primeira-vez --simular` também não. |
| 🟢 data do backup em Manaus | **Resolvido** (`:903`). |
| 🟢 [SUPOSIÇÃO] dos limites 1 a 3 no `--primeira-vez` | **Resolvido** (ADR §3.1, a confirmar com o po). |
| 🟢 pendente de instale some do log no dia seguinte | Aberto (sugestão). |
| 🟢 `--confirmar` sozinho ignorado em silêncio | Aberto (sugestão). |
| 🟢 RN para a rotina em `03-regras.md` | Aberto (sugestão ao po). |

## O que segue igual à 1ª rodada
- O diff `46f6ee2..38a262e` não mexe em `.json`, bases, dado digitado nem segredo.
- O log continua sem dado pessoal.
- A ADR 0002 foi atualizada para as correções e continua fiel ao R-20261124-214958-alexandre.

## Redundância
- **Sem achado.** A correção não duplica regra e continua reusando as funções da T-0003.
