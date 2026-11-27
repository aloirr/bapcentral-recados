# Revisão de código — PR #176 (T-0045, diff único de governança)

- **Revisor:** revisor-codigo · **Data:** 27/11/2026
- **Head revisado:** `c28215f15403b616ecd43fc2d68089c982e95c5c` (branch `engenheiro-software/T-0045-governanca`). Commit novo = revisão nova.
- **Base conferida:** `origin/main` 85bc589.
- **Resultado:** sem 🔴. Há 2 🟡 a corrigir antes do merge e 3 🟢.

## O que foi conferido

1. **O diff aplica limpo:** `git apply --check docs/desenho/T-0045-governanca.diff` passou num worktree limpo do 85bc589, e a aplicação real também. Os blobs de base do diff (`fc19792`, `c590d6f`, `3eab825`) são os do 85bc589. O `donos.json` resultante é JSON válido, com 131 regras, e o `render.yaml` é YAML válido. Com o diff aplicado, os 176 testes de `scripts/*.test.mjs` e `.claude/hooks/*.test.mjs` passam. O PR também faz merge limpo no 85bc589 (`git merge-tree`).
2. **Guardião (`coord.mjs dono` sobre o arquivo aplicado):**
   - `nuvem/visitas/Dockerfile` e `.dockerignore` vão para o engenheiro-software;
   - `nuvem/visitas/{rodar,agenda,__init__}.py` e `nuvem/**` vão para o modulo-robo;
   - `web/.dockerignore` continua com o modulo-web; `render.yaml`, `.coord/donos.json` e `.claude/**` continuam com o alexandre.
   - As 3 regras entram depois de todas as regras específicas e antes de `web/**` e `docs/**`. Nenhum caminho que já tinha dono troca de dono (`nuvem/` não existe no main; `.dockerignore` era sem-dono), e as 11 regras de governança ficam intactas.
3. **`render.yaml`:**
   - Nenhum valor secreto: só `sync: false` (os 2 da Máxima) e `generateValue: true` (`BAP_VISITAS_TOKEN` do site).
   - `fromService` coerente: `type: web` e `name: bap-central`, com `property: hostport` para o endereço e `envVarKey: BAP_VISITAS_TOKEN` para o token.
   - `schedule: "*/10 10-23,0-1 * * *"` em UTC: a 1ª volta é às 10h00 UTC (06h00 em Manaus) e a última às 01h50 UTC (21h50 em Manaus). Está certo.
   - `buildFilter`: estão nele todos os arquivos do `COPY` do Dockerfile proposto (`requirements-visitas.txt`, `visitas_maxima.py`, `visitas_nucleo.py`, `relatorios_nucleo.py`, `bap_dados.py` e `nuvem/visitas/**`, que inclui o próprio Dockerfile), além do `.dockerignore`.
   - No `bap-central`, a única mudança é a variável nova. O resto do diff no arquivo é o comentário do topo.
4. **A frase do Alexandre funciona ao pé da letra:**
   - Todos os parâmetros existem no `scripts/coord.mjs enviar`: `--de`, `--para`, `--cc`, `--tipo`, `--tarefa`, `--prioridade alta|normal|baixa`, `--assunto` e `--corpo`. O `--tipo resposta` sem `--responde-a` é aceito.
   - O corpo sem `|` vai inteiro para o recado. `--de alexandre` só passa com `BAP_AGENTE=alexandre`.
   - O `RE_AUTORIZACAO` (`.claude/hooks/guarda-merge-lib.mjs`) casa com "autorizo o merge do PR #N no commit <sha completo>".
   - A frase manda parar se o `git apply` falhar e não leva a sessão a editar nada à mão.
5. **ADR 0004 (adendo 1) × contrato:** a D4 revista bate com o contrato §1. A regra "uma tentativa só" tem garantia no código do main:
   - `web/app/visitas.py`: `PAUSAM` na linha 65, o 423 enquanto está pausado e o `diagnostico.estado = "falhou"`;
   - os testes `test_RN_VIS_005_*`;
   - os códigos `MAXIMA_*` pausam e não entram em `NOVA_TENTATIVA`.
   - A brecha do "Retomar" está declarada.
6. **Segredos e dado pessoal:** nada no diff (nenhum valor, token, CNPJ, e-mail ou telefone).
7. **Donos:** `verificar --base origin/main` no head dá OK (7 arquivos, nenhuma violação). O commit tem o trailer `Agente: engenheiro-software`.
8. **G3** (`revisor-ux.md`, linha 40): o texto bate com o site (`web/app/templates/_faixa.html`: data e hora à vista, e "Dados de …, horário de Manaus" no `title`) e com o R-20261127-054626-po.

## 🟡 Corrigir antes do merge

