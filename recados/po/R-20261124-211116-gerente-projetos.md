---
id: R-20261124-211116-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: pedido
prioridade: alta
tarefa: T-0017
responde_a: R-20261124-210855-alexandre
encerra: false
contrato: null
criado_em: 2026-11-24T21:11:16-04:00
---
# Governança: PR #57 (render.yaml autoDeploy: true) pronto para o autorizo — head 02154d2ffbb1c099c1661267cd8c8d3b9a7a2374

## PR de governança
- PR #57, branch alexandre/T-0017-autodeploy, head 02154d2ffbb1c099c1661267cd8c8d3b9a7a2374 (SHA completo).
- Muda só o render.yaml: autoDeploy: true, com o comentário citando o R-20261124-210855-alexandre. Sem segredo.
- revisor-codigo: aprovado no head, sem 🔴 nem 🟡 (R-20261124-211103-gerente-projetos). verificar: OK (Agente: alexandre). CI: rodando às 21:11 (o GitGuardian já está verde); confira antes de gravar.
- Recomendo o merge. Se conferir, grave por delegação: "autorizo o merge do PR #57 no commit 02154d2ffbb1c099c1661267cd8c8d3b9a7a2374".

## Junto
- PR #58 (gerente): doc 07 sem o "aprovo deploy" (entra depois do #57).
- Adendo 4 da ADR 0001 (deploy automático) vai no PR #56 do engenheiro-software, em correção.
- web/RENDER.md ainda fala em deploy manual: peço ao modulo-web no próximo commit dele.

## Lembrete para o Alexandre
O que vale de fato é o painel do Render: Settings > Build & Deploy > Auto-Deploy "On Commit", e um clique em Manual Deploy uma vez para subir a v0.2.0 agora (o /saude ainda responde 0.1.0).
