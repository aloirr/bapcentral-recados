# Revisão geral de redundâncias: site BAP Central (todos os faróis e telas)

- **Pedido:** R-20261126-174334-alexandre (item 1: corretor de redundância em todos os faróis).
- **Código revisado:** `main` em **c8f6004** (T-0031), extraído com `git archive` para `.../scratchpad/revisao-geral/src/`. Nenhum arquivo do repositório foi alterado.
- **Escopo:** `web/app/` inteiro (rotas, 17 templates, `estilo.css`, `bc3.js`, `render.py`, `tabelas.py`, `cobranca.py`, `edicoes.py`, `pacotes.py`, `exportar.py`), `web/tests/` e a parte web do `bap_automation.py` (linhas 6593 a 7760).
- **Telas:** 73 páginas geradas com a fixture fictícia (`web/simular_farol.paginas` + fixtures de `web/tests`), nos perfis admin, gerente, diretor, pre_venda, pos_venda e vendas. Cada página foi capturada no PC 1366×768, no PC 1920×1080 e no celular 390×844, com a tela inteira no 1366 e no 390: 365 PNG em `.../scratchpad/revisao-geral/telas/`. Os textos visíveis de cada página estão em `.../scratchpad/revisao-geral/textos.json`.
- **Scripts:** `.../scratchpad/revisao-geral/scripts/gerar_html.py` e `fotos.mjs` (Chromium do `/opt/node-tools`, nada instalado).
- **Ferramentas:** pylint e vulture não estão instalados. A duplicação foi medida com dois scripts próprios, `dup.py` (janelas de 4 linhas) e `cssdup.py` (seletor × @media).
- **Numeração:** o último RD usado era o RD-0031 (`grep -rho "RD-[0-9]*"` no repositório e nos recados). Este parecer usa do RD-0032 ao RD-0062.

`P` = `.../scratchpad/revisao-geral/telas/` (caminho absoluto: `/tmp/claude-0/-home-user/4f3da797-8ad2-51e5-b58d-a720ae0afc4c/scratchpad/revisao-geral/telas/`).

## Resumo

| Prioridade | Qtd | RDs |
|---|---|---|
| alta | 6 | 0032 · 0033 · 0034 · 0035 · 0036 · 0037 |
| média | 16 | 0038 a 0053 |
| baixa | 9 | 0054 a 0062 (0060 e 0062 marcados `manter?`) |
| **total** | **31** | |

| Dono | RDs |
|---|---|
| modulo-web | 0032 a 0040, 0043 a 0051, 0053 a 0059, 0061, 0062 (e parte de 0041, 0042, 0052, 0060) |
| modulo-robo | 0039 (aviso), 0041, 0042, 0052 (listas), 0060 |
| modulo-farois | 0035 (alternativa no PC), 0038 (títulos das abas do PC) |
| testes | 0037 (teste de igualdade), 0052 (testes de espelho); recado sobre o valor errado do RD-0032 |
| design-de-marca · designer-ux | parecer sobre 0043 e 0058 (layout único e marca) |

**Parecer:** o lote **não sai** com estes achados em aberto. Pela regra de liberação, só baixa em comentário ou título de teste não segura; nenhum dos 31 é desse tipo.

**Recados:** não enviados. O pedido foi "só auditoria". O gerente distribui (um recado por dono, cc gerente-projetos) ou me pede o envio.

---

## Alta

### RD-0032 · A contagem de linhas aparece 2 ou 3 vezes, e o rodapé erra acima de 100 linhas
- **Onde:** em todas as abas de tabela (BC3):
  - `_bc3_cab.html:30` põe "· N" na aba ativa;
  - `bc3.js:78-83` cria o rodapé `.bc3-rod` com "N pedidos" ou "N linhas".
  - Em Pedidos e Entregas, o cartão da faixa repete o mesmo número.
- **Tipo:** indicador · texto.
- **O que se repete:**
  - Pedidos: "PEDIDOS 21", "Pedidos · 21" e "21 pedidos", **3×** (`P/admin__pv_pedidos-pedidos__pc1366.png`, `..._cel390-inteira.png`);
  - Entregas: "ENTREGAS NO MÊS 18", "Entregas · 18" e "18 linhas", **3×**;
  - Títulos, Visita e Metas: "Títulos · 12" e "12 linhas", **2×**.
  - Em "Cliente a cliente" a aba diz "· 230" e o rodapé diz **"100 linhas"** (conta só as linhas da página do servidor), com "Página 1 de 3" logo abaixo (`P/admin__vc_visitas-cliente__pc1366.png`).
- **Impacto:** leitura e decisão. O rodapé contradiz a aba quando há mais de 100 linhas.
- **Proposta:**
  - **antes:** `bc3.js:78-83`
    ```js
    var rod = document.createElement("div"); rod.className = "bc3-rod";
    rod.textContent = tb.rows.length + (document.querySelector(".sem-rolagem") ? " pedidos" : " linhas");
    cima.after(rod);
    ```
  - **depois:** o bloco sai e fica só "· N" na aba.
  - Em `estilo.css` saem também `.bc3-rod`, `body.uma-tela .rolagem-dados.bc3-cima .bc3-rod` e `body.uma-tela .bc3-cima+.bc3-rod`.
  - O cartão da faixa fica: é indicador e muda com o filtro.
- **Dono:** modulo-web.
- **Recado ao testes:** o valor errado ("100 linhas" com 230) é escopo dele e não entra no catálogo.

### RD-0033 · "Cobrar no WhatsApp": o título aparece 2 vezes, há duas datas e um texto que explica o sistema
- **Onde:**
  - `farol.html:6`: faixa "Situação do PC até 24/11 08:07. O que você marcar aqui chega ao PC às 08h ou 14h.";
  - `_bc3_cab.html:13-14`: h1 "Farol de Inadimplência" e "Dados de 24/11/2026 08:30";
  - aba ativa "Cobrar no WhatsApp";
  - `_fila.html:21`: h1 "Farol de Inadimplência · Cobrar no WhatsApp" e o link "N já tratados hoje";
  - `_fila.html:31`: "Já tratados hoje (N)".
