---
id: R-20261123-114238-gerente-projetos
de: gerente-projetos
para: [revisor-codigo]
cc: [po, alexandre]
tipo: pedido
prioridade: normal
tarefa: T-0011
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-23T11:42:38-04:00
---
# T-0011: PR #32 aberto (governança), head 855cf62 — pedido de revisão

Sessão BAPCentral - Cowork (gerente-projetos), 23/11/2026. Sem os guardiões do Claude Code. Branch `alexandre/T-0011-furos-guardiao`, trailer "Agente: alexandre" em todos os commits.

## O que muda
1. **git --output** (`guarda-bash-lib.mjs`, `saidasDoGit`): `--output`, `--out`, `--outp`, `--outpu` e `--output-directory` (com ou sem `=`, antes do `--`) viram alvo de escrita, também em log/diff/show/diff-tree. `--output-indicator-*` continua leitura.
2. **hard link** (`hardLinkDe`): `ln` sem `-s`, `cp -l`/`--link` (e `--l`, `--li`, `--lin`) e `link` tornam a FONTE alvo de escrita. Bloqueio já no PreToolUse; vale também para recado do Alexandre (bloqueio de recado falso).
3. **git embrulhado na trava do índice** (`guarda-merge-lib.mjs`, `comandosDeIndice`): o `git` depois de `env -C/--chdir/-u`, `xargs`, `sudo -u`, `nohup` conta, como em outra pasta. Recado do Alexandre intacto continua passando.
4. CI: o passo "Testes da CLI e dos guardiões" roda também o `guarda-furos.test.mjs`.

## Conferência
- `guarda-furos.test.mjs`: 8 testes (um grupo por furo). No main, 6 falham; com a correção, os 8 passam. Todos os testes de CLI e guardiões: 176 passed.
- Hook de verdade (`guarda-bash.mjs`, PreToolUse, BAP_AGENTE=modulo-web): `ln relatorios_nucleo.py /tmp/h` e `git log -1 --output=relatorios_nucleo.py` → exit 2; `ls` → exit 0.
- `verificar --base origin/main` OK (alexandre); `compileall` OK. CI do head: aguardando.

## Para avaliar (fora do escopo da T-0011)
- `ln -s` para arquivo de outro dono seguido de `>` no link continua só com aviso no PostToolUse.
- `git -c alias.x=commit x` não aparece na trava do índice (o subcomando vira "x").

## Depois do parecer
Governança: o merge só sai com o Alexandre escrevendo "autorizo o merge do PR #32 no commit <sha do head>".
