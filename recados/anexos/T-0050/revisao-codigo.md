# T-0050 — Parecer do revisor-codigo

- **Branch:** `modulo-web/T-0050-acesso-usuario` · **head SHA revisado:** `a5e723be225dc8f31755c8864bbf7bec8395c868` · **base:** `origin/main` `4fc6429` (web 0.8.0)
- **Desenho:** `docs/desenho/T-0050.md` (engenheiro-software/T-0050-desenho, `8a91c11`). Decisões: P1 B, P2 A, P3 A, P4 A.
- **Data:** 27/11/2026 (Manaus). Este parecer vale só para o head acima: um commit novo pede revisão nova.

## Resultado: **não aprovado**. Nenhum 🔴, 2 🟡 e 8 🟢.

## 🟡 Corrigir antes do merge

1. **`GET /farol/vc_painel` dá 500 (KeyError) onde antes dava 403.** Ref.: `web/app/main.py:827` (`exige`), `:839` (`nome = render.FAROIS[rid][0]`).
   - **Por quê:** o `acesso.pode_ver` aceita o `vc_painel`, que está em `rids_da_lista()`. Assim, `exige(u, rid)` deixa passar o rid do Painel pelas rotas `/farol/{rid}`.
   - **Quem é afetado:** quem vê o Painel (admin, gerente, analista, diretor e quem o recebeu por "mais").
   - **O que acontece:** a rota grava uma linha em `acessos/` com o rid `vc_painel` e cai em `render.FAROIS["vc_painel"]`.
   - **Efeito ao lado:** no admin, o `/farol/vc_painel/editar` passou de 403 a 404.
   - **Prova:** a comparação antes × depois abaixo mostra `admin|gerente|analista|diretor /farol/vc_painel 403 -> EXC:KeyError`.
   - **Correção sugerida:** nas rotas `/farol/{rid}` (`farol` e `/linhas`, `editar_get`, `editar_post`, `tabelas_para_exportar`), exigir também `rid in render.FAROIS`. Pode ser um `exige_farol(u, rid)`, ou o `exige` com `rid != acesso.PAINEL`. O `/painel` continua com o `exige(u, PAINEL_RID)`.
   - **Teste a acrescentar:** `/farol/vc_painel`, `/farol/vc_painel/linhas`, `/farol/vc_painel/editar` e `/farol/vc_painel/exportar?formato=xlsx` dão 403 para o admin.

2. **A tela "Atualizar visitas" abre para quem recebeu o Visita por "mais".** Ref.: `web/app/main.py:1141-1147` (`visitas_tela`).
   - **O que acontece:** `GET /visitas/atualizar` dá 200 para pre_venda, pos_venda e trade com o `vc_visitas` liberado. A tela não tem dado pessoal (`visitas.tela()`), mas não é o Resumo.
   - **O que o desenho e a decisão dizem:** a §5 do desenho põe "Atualizar visitas 403" para quem é de fora, e a P4 A diz que o liberado vê só o Resumo.
   - **O link:** o item da lateral já some, porque `PODEM_PEDIR` ⊂ perfis do Visita. Só a URL direta abre.
   - **Correção sugerida:** manter o `exige(u, "vc_visitas")` e acrescentar o corte por perfil `if not acesso.perfil_ve(u["perfil"], "vc_visitas"): raise PermissionError`. Isso preserva diretor e vendas, que já abriam a tela antes. Não use `PODEM_PEDIR` no GET: diretor e vendas perderiam o acesso que têm hoje.
   - **Teste a acrescentar:** pre_venda com `vc_visitas` em "mais" leva 403 no `GET /visitas/atualizar`; vendas e diretor do padrão levam 200; nos POST, o 403 continua.

## 🟢 Sugestões

1. **Parcial de Pedidos e de Visita para o liberado (200).** É o que diz a §6, item 4, do desenho, mas apoiado numa [SUPOSIÇÃO]: que essas imagens do PC não têm cliente nem meta RH. Vale o `testes` ou o po confirmar com uma imagem real. A de Entregas está corretamente em 403.
2. **Falta teste da falha no passo 1 do registro.** Hoje só a falha do `_salvar` tem teste. Caso a cobrir: `acrescentar_linha` falha, a resposta é 503, o `usuarios.json` não muda e, no `criar`, o usuário não fica na memória.
   - Caso extremo: o `desfeito` também falha. Fica uma linha órfã que o `ultima_mudanca` mostraria como mudança. É o melhor esforço que o desenho aceitou; fica só registrado.