- **Tipo:** texto · layout.
- **O que se repete:**
  - o nome do farol 2× e o nome da aba 2×;
  - 2 horários diferentes (08:07 e 08:30) para "quando é o dado";
  - "já tratados hoje" com a contagem 2×.
  - No celular, só 1 cartão fica acima da dobra (`P/pos_venda__pl_inadimplencia-cobrar__cel390.png`, `..._pc1366.png`).
- **Impacto:** leitura, acima da dobra e regra 3 ("chega ao PC às 08h ou 14h" é o que o sistema faz por trás).
- **Proposta:**
  - `farol.html:6`: sai o bloco `faixa` da fila.
  - `_bc3_cab.html:14`: na aba `cobrar` a data vira a da fila: `{% if fila is defined %}Cobranças do PC até {{ pc_ate|hhmm }}{% else %}Dados de …{% endif %}`.
  - `_fila.html:21`:
    - **antes:** `<header class="cab-painel"><h1>{{ farol_nome }} · Cobrar no WhatsApp</h1><span>{{ n_fila }} clientes{% if n_tratados %} · <a …>{{ n_tratados }} já tratados hoje</a>{% endif %}</span></header>`;
    - **depois:** `<p class="cab-fila">{{ n_fila }} a cobrar</p>`. O total de tratados fica só no `summary` "Já tratados hoje (N)".
- **Dono:** modulo-web.

### RD-0034 · Com estado escolhido, "só na BAP inteira" aparece em cada cartão, e ainda há um aviso
- **Onde:**
  - `render.py:524` põe `detalhe: SEM_RECORTE` em cada cartão sem recorte;
  - `render.py:544` acrescenta o aviso `AVISO_UF`.
- **Tipo:** texto · indicador.
- **O que se repete:** em Pedidos com AM, "— só na BAP inteira" aparece **5×** na faixa, mais "Resumo e gráficos: BAP inteira." (`P/admin__pv_pedidos-resumo-AM__pc1366.png`). É o mesmo fato 6 vezes.
- **Impacto:** a faixa verde, a área mais vista, fica cheia de traços. Checklist C: o aviso repetido em vários cartões vira um aviso global só.
- **Proposta:**
  - `render.py:524`:
    - **antes:** `{"rotulo": …, "valor": "—", "cor": "neutro", "detalhe": SEM_RECORTE}`;
    - **depois:** `{"rotulo": …, "valor": "—", "cor": "neutro"}`. O `cartao_vazio` já tira da tela o cartão só com "—".
  - `render.py:158`:
    - **antes:** `AVISO_UF = "Resumo e gráficos: BAP inteira."`;
    - **depois:** `AVISO_UF = "Os outros cartões, o resumo e os gráficos: só na BAP inteira."`.
  - `SEM_RECORTE` sai.
- **Dono:** modulo-web.

### RD-0035 · No Resumo gerencial do Painel, cada frase do "O que o painel diz" aparece de novo no placar
- **Onde:**
  - `visao_executiva.py:349-358` monta os insights com o `frase` dos cartões do placar (os 2 primeiros e os 3 de maior impacto);
  - `bap_automation._blocos_painel_web` (:7099-7104) manda o `frase` também dentro do placar;
  - `_resumo.html:38` desenha `pl-frase`.
- **Tipo:** texto.
- **O que se repete:**
  - "No ritmo de hoje o mês fecha R$ X abaixo do desafio." aparece 2× (insight e cartão "Meta x Real"), e o mesmo vale para até 5 frases.
  - Na fixture, o mesmo fato aparece 3 vezes: "A projeção está 48% abaixo do desafio.", "52% ating. projetado" e a frase do cartão (`P/admin__painel-resumo__pc1366-inteira.png`).
  - O `sem_repeticao` não pega porque compara números, e a frase repetida é idêntica.
- **Impacto:** é a tela principal do Diretor e, pela ordem de 26/11, vai ser a página inicial.
- **Proposta (web):** em `render.farol_para_tela`, depois de montar `insights`:
  ```python
  ditas = {i["texto"] for i in insights}
  for b in blocos:
      if b["tipo"] == "placar":
          for c in b["cartoes"]:
              if c["frase"] in ditas:
                  c["frase"] = ""
  ```
  - A frase fica só na lista ordenada por impacto.
  - **Alternativa no PC (modulo-farois):** `visao_executiva` não põe no insight a frase que já vai no placar.
- **Dono:** modulo-web, com o modulo-farois avisado.

### RD-0036 · CSS repetido sobrescreve o celular: as tabelas de baixo do Pedidos ficam em 3 colunas espremidas
- **Onde:**
  - `estilo.css:438` tem `@media(max-width:700px){… .bc3-juntas{grid-template-columns:1fr} …}`;
  - `estilo.css:466` tem `.bc3-juntas{grid-template-columns:repeat(auto-fit,minmax(0,1fr))}`. A regra vem depois, sem @media, e vence.
- **Tipo:** layout · código.
- **O que se repete:** o seletor `.bc3-juntas` está declarado 3× (390, 438 e 466).
- **Impacto:** no celular, "Gerar ID de separação CD", "Gerar reversa" e "Analítico" ficam lado a lado com ~110 px cada e uma coluna de data por linha (`P/admin__pv_pedidos-pedidos__cel390-inteira.png`).
- **Proposta:**
  - **antes:** linha 466 `.bc3-juntas{grid-template-columns:repeat(auto-fit,minmax(0,1fr))}`;
  - **depois:** a linha 390 vira `.bc3-juntas{…;grid-template-columns:repeat(auto-fit,minmax(0,1fr));…}` e a 466 sai, de modo que o @media de 700 px volta a valer.
