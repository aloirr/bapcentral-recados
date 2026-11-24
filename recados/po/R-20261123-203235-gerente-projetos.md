---
id: R-20261123-203235-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre, gerente-projetos]
tipo: entrega
prioridade: normal
tarefa: T-0014
responde_a: R-20261123-195144-alexandre
encerra: false
contrato: null
criado_em: 2026-11-23T20:32:35-04:00
---
# Fim do lote (noite de 23/11): T-0011, T-0012 e T-0014 no main; T-0010 instalada no PC

Sessão BAPCentral - Cowork. Main em `3623986`. Merges com a autonomia dada pelo Alexandre (R-20261123-201156-alexandre) e, nos de governança, com a frase dele.

## 1. Entregue
| PR | Dono | Commit no main | O quê |
|---|---|---|---|
| #32 | alexandre (gov.) | 249380a | T-0011: 3 furos do guardião (git --output, hard link, git embrulhado) |
| #33 | alexandre (gov.) | 42b66f1 | T-0012: agentes corretor-redundancias, design-de-marca e designer-ux |
| #34 | gerente-projetos | d44a13e | T-0012: doc 07 e definição de pronto com os 3 agentes |
| #38 | modulo-web | df697f3 | T-0014: filtro por estado no Painel da web (+ correção dos testes da web das 20h à meia-noite) |
| #36 | engenheiro-software | 0169ceb | T-0014: desenho |
| #35 | testes | 356b90d | T-0014: testes do robô |
| #37 | modulo-robo | 3623986 | T-0014: pacote da web leva as visões por estado |

- T-0010 instalada na pasta de produção (R-20261123-192521-gerente-projetos).
- Conferência no main: `pytest tests/` 147 passed; `pytest web/tests` 38 passed.

## 2. Em andamento
- T-0013: deploy v0.1.0 aprovado (R-20261123-184341-alexandre); falta o serviço e os 4 segredos no Render (ação do Alexandre).
- T-0004: smoke bloqueante depois que o testes fechar as 3 falhas da rota.
- Quadro e tarefas (T-0011, T-0012, T-0014 concluídas) num PR do gerente.

## 3. O que o time pede ao Alexandre
- Render: serviço + 4 segredos (SESSION_SECRET, BAP_WEB_TOKEN, BAP_ADMIN_USUARIO, BAP_ADMIN_SENHA_INICIAL).
- Cofre do PC do robô: senha do robô e BAP_WEB_URL/BAP_WEB_TOKEN; depois, "instale" do bap_automation.py (passo 4f e os recortes da T-0014).

## 4. Próximo passo
1. PR do gerente com quadro e tarefas. 2. Deploy no Render quando os segredos existirem. 3. T-0004 (smoke).

## Como testar a T-0014 em 5 passos (depois do deploy e do "instale" do robô)
1. Rode o robô no PC (passo 4f manda o pacote para a web).
2. Entre na BAP Central web com o admin.
3. Abra Painel · resultado: a linha "Estado" mostra BAP inteira e os estados.
4. Clique num estado: cada cartão mostra o número e o % do estado; compare com a barra desse estado no Painel do Diretor do PC (têm de ser iguais).
5. Troque para Painel · produtividade: o estado escolhido continua marcado.

## Aviso
- Os pareceres desta sessão (revisor-codigo, corretor-redundancias, designer-ux) foram escritos na mesma sessão que fez o código, sem os guardiões do Claude Code. Na volta, vale uma revisão independente do lote (main de `646ff3c` a `3623986`).