3. **`ultima_mudanca` relê o `.jsonl` inteiro para cada usuário** a cada `GET /usuarios` (`usuarios.py`, chamado por `linhas_usuarios`). O arquivo não tem retenção. Ler uma vez por requisição e montar o mapa login → última mudança resolve.
4. **Redundância:** `acesso.contagem` refaz a conta de `visiveis` e `padrao_do_perfil`. Com `pad = padrao_do_perfil(p)` e `vis = visiveis(p, acesso)`, bastaria `(len(pad - vis), len(vis - pad))`.
5. **Redundância:** o `acesso.pode_ver(u, rid)` dentro do `correcao=` de `farol_abas` (`main.py:405`) repete a checagem que o `exige` da rota já fez.
6. **Versão da web:** vai de 0.8.0 direto a 0.10.0, pulando a 0.9.0 que o desenho previa para o #158. Confirmar que é intencional.
7. **Tela:** o pacote de revisão não traz o print do head. A conferência da tela fica com o parecer do designer-ux no mesmo SHA.
8. **T-0025 v2 (`vc_champions`, `RESTRITAS`):** quando entrar, falta o `test_RN_GER_015_liberado_sem_total_a_pagar` da §11. Hoje o `TOTAL A PAGAR` não existe no código; no teste do liberado, a página não tem o texto.

## Conferido sem achado

- **O pedido foi atendido, sem mudança a mais.** Só `web/**` mudou (12 arquivos). `node scripts/coord.mjs verificar --base origin/main` na head dá "nenhuma violação para modulo-web".
- **Dados digitados e configs intocados:** `_EDICOES_POS_VENDA`, `_NCC`, `_GARANTIAS`, `_AUTORIZACOES`, `champions_config.json`, `transportadoras_config.json`, `painel_diretor_config.json` e `planner_config.json`. `bap_dados.py` segue com `VERSAO = 27`.
- **Segredos:** nenhuma chave, senha ou token no diff. Nenhum arquivo de chave foi lido.
- **`pode_ver` com rid desconhecido dá falso** (`acesso.py`: `rid not in rids_da_lista()`). O rid inerte fica guardado pelo `normalizar`, como diz a §7. Há teste.
- **Nenhuma rota de farol escapa do `pode_ver`.** Passam por ele as 12 rotas: `/farol/{rid}` e `/linhas`, `/exportar`, `/parcial`, `.png` e `.pdf`, `/editar` (GET e POST), o CSV, a correção, a cobrança, o `/painel` e `/visitas/*`. O teste estrutural acha as rotas pelo AST, e não sobrou nenhum `FAROIS[rid][1]` nem `VERES` no `main.py`.
- **O liberado além do perfil não vê dado de cliente.** Rodei um usuário de cada perfil com tudo em "mais":
  - deram 403 todas as abas de tabela e `/linhas`, o Exportar (xlsx, pdf e `todas`), o `/editar`, o CSV, a correção, a cobrança e as ações de `/visitas/*`;
  - "Exportar" não aparece no HTML;
  - o motivo é que os cortes de dado são listas brancas, e o liberado não está em nenhuma: `tabelas.VE_TABELAS[rid]` ⊆ `FAROIS[rid][1]` em todos os faróis, e `cobranca.VE_TABELAS` e `COBRA` ⊆ os perfis da Inadimplência.
- **O admin não tira Usuários de si mesmo.** Usuários e Trocar senha não estão em `rids_da_lista()`, e o `/usuarios` segue pelo perfil admin. Há teste.
- **CSRF:** o `acao=acesso` e o `criar` passam pelo `formulario()` (`hmac.compare_digest`). Há teste com CSRF errado (403) e com usuário que não é admin (403). Nos `/visitas/*`, a ordem é `usuario`, depois `exige`, depois o CSRF.
- **O registro não leva dado de cliente.**
  - O `usuarios_acesso.jsonl` só tem as chaves `quando`, `lote`, `quem`, `alvo`, `perfil`, `rid`, `mudanca`, `origem` e `acao`, sem IP. O teste confere as chaves.
  - No log, só "acesso de usuário alterado" e "falha ao gravar", sem login.
  - O registro só cresce: o teste confere byte a byte.
- **A falha de gravação não deixa json e registro divergentes:**
  - o registro é gravado antes do json, com `flush` e `fsync`;
  - se o json falha, entra a linha `desfeito`, a tela dá 503 e a memória volta ao estado anterior (`u["acesso"] = antes`; no `criar`, `pop`);
  - o `ultima_mudanca` ignora os lotes desfeitos.
- **Nenhum perfil existente perde acesso.** Comparei 8 perfis × 692 pontos, sem exceções, no `main` `4fc6429` e na head, com o mesmo pacote (Painel completo e 3 faróis). Entraram:
  - o menu e a página inicial;
  - o `/painel` e cada `/farol/{rid}`, com todas as abas, `/linhas` e Exportar;
  - a parcial, o `/editar`, o CSV, a correção, `/visitas/atualizar` (GET e POST) e a cobrança.

  Menu e página inicial deram iguais nos 8 perfis. As únicas diferenças são as do 🟡 1 (`/farol/vc_painel`).