- **Dono:** modulo-web.
- **Recado ao designer-ux:** reteste no 390.

### RD-0037 · A lista de colunas proibidas (RN-GER-011) tem uma 5ª cópia, diferente, na Inadimplência
- **Onde:**
  - `cobranca.py:91`: `COLUNAS_PROIBIDAS = {"TELEFONE","CNPJ","CPF","E-MAIL","EMAIL"}` (5 nomes), usada em `:121` e `:154`;
  - `render.COLUNAS_FORA` (`render.py:374`) tem 10 nomes: + CELULAR, WHATSAPP, CONTATO, FOTO, ENDERECO;
  - o teste de igualdade `tests/test_T0017_pacote_tres_farois.py:933-938` confere `bap_automation`, `render` e a cópia do próprio teste, mas não o `cobranca`.
- **Tipo:** código (regra).
- **O que se repete:** a mesma regra em 5 listas: robô, render, cobranca, o teste e `bap_automation._COLUNAS_PESSOA_TABELA_WEB`. O RD-0021 unificou as outras, e esta ficou fora.
- **Impacto:** a regra de dado pessoal diverge. Uma coluna "CELULAR" ou "WHATSAPP" na Inadimplência passa no filtro de nome (hoje só a lista fechada segura).
- **Proposta:**
  - `cobranca.py`: `from .render import coluna_fora`;
  - `:121` **antes:** `k.upper() in COLUNAS_PROIBIDAS` → **depois:** `coluna_fora(k)`;
  - `:154` **antes:** `if COLUNAS_PROIBIDAS & set(nomes):` → **depois:** `if any(coluna_fora(n) for n in nomes):`;
  - `COLUNAS_PROIBIDAS` sai.
- **Dono:** modulo-web.
- **Testes:** acrescentar `assert not hasattr(web_app.cobranca, "COLUNAS_PROIBIDAS")`, ou conferir `cobranca` no teste de igualdade.

## Média

### RD-0038 · Painel Executivo: o mesmo painel tem 3 nomes, "Painel ·" se repete nas abas e duas abas se chamam quase igual
- **Onde:**
  - menu "Painel Executivo" (`main.RELATORIO`, `render.menu_lateral:178`, `painel.html:2,6,19`);
  - h1 das abas RRM "Painel do Diretor · resultado/produtividade/por dia útil" (`render.TITULOS:16-18`);
  - abas "Painel · resultado", "Painel · produtividade" e "Painel · por dia útil", que são títulos do pacote (`bap_automation._TITULOS_ABAS_WEB:6605`);
  - mais a aba "Produtividade" (chave `visitas`, `render.PAINEIS:85` e `ba.PAINEIS_WEB:7044`).
- **Tipo:** texto.
- **O que se repete:**
  - "Painel" 3× na barra de abas;
  - o h1 repete a aba ativa;
  - "Painel · produtividade" e "Produtividade" ficam lado a lado (`P/admin__painel-resultado__pc1366.png`, `P/admin__painel-resumo__pc1366-inteira.png`).
- **Impacto:** leitura, e escolher a aba errada.
- **Proposta:**
  - h1 único "Painel Executivo" em todas as abas: `render.TITULOS` sai e `aba_para_tela` devolve `titulo="Painel Executivo"`;
  - abas "Resultado", "Produtividade", "Por dia útil", "Resumo gerencial", …, e "Visitas" no lugar de "Produtividade" (chave `visitas`);
  - na web, `render.localizar_abas` usa o rótulo da web (`{"resultado": "Resultado", "produtividade": "Produtividade", "por_dia_util": "Por dia útil"}`) em vez de `a["titulo"]`;
  - em `render.PAINEIS`, `("visitas", "Visitas")`, com o mesmo ajuste em `ba.PAINEIS_WEB` e no teste `test_T0022_numero_bate.py:43`.
- **Dono:** modulo-web; modulo-robo (`PAINEIS_WEB`); modulo-farois (título no PC, se quiser igual).

### RD-0039 · O aviso "Sem filtro por estado" segue nas 7 abas da Visita e no Resumo (RD-0023 não aplicado)
- **Onde:**
  - `main.py:353-354`: `aviso_uf = tabelas.AVISO_SEM_ESTADO if rid == "vc_visitas" else aviso_tabs_uf`. O comentário cita o RD-0023, mas faz o contrário da proposta dele;
  - o robô manda "Sem filtro por estado: os cartões mostram a BAP inteira." no Resumo;
  - `render.py:542-543` separa pelo prefixo do texto.
- **Tipo:** texto (aviso).
- **O que se repete:** o mesmo fato, com 2 textos, em 8 páginas.
- **Impacto:** no BC3, a Visita não tem seletor de estado (`P/admin__vc_visitas-vendedor__pc1366.png`, `..._resumo__pc1366-inteira.png`). O aviso explica um controle que não está na tela (regra 3).
- **Proposta:**
  - `main.py:354`: **antes:** `aviso_uf = tabelas.AVISO_SEM_ESTADO if rid == "vc_visitas" else aviso_tabs_uf` → **depois:** `aviso_uf = aviso_tabs_uf`;
  - o robô para de mandar o aviso do Resumo da Visita;
  - `render.py:542-543` deixa de separar `avisos_info` pelo prefixo.
- **Dono:** modulo-web e modulo-robo.

### RD-0040 · "Sem pacote" aparece em dois avisos na mesma página, e "ainda não disponível na web" em cada quadro
- **Onde:**
  - `base.html:30` ("Ainda não chegou nenhum pacote do PC.") e `farol.html:16` ("Ainda não disponível na web."), juntos na página do farol;
  - `base.html:51` repete o aviso no layout antigo;
  - `home.html:5` põe `<small>{{ indisponivel }}</small>` em cada quadro cinza.
