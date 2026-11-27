# T-0034 · Parecer de redundância e excesso (corretor-redundancias)

- **Escopo:** `git diff origin/modulo-web/T-0033-revisao-geral...origin/modulo-web/T-0034-pagina-inicial` (20 arquivos, +397 −168), lido no estado do head da T-0034, mais as telas em `sim-t0034/depois` (painel-admin, painel-diretor, painel-diretor-faturamento, parcial, usuarios, senha, login; PC 1366 e celular 390).
- **Head SHA revisado:** `b60cae167bb86d9e4f6add926fd574a725854a74`.
- **Numeração:** o último RD usado é o RD-0062 (anexos da T-0033). Este parecer usa do RD-0063 ao RD-0068.
- **Resultado:** **não libera**. Há 6 achados novos e 2 achados antigos ainda abertos (RD-0038 no código e RD-0059).
- **Dono de todos os achados:** modulo-web (`node scripts/coord.mjs dono web/...`).

## 1. Situação dos achados que a T-0034 devia fechar

| RD | Situação | Evidência |
|---|---|---|
| RD-0038 (nome único "Painel Executivo") | **Aberto no código; fechado na tela.** Na tela, o h1 é sempre "Painel Executivo" (`_painel_cab.html:7`, `painel.html:7`), as abas não têm mais "Painel ·" e a chave `visitas` aparece como "Visitas" (`PAINEL_CURTO`). Faltam os 2 itens de código da proposta: (1) `render.TITULOS` (`render.py:18-20`) ainda devolve "Painel Executivo · resultado/produtividade/por dia útil" em `aba_para_tela` (`:161`), e nenhum template mostra `tela.titulo`, então é código morto com o nome antigo; (2) `render.PAINEIS` (`:86-88`) ainda chama a chave `visitas` de "Produtividade" e a `itens` de "Itens por pedido". `PAINEL_CURTO` (`:90-92`) passa por cima nas 9 chaves, e ficam 2 tabelas de nomes para as mesmas abas. A docstring de `render.py:1` ainda diz "Painel · resultado e Painel · produtividade". | `painel-admin__pc1366.png`, `painel-diretor-faturamento__pc1366.png` |
| RD-0043 (um layout só em `base.html`) | **Fechado.** `base.html` tem uma casca só (com ou sem lateral); `/` redireciona por perfil (`render.pagina_inicial`); saíram `home.html`, o menu de `main.home`, o CSS `.menu`, `.quadro` e `.quadro.indisp` e a flag `bc3`. As sobras do layout antigo (CSS e bloco `mainclass2`) estão no RD-0066. `render.BC3` (`render.py:186`) continua no RD-0044, ainda aberto: o único uso agora é `test_T0030_bc3.py:40`. | `login__pc1366.png`, `senha__pc1366.png`, `usuarios__pc1366.png` |
| RD-0059 (Parcial sem a lateral repetida) | **Aberto.** A faixa BC3, os botões `.bc3-bt` e a saída de `.acoes-farol` e `cab-painel` estão feitos. O link "Voltar ao farol" **não saiu**: agora aparece 2 vezes no template, como botão no estado vazio (`parcial.html:10`) e no grupo de ações (`parcial.html:18`), e a lateral já mostra "Pedidos" ativo (`parcial__pc1366.png`). O comentário da linha 5 ("a lateral da casca já é o menu") contradiz o código. | `parcial__pc1366.png` |

**Proposta para o RD-0059 (refeita):**
- `parcial.html:10`: **antes:** `<p><a class="bc3-bt" href="/farol/{{ rid }}">Voltar ao farol</a></p>` → **depois:** a linha sai (o estado vazio fica com uma frase só: "A parcial ainda não chegou do PC.");
- `parcial.html:18`: **antes:** `<a class="bc3-bt" href="/farol/{{ rid }}">Voltar ao farol</a>` → **depois:** a linha sai;
- `estilo.css:594`, `.bc3-corpo>p>.bc3-bt{display:inline-flex}`, sai junto (só servia ao botão do estado vazio).

