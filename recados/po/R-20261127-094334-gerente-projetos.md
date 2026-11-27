---
id: R-20261127-094334-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: resposta
prioridade: normal
tarefa: T-0045
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T09:43:34-04:00
---
# T-0045: opção B em preparo (diff único, frase e Render mínimo)

Recebi a opção B (R-20261127-094157-alexandre). O time segue pela nuvem.

**Em preparo agora (engenheiro-software):**
- `docs/desenho/T-0045-governanca.diff`: um diff só, com
  - a governança 1: as 3 linhas do `donos.json` para `nuvem/**`;
  - a governança 2: o `render.yaml` com o serviço `bap-visitas-maxima`;
  - de carona, a linha 40 do checklist do revisor-ux, alinhada à sua decisão R-20261127-054626. Não acrescenta nenhum passo para o Alexandre.
- A frase exata para o Alexandre colar numa sessão dele. A própria sessão dele:
  - cria a branch;
  - aplica o diff;
  - abre o PR;
  - manda ao gerente o "autorizo o merge do PR #N no commit <sha>".
- O passo a passo do Render, reduzido ao mínimo (no máximo 4 passos): confirmar o sync do Blueprint, se o Render pedir, e preencher BAP_MAXIMA_USUARIO e BAP_MAXIMA_SENHA. O diagnóstico, os logs e o "Ligar a agenda" ficam com o time.
- Muda a ordem da ADR 0004: a governança passa a vir antes do Dockerfile e do código da nuvem, que dependem dela. O engenheiro registra num adendo e diz como evitar uma imagem rodando sem o código.

**Previsão:** no main até umas 10h45 de Manaus. Mando a frase e os passos por recado assim que estiverem no main.

**O login da Máxima:** aguardo a resposta dele. Vale qualquer uma das duas. Se for o mesmo do notebook, o risco é o que você já explicou.

**Merges desde o último recado:**
- #173: RN-GER-018, da T-0050 (d0588e6);
- #163: contrato §10.9 e §10.10, da T-0023 (d1568f8).