- **Tipo:** texto (estado vazio).
- **O que se repete:** o mesmo estado 2× por página, e na home N× (um por farol).
- **Impacto:** poluição e texto vago.
- **Proposta:**
  - `farol.html:16`: **antes:** `<p class="aviso atencao">{{ indisponivel|capitalize }}.</p>` → **depois:** `{% if gerado_em %}<p class="aviso atencao">Este farol não veio no último pacote do PC.</p>{% endif %}`;
  - `home.html:5`: sai `<small>{{ indisponivel }}</small>`. O quadro cinza sem link basta, como na barra lateral;
  - `render.INDISPONIVEL` fica só para o bloco "indisponível" do gráfico.
- **Dono:** modulo-web.

### RD-0041 · "Cliente a cliente" (Visita): o código do cliente aparece 2 vezes na linha, e são 3 colunas para o mesmo cliente
- **Onde:**
  - `tabelas.COLUNAS["Cliente a cliente"]` (`:126-131`): CÓD., CLIENTE e NOME FANTASIA;
  - o robô limpa CLIENTE como `"cliente_sem_documento"`, que fica "código - nome" (`bap_automation._COLUNAS_LIMPAS_WEB:7652`);
  - `tabelas.colunas_ocultas` (`:863`) só reconhece "FANTASIA…" e "RAZÃO SOCIAL", então "NOME FANTASIA" não esconde CLIENTE.
- **Tipo:** layout (coluna).
- **O que se repete:** "900001-01" em CÓD. e "900001 - CLIENTE …" em CLIENTE, mais NOME FANTASIA (`P/admin__vc_visitas-cliente__pc1366.png`).
- **Impacto:** largura (a tabela já rola para o lado) e leitura.
- **Proposta:**
  - robô `:7652`: **antes:** `"CLIENTE": "cliente_sem_documento"` → **depois:** `"CLIENTE": "sem_documento"` (o código já está em CÓD.);
  - web `colunas_ocultas`: **antes:** `fan = next((i for i, n in enumerate(nomes) if n.startswith("FANTASIA")), None)` → **depois:** `fan = next((i for i, n in enumerate(nomes) if n.startswith(("FANTASIA", "NOME FANTASIA"))), None)`, e a coluna escondida passa a ser `("RAZÃO SOCIAL", "RAZAO SOCIAL", "CLIENTE")`, só quando FANTASIA está preenchida em todas as linhas (mesma regra de 25/11).
- **Dono:** modulo-robo e modulo-web.

### RD-0042 · Títulos da Inadimplência: o atraso aparece em 3 representações (VENCIMENTO, DIAS ATRASO, FAIXA)
- **Onde:**
  - `cobranca._T` (`:49-53`): VENCIMENTO, DIAS ATRASO e FAIXA ("31-60");
  - `bap_automation._COLUNAS_SEM_STATUS_WEB` (:7316) é o espelho.
- **Tipo:** indicador · coluna.
- **O que se repete:** o atraso de um título 3× por linha (`P/admin__pl_inadimplencia-titulos__pc1366.png`).
- **Impacto:** largura e leitura (checklist B: mais de 2 representações).
- **Proposta:**
  - FAIXA passa a coluna `oculta` (sai da grade e continua como filtro e no Excel): `_OC = ("STATUS PROTHEUS", "SITUAÇÃO PLANNER", "FAIXA")` na web;
  - `_STATUS_OCULTAS_WEB | {"FAIXA"}` no robô, com o contrato §10.6.2 ajustado pelo engenheiro-software.
  - VENCIMENTO e DIAS ATRASO ficam: um é a data, o outro ordena.
- **[SUPOSIÇÃO]:** FAIXA deriva de DIAS ATRASO, como o nome "31-60" indica. A fixture traz 19 dias na faixa 31-60, o que é artefato dela.
- **Dono:** modulo-robo e modulo-web.

### RD-0043 · A página inicial repete a barra lateral, e o `base.html` tem dois layouts inteiros
- **Onde:**
  - `main.home` (`:239-249`) e `home.html`: quadros "Painel Executivo … Usuários, Trocar senha" (`P/admin__home__pc1366.png`) com a mesma lista e a mesma regra de `render.menu_lateral`;
  - `base.html:10-36` (BC3) e `:37-56` (antigo) duplicam cabeçalho, "Sair", aviso de pacote e área de conteúdo;
  - Painel, Usuários, Senha, home e erro ficam no visual antigo; os faróis, no BC3.
- **Tipo:** layout · código.
- **O que se repete:** o menu em 2 lugares e 2 layouts para o mesmo site (ao ir do farol para o Painel, a barra lateral some).
- **Impacto:** cliques, consistência e manutenção. A ordem de 26/11 já pede a página inicial no Painel Executivo em formato farol.
- **Proposta:**
  - `/` redireciona para `/painel` (perfis `VERES`) ou para o 1º farol do perfil;
  - saem `home.html`, o menu de `main.home` e o CSS `.menu`, `.quadro` e `.quadro.indisp`;
  - `pagina()`: **antes:** `ctx.setdefault("bc3", bool(u) and ctx.get("rid") in render.BC3)` → **depois:** `ctx.setdefault("bc3", bool(u))`;
  - o layout antigo fica só para o login.
- **Dono:** modulo-web, com parecer do designer-ux e do design-de-marca.

### RD-0044 · Ramos mortos `{% if not bc3 %}`, o `_acoes.html` morto, e a busca, o filtro de estado e o Exportar escritos várias vezes
- **Onde:** desde a T-0031, `render.BC3 = set(FAROIS)`, e todo farol abre com `bc3=True`. Ficam mortos:
  - `farol.html:11-13, 15, 23-30`;
  - `_tabela.html:9-16, 19-20, 33-41, 71` (`and not bc3`) e `81-86`;
  - `_resumo.html:4` (ramo `not bc3`);
  - `_acoes.html` inteiro: só é chamado nesses ramos e repete "Excel desta tabela / PDF desta tabela / Excel de todas as abas" de `_bc3_cab.html:54-56`.
