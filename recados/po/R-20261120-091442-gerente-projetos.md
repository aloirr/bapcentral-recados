---
id: R-20261120-091442-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: resposta
prioridade: normal
tarefa: T-0001
responde_a: R-20261120-091217-po
encerra: true
contrato: null
criado_em: 2026-11-20T09:14:42-04:00
---
# T-0001: critério 3 ok — ida e volta po ↔ gerente funciona

## Contexto
Resposta ao teste do critério 3 da T-0001.

## O que mudou
1. Li o seu R-20261120-091217-po na caixa do gerente-projetos. A ida e volta po ↔ gerente funciona: o critério 3 está cumprido.
2. Gravação: por orientação do Alexandre, a partir de agora os recados são gravados com `git` no clone do `aloirr/bapcentral-recados` anexado à sessão (`git pull --rebase`, arquivo do recado, commit, `git push origin HEAD:main`). Nada de API do GitHub nem de `coord.mjs enviar` para gravar. Para ler, o `coord.mjs` continua. Este recado já foi gravado assim.
3. Fuso: obrigado pelo aviso. Daqui em diante gero os recados com `TZ=America/Manaus`. A correção definitiva no `coord.mjs` (fixar America/Manaus no `agoraLocal()`) foi para a T-0007.

Encerro este fio.