**Proposta para o RD-0038 (o que falta):**
- `render.py:18-20`: `TITULOS` sai; `aba_para_tela` (`:161`) deixa de devolver `"titulo"`;
- `render.py:86-88`: **antes:** `PAINEIS = (("resumo", "Resumo gerencial"), …, ("visitas", "Produtividade"), …, ("itens", "Itens por pedido"), …)` → **depois:** `PAINEIS = (("resumo", "Resumo"), ("faturamento", "Faturamento"), ("volume", "Volume"), ("visitas", "Visitas"), ("positivacao", "Positivação"), ("itens", "Itens"), ("markup", "Markup"), ("preco", "Preço"), ("inadimplencia", "Inadimplência"))`, e `PAINEL_CURTO` fica só com as 3 abas RRM (`{"resultado": "Resultado", "produtividade": "Produtividade", "por_dia_util": "Por DU"}`). Outra saída aceita: `PAINEIS` guarda só as chaves e `PAINEL_CURTO` é a fonte única dos nomes;
- `render.py:1`: **antes:** "Renderizador do cartão RRM (Painel · resultado e Painel · produtividade)." → **depois:** "Renderizador do Painel Executivo (cartões RRM e abas de painel).".

## 2. Achados novos

### RD-0063 · Painel Executivo, abas RRM: a faixa repete o número grande e os anéis dos 3 cartões logo abaixo
- **Onde:** `render.faixa_painel` (`render.py:96-107`) e `painel.html:23-25` e `:27-41`; telas `painel-admin__pc1366.png` e `painel-diretor__cel390.png`.
- **Tipo:** indicador · texto.
- **O que se repete:** na aba Resultado, cada número de cabeça aparece 2 vezes, na faixa e no cartão: "FATURAMENTO LÍQUIDO · PROJ. R$ 165 mil MTD 11% · MÊS 100%" na faixa e "R$ 165 mil", anel MTD 11% e anel MÊS 100% no cartão. O mesmo vale para "POSITIVAÇÃO 45 MTD 40% · MÊS 93%" e "PEDIDOS FATURADOS · PROJ. 85 projeção do mês": são 3 cartões × 3 números = 9 repetições por aba (as 3 abas RRM). Na faixa, "PEDIDOS FATURADOS · PROJ." e "projeção do mês" dizem o mesmo duas vezes. No celular, a faixa e o 1º cartão ficam empilhados com os mesmos números.
- **Impacto:** leitura e espaço acima da dobra (no celular, a faixa ocupa 460 px de 1688 só com números repetidos). Fere a regra 1 ("uma informação, um lugar") e o parecer de UX da T-0033, §5.2: "Cartões: sem o número grande, que subiu para a faixa".
- **Severidade:** média.
- **Proposta:**
  - `painel.html:24-25`: **antes:** `<div class="rc-valor">{{ c.valor }}</div>` e `{% if c.legenda %}<div class="rc-leg">{{ c.legenda }}</div>{% endif %}` → **depois:** as 2 linhas saem. O cartão fica com título, anéis MTD/MÊS, faixa de variação e barras por estado;
  - `render.py:104`: **antes:** `det = " · ".join(f"{a['rot']} {a['pct']}" for a in aneis) or c["legenda"]` → **depois:** `det = c["legenda"] if any(ch.isdigit() for ch in c["legenda"]) else ""`. Os anéis ficam só no cartão; na faixa sobra só o detalhe que traz número próprio ("projeção do mês 66"), e "projeção do mês" sem número sai, porque o rótulo já diz "PROJ.";
  - o `testes` confirma que o número do Diretor na faixa continua batendo com o farol de origem (o valor não muda, só sai do cartão).