- **Tipo:** código (templates).
- **O que se repete:**
  - o filtro de estado está escrito 4× (`farol.html:26-29`, `_tabela.html:12-15`, `_bc3_cab.html:16-19`, `painel.html:13-16`), com dois rótulos: "BAP inteira" e "BAP";
  - a busca, 2× (`_bc3_cab.html:39-48`, `_tabela.html:33-41`);
  - "Arquivos para importar no Protheus", 2× (`_bc3_cab.html:57`, `_tabela.html:83`);
  - os campos ocultos de filtro, recorte, estado e sub-aba, 3×.
- **Impacto:** manutenção. Cada ajuste é feito 2 a 4 vezes, e os testes antigos validam marcação morta (RD-0053).
- **Proposta:**
  - apagar os ramos `not bc3` e o `_acoes.html`;
  - um macro `filtro_uf(base, ufs, uf, rotulo="BAP")` em `_bc3_cab.html`, usado também pelo Painel depois do RD-0043;
  - um macro `ocultos(tabela, uf, sub)` para os campos ocultos;
  - depois do RD-0043, `render.BC3` e a flag `bc3` saem.
- **Dono:** modulo-web.

### RD-0045 · `estilo.css`: 75 seletores declarados 2 ou 3 vezes, 10 blocos @media de 600 px e regras mortas
- **Onde:** `estilo.css` (468 linhas). As camadas "visual C" (T-0020, `:215-264`) e BC3 (T-0030, `:345-468`) vieram por cima das regras antigas.
  - Exemplos: `body` (3, 216), `main` (7, 224), `.abas a` (19, 226), `.kpi` (68, 231), `.juntas .rolagem-dados` (270, 327, 333), `.juntas .tab-dados td` (271, 331, 332), `.tab-dados th:first-child` (170, 171, 245) e `.filtros-tab a` (136, 209, 210, 256).
  - @media(max-width:600px) aparece 10×; o de 1500 px, 3×.
  - Regras mortas (nenhum template ou JS usa): `.tb` e `.tb th/td/.n/tfoot` (`:106-114`, `:214`, `:245`), `.tb-rol` (`:106`, `:122`), `.dica-rolar` (`:124-125`), `.indisp-bloco` (`:93`) e `.bc3-pag` (`:394-396`).
- **Tipo:** código (CSS).
- **O que se repete:** 75 pares seletor×@media (lista completa: `python3 .../scratchpad/revisao-geral/cssdup.py <estilo.css>`).
- **Impacto:** manutenção. Causou o RD-0036, e a próxima mudança visual de marca vai bater nas regras antigas.
- **Proposta:**
  - apagar as regras mortas;
  - fundir cada seletor numa declaração só, com o valor que vence hoje;
  - um bloco @media por largura (600, 700, 900, 1500), no fim do arquivo;
  - critério de pronto: `cssdup.py` mostra 0 seletor repetido fora de @media e os PNG antes/depois saem iguais.
- **Dono:** modulo-web.

### RD-0046 · Quem vê o quê está escrito em 3 lugares (faróis × Inadimplência × menu)
- **Onde:**
  - `tabelas.VE_TABELAS` e `ve_aba` (4 faróis);
  - `cobranca.VE_TABELAS` e `COBRA`, conferidos à mão em `main.farol:642-659`, que repete a lógica de `farol_abas:294-299`;
  - `main.PERFIS_PARCIAL:372-373` mistura `render.FAROIS` e `tabelas.VE_TABELAS`;
  - `main.home:242-248` refaz o menu de `render.menu_lateral` (VERES, `farois_do_perfil`, admin → Usuários, Trocar senha);
  - "Painel Executivo" está escrito em `main.RELATORIO:27`, `render.menu_lateral:178` e `painel.html:2,6,19`.
- **Tipo:** código (regra de acesso).
- **Impacto:** risco de um perfil ver uma aba num caminho e não no outro.
- **Proposta:**
  - `tabelas.VE_TABELAS["pl_inadimplencia"] = cobranca.VE_TABELAS` e `tabelas.ABAS["pl_inadimplencia"]` passam a valer para as abas de tabela;
  - `ve_aba(rid, "cobrar", perfil)` = `perfil in cobranca.COBRA`;
  - `main.farol` usa `ve_aba` como os outros;
  - o menu fica só em `render.menu_lateral` (a home sai no RD-0043);
  - `render.NOME_PAINEL = "Painel Executivo"`.
- **Dono:** modulo-web.

### RD-0047 · A validação do pacote repete os mesmos utilitários em 3 a 6 módulos
- **Onde:**
  - `cobranca._chip_ok` (`:86-89`) é idêntica a `tabelas._chip_texto_ok` (`:262-265`);
  - `_int` e `_num` existem em `tabelas`, `cobranca`, `edicoes`, `render`, `exportar` e `pacotes`, com 2 semânticas (`tabelas._num` exige número finito e `cobranca._num` não);
  - `RE_COR` está em 3 lugares (`render._COR`, `tabelas`, `cobranca`), e `RE_DATA` em 2 (`render` sem `$`, `cobranca` com `$`);
  - `RE_UF` está em `pacotes:52` e `tabelas:184`, e inline em `render.py:527`;
  - há 3 rotinas que procuram chave proibida (`pacotes._chave_proibida`, `tabelas._proibida`, `cobranca._achar_proibida`), cada uma com a sua lista (`pacotes.PROIBIDAS`, `tabelas.PROIBIDAS/PROIBIDAS_KPI`, `cobranca.PROIBIDAS_TABELA`);
  - `tabelas.NUM_TIPOS` é igual a `exportar._NUM`;
  - `TONS` existe em `render` (4 tons) e em `tabelas` (8).
