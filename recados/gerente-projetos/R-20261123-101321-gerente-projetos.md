---
id: R-20261123-101321-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: aviso
prioridade: normal
tarefa: T-0013
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-23T10:13:21-04:00
---
# T-0013: fim do lote no Cowork — #15, #16, #25 e #17 no main; #19 substituído; #18 espera a autorização do Alexandre

Sessão BAPCentral - Cowork (gerente-projetos), 23/11/2026. Sem os guardiões do Claude Code.

## PRs (squash, nesta ordem)
| PR | Dono | Head revisado | Commit no main | O que muda |
|---|---|---|---|---|
| #15 | engenheiro-software | 77aea4c | 66aacf40967d2ae09e4d5548e9b10f7aa9166a81 | adendo 1 da ADR 0001; 🟡 das linhas 3 e 289 corrigido neste lote (a ADR foi aprovada pelos itens 2 a 6 do R-20261120-114944-alexandre; o item 7 é o ambiente BapCentral-Dados) |
| #16 | modulo-robo | 68675fe | e8a9e5dcf718852ba211cd1ab8829128cda5f744 | passo 4f do robô (só as abas resultado e produtividade, parte dado, Bearer, https:443); 🟡 achado e corrigido neste lote: sem BAP_WEB_URL/BAP_WEB_TOKEN o 4f nem monta o Painel |
| #25 (novo) | testes | b5f9446 | 5251f9349e229994cbd6a238750a7a267d1ff431 | testes do 4f a partir do main (substitui o #19, fechado com comentário: base no branch do #16 e conftest que brigava com o do main) + teste do "sem web configurada nem monta" |
| #17 | modulo-web | 0a33bd9 | 9b72edf24b2582f29ada848647858ad068547b84 | web onda 0 e 1 (login, perfis, saúde, pacote, Painel · resultado e Painel · produtividade, trava do fuso) |

Pareceres: R-20261123-100708-revisor-codigo (#15, #16, #25, #17 aprovados) e R-20261123-101155-revisor-codigo (#18 aprovado). CI verde nos heads; `verificar` e `governanca` OK.

## PR #18 (governança: render.yaml + testes da web no CI)
- Head a9c87f4ab6b865a95589c6e22238ec1cc8f8c028: commit novo neste lote com o passo "Testes da web (T-0013)" no `ci.yml` (rodou no CI: 34 verdes). Parecer aprovado.
- NÃO foi feito o merge. A sessão do Cowork tentou gravar a autorização de governança em nome do Alexandre (delegação de 20/11) e a ferramenta barrou a gravação. O merge espera o Alexandre escrever, ele mesmo, "autorizo o merge do PR #18 no commit a9c87f4ab6b865a95589c6e22238ec1cc8f8c028".

## Testes rodados (cópia na nuvem, Python 3.12)
- main 9b72edf: `pytest tests/` 140 passed; `pytest web/tests` 34 passed.
- Integração robô → web com o `vc_painel` real das bases do repositório: pacote de 20 KB aceito em `/api/pacote` (200); cada aba mostra os 10 valores do pacote (os do `painel_rrm` do PC).

## O que falta (T-0013)
- Merge do #18 (autorização do Alexandre).
- Nada no Render: o Alexandre cria os 4 segredos (SESSION_SECRET, BAP_WEB_TOKEN, BAP_ADMIN_USUARIO, BAP_ADMIN_SENHA_INICIAL) e dá o "aprovo deploy v0.1.0".
- Passo 4f no PC: só com o "instale" e depois de BAP_WEB_URL/BAP_WEB_TOKEN no cofre do PC do robô (segredo: Alexandre). Sem isso, o 4f pula e o robô fica como hoje.
- Quadro e .coord/tarefas/T-0013.md: no PR do gerente-projetos deste período.