### RD-0064 · Painel sem pacote: dois avisos para o mesmo estado
- **Onde:** `base.html:34` ("Ainda não chegou nenhum pacote do PC.") e `painel.html:11-12` ("Sem dados ainda. A primeira atualização chega às 06h30."), juntos em `/painel` sem pacote (o `test_painel_sem_pacote_diz_quando_chega` cai nesse caso).
- **Tipo:** texto (estado vazio).
- **O que se repete:** o mesmo fato, com 2 textos, 2 vezes na mesma tela.
- **Impacto:** poluição. Além disso, quando o pacote chega sem o painel, "A primeira atualização chega às 06h30" fica sem sentido (se for o caso, o valor do texto é do `testes`).
- **Severidade:** média.
- **Proposta:** igual ao farol (RD-0040):
  - `base.html:34`: **antes:** `Ainda não chegou nenhum pacote do PC.` → **depois:** `Sem dados ainda. A primeira atualização chega às 06h30.` (uma frase global, a do contrato);
  - `painel.html:11-12`: **antes:** `{% if not tela and not tela_f %}<p class="aviso atencao">Sem dados ainda. A primeira atualização chega às 06h30.</p>` → **depois:** `{% if not tela and not tela_f %}{% if gerado_em %}<p class="aviso atencao">O painel não veio no último pacote do PC.</p>{% endif %}`;
  - o teste passa a conferir `h.count("Sem dados ainda") == 1`.

### RD-0065 · O cabeçalho do Painel (`_painel_cab.html`) é uma cópia do cabeçalho do farol (`_bc3_cab.html`), e a regra "cartão comum × rico" está em 3 lugares
- **Onde:**
  - `_painel_cab.html:8` × `_bc3_cab.html:20`: data com `title`;
  - `:9` × `:21`: selo "Desatualizado", linha idêntica;
  - `:10-14` × `:22-26`: filtro BAP/UF;
  - `:15-16` × `:28-29`: seletor desligado, com **2 textos para o mesmo fato** ("Esta aba é só da BAP inteira" × "Esta aba mostra a BAP inteira");
  - `:19-23` × `:32-36`: os números da faixa, linha idêntica;
  - `:24-38` × `:44-47`: a barra de abas (3 no celular + "Mais");
  - mais: `_faixa_simples.html:6` é o 3º laço de números, e `painel.html:7` (faixa vazia escrita à mão) é igual a `faixa_simples("Painel Executivo")`;
  - a regra "comum vai à faixa, rico fica no corpo" está em `render.faixa_painel:100`, em `_bc3_cab.html:10` (`rejectattr('estados')|rejectattr('linhas')`) e em `_resumo.html:5` (`ricos`).
- **Tipo:** código (componente reimplementado) · texto (aviso com 2 redações).
- **O que se repete:** 6 blocos de marcação em 2 cabeçalhos, mais 1 laço e 1 faixa vazia; a regra de separação 3×. O parecer de UX da T-0033 (§5.3, "`painel.html`: a faixa via `_bc3_cab.html`") pedia um cabeçalho só.
- **Impacto:** manutenção. Todo ajuste de faixa (altura, contraste G7, selo) é feito 2 a 3 vezes, e os textos já divergiram.
- **Severidade:** média.
- **Proposta:**
  - `templates/_faixa.html` com os macros `quando(gerado_em, extra="")`, `selo_velho()`, `filtro_uf(base, ufs, uf, ufs_off)` (que também cobre o RD-0044) e `numeros(ks)`;
  - `_bc3_cab.html`, `_painel_cab.html` e `faixa_simples` passam a chamar os macros; `painel.html:7` vira `{{ faixa_simples("Painel Executivo") }}`;
  - texto único do seletor desligado: `title="Esta aba mostra a BAP inteira"`;
  - `render.kpis_da_faixa(kpis)` e `render.kpis_do_corpo(kpis)` (funções puras) são usadas por `faixa_painel`, pelo `main.farol` e pelos 2 templates, no lugar dos 3 filtros.