- **Tipo:** código.
- **Impacto:** a mesma célula pode ser aceita num módulo e recusada no outro (ex.: NaN na Inadimplência).
- **Proposta:** um módulo `web/app/regras_pacote.py` com `e_int`, `e_num` (finito), `RE_COR`, `RE_DATA`, `RE_UF`, `NUM_TIPOS`, `chip_texto_ok` e `chave_proibida(o, proibidas, nivel_max)`. Os outros módulos importam dele, e as listas específicas continuam em cada módulo.
- **Dono:** modulo-web.

### RD-0048 · O diário da cobrança e a fila de edições são duas cópias do mesmo diário jsonl
- **Onde:**
  - `cobranca.Diario` (`:352-525`) e `edicoes.Fila` (`:268-…`) repetem a época com `estado.json`, o seq nunca reaproveitado, o acréscimo com fsync, o `_ler` que ignora linha truncada e o `desde(limite)` (o mesmo corpo de 4 linhas);
  - `ErroCobranca` (`:342`) é igual a `ErroEdicao` (`edicoes:264`);
  - `main.api_cobranca:772-780` e `main.api_edicoes:798-806` repetem a validação de `desde`.
- **Tipo:** código.
- **Proposta:**
  - classe `DiarioJsonl(pasta, prefixo)` em `arquivos.py` com `_tranca`, `_estado`, `_acrescentar`, `_ler` e `desde`;
  - `Diario` e `Fila` só com o que é deles (retenção e status);
  - um `ErroDiario(status, msg)`;
  - em `main`, `def _desde(request) -> int | JSONResponse`.
- **Dono:** modulo-web.

### RD-0049 · Rotas: trechos copiados em `main.py` e duas funções mortas ou repetidas no `render` e no `cobranca`
- **Onde:**
  - `main.tabelas_para_exportar:476-479` repete `cobranca.tabela_para_tela` (`:556-558`) parâmetro a parâmetro;
  - `farol` e `farol_abas` repetem o começo (aba → resumo, `registrar_acesso`, nome, farol sem pacote) (`:296-304` × `:646-652`);
  - o `painel` tem 2 caminhos para a aba em forma de farol (`:262-270` × `:271-273`);
  - a escolha de estado é feita de 4 jeitos (`uf.upper()[:2] in …` em `:266`, `:306` e `:451`, e `render.escolher_uf`);
  - `next((x for x in rel.get("tabelas") … if x.get("titulo") == tit), None)` aparece 5×;
  - a mensagem "Esta linha não está mais no pacote do PC. Volte ao farol e abra de novo." está escrita 2× (`:596-598`, `:614-616`);
  - `render.kpis_para_tela` (`:268-270`) é igual ao trecho inline de `farol_para_tela:537`;
  - `cobranca.fmt_celula` (`:547-549`) não tem nenhuma chamada.
- **Tipo:** código.
- **Proposta:**
  - `tabelas_para_exportar` chama `cobranca.tabela_para_tela(t, t["titulo"], q, pagina_tam=10**9)`;
  - `def _tabela_do(rel, titulo)`;
  - `def _uf_valida(uf, ufs)`;
  - constante `MSG_LINHA_SUMIU`;
  - `farol_para_tela` usa `kpis_para_tela(kpis)`;
  - `cobranca.fmt_celula` sai.
- **Dono:** modulo-web.

### RD-0050 · Dinheiro formatado à mão no template da fila e 3 formatos de moeda no `render`
- **Onde:**
  - `_fila.html:5`: `'{:,.2f}'.format(c.em_atraso).replace(',', 'X').replace('.', ',').replace('X', '.')`;
  - `render.moeda` (`:204`), `render.fmt_celula(painel=True)` (`:415-416`) e `render.fmt_celula` (`:427-428`);
  - o percentual sai com 1 casa no ramo `painel` e com 0 casa no ramo normal (o RD-0022 unificou a função, mas manteve os dois ramos).
- **Tipo:** código.
- **Proposta:**
  - filtro Jinja `brl = lambda v: render.fmt_celula(v, "moeda2")` registrado em `criar_app`;
  - `_fila.html:5`: **depois:** `{{ c.em_atraso|brl }}`;
  - o ramo `painel=True` passa a diferir só no vazio ("—"); `pct1` já cobre o 1 decimal.
- **Dono:** modulo-web.

### RD-0051 · A edição explica o funcionamento do sistema em 3 textos (regra 3)
- **Onde:**
  - `editar.html:42`: "A edição vai para a fila do site e chega ao PC na próxima rodada do robô (a cada 30 min), gravada pela mesma função da tela do PC.";
  - `edicoes.MSG_ENVIADA` (`:42`): "Edição enviada. Ela chega ao PC na próxima rodada do robô (a cada 30 min).";
  - `editar.html:9`: "… O que você mandar agora vai depois dela.".
- **Tipo:** texto.
- **O que se repete:** "chega ao PC na próxima rodada do robô (a cada 30 min)" 2×, mais a explicação interna.
- **Proposta:**
  - `editar.html:42` sai;
  - `MSG_ENVIADA = "Edição enviada: aguardando o PC."`;
  - `editar.html:9`: **depois:** `Aguardando o PC: edição de {{ hh:mm }} por {{ usuario }}.`
- **Dono:** modulo-web.

