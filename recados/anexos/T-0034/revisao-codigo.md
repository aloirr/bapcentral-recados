# T-0034 · Revisão de código (revisor-codigo)

- **Branch:** `modulo-web/T-0034-pagina-inicial`. **Head revisado:** `9ad9ae99ecc091f1ebf14c0c21fe675113635073`.
- **Escopo:** só a T-0034, `git diff origin/modulo-web/T-0033-revisao-geral...origin/modulo-web/T-0034-pagina-inicial`. A base de comparação é o `94b3440` (T-0033 web, já aprovada) e o merge-base confere.
- **Decisões usadas como régua:** R-20261126-174334-alexandre e R-20261126-180314-alexandre (2 A).
- O parecer vale só para este head. Commit novo pede revisão nova.

## Resultado: **não aprovado**. 1 🔴, 2 🟡, 4 🟢

## O que foi rodado
- **Cópia do head fora do clone:** `git archive 9ad9ae9` no scratchpad. O clone não mudou de branch e nada foi alterado nele.
- **Testes:** `python -m compileall -q web/app` limpo. `pytest web/tests`: **365 passed**, 1 warning (deprecação do starlette), sem falha.
- **Donos:** `node scripts/coord.mjs verificar --por-commit origin/main..origin/modulo-web/T-0034-pagina-inicial`: "OK — 11 commit(s) conferido(s), nenhuma violação". Todo arquivo do diff está em `web/`.
- **Prova do 🔴:** um teste avulso, criado só na cópia e apagado depois, põe um 4º cartão RRM ("Ticket", valor `R$ 9.876`) no `pacote_ficticio`.
  - **Head 9ad9ae9:** o título do cartão aparece e o valor some. O teste falha.
  - **Base 94b3440:** o valor aparece. O teste passa.

## 🔴 Bloqueia

### R1 · Painel Executivo: do 4º cartão RRM em diante, o número grande e a legenda somem da tela
- **Onde:** `web/app/templates/painel.html:27` e `web/app/render.py:125`.
  - Em `painel.html:27`, `rc-valor` e `rc-leg` saíram de **todos** os cartões.
  - Em `render.py:125`, `faixa_painel` leva só os 3 primeiros cartões para a faixa: `for c in (...)[:3]`.
- **Efeito:**
  - O PC manda 10 cartões no Resultado, 10 na Produtividade e 6 no Por DU (`painel_rrm.py:6-12`, docstring de `calcular`).
  - Do 4º cartão em diante, o valor não aparece em lugar nenhum da web. São Ticket, Peças, Markup, Desconto, TOP 30, Cadastros e Inadimplência, e na Produtividade conversão, 1ª visita, fora de rota, jornada, horários, TMA e TMD.
  - O número do Diretor deixa de bater com o farol de origem: no PC ele está no cartão.
- **O que o pedido dizia:** o U1 do `revisao-ux.md` diz "tirar `rc-valor` e `rc-leg` do cartão **quando o número estiver na faixa**". A condição se perdeu.
- **Por que os testes passam:** a fixture tem só 3 cartões em `res` e 1 em `prod` (`conftest.pacote_ficticio`), e `test_T0034_pagina_inicial.py:34` fixa `h.count("<article") == 3`. O caso real não é exercitado.
- **Correção sugerida:**
  - manter `rc-valor` e `rc-leg` no cartão quando ele não está na faixa (`loop.index0 >= 3`), usando o mesmo corte de `faixa_painel`, num lugar só;
  - ou levar todos os números para a faixa, se o UX decidir assim.
- **Teste novo:** um teste com 4 ou mais cartões por visão confere que todo `valor` do pacote aparece uma vez na página (cita RN/RD).

## 🟡 Corrigir antes do merge

### Y1 · A versão da web não subiu
- **Onde:** `web/app/__init__.py:2`, que segue em `VERSAO = "0.4.0"`, igual ao `origin/main`.
- **Por quê:** o código do app mudou (`main.py`, `render.py`, `bc3.js`, templates e CSS), e a `/` mudou de comportamento (a grade saiu, agora é um redirect).
- **Risco:** a regra 11 do CLAUDE.md compara a versão do `main` com a do `/saude`. Com a mesma versão, essa conferência não distingue o deploy novo do antigo.
- **Correção:** subir a versão, por exemplo para `0.5.0`.

