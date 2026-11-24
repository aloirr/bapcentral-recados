---
id: R-20261124-183615-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T18:36:15-04:00
---
# Parecer do corretor-redundancias: #49 cb2f607 e #51 44c6e3b sem achado em aberto

> Parecer do corretor-redundancias (subagente do gerente-projetos; gravado pelo gerente sem alteração, pela limitação do --de no coord.mjs).

# Reteste do corretor-redundancias: T-0017, PRs #49 e #51 (só os deltas)

Data: 24/11/2026. Fiz só leitura: `git fetch` dos 2 branches e `git diff <head antigo> <head novo>`. Não alterei código e não gravei recado.
Base: o parecer anterior, `rd2-47-51.md`.

---

## PR #49 · modulo-robo/T-0017-farol-inadimplencia · head cb2f6078bb750f39ce52e1a3631bdf3f5809c3db

**Veredito: sem achado em aberto.** O delta desde o e8bd178 muda só o `bap_automation.py`, com 5 linhas a mais e 5 a menos.

| ID | Situação | Evidência |
|---|---|---|
| RD-0015 | fechado | `_FONTE_BAIXADO_WEB["pl_inadimplencia"]` agora usa `(Path(BKP_BAPTOOLS), "Relatorio_Titulos_em_Abertos_*.xlsx")` (linha 6695). `BKP_BAPTOOLS` vale `"SISTEMA BAP/BACKUP_RELATORIOS/BKP_RELATORIOS_BAPTOOLS"` (linhas 267 a 269), o mesmo caminho de antes. O caminho escrito à mão não aparece mais no código. Os outros `BKP_RELATORIOS_BAPTOOLS` que restam no arquivo estão em comentário ou docstring. |
| RD-0012 | fechado | O comentário sobre `WEB_GRAFICOS_COM_NOME` agora registra a decisão D1 ("2 A", 24/11) e bate com o valor `True`. A docstring de `selecionar_farol_web` não cita mais o `tests/test_T0017_farol_web_robo.py`, que não existe. |

O encaminhamento ao `testes` continua de pé (é valor e não entra no catálogo): o `baixado_em` usa o `st_mtime` do arquivo, e o branch ainda não tem teste T-0017 do robô.

---

## PR #51 · engenheiro-dados/T-0017-fotos-sem-internos · head 44c6e3bd441c4b9026c5228c736502ac89e597d6

**Veredito: sem achado em aberto do lado do #51.** O delta desde o 464711a muda só o `bap_dados.py`, com 7 linhas a mais e 6 a menos.

| ID | Situação | Evidência |
|---|---|---|
| RD-0016 (lado #51) | fechado | `fotos_sem_internos` passou a se chamar `bap_dados.titulos_sem_internos` (linha 1427), e a docstring diz que é a "fonte unica" usada nas fotos e nos títulos do farol. A única chamada foi atualizada (linha 1473). Não sobrou nenhuma referência a `fotos_sem_internos` no branch. |

O RD-0016 do lado do #50 continua pendente: o modulo-farois precisa apagar a cópia `relatorios_nucleo.titulos_sem_internos` e chamar `bd.titulos_sem_internos` depois do merge do #51. O achado só fecha no catálogo quando o #50 fizer isso.

Encaminhamento ao `testes` (é regra e valor, não entra no catálogo): a docstring nova diz "O 000040 e o vendedor de teste, nao cliente: nao sai do saldo". Conferir se isso bate com a RN-GER-004 em `docs/produto/03-regras.md` e com o CLAUDE.md ("a conta 000040 fora"). Continua faltando o `test_RN_GER_004_...`.

---

## Resumo

| PR | Head | Veredito |
|---|---|---|
| #49 | cb2f607 | sem achado em aberto (RD-0015 e RD-0012 fechados) |
| #51 | 44c6e3b | sem achado em aberto (RD-0016 fechado do lado do #51; o lado do #50 segue pendente) |