### RD-0052 · Listas do contrato espelhadas no PC e na web sem teste de igualdade
- **Onde:** só `COLUNAS_FORA` e `COLUNAS` (§10.7.3) têm teste de igualdade (`tests/test_T0017_pacote_tres_farois.py:756-764, 933-939`). Ficam sem teste:
  - `ba._COLUNAS_SEM_STATUS_WEB`/`_STATUS_WEB` × `cobranca.COLUNAS`/`STATUS_BLOCO`;
  - `ba._COLUNAS_EXTRAS_COBRANCA_WEB` × `cobranca.COLUNAS_EXTRAS`;
  - `ba._COLUNAS_COM_CHIP_WEB` × `cobranca.COLUNAS_CHIP`;
  - `ba._STATUS_OCULTAS_WEB` × `cobranca._OC`;
  - `ba._JUNTAS_WEB` × `tabelas.JUNTAS`;
  - `ba._ABAS_TABELAS_WEB` × `tabelas.ABAS`;
  - `ba.PAINEIS_WEB` × `render.PAINEIS`;
  - `ba._ABAS_WEB` × `render.CHAVES_ABAS`.
- **Tipo:** código · teste.
- **Impacto:** é uma duplicação necessária (a web no Render não importa o PC), mas sem um guarda as listas divergem em silêncio, e o robô manda o pacote que a web recusa.
- **Proposta:** `manter` as duas cópias e criar 1 teste parametrizado `test_contrato_espelho_pc_web` com os 8 pares.
- **Dono:** testes (teste); modulo-robo e modulo-web avisados.

### RD-0053 · Testes de "sem barra de abas" passam sem testar nada desde o BC3
- **Onde:** `'class="abas' not in h` em:
  - `web/tests/test_abas.py:104` (`test_diretor_so_resumo_sem_barra_de_abas`) e `:654`;
  - `web/tests/test_cobranca.py:153` e `:188`.
  - No BC3, a barra é `class="bc3-abas"`, então a afirmação é sempre verdadeira.
  - Na mesma linha, `h.split("<main")[1].split("<header")[0]` corta antes da barra.
- **Tipo:** teste.
- **Impacto:** a regra "diretor só vê o Resumo, sem barra de abas" ficou sem guarda na tela.
- **Proposta:**
  - **antes:** `assert 'class="abas' not in h …`;
  - **depois:** `assert 'class="bc3-abas"' not in h and 'aria-label="Abas do farol"' not in h`.
- **Dono:** modulo-web (`web/tests/**`).

## Baixa

### RD-0054 · O fuso de Manaus está escrito em 4 módulos da web
- **Onde:**
  - `ZoneInfo("America/Manaus")` em `main.py:25`, `cobranca.py:28`, `edicoes.py:30` e `pacotes.py:19`, além de `config.TZ_ALVO`;
  - `agora()` em `cobranca:294` e `edicoes:61`;
  - `main.hhmm` usa `cobranca.agora`.
  - É o mesmo padrão do RD-0031 (PC).
- **Tipo:** código.
- **Proposta:** `config.MANAUS = ZoneInfo(TZ_ALVO)` e `config.agora()`; os módulos importam de `config`.
- **Dono:** modulo-web.

### RD-0055 · Constantes de texto da edição definidas e nunca usadas; o template escreve o texto à mão
- **Onde:**
  - `edicoes.MSG_AGUARDA`, `MSG_ERRO` e `MSG_SEM_CHAVE` (`:43-45`) não têm nenhum uso;
  - `_grade.html:4` escreve "Aguardando o PC", "O PC recusou" e "Nota concluída (anterior ao controle de 01/10/2026).";
  - `editar.html:9` e `:34` repetem "Aguardando o PC".
- **Tipo:** código (texto).
- **Proposta:** `modelos.env.globals["ED"] = edicoes` e `{{ ED.MSG_AGUARDA }}` etc. nos dois templates.
- **Dono:** modulo-web.

### RD-0056 · "Role para o lado para ver mais colunas →" aparece no PC sem rolagem
- **Onde:** `_grade.html:9` mostra a dica quando há mais de 6 colunas, sem ver se a tabela passa da largura.
- **Evidência:** a tabela "Frete por estado", que cabe inteira em 1920, mostra a dica (`P/admin__pl_entregas-resumo__pc1920.png`).
- **Tipo:** texto.
- **Proposta:** a dica fica só no celular: `.dica-rolagem{display:none}@media(max-width:700px){.dica-rolagem{display:block}}`. A regra `.dica-rolar` morta (RD-0045) já fazia isso.
- **Dono:** modulo-web.

### RD-0057 · `bc3.js`: a paginação morta e um comentário duplicado
- **Onde:**
  - `bc3.js:17-48`: `paginar()` nunca é chamada (a T-0031 trocou as páginas pela rolagem), e o CSS `.bc3-pag` dela também está morto;
  - `:53-55`: o comentário "a tabela de cima: …" aparece 2×;
  - as juntas são abertas em `umaTela()` e de novo no `else` final.
- **Tipo:** código.
- **Proposta:** apagar `paginar`, a 1ª linha do comentário e o `else` (a `umaTela` já abre as juntas no PC).
- **Dono:** modulo-web.

### RD-0058 · "Dados de … (horário de Manaus)" em páginas sem dado, e a marca escrita 2× no layout antigo
- **Onde:**
  - `base.html:50` mostra a faixa de dados em Usuários, Trocar senha e home (`P/admin__usuarios__pc1366.png`);
  - `base.html:40` ("BAP Central BAP AUTOPARTS") e `:54` ("BAP AUTOPARTS · BAP Central web v0.3.0").
- **Tipo:** texto.
- **Proposta:**
  - a faixa só nas páginas com dado: `{% if gerado_em and rid is defined %}`;
  - a marca fica conforme o parecer do design-de-marca (no BC3 não aparece "BAP AUTOPARTS"; regra 8 do CLAUDE.md);
  - some de vez com o RD-0043.
- **Dono:** modulo-web (design-de-marca decide a marca).

