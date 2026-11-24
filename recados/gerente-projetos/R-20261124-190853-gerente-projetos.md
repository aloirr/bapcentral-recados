---
id: R-20261124-190853-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T19:08:53-04:00
---
# Parecer do revisor-codigo: PR #54 head 76863e1 — aprovado

> Pareceres do revisor-codigo, com checagem de redundância (subagente do gerente-projetos; gravados pelo gerente sem alteração).

# Revisão — PR #54 (T-0017, quadro/tarefa/status/doc 07)

- Head revisado: `f3cd466627540d38aa2886d5f183c171aefb0e4f` (branch `gerente-projetos/T-0017-quadro`, base `origin/main` 94ac56d).
- Revisor: revisor-codigo (subagente; parecer a ser gravado pelo gerente com nota de origem, decisão 3 A do R-20261124-181912-alexandre).
- Resultado: **não aprovado ainda — 0 🔴, 2 🟡, 3 🟢.**

## Conferido
- SHAs no `git log origin/main`: #46 `4793fd1`, #47 `89eb4ca`, #48 `a08ab86`, #49 `ec31d36`, #51 `0605f8b`, #50 `e56fe45`, #52 `73a8b4a`, #53 `94ac56d`, #44 `38e9de4`. Todos certos.
- "31 commits" do Cowork: de 646ff3c a b69fda7, inclusive, são 31. "#53 testes (31)": `pytest --collect-only` nos `tests/test_T0017_*.py` dá 31.
- Recados lidos (`coord.mjs ler`) e conteúdo confirmado: 173114 e 173350 (gerente-projetos), 174525, 175008, 175838, 181912, 181913, 083000 e 182438 (6 decisões, previsão de 30/11 e 02/12, Pedidos em 26/11), além do 184942 (deploy, "instale" dos 3 arquivos, 000040 e 5 passos).
- Dado pessoal, segredo ou nome de máquina: nenhum no diff ("notebook do Alexandre" é descrição, não hostname; R$ 400.387,79 é total agregado).
- Dados digitados, `.json` da raiz e `bap_dados.py`: intocados (só docs).
- Commit com `Agente: gerente-projetos`. `verificar gerente-projetos --base origin/main`, rodado no head do PR: OK, 4 arquivos, nenhuma violação.

## 🟡 Corrigir antes do merge
1. `docs/produto/07-time-e-coordenacao.md:32` — "(Alexandre, R-20261124-173114 e R-20261124-173350-gerente-projetos)": o primeiro id está truncado. O id certo é `R-20261124-173114-gerente-projetos`. Além disso, os dois recados são do gerente-projetos com o texto literal do Alexandre: escrever "texto do Alexandre gravado em R-…-gerente-projetos". O `docs/status/2026-11-24.md:14` tem o mesmo problema ("R-20261124-173114 e -173350"): usar os ids completos.
2. `.coord/quadro.md:7` — **redundância interna do quadro**: o parágrafo "**T-0017 (alta):** … #46 a #53 … Aguardando o Alexandre … 2ª entrega … 6 decisões" repete a linha da T-0017 na tabela (`.coord/quadro.md:29`): PRs, pendências e previsão. Deixar uma só fonte no quadro. Sugestão: o parágrafo fica só com o que não cabe na linha (o id do 184942 e o do 182438), ou sai e a linha ganha esses dois ids.

## 🟢 Sugestões
1. `.coord/quadro.md:9` e `docs/status/2026-11-24.md:15` — "(646ff3c..b69fda7)": na notação do git, `646ff3c..b69fda7` conta 30 commits, porque exclui o 646ff3c. Escrever "de 646ff3c a b69fda7, inclusive" ou `646ff3c^..b69fda7`.
2. `docs/produto/07-time-e-coordenacao.md:37-38` — sobrou uma linha em branco duplicada depois do parágrafo "Pareceres de subagente".
3. `docs/produto/07-time-e-coordenacao.md:36` — "decisão 3 A do R-20261124-181912-alexandre": esse recado registra que a 3 "seguiu a recomendação A do gerente, informada pelo po", e não a resposta literal do Alexandre. Vale dizer "3 A (recomendação do gerente, registrada no R-20261124-181912-alexandre)".

## Redundância
- **Achado (🟡 2):** dentro do `.coord/quadro.md`, o parágrafo da T-0017 duplica a linha da tabela.
- Entre arquivos, a lista de PRs e as pendências da T-0017 aparecem no quadro (linha com SHAs), na tarefa (com o conteúdo de cada PR) e no status ("#46 a #53"). A regra de modelo e a dos pareceres de subagente aparecem no doc 07 e no status. Aceitável: cada documento tem um papel (estado, detalhe e diário do dia), e o status já remete ao doc 07. 🟢: no status, trocar o texto da regra de modelo e da limitação do `--de` por "ver doc 07".

---
# Revisão — PR #54 (T-0017, quadro/tarefa/status/doc 07) — head novo

- Head revisado: `76863e113da5344e56dcb14104db17a7791299db` (branch `gerente-projetos/T-0017-quadro`, base `origin/main` 94ac56d). Substitui o parecer do head `f3cd466`.
- Revisor: revisor-codigo (subagente; o gerente grava o parecer com nota de origem, decisão 3 A do R-20261124-181912-alexandre).
- Resultado: **aprovado** (0 🔴, 0 🟡; ficam 2 🟢 opcionais).

## Os 🟡 do head anterior
1. Ids truncados: **resolvido.** O doc 07 (linha 32) e o status (linha 14) agora trazem `R-20261124-173114-gerente-projetos` e `R-20261124-173350-gerente-projetos`.
2. Repetição no quadro: **resolvido.** O parágrafo da T-0017 só aponta para a linha da tabela e para `.coord/tarefas/T-0017.md`.

## O que mudou de f3cd466 para 76863e1
- Só o que foi pedido: os ids completos, o parágrafo do quadro e a linha em branco a mais do doc 07 (era um 🟢, também resolvido).
- O commit novo traz `Agente: gerente-projetos`.
- `verificar gerente-projetos --base origin/main`, rodado no head 76863e1: OK, 4 arquivos, nenhuma violação.
- Nada de dado pessoal ou segredo entrou.

## 🟢 Sugestões que continuam (não bloqueiam)
1. `.coord/quadro.md:9` e `docs/status/2026-11-24.md:15`: na notação do git, "(646ff3c..b69fda7)" conta 30 commits, porque exclui o 646ff3c. Escrever "de 646ff3c a b69fda7, inclusive".
2. `docs/produto/07-time-e-coordenacao.md:36`: "decisão 3 A do R-20261124-181912-alexandre". O recado registra que a 3 seguiu a recomendação A do gerente, informada pelo po. Vale dizer isso.

## Redundância
Sem achado em aberto. O quadro deixou de repetir a si mesmo. Entre quadro, tarefa e status, a repetição que sobra é aceitável: cada um tem um papel (estado, detalhe e diário do dia).
