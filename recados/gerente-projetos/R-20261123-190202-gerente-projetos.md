---
id: R-20261123-190202-gerente-projetos
de: gerente-projetos
para: [gerente-projetos, todos]
cc: [po, alexandre]
tipo: aviso
prioridade: alta
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-23T19:02:02-04:00
---
# Passagem da sessão BAPCentral - Cowork (23/11/2026) para a volta ao Claude Code

A sessão rodou **sem os guardiões do Claude Code** (GitHub operado pelo site, no navegador do app Claude). Período no main: de `646ff3c` até `249380a` (#32). Confira tudo com `node scripts/coord.mjs verificar --base <sha>` na volta.

## 1. Entregue (no main)
- T-0003 (#20, #21), T-0010 código (#13, #23), T-0013 código da web e passo 4f (#15, #16, #25, #17, #18), T-0004 parcial (#27: pytest bloqueante, smoke informativo), T-0015 (#28, #29, #31), quadro (#24, #26, #30), T-0011 (#32, `249380a`, autorizado em R-20261123-184340-alexandre).

## 2. Em andamento
- **T-0012** (3 agentes novos): PR #33, head `3acedfc`, governança. Falta: CI, parecer do revisor-codigo e a frase do Alexandre; depois, PR do gerente com o doc 07 (destinos: 15 agentes) e a definição de pronto do CLAUDE.md.
- **T-0014** (filtros por estado e supervisor na web): desenho + robô + web + testes prontos SÓ LOCAL (pytest tests 148, web 38, CLI 168, verificar OK). O patch completo está em `recados/anexos/T-0014-trabalho-local.patch` (base `3398a52`; 10 arquivos: docs/desenho/T-0014.md, bap_automation.py, tests/test_T0013_pacote_web.py, tests/test_T0014_recortes_web.py, web/app/{main,pacotes,render}.py, web/app/static/estilo.css, web/app/templates/painel.html, web/tests/test_web.py). Na volta: aplicar (`git apply`), separar um PR por dono (engenheiro-software, modulo-robo, modulo-web, testes), mostrar a simulação ao Alexandre ANTES do PR (regra "Simule"; as 5 PNGs da sessão não subiram: regerar com uvicorn + playwright). Perguntas abertas ao Alexandre: (a) visão do estado sem anel e faixa atende? (b) primeiro nome do supervisor no filtro, ok? (c) supervisor só vê o próprio estado (perfil novo)?
- **T-0004**: smoke bloqueante depois que o testes fechar as 3 falhas da rota (R-20261123-062830-gerente-projetos).
- **T-0013**: "aprovo deploy v0.1.0" DADO (R-20261123-184341-alexandre). Falta conferir/criar no Render o serviço e os 4 segredos (ação do Alexandre) e disparar o deploy manual.

## 3. O que o time pede ao Alexandre
- "instale" da T-0010 (7 arquivos; simulação feita, backup ANTES_T0010_NOV2026).
- Merge do #33 (T-0012) depois do parecer.
- Serviço e 4 segredos no Render; senha do robô e BAP_WEB_URL/TOKEN no cofre do PC do robô (DT-AMADMBAP-03); depois, "instale" do bap_automation.py.
- Respostas (a), (b), (c) da T-0014.

## 4. Próximo passo
1. CI + revisão do #33. 2. Deploy v0.1.0 no Render. 3. Simulação da T-0014 ao Alexandre e PRs por dono. 4. quadro e docs/status/2026-11-23-sessao-cowork.md num PR do gerente.

## Avisos
- Ficou um lock velho do git na pasta de produção (`.git/stale-maintenance-lock-cowork`), inofensivo; apagar quando quiser.
- Pendente de lidos do gerente-projetos: R-20261123-114709-revisor-codigo, R-20261123-184340-alexandre, R-20261123-184341-alexandre.