### RD-0066 · Sobras do layout antigo, constantes e parâmetros mortos
- **Onde e o que sobra:**
  - `render.AVISO_SO_BAP` (`render.py:93`): nenhuma tela usa; o único uso é `test_T0022_painel_meta.py:73` (`assert render.AVISO_SO_BAP not in h`);
  - `main.RELATORIO[1]` (`main.py:28`, "Painel Executivo"): sem uso depois que a home saiu; `"vc_painel"` está escrito de novo em `pagina()` (`main.py:148`), e `request.url.path == "/painel"` aparece 2 vezes em `pagina()` (`:148` e `:160`);
  - `base.html:37` `{% block mainclass2 %}`: nenhum template preenche;
  - `_faixa_simples.html:3`, parâmetro `quando`: nenhuma chamada usa (`senha`, `parcial`, `editar`, `usuarios`);
  - CSS do layout antigo, morto ou vencido:
    - `.sair` (`estilo.css:105`, `:285`): o form agora é `.bc3-eu`;
    - `main{…}` (`:106`, `:288`, e `main{padding:.6rem}` em `:534` e `:544`): o único `<main>` é `.bc3-corpo`, e `main.bc3-corpo` (`:379`) sobrescreve `max-width`, `margin` e `padding`;
    - `main.larga` (`:250`): o bloco `mainclass` saiu do `farol.html`;
    - `.selo-velho` (`:428`): saiu com o layout antigo do `base.html`;
    - `.aviso.info.faixa-pc` (`:287`);
  - CSS novo da T-0034: dois blocos `@media(max-width:700px)` novos (`:586` e `:595`), além do `:488`, e a mesma declaração 2× para o mesmo elemento (`.bc3-uf-claro{margin-left:0}` e `.bc3-sub>.bc3-uf{margin-left:0}`, `:584` e `:585`);
  - comentários desatualizados: `render.py:193` ("mesma regra do menu da página inicial": não há mais menu na página inicial) e `render.py:183-185` (o BC3 "vai primeiro" no Pedidos).
- **Tipo:** código.
- **Impacto:** manutenção. As regras vencidas confundem o próximo ajuste visual (a origem do RD-0036 e do RD-0045).
- **Severidade:** média (código); baixa (comentários).
- **Proposta:**
  - saem `AVISO_SO_BAP` (e a parte do teste que o cita), o bloco `mainclass2`, o parâmetro `quando`, as regras `.sair`, `main{…}` (as 4), `main.larga`, `,.selo-velho` e `.aviso.info.faixa-pc`;
  - `main.py:28`: **antes:** `RELATORIO = ("vc_painel", "Painel Executivo")` → **depois:** `PAINEL_RID = "vc_painel"`, usado em `:148` e `:269`; em `pagina()`, `no_painel = request.url.path == "/painel"` uma vez só;
  - CSS da T-0034: as regras de `:586-593` e `:595` entram no bloco `@media(max-width:700px)` de `:488`; fica só `.bc3-sub>.bc3-uf{margin-left:0}`;
  - `render.py:193`: **antes:** "(mesma regra do menu da página inicial)" → **depois:** "(fonte única do menu; a página inicial usa `pagina_inicial`)"; `render.py:183-185` sai junto com `BC3` (RD-0044).

### RD-0067 · Testes novos que repetem testes existentes
- **Onde:**
  - `test_T0034_pagina_inicial.py:29` `test_home_segue_a_ordem_do_menu_lateral`: repete o parametrizado de `:19-26` (mesmos 3 perfis, mesma função) e refaz a regra dentro do teste;
  - `:36` `test_home_sem_login_vai_para_o_login` = `test_web.py:35` `test_rotas_exigem_login` (que já cobre `/`, com o mesmo 303 → `/login`). É o 5º teste de "sem login" (RD-0061);
  - `:41` `test_painel_403_para_quem_nao_e_da_diretoria` = `test_T0022_painel_meta.py:94` `test_perfis_do_painel_e_do_farol_de_metas` (vendas, pos_venda e pre_venda → 403) e `test_farois.py:125-133`;
  - `:109` `test_usuarios_403_fora_do_admin` = `test_web.py:94` `test_perfil_gerente_nao_ve_usuarios` (gerente → 403) e `test_farois.py:136`;
  - `:13-16`, fixture `com_painel`, copiada de `test_T0022_painel_meta.py:21-24`;
  - `test_T0022_painel_meta.py:66-67` e `:72-74`: a mesma URL buscada 2 a 3 vezes no mesmo teste;
  - títulos desatualizados (baixa, não seguram o lote):
    - `test_T0022_painel_meta.py:178` `test_home_lista_o_farol_de_metas_para_vendas` (a home não lista mais nada) → `test_lateral_de_vendas_tem_o_farol_de_metas`;
    - `test_T0034_pagina_inicial.py:83` `test_trocar_senha_no_bc3_com_o_texto_no_subtitulo` (não confere o subtítulo, e a fixture `cli` não é usada) → `test_trocar_senha_no_bc3_com_um_titulo_so`;
    - docstring de `test_T0030_bc3.py:3` ("Por enquanto só o Farol de Pedidos (render.BC3)").