- **`/visitas/*`:** os 5 POST e o GET exigem `pode_ver("vc_visitas")`, inclusive as ações só do admin (`acao_visitas`). Com `vc_visitas` em "menos", o admin leva 403 (há teste).
- **Número do Diretor:** o Painel e os cartões não mudaram. Só mudou quem abre a tela.
- **Testes:** `pytest web/tests` numa cópia (worktree da head) deu **597 passed**, 0 falhas. `compileall` limpo. Os 22 testes novos citam a RN-GER-018.

## Como reproduzir

- Crie os worktrees com `git worktree add <dir> origin/main` e `git worktree add <dir> a5e723b` (os da revisão já foram removidos).
- Os scripts da comparação ficam em `/tmp/claude-0/rev50/scripts/`:
  - `test_zz_cmp.py`: antes × depois por perfil;
  - `test_zz_lib.py`: o liberado.
- Para rodar, copie os scripts para `web/tests/` e use `CMP_OUT=<arquivo.json> pytest web/tests/test_zz_cmp.py`.
- Saídas em `/tmp/claude-0/rev50/antes.json`, `depois.json` e `lib.json`.

---

# Reteste — head `e0a17f6e2c063a17d00a1a1a5d98f938976f6a22` (27/11/2026, Manaus)

- **Delta revisado:** `a5e723b..e0a17f6`. São o `36b059e` (correções) e o merge do `origin/main` `d2cd695`. O merge não mexe em `web/`; contra o `origin/main`, a branch só altera `web/**` (12 arquivos).
- **Este parecer vale só para `e0a17f6`.**

## Resultado: **aprovado**. Nenhum 🔴 e nenhum 🟡 em aberto.

## Os dois 🟡 do primeiro parecer foram resolvidos
1. **`/farol/vc_painel`.** O novo `exige_farol` (`main.py`) e o `rid not in render.FAROIS` em `tabelas_para_exportar` e no `editar` (GET e POST) devolvem 403 a todo rid fora de `render.FAROIS`. O `/painel` segue com `exige(u, PAINEL_RID)`. O teste `test_RN_GER_018_vc_painel_nao_e_rota_de_farol` cobre `/farol/vc_painel`, `/linhas`, `/editar` (GET e POST) e `/exportar`. Na comparação, os 5 pontos que tinham mudado voltaram a ser iguais ao main (403).
2. **`/visitas/atualizar`.** O `GET` agora exige `pode_ver` e também `perfil_ve(perfil, "vc_visitas")`.
   - O liberado (pre_venda, pos_venda, trade) leva 403.
   - Vendas, diretor, gerente e analista do padrão continuam com 200.
   - Teste: `test_RN_GER_018_atualizar_visitas_so_de_quem_tem_o_farol_pelo_perfil`.

## O resto do delta, conferido
- **🟢 4 e 5 resolvidos.**
  - O `contagem` agora usa `visiveis` e `padrao_do_perfil`.
  - Saiu o `pode_ver` redundante em `correcao`.
  - O `normalizar` foi absorvido pelo `excecoes(perfil, marcados, antigo)`. O resultado é equivalente: o rid inerte continua guardado, e há teste.
- **RD-0182 a 0191.**
  - `render.nome_curto`, `NOME_PAINEL` e `GRUPO_PAINEL` passam a ser a fonte única.
  - A `pagina_inicial` recebe o `padrao`, e o caso "só o Painel liberado" fica dentro dela. É equivalente ao que o `home` fazia antes.
  - O `menu_lateral` recebe `atualizar_visitas`, calculado uma vez só no `pagina()`.
  - Saiu o `acesso.liberado`, que não era usado.
  - Os testes de versão leem `VERSAO`.
- **"Alterado em".** O `ultima_mudanca` devolve o ISO, e a tela formata com o filtro `manaus` (`fmt_manaus`). Se o ISO vier inválido, o filtro devolve o texto como está: não dá 500, e o Jinja escapa.
- **Comparação antes × depois, refeita.** Main `d2cd695` × head `e0a17f6`, 8 perfis × 692 pontos, sem exceções: **0 diferenças**. Isso inclui o menu, a página inicial e todas as rotas, `/farol/vc_painel` também.
- **O liberado, com tudo em "mais", por perfil.**
  - Dão 403: todas as abas de tabela e `/linhas`, o Exportar (xlsx, pdf e `todas`), o `/editar`, o CSV, a correção, o Cobrar, os POST de `/visitas/*` e agora o `GET /visitas/atualizar`.
  - "Exportar" não aparece na página.
  - Fica aberta a parcial de Pedidos e de Visita: é a decisão da §6, item 4 (🟢 1).