### Y2 · A regra "quem vê o Painel" ficou escrita duas vezes
- **Onde:** `web/app/render.py:238`, `pagina_inicial`, fixa a tupla `("admin", "diretor", "gerente")`. A mesma regra já existe em `web/app/main.py:27` como `VERES`, que protege `/painel` e a lateral.
- **Risco:** se uma das duas mudar sem a outra, a `/` manda o perfil para `/painel` e ele cai no 403, ou o contrário.
- **Correção:**
  - passar a constante para `render`, por exemplo `render.VEEM_PAINEL`, e `main.VERES` passa a apontar para ela;
  - ou receber os perfis como parâmetro em `pagina_inicial`.

## 🟢 Sugestões
- **G1:** `render.BC3` (`render.py:209`) ficou morto. `pagina()` não consulta mais essa constante, e só `test_T0030_bc3.py:40` ainda a usa. Dá para remover os dois no mesmo lote.
- **G2:** na troca de senha obrigatória, `/senha` mostra a lateral completa com os faróis.
  - Não há dado exposto: `usuario()` manda tudo de volta para `/senha`.
  - Mesmo assim, são links que não levam a lugar nenhum. Sugestão: sem `nav` quando `u["trocar_senha"]`.
- **G3:** `du_do_painel` (`render.py:90`, regex `_DU`) lê o DU do texto livre `sub` do PC. Não recalcula nada, o que está certo.
  - Mas, se a frase do PC mudar, o DU some da faixa sem aviso.
  - Para um lote futuro: um campo estruturado (ndp/ndm) no pacote, que é mudança de contrato com o modulo-robo.
- **G4:** em `abas_no_celular`, com uma aba inválida, o celular mostra `[0, 1, 2]`. Antes mostrava `[0, 1]`. É inofensivo, mas é mudança de comportamento: vale um comentário.

## Conferidos sem achado
- **Redirect por perfil:** `/` responde 302.
  - admin, diretor e gerente vão para `/painel`;
  - pré-venda vai para `/farol/pv_pedidos`, pós-venda para `/farol/pl_entregas` e vendas para `/farol/vc_visitas`, pela ordem de `GRUPOS_MENU`;
  - perfil desconhecido vai para `/senha`.
  - Sem login, a `/` leva ao `/login`. Com troca obrigatória, leva ao `/senha`.
  - O teste é parametrizado pelos 6 perfis.
- **403:**
  - `/painel` segue com `usuario(request, VERES)`;
  - o farol e a parcial seguem com a checagem de `FAROIS[rid][1]` (o teste de vendas na parcial de Pedidos dá 403);
  - a página de acesso negado usa `u=None` e por isso não mostra a lateral.
  - Nenhuma tela ficou exposta a perfil errado: a lateral vem de `menu_lateral` (perfil), e o Usuários segue só para admin.
- **Desativar:** a confirmação usa `<details>`, sem JS. O POST é o mesmo (`acao=desativar`, `login`, `csrf`) e o handler `usuarios_post` não mudou. O teste confere que não há `value="desativar"` fora da confirmação. O `<option value>` do perfil manda o mesmo valor de antes.
- **CSP:** segue `default-src 'self'`, sem `unsafe-inline` para script. Os templates não têm script inline nem `on*=`: só `/static/bc3.js` e `/static/parcial.js`. A logo do login vem de `/static/logo_bap.png`.
- **Login e senha:** o CSRF está em todos os formulários (login, senha, usuários, sair). Sessão, cookie, bloqueio por tentativas e a derrubada de outra sessão na troca de senha não mudaram, e os testes de sessão foram só reapontados de `/` para `/painel`.
- **Dados pessoais:** as fixtures são fictícias (`gerente.um`, valores inventados), sem CNPJ, telefone ou e-mail.
- **Regras do repositório:**
  - `bap_dados.VERSAO = 27`;
  - nenhuma base congelada, config `.json` ou dado digitado no diff;
  - os donos estão OK.
- **Redundância resolvida:**
  - `kpis_da_faixa` e `kpis_do_corpo` têm a mesma semântica dos filtros Jinja que substituem;
  - `abas_no_celular` é uma regra só;
  - os macros de `_faixa.html` não repetem a faixa;
  - `fmt_manaus_curto` é reusado em `hhmm`.

## [SUPOSIÇÃO]
- O número de cartões por visão (10/10/6) foi lido em `painel_rrm.py` do head, sem rodar o PC.
- Não houve print novo para esta revisão. O 🔴 foi provado por HTML no teste avulso.