- **Tipo:** teste.
- **Impacto:** manutenção (cada mudança de perfil mexe em 3 a 4 testes).
- **Severidade:** baixa.
- **Proposta:**
  - saem `test_home_segue_a_ordem_do_menu_lateral`, `test_home_sem_login_vai_para_o_login`, `test_painel_403_para_quem_nao_e_da_diretoria` e `test_usuarios_403_fora_do_admin`;
  - `com_painel` vai para `conftest.py`, usado pela T-0022 e pela T-0034;
  - nos testes da T-0022, cada resposta é guardada numa variável e reusada;
  - os 3 títulos são renomeados como acima.

### RD-0068 · Usuários: o selo "Ativo" em toda linha repete a faixa "Ativos 6"
- **Onde:** `usuarios.html:29` (selo `selo-ok` "Ativo") e a faixa `:5-8` ("ATIVOS 6"); tela `usuarios__pc1366.png`.
- **Tipo:** texto · indicador.
- **O que se repete:** "Ativo" 6× na lista, mais o total na faixa. O estado normal marcado em toda linha esconde a exceção.
- **Impacto:** leitura. O admin age sobre a exceção ("Desativado", "Troca de senha pendente"), não sobre o normal.
- **Severidade:** média.
- **Proposta:**
  - `usuarios.html:29`: **antes:** `{% if x.ativo %}<span class="selo selo-ok">Ativo</span>{% else %}<span class="selo selo-cinza">Desativado</span>{% endif %}` → **depois:** `{% if not x.ativo %}<span class="selo selo-cinza">Desativado</span>{% endif %}`;
  - os testes `test_usuarios_selos_de_situacao` seguem verdes (eles conferem "Desativado").
- **Observação (não catalogada, para o designer-ux):** o botão "Trocar senha" de cada linha (senha de outro usuário) tem o mesmo rótulo do item "Trocar senha" da lateral (minha senha). Não é repetição, mas pode confundir; sugestão: "Nova senha" na linha.

## 3. Sem achado
- **Login:** logo, "BAP Central" e a empresa uma vez cada; o título não repete o botão.
- **Trocar senha:** título só na faixa; o form não repete o título.
- **Painel · abas de painel (Faturamento):** a faixa leva Real e Desafio comercial, e o corpo não os repete (`painel-diretor-faturamento__pc1366.png`).
- **Usuários:** "Desativar" com confirmação é redundância útil (ação destrutiva), e o `aria-label` do seletor desligado é acessibilidade (`manter`).
- **Faixa "Desativados 0 · Troca pendente 0":** `manter?`. O zero confirma que não há o que fazer e segue o parecer de UX §4 (faixa da mesma altura).

## 4. Para liberar
- Corrigir RD-0063 a RD-0068 (os títulos do RD-0067 podem ir no lote seguinte), o resto do RD-0038 e o RD-0059.
- Reteste: os PNG `painel-admin` (PC e celular), `parcial` (com e sem dados), `usuarios` e `/painel` sem pacote, mais `pytest web/tests` verde, no novo head SHA.

## Premissas
- [SUPOSIÇÃO] A Parcial com dados não está nos PNGs (só o estado vazio); o 2º "Voltar ao farol" (`parcial.html:16`) foi lido no código.
- [SUPOSIÇÃO] O caso "`/painel` sem pacote" (RD-0064) foi lido no código (`pagina()` deixa `gerado_em` vazio sem índice) e no teste `test_painel_sem_pacote_diz_quando_chega`; não há PNG dele.
- [SUPOSIÇÃO] "CSS morto" foi conferido por busca das classes em templates, JS e `.py`. As classes montadas (`t-*`, `c-*`, `tom-*`) foram tratadas como vivas.
