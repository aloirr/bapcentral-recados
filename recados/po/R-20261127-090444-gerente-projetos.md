---
id: R-20261127-090444-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: aviso
prioridade: normal
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T09:04:44-04:00
---
# Estado das 09h05 e previsões refeitas depois da pausa do limite de 5 h

Estado das 09h05 (Manaus), depois da pausa do limite de 5 horas. A sessão parou por volta das 08h12 e voltou às 09h02. Todo o trabalho dos agentes ficou salvo, e eles retomaram de onde pararam.

## No main desde o resumo das 05h45
- **T-0045 (visitas da Máxima), parte 1 no ar, web 0.6.0:**
  - #151: web das visitas;
  - #152: botão do PC usando a regra do núcleo;
  - #161: testes.
- **T-0023 (Garantias, Devoluções e NCC):**
  - #154: web, **0.7.0 no ar**;
  - #155: núcleo;
  - #153: ponte de teste;
  - #167: testes;
  - #171: robô, que entrou agora. Ele chega ao PC na rotina das 06h30 de amanhã (regra 11), e a partir daí os 3 faróis aparecem no site com dados.
- **T-0036 (Analista e perfis):**
  - #156: regras;
  - #160: desenho e contrato;
  - #157: faróis;
  - #158: web, **0.8.0 no ar**;
  - #168: conserto de um teste que a web da T-0036 quebrou no main.
- **T-0037 (Fretes):** #164, as regras.
- **Quadro:** #162.

## Previsões refeitas (hoje, Manaus)
- **T-0023:** falta a trava dos 3 faróis (testes) e o contrato (#163). Previsão: até 10h30. O PR 2 de faróis (PC só leitura das garantias, NCC e devoluções) vem a seguir, até 12h.
- **T-0036:** faltam os testes e o robô (#159). Previsão: até 11h.
- **T-0045 parte 2** (o robô pronto para a nuvem e a sincronização no PC, #165 e #166): na revisão final, depois de dois defeitos de login que os testes acharam e foram corrigidos. Previsão: até 11h.
- **T-0037:** simulação aprovada por você. O corretor pediu 12 ajustes de redundância; estão em curso. Os PRs entram até umas 13h.
- **T-0050:** a simulação espera a sua aprovação (R-20261127-063731). O código está pronto e corrigindo os achados das revisões. Previsão de merge: até 13h depois da aprovação.
- **T-0025 v2** (DDR, Campanhas e Expositores): começa depois da T-0023, hoje à tarde.

## Governança da T-0045 (você pediu número e SHA)
Ainda não há PR, porque nenhum agente, nem o gerente, pode gravar o `.coord/donos.json` nem o `render.yaml`: o guardião não deixa, e o time não contorna. A **governança 1** são 3 linhas no `donos.json`, com o texto pronto no R-20261127-060213 e no `docs/desenho/T-0045-render-yaml.md` §3. Ela precisa ser gravada numa sessão do Alexandre, como no PR #57. Assim que o PR existir, eu confiro o CI e mando o número e o SHA para o "autorizo". A governança 2 (render.yaml) vem depois dos itens 7 e 8.

## Ritmo
Para não bater de novo no limite de 5 horas, vou manter no máximo uns 6 agentes ao mesmo tempo.
