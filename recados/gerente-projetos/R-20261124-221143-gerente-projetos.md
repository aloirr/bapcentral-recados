---
id: R-20261124-221143-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: null
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T22:11:43-04:00
---
# Pareceres do revisor-codigo: #58 head cd90887 e #61 head 7c8ef56 — aprovados

> Pareceres do revisor-codigo, com checagem de redundância (subagente do gerente-projetos; gravados pelo gerente; nomes de máquina omitidos).

# Revisão — PRs #58 e #61 (revisor-codigo, 2026-11-25)

Base: origin/main e74de94. Os dois PRs alteram só 1 doc cada, o merge com o main atual sai limpo (`git merge-tree`) e o `verificar --base origin/main` em worktree temporário sai 0, sem violação.

---

## PR #58 — gerente-projetos/T-0017-deploy-automatico — head 1887577

Diff: `docs/produto/07-time-e-coordenacao.md:19` (item 5). 1 commit, trailer `Agente: gerente-projetos`. verificar: OK.

**Parecer: 🟡 (1 item)**

- Fidelidade: confere com o R-20261124-210855-alexandre. O site publica a cada commit no main, o merge com CI verde e pareceres libera o site e o robô só vai para o PC depois do /saude. Também bate com o `render.yaml` do main (`autoDeploy: true`, linha 14) e com a ADR 0001 §4.7 e o adendo 4 (já no main). A retirada de "('acelere' e similares não aprovam deploy)" está coerente: não existe mais frase de deploy.
- 🟡 `docs/produto/07-time-e-coordenacao.md:19`: a mesma linha mantém "pede o 'instale' quando vai para a produção (T-0003)". Isso contradiz a decisão 4 A do R-20261124-214958-alexandre (ADR 0002 no main; regra 11 nova no PR #61): os `.py`/`.bat` da raiz vão pela rotina diária, e o "instale" fica só para os `.bat` de instalação, o `atualizar_do_github.py`, o `tarefa_bap.xml` e as configs. A linha já está sendo editada e o dono é o mesmo. Proposta: "...pede o 'instale' só para os .bat de instalação, o atualizador, o tarefa_bap.xml e as configs; o resto chega ao PC pela rotina diária (regra 11, ADR 0002)". Outra saída: casar o merge com o do #61.
- 🟢 `docs/produto/07-time-e-coordenacao.md:21` ("Fontes:"): acrescentar R-20261124-210855-alexandre (hoje ele só aparece no corpo do item 5).

---

## PR #61 — alexandre/T-0018-regra-11 — head cdeaec8

Diff: `CLAUDE.md:71` (regra 11). 1 commit, trailer `Agente: alexandre` (governança: o merge depende do "autorizo o merge do PR #61 no commit cdeaec8..." completo). verificar: OK, com o aviso informativo de que o CLAUDE.md pertence ao gerente-projetos.

**Parecer: 🟡 (1 item, redundância/contradição fora do diff)**

- Fidelidade: o texto é a ADR 0002 §4 do main, com diferenças só de redação ("com backup ... e conferência byte a byte", "pausa por", "do Alexandre (ADR 0002)"). Também bate com o R-20261124-214958-alexandre: decisões 1 B (pasta pessoal), 2 A (06h30, notebook do robô) e 4 A (5 limites; .bat de instalação, tarefa_bap.xml e configs continuam com "instale"). O limite 3 (versão web = /saude) é coerente com o `render.yaml` (`autoDeploy: true`) e com o R-20261124-210855.
- 🟡 Texto que contradiz a regra 11 nova, no main e intocado pelo PR:
  - `.claude/agents/gerente-projetos.md:84`: "Código do `main` só chega lá pelo `ATUALIZAR_DO_GITHUB.bat` ... depois do 'instale' do Alexandre" (a linha 85, "Nunca diga 'instalado' antes disso", depende dela);
  - `.claude/agents/po.md:85`: "só instala com o 'instale' dele".
  Os dois são governança. Incluir no próprio #61 (mesmo trailer `Agente: alexandre`, mesmo autorizo) ou num PR de governança gêmeo, com merge junto. Senão o gerente e o po seguem a regra antiga.
- 🟢 Mesma família, sem bloquear:
  - `docs/produto/05-roadmap.md:6` ("produção recebe só pelo ATUALIZAR_DO_GITHUB.bat com o 'instale'");
  - `docs/decisoes/0001-bap-central-web-render.md:170`, `:216` e `:417` ("O PC só recebe com 'instale'", "por instalação, regra 11"): cabe uma nota remetendo à ADR 0002;
  - `.claude/skills/entrega/SKILL.md:15` ("'instale' no PC"): ok se ler como "quando couber".
  Também há "aprovo deploy" residual na ADR 0001 (`:222`, `:291`, `:327`, `:340`, `:375`). São registros históricos que o adendo 4 já declara substituídos. O `:340` ("deploy manual com autoDeploy: false") é o mais enganoso; marcar como substituído.
- 🟢 `CLAUDE.md:71`: o `atualizar_do_github.py` na lista "continuam com instale" vem de uma [SUPOSIÇÃO] da ADR 0002 §3, não do texto do recado. Como é conservador e a ADR foi aprovada, aceito. A regra também deixou de citar o backup `ANTES_<ASSUNTO>_<MÊS><ANO>` do "instale" manual (T-0003); se valer, uma meia frase resolve.

---
# Revisão 2 — PRs #58 e #61 (revisor-codigo, 2026-11-25)

Base: origin/main e74de94. Os dois heads novos fazem merge limpo com o main (`git merge-tree`). O `verificar --base origin/main`, rodado em worktree temporário, sai 0 nos dois. Os pareceres anteriores (heads 1887577 e cdeaec8) ficam substituídos por este.

---

## PR #58 — gerente-projetos/T-0017-deploy-automatico — head cd90887

Diff contra o main: só `docs/produto/07-time-e-coordenacao.md:19`. São 2 commits, os dois com `Agente: gerente-projetos`. verificar: OK, 1 arquivo, nenhuma violação.

**Parecer: aprovado**

- O 🟡 anterior caiu. O item 5 deixou de pedir "instale" para a produção em geral. Agora remete à rotina diária (regra 11, ADR 0002, T-0018) e guarda o "instale" para os `.bat` de instalação, o `atualizar_do_github.py`, o `tarefa_bap.xml` e as configs. Isso bate com a decisão 4 A do R-20261124-214958-alexandre e com o texto do #61.
- O deploy automático continua fiel ao R-20261124-210855-alexandre e ao `render.yaml` (`autoDeploy: true`). "aprovo deploy" não sobrou no doc 07.
- 🟢 (de novo) A linha "Fontes:" (`:21`) poderia citar o R-20261124-210855 e o R-20261124-214958.
- Observação: o item 5 cita a regra 11 nova, que só existe depois do #61. O ideal é fazer o merge do #61 antes do #58, ou os dois juntos.

---

## PR #61 — alexandre/T-0018-regra-11 — head 7c8ef56

Diff contra o main: `CLAUDE.md:71` (sem alteração desde cdeaec8), `.claude/agents/gerente-projetos.md:83-84` e `.claude/agents/po.md:85`. São 2 commits, os dois com `Agente: alexandre`. verificar: OK, 3 arquivos, nenhuma violação. O CLAUDE.md aparece como "outro dono" apenas a título informativo. Por ser governança, o merge depende do "autorizo o merge do PR #61 no commit 7c8ef565e7e162ac3a4aa9a329171a1299e786e8". Uma autorização dada para o cdeaec8 não vale mais.

**Parecer: aprovado**

- O 🟡 anterior caiu. No `gerente-projetos.md`, a seção Produção agora descreve a rotina diária, os 5 limites e o que continua com "instale". No `po.md`, a linha "Simule" segue o mesmo texto. Os dois estão coerentes com a regra 11 e com a ADR 0002 §2/§3. O nome de máquina saiu do `gerente-projetos.md`.
- O "Nunca diga 'instalado' antes disso" (`gerente-projetos.md:85`) continua fazendo sentido: só depois que a rotina instalou ou que o "instale" aconteceu.
- 🟢 `gerente-projetos.md:83`: "a mudança do robô para ela é da T-0018". A ADR 0002 §2 (1 B) diz que a mudança é do modulo-robo, "à parte". Vale trocar para "do modulo-robo (T-0018)". A linha também perdeu a informação de onde rodam os faróis (notebook e desktop). Se o gerente usar isso no dia a dia, convém repor sem nome de máquina.
- 🟢 Fora do diff, para uma limpeza futura: o nome de máquina continua em `.claude/agents/engenheiro-software.md:35` e em `.claude/agents/modulo-posvenda.md:23`. Os 🟢 da revisão 1 também seguem abertos: `docs/produto/05-roadmap.md:6`, ADR 0001 `:170`/`:216`/`:340`/`:417`, e `.claude/skills/entrega/SKILL.md:15`.
