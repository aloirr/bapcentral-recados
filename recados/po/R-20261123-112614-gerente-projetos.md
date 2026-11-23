---
id: R-20261123-112614-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: aviso
prioridade: normal
tarefa: T-0004
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-23T11:26:14-04:00
---
# T-0004 e T-0015: fim do lote no Cowork — #27, #28, #29, #31 e #30 no main

Sessão BAPCentral - Cowork (gerente-projetos), 23/11/2026. Sem os guardiões do Claude Code.

## PRs (squash, nesta ordem)
| PR | Dono | Head revisado | Commit no main | O que muda |
|---|---|---|---|---|
| #27 | alexandre (governança) | 3bb4409 | 9dcfd0844e9d0e4ce4e0c758854d7c14804914af | CI: `pytest tests` da raiz bloqueante; `smoke_processos` informativo (`continue-on-error`) quando muda `.py` ou o `ci.yml` |
| #28 | alexandre (governança) | 27444f9 | 19c51103cbb9245ebb18bde69b78d06723fe3035 | `.gitattributes` com `*.bat text eol=crlf`; `.gitattributes` com dono alexandre no `donos.json` |
| #29 | testes | 8e9db2e | c217c9be41f0f1cd5fc88a6586052bfa17cd1b62 | teste `test_T0015_bat_crlf.py` (função pura `lf_soltos`) |
| #31 | engenheiro-software | 1e4c939 | 8f31c54076244ccaee7a8979056823bea16dd410 | `ATUALIZAR_DO_GITHUB.bat` com o mesmo conteúdo, guardado em LF (era o único com CRLF no repositório e aparecia como modificado depois do #28) |
| #30 | gerente-projetos | ba65652 | 3398a527def0459c11db9df83ad3a033ae5396cd | quadro, T-0004, T-0015 e diário |

Autorização de governança (#27 e #28): R-20261123-110206-alexandre, escrita pelo Alexandre. Pareceres: R-20261123-105430 (#27), R-20261123-105938 (#28), R-20261123-110942 (#29), R-20261123-111741 (#31) e R-20261123-112418 (#30), todos do revisor-codigo e aprovados. CI verde em todos os heads; `verificar` OK.

## Situação
- T-0015 concluída: o checkout e o zip do main saem com CRLF nos `.bat`, iguais byte a byte aos 13 `.bat` da produção. Clone limpo do main sem arquivo modificado.
- T-0004 em andamento: falta tornar o `smoke_processos` bloqueante depois que o testes fechar as 3 falhas da rota (R-20261123-062830-gerente-projetos). No CI do #27 o smoke deu as 4 falhas conhecidas do main.

## Próximo
- T-0011 e T-0012 (governança: precisam do "autorizo" do Alexandre no PR).
- T-0014 (filtros por UF e supervisor): desenho e simulação antes.
- Aprovações pendentes do Alexandre: "instale" da T-0010; "aprovo deploy v0.1.0" depois dos 4 segredos no Render; senha do robô e BAP_WEB_URL/TOKEN no cofre do PC do robô.
