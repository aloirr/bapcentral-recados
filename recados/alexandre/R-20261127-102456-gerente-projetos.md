---
id: R-20261127-102456-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pedido
prioridade: alta
tarefa: T-0045
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T10:24:56-04:00
---
# T-0045: frase do Alexandre e passos do Render (governança no main)

**T-0045: a governança está pronta para o Alexandre.** O desenho está no main: PR #176, commit 6ebdb6f. Revisor de código aprovado, CI verde.

## O passo único dele
Abrir uma sessão no ambiente **BapCentral-Governanca** (o mesmo do PR #57), com o repositório de recados anexado, e colar esta frase:

> Atualize o origin/main, crie a branch alexandre/T-0045-governanca a partir dele, rode git apply docs/desenho/T-0045-governanca.diff (se falhar, pare e me diga o erro, sem editar nada à mão), faça um commit só com a mensagem "T-0045: governança do serviço de visitas na nuvem", a linha "Inclui a linha 40 do revisor-ux (T-0036, R-20261127-054626-po)" no corpo e o trailer "Agente: alexandre", confira que git diff --name-only origin/main..HEAD lista só .claude/agents/revisor-ux.md, .coord/donos.json e render.yaml (se listar outro arquivo, pare e me diga, sem dar push nem enviar o recado), dê push sem force, abra o PR para o main e, com o número N desse PR e o SHA completo do head dele, envie o recado com node scripts/coord.mjs enviar --de alexandre --para gerente-projetos --cc po --tipo resposta --tarefa T-0045 --prioridade alta --assunto "Autorizo o merge do PR #N (governança T-0045)" --corpo "autorizo o merge do PR #N no commit <sha>", trocando N e <sha> pelos valores reais, e me mostre o número, o SHA e o id do recado.

A própria sessão dele abre o PR e manda o "autorizo". Eu confiro o CI e faço o merge.

## No Render, depois do merge (no máximo 4 passos)
1. **Blueprints**, no Blueprint da BAP Central: se aparecer uma sincronização pendente, confirmar. Vai aparecer o serviço novo `bap-visitas-maxima`. Se a própria tela já pedir `BAP_MAXIMA_USUARIO` e `BAP_MAXIMA_SENHA`, preencher ali, como no passo 3, e pular o passo 2.
2. Abrir **bap-visitas-maxima > Environment**.
3. Preencher `BAP_MAXIMA_USUARIO` e `BAP_MAXIMA_SENHA` com **o mesmo usuário e a mesma senha da Máxima que o notebook já usa** e clicar em **Save Changes**. Não precisa criar usuário.
4. Dizer a você só "preenchi". Usuário e senha nunca vão para chat, recado ou print.

## O que esperar
- **O primeiro build do serviço novo vai falhar**, porque o código e o Dockerfile ainda não estão no main. É esperado: nada roda e o site não cai.
  - O site faz um deploy normal, de alguns segundos, pela variável nova do token.
  - Quando o time puser o código e o Dockerfile no main, o Render refaz o build sozinho.
- **O diagnóstico faz uma tentativa só** de login na Máxima. Se houver confirmação, captcha ou bloqueio, nada é tentado de novo, e eu aviso você na hora.
- **Brecha conhecida:** com 2 cliques do admin no site ("Retomar" e "Pedir diagnóstico") sai um segundo login no mesmo dia. Até a correção, que vai como ajuste da RN-VIS-005, o time não aperta esses dois sem o "ok" do Alexandre.

## A seguir (time)
O modulo-robo põe o código do serviço (`nuvem/visitas/`) e depois o engenheiro põe o Dockerfile, cada um no seu PR. Os testes vêm depois. Isso começa assim que a governança dele estiver no main.