### RD-0059 · Parcial: "Voltar ao farol" repete a barra lateral, e a página mistura o visual antigo com o BC3
- **Onde:** `parcial.html:5` ("Voltar ao farol", e o farol já está ativo na barra lateral), com `cab-painel`, `.abas` e `.acoes-farol` dentro do BC3 (`P/admin__pv_pedidos-parcial__pc1366.png`).
- **Tipo:** layout.
- **Proposta:**
  - o link sai;
  - o título vai para a faixa BC3 (`_bc3_cab` com `farol_nome ~ " · Parcial"`);
  - os botões passam a `.bc3-bt`, e `.acoes-farol` sai do CSS.
- **Dono:** modulo-web.

### RD-0060 · Datas e colunas de dia (`manter?`)
- **Onde:** pedido explícito do gerente ("duas datas").
  - **Visita:** "Dia a dia", "Cliente a cliente" e "Indicação" têm DATA e DIA (o dia da semana sai da data); "Prospecção" tem DATA, HORA e DIA.
  - **Pedidos:** DT. PED e FATURAR ATÉ (DT. NF só no popup).
  - **Entregas:** DT. PED, DT. NF, DT. PREVISTA, DT. REAL, mais o SLA.
  - **Indicação:** DATA, VISITADA EM e REGISTRADO EM.
- **Tipo:** coluna.
- **Proposta:**
  - a coluna DIA sai da grade e a DATA mostra "03/11/2026 ter" (a coluna continua no Excel). Muda o §10.7.3: modulo-robo, modulo-web e engenheiro-software;
  - as datas de Pedidos, Entregas e Indicação ficam (`manter?`): cada uma é um marco diferente (pedido, prazo, nota, previsão, entrega). O po confirma se DT. PED é usada no Entregas.
- **Dono:** modulo-robo e modulo-web; decisão do po.

### RD-0061 · Testes repetidos e helpers copiados em `web/tests`
- **Onde:**
  - `test_T0022_painel_meta.test_diretor_so_ve_o_resumo_do_farol_de_metas` (`:134`) já está coberto por `test_abas.test_diretor_so_resumo_sem_barra_de_abas`, porque `RIDS` inclui `vc_meta`;
  - `test_cobranca.test_aba_de_tabela_em_outro_farol_403` (`:169`) já está coberto por `test_abas.test_aba_de_outro_farol_ou_da_inadimplencia_403` (`:117`);
  - há 3 `test_sem_login_vai_ao_login` (`test_abas:123`, `test_cobranca:179`, `test_T0021_edicao:129`) e mais `test_T0021_csv_protheus.test_sem_login_nao_baixa`;
  - `_recusa` está copiado em `test_abas:150` e `test_cobranca:42`;
  - há 4 helpers de "criar usuário com perfil e entrar": `test_T0021_edicao._criar` + `_entrar_como`, `test_abas._cli_de`, `test_farois._usuario` e `test_web._logar_outro`, além de `simular_farol.paginas`;
  - `test_abas._sem_cache` (`:34`) é uma função vazia.
- **Tipo:** teste.
- **Proposta:**
  - `conftest.py` ganha `recusa(cli, p, trecho, proibidos)` e a fixture `cliente_de(perfil)`;
  - um `test_sem_login_vai_ao_login` parametrizado pelas 4 URLs;
  - saem os 2 testes cobertos e `_sem_cache`.
- **Dono:** modulo-web.

### RD-0062 · O selo "A COBRAR" aparece em todo cartão pendente da fila (`manter?`)
- **Onde:** `_fila.html:7`, `{{ c.situacao or 'A COBRAR' }}`.
- **Tipo:** texto.
- **O que se repete:** em todos os cartões da lista de pendentes, onde "a cobrar" é o estado da própria lista (3× no PNG, N× no real).
- **Proposta:**
  - o selo só quando difere do padrão (ENVIADO dd/mm, ENVIADO HOJE, PULADO HOJE): `{% if c.situacao %}<span class="selo …">{{ c.situacao }}</span>{% endif %}`;
  - o JS (`cobranca.js`) cria o selo ao marcar.
  - `manter?`: o selo também é a resposta visual depois do clique. Se o designer-ux preferir o selo fixo, fecha como "manter".
- **Dono:** modulo-web; decisão do designer-ux.

---

## Fora do escopo (encaminhar, não catalogado)
- **testes:**
  - o rodapé "100 linhas" com 230 linhas (RD-0032);
  - na fixture, "Real R$ 500 mil (projeção)" e "proj. R$ 780 mil" no mesmo Resumo gerencial, e "Frete do mês" com R$ 52 mil no Resumo e R$ 4,6 mil na aba (provavelmente artefato da fixture; conferir com o pacote real).
- **designer-ux:**
  - o placeholder "Buscar pedido, cliente ou produto" aparece igual na Inadimplência, na Visita e nas Metas (texto errado para o contexto, não redundância);
  - "Trocar senha" é o rótulo de duas ações diferentes (a própria senha no menu e a do usuário em Usuários);
  - o perfil aparece em código cru ("pre_venda").

## Redundância útil (mantida)
- O total no rodapé das tabelas longas (Títulos, Metas Equipe).
- VALOR e SALDO, e EMISSÃO e VENCIMENTO, na Inadimplência: são fatos diferentes.
- A contagem "N linhas" das juntas: é o único lugar em que aparece.
- O aviso "Ainda não chegou nenhum pacote do PC.": diz que o dado guia a decisão (fica um só, RD-0040).

## Premissas
- [SUPOSIÇÃO] As telas são da fixture fictícia. Os achados de texto do PC (RD-0035, RD-0042, RD-0060) foram confirmados no código do PC (`visao_executiva.py:349-358`, `bap_automation.py:7099-7104, 7316, 7652`), não num pacote real.
- [SUPOSIÇÃO] A nova página inicial (ordem de 26/11) segue o BC3, e por isso o RD-0043 propõe tirar a home atual em vez de consertá-la.
- [SUPOSIÇÃO] O RD-0023 ficou sem decisão registrada: o código o cita, mas faz o contrário. Ele foi reaberto como RD-0039, não como achado novo de regra.
