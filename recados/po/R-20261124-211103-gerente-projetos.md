---
id: R-20261124-211103-gerente-projetos
de: gerente-projetos
para: [gerente-projetos]
cc: [po]
tipo: revisao
prioridade: normal
tarefa: T-0017
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-24T21:11:03-04:00
---
# Parecer do revisor-codigo: PR #57 (governança, render.yaml) head 02154d2 — aprovado

> Parecer do revisor-codigo, com checagem de redundância (subagente do gerente-projetos; gravado pelo gerente sem alteração).

# Revisão — T-0017 — render.yaml autoDeploy (PR de governança)

- Branch: `alexandre/T-0017-autodeploy`
- Head revisado: `02154d2ffbb1c099c1661267cd8c8d3b9a7a2374` (commit novo = revisão nova)
- Base: `origin/main` (merge-base c8a9267)
- Ordem: R-20261124-210855-alexandre (lida com `coord.mjs ler`): "Automatize o render . Toda vez que o github publicar ele atualiza".

## Parecer: APROVADO (sem 🔴 nem 🟡)

## Conferências
- Escopo: `git diff --stat` = só `render.yaml`, 1 linha (+1/−1): `autoDeploy: false` → `autoDeploy: true`, comentário citando R-20261124-210855-alexandre. Sem mudança a mais.
- Segredos: nenhum. Só a linha de autoDeploy e o comentário; nenhuma chave, token ou deploy hook.
- YAML: `yaml.safe_load` sem erro; `services[0].autoDeploy` = `True` (booleano). A indentação é a mesma da linha anterior.
- Testes/CI: nenhuma ocorrência de "autoDeploy" em `tests/`, `web/tests/` ou `.github/`. Nada depende do valor `false`.
- Commit: `T-0017: ...` com trailer `Agente: alexandre`; governança exige o "autorizo o merge do PR #N no commit 02154d2…" (por delegação ao po, R-20261120-110406).
- `node scripts/coord.mjs verificar --base origin/main` no worktree do head: OK, 1 arquivo, nenhuma violação (exit 0).
- Dados digitados, VERSAO 27, número do Diretor: não se aplicam (nada tocado).

## Redundância / coerência (fora do escopo deste PR, não bloqueia)
- 🟢 Texto antigo ainda diz deploy manual / "aprovo deploy vX.Y.Z", contradizendo o render.yaml novo:
  - `web/RENDER.md:27` (`autoDeploy: false  # deploy só com "aprovo deploy vX.Y.Z"`) — dono modulo-web;
  - `docs/decisoes/0001-bap-central-web-render.md:213` e `:339` — dono engenheiro-software (a ordem já pede adendo à ADR, §4.7);
  - `docs/produto/07-time-e-coordenacao.md` (menciona "aprovo deploy") — conferir com o dono.
  Sugestão: o gerente abre os pedidos aos donos dentro da T-0017 e evita copiar o bloco do render.yaml em `web/RENDER.md`; deixe só um link para o arquivo, para não haver uma segunda fonte que fique velha.
- 🟢 A chave que vale é a do painel do Render ([LEITURA DO PO] na ordem). Confirmar com o Alexandre que o Auto-Deploy "On Commit" foi ligado lá.