1. **`docs/decisoes/0004-visitas-maxima-no-render.md`, linhas 33, 156, 238, 267, 275 e 289:** o corpo da ADR ainda afirma a D4 antiga, sem indicar o adendo.
   - O §7 (linha 238) diz "um vazamento expõe só esse usuário, que o Alexandre desativa", o que agora é falso.
   - O §9 (linha 267, item 2) ainda manda criar o usuário próprio na Máxima.
   - O item 10 (linha 275) ainda depende de 5, 7, 8 e 9.
   - A linha 289 diz que o PC e a nuvem usam logins diferentes.
   - Correção: acrescentar "(revista no adendo 1)" em cada um desses pontos, sem reescrever o texto aceito. Quem seguir a tabela do §9 hoje executa o passo errado.
2. **`docs/desenho/T-0045-governanca.md`, frase (a):** o "autorizo" sai sem que o Alexandre veja o que entrou no commit.
   - Inserir, antes do envio: "confira que `git diff --name-only origin/main..HEAD` lista só `.claude/agents/revisor-ux.md`, `.coord/donos.json` e `render.yaml`; se listar outro arquivo, pare e me diga, sem enviar o recado".
   - É a única trava da sessão antes da autorização de governança.

## 🟢 Sugestões

1. **`docs/desenho/T-0045-governanca.md`, linha 5:** "aplica … sobre o `origin/main` d1568f8". Ele aplica também no 85bc589 (conferido), então vale trocar por "o `origin/main` do dia (conferido até 85bc589)".
2. **Mensagem de commit da frase:** a G3 é da T-0036 (R-20261127-054626-po). Vale citar isso numa linha do corpo do commit ou do PR, porque o assunto só fala das visitas.
3. **Imagem:** o BuildKit aceita um `nuvem/visitas/Dockerfile.dockerignore`, que tem precedência sobre o `.dockerignore` da raiz, e esse arquivo cairia com o modulo-robo pelo `nuvem/**`.
   - O impacto é nulo, porque o `COPY` é uma lista fechada.
   - Vale o agente testes conferir que não existe `*.dockerignore` em `nuvem/visitas/`.
   - Pelo mesmo motivo, vale conferir que não há fixture com dado em `nuvem/visitas/`, porque essa pasta entra inteira na imagem.

## Reteste — head `4b235b0b51bc1fcfac867826ba0ca60cd4ccb21a` (delta c28215f..4b235b0; main 57cf6fa)

- **O `T-0045-governanca.diff` não mudou:** o delta tem 0 linhas nesse arquivo, e ele é idêntico byte a byte (`cmp`) ao do c28215f.
- **Aplica no 57cf6fa:** `git apply --check` passa num worktree limpo e a aplicação real também. O resultado tem 131 regras, JSON e YAML válidos, e os mesmos donos (`nuvem/visitas/Dockerfile` e `.dockerignore` → engenheiro-software, `nuvem/visitas/rodar.py` → modulo-robo, `render.yaml` → alexandre). Entre o d1568f8 e o 57cf6fa, o main não tocou no `donos.json`, no `render.yaml` nem no `revisor-ux.md`.
- **🟡1 (ADR 0004) — resolvido:** as linhas 33, 156, 238, 267, 275 e 289, além da linha "Ordem" e da linha "Web antes do robô" do §9, agora apontam para o adendo 1. O §7 foi corrigido: o vazamento expõe o login do notebook, e a senha é trocada nos dois lugares.
- **🟡2 (frase) — resolvido:** a conferência do `git diff --name-only origin/main..HEAD` com os 3 arquivos vem antes do push e do recado, e se aparecer outro arquivo a sessão para sem dar push e sem enviar o recado.
- **🟢1, 🟢2 e 🟢3 — atendidos:**
  - a referência do desenho virou "o `origin/main` atual (conferido até o 85bc589)";
  - a G3 é marcada como "carona da T-0036" no desenho e citada no corpo do commit da frase;
  - o teste do `*.dockerignore` e da fixture em `nuvem/visitas/` está no §3 do `T-0045-render-yaml.md`.
- **Donos:** `verificar --base origin/main` no head novo dá OK (7 arquivos, nenhuma violação). Os 2 commits têm `Agente: engenheiro-software`. Não há segredo nem dado pessoal no delta.

### 🟡 novo (fora do delta, apareceu com o main 57cf6fa)

1. **`.coord/diario/engenheiro-software.md`:** `git merge-tree origin/main 4b235b0` dá **CONFLICT**. O main acrescentou a linha da T-0050 no mesmo ponto em que o PR acrescentou a linha da T-0045.
   - Correção: trazer o `origin/main` para a branch com merge, sem rebase e sem force push, e manter as duas linhas (a da T-0050 e depois a da T-0045, porque o diário só recebe acréscimo).
   - Commit novo = reteste novo. O delta esperado é só o diário.

**Resultado do reteste:** os 2 🟡 e os 3 🟢 do parecer foram resolvidos, sem 🔴. Fica 1 🟡 aberto, o conflito do diário com o main, e com ele o PR não é aprovado.