- **`pytest web/tests`** numa cópia da head: **599 passed**, nenhuma falha. `compileall` limpo.
- **`verificar --base origin/main`:** nenhuma violação para modulo-web.
- **Intocados:** os dados digitados e as configs. `bap_dados.VERSAO` segue em 27. Nenhum segredo no diff.

## 🟢 que continuam (não bloqueiam)
- 🟢 1: confirmar com uma imagem real que a parcial de Pedidos e a de Visita não têm cliente nem meta RH.
- 🟢 2: teste para a falha no primeiro passo do registro (`acrescentar_linha`).
- 🟢 3: o `ultima_mudanca` relê o `.jsonl` para cada usuário.
- 🟢 7: o print da tela fica com o designer-ux, no mesmo SHA.
- 🟢 8: quando a T-0025 v2 trouxer o `vc_champions`/`RESTRITAS`, entra o `test_RN_GER_015_liberado_sem_total_a_pagar`. Hoje não há `RESTRITAS` em `web/app`.

---

# Reteste 2 — head `8586ab77137c2fd3abc2be101abcb6bb9e2d3d81` (27/11/2026, Manaus)

- **Delta revisado:** `e0a17f6..8586ab7`, um commit só (RD-0210 a 0213 e UX 14). Mexe em 5 arquivos de `web/`. Contra o `origin/main` `d2cd695`, a branch continua alterando só `web/**`.
- **Este parecer vale só para `8586ab7`.**

## Resultado: **aprovado**. Nenhum 🔴 e nenhum 🟡.

## O delta, conferido
- **Exportar e editar (GET e POST):** agora chamam `exige_farol(u, rid)` e, depois, `if not rel` (exportar) e `if perfil not in edicoes.EDITA` (editar).
  - É a mesma condição de antes, só que dividida: toda falha continua sendo `PermissionError` (403).
  - A ordem foi mantida: o 403 do editar vem antes de ler o formulário, e o CSRF continua depois.
- **`PAINEL_RID`:** passou para o `render` (`"vc_painel"`). O `acesso.PAINEL` e o `main.PAINEL_RID` apontam para ele, e o valor não mudou.
- **Assert retirado:** saiu a linha `diretor` → `GET /visitas/atualizar` = 200 do teste da T-0050. A cobertura continua em `web/tests/test_T0045_visitas.py:414-416`, que testa o diretor com 200 e sem o botão.
- **CSS:** a regra `.u-novo-form>.f-rodape` foi juntada numa só, e entrou um `column-gap` no "Novo usuário" do Trade. Não muda nenhuma checagem.

## Testes
- **Comparação antes × depois refeita:** main `d2cd695` × head `8586ab7`, 8 perfis × 692 pontos, sem exceções. Entram o menu, a página inicial, `/painel` e cada `/farol/{rid}` com todas as abas, `/linhas` e o Exportar (incluindo `vc_painel` e um rid desconhecido). Entram também a parcial, o `/editar`, o CSV, a correção, `/visitas/atualizar` (GET e POST) e a cobrança. **Resultado: 0 diferenças.**
- **Teste do liberado refeito** (um usuário de cada perfil com tudo em "mais"):
  - deram 403 todas as abas de tabela e `/linhas`, o Exportar (xlsx, pdf e `todas`), o `/editar`, o CSV, a correção, o Cobrar, os POST de `/visitas/*` e o `GET /visitas/atualizar`;
  - "Exportar" não aparece na página;
  - o resultado é idêntico ao do `e0a17f6`;
  - continua aberta só a parcial de Pedidos e de Visita, que é a decisão da §6, item 4 (🟢 1).
- **`pytest web/tests`** numa cópia da head: **599 passed**, nenhuma falha. `compileall` limpo.
- **`verificar --base origin/main`:** nenhuma violação para modulo-web.
- **Intocados:** `bap_dados.VERSAO` segue em 27. Nenhum segredo no diff. Dados digitados e configs não foram tocados.

## 🟢 que continuam (não bloqueiam)
Os mesmos do reteste anterior:
- 🟢 1: a parcial de Pedidos e de Visita, sem cliente (confirmar com uma imagem real).
- 🟢 2: teste para a falha no primeiro passo do registro.
- 🟢 3: o `ultima_mudanca` relê o `.jsonl` para cada usuário.
- 🟢 7: o print da tela fica com o designer-ux.
- 🟢 8: o `test_RN_GER_015` entra com a T-0025 v2.
