# Revisão geral de UX do site BAP Central (designer-ux)

- **Base:** `main` c8f6004 (o 81d09cc só mexe no quadro; `web/` idêntico).
- **Pedido:** R-20261126-174334-alexandre.
- **Decisões que valem:** R-20261126-171559 (BC3 no PC, M3 no celular, popup do pedido, sem barra de rolagem, cabeçalho único) e R-20261125-174000 (tabelas de baixo lado a lado, sem repetições).
- **Telas:** fixture fictícia, geradas por mim em `revisao-geral/ux-telas/` (PNG 1366×768, 1920×1080 e celular 390×844, com o CSS e o JS embutidos). Métricas de rolagem em `ux-telas/metricas.json`.
- **Scripts:** `revisao-geral/ux_gerar.py` e `ux_png.mjs`.
- **Escopo:** só auditoria; nenhum código alterado.

Legenda: 🔴 segura a entrega · 🟡 ajuste · 🟢 ok. Prioridade: **P1** (próximo lote), **P2** (ajuste fino), **P3** (quando tocar no arquivo).

---

## 1. Visão geral (o que mais pesa)

| # | Achado | Onde | Sev. | Prio. |
|---|---|---|---|---|
| G1 | **Dois visuais no mesmo site.** BC3 (barra lateral + faixa verde) só nos faróis. Painel Executivo, página inicial, Usuários, Trocar senha, Login e Parcial seguem no visual antigo (topo branco, logo "b", `cab-painel`, rodapé com versão). Isso contraria o "padrão para todos os faróis e telas". | `main.py:145` (`bc3` só quando `rid in render.BC3`); `base.html:38-55`; `painel.html`, `home.html`, `usuarios.html`, `senha.html`, `parcial.html` | 🔴 | P1 |
| G2 | **Rolagem lateral dentro da tabela em quase todo farol.** Só o Pedidos tem grade × popup (`NO_POPUP`). Medido (largura do conteúdo ÷ largura da caixa): Entregas 1991/1142 a 1366 e **1991/1650 a 1920**; Visita · Cliente a cliente 2445/1142 (**2445/1650 a 1920**); Visita · Por vendedor 1767/1142; Prospecção 1684/1142; Aderência 1462/1142; Inadimplência · Por cliente 1626/1142; Títulos 1419/1142. | `tabelas.py:794` (`NO_POPUP` só do Pedidos); `main.py:502-516` (`sel_col` só onde há junta ligada) | 🔴 | P1 |
| G3 | **Celular: as tabelas de baixo do Pedidos ficam espremidas em 3 colunas de 112 px.** A regra solta da linha 466 (`.bc3-juntas{grid-template-columns:repeat(auto-fit,minmax(0,1fr))}`) vem depois do `@media(max-width:700px)` (linha 416) e anula o `grid-template-columns:1fr` do M3. | `estilo.css:466` | 🔴 | P1 |
| G4 | **Celular: só o Pedidos tem M3.** Os outros faróis mostram a tabela larga com rolagem lateral (Entregas 1926/360, Visita · Vendedor 1673/360, Metas 477/360, Inadimplência 1391/360). A "lista que abre" sai do Pedidos por causa da condição `sc is not none`. | `_grade.html:19-24`; `tabelas.py:836` (`colunas_do_celular` só com `sel_col`) | 🔴 | P1 |
| G5 | **Páginas no lugar da rolagem por dentro**, ao contrário da T-0031. A tabela com mais de 100 linhas mostra "Página 1 de 3 · Próxima »" embaixo, e o rodapé diz "100 linhas" enquanto a aba diz "· 230" (Visita · Cliente a cliente). | `tabelas.py:708` (`pagina_tam=100`); `main.py:332` (chama sem `pagina_tam`); `_tabela.html:63-68`; `bc3.js:80` (conta as linhas do DOM) | 🔴 | P1 |
| G6 | **Cabeçalho muda de altura e de conteúdo entre as abas.** No Resumo, a faixa usa padding 16/24 e título de 24 px; nas abas de tabela, 12/22 e 21 px. Solicitação BAP e as abas de tabela da Inadimplência ficam sem números (a faixa encolhe para só o título). Ao trocar de aba, tudo "pula". | `estilo.css:361`, `:400` (`body.uma-tela .bc3-faixa`); `main.py:355-361` (Solicitação sem kpis); `main.py:670-673` (Inadimplência não passa `kpis`) | 🟡 | P1 |
| G7 | **Contraste da faixa verde abaixo do mínimo** no canto claro do degradê (`#3C9440`), onde ficam o título, a data e os primeiros números. Rótulos `#D2E7D3` de 11 px: 2,9:1 (mínimo 4,5). Número em alerta `#FFB4A9`: 2,3:1 (mínimo 3). Em atenção `#FFE08A`: 3,0:1. Em ok `#A6E3A9`: 2,6:1. | `estilo.css:361`, `:364`, `:369`, `:371`, `:441` | 🟡 | P1 (validar com o design-de-marca) |

---

## 2. Achados por tela

### 2.1 Farol de Pedidos (`/farol/pv_pedidos`)

**Faixa e popup**

- 🟢 Faixa, filtro por estado, abas, busca, Exportar e caixa "Ignorar fora da base" numa linha só. A tela cabe a 1366 e a 1920, e o popup do pedido abre ao passar o mouse e ao focar com o teclado.
- 🟡 P2: **o popup repete a grade.** Ele mostra as 24 colunas, inclusive DT. PED, FANTASIA, UF, CIDADE, R$ VENDA, SLA e VENDEDOR, que já estão na linha. Correção em `tabelas.dados_do_popup` (`tabelas.py:845`): receber `so=colunas_no_popup(tab)` e devolver só as colunas fora da grade, mais a RAZÃO SOCIAL. No celular (`_grade.html:22`) continua tudo. Agrupar em blocos: Cliente / Crédito / Pedido / Nota (ver §3.1).
- 🟡 P2: **"PED. MÁX." igual ao número do pedido** aparece no popup. Mostrar só quando for diferente do PEDIDO (`dados_do_popup`).

**Tabelas de baixo**

- 🟡 P1: **a 1366, as duas da esquerda passam da largura** (405/351 px). A coluna FILIAL DEST. fica cortada ("FILI… FICT…"). Correção na lista de §3.1: DATA vai ao popup da linha, e FILIAL DEST. vira a sigla da filial.
- 🟡 P2: **a 1920, a DESCRIÇÃO e o "CD FICTICIO" quebram em 3 linhas.** Cada linha fica com ~58 px, e as 5 linhas ocupam a altura toda. Correção em `estilo.css:443-445` (`body.uma-tela .bc3-juntas td{white-space:normal}`): `nowrap` com reticências (`text-overflow:ellipsis; max-width:18ch`) e o texto inteiro no `title`.
- 🟡 P2: as 3 caixas de baixo têm alturas diferentes: o Analítico, com 5 linhas, deixa o espaço vazio embaixo. Use `align-items:start` na grade ou uma altura fixa das caixas, igual para as 3.

**Contagem e busca**

- 🟡 P2: **contagem em 3 lugares:** faixa "PEDIDOS 21", aba "Pedidos · 21" e rodapé "21 pedidos". Tirar o rodapé `bc3-rod` (`bc3.js:76-82`); fica a contagem da aba, que acompanha filtro e busca.
- 🟡 P2: a dica da busca aparece cortada ("Buscar pedido, cliente o", tanto a 1366 quanto a 1920). Encurte para "Buscar" + o que a aba busca (ver G9).

**Celular**

- 🟡 P2: o botão "Ver mais 10 de 11" é confuso. Troque por "Ver mais 10 (faltam 11)", em `bc3.js:97`.

**Comandos**

- 🟡 P3: "Filtros" usa o marcador ► do navegador e "Exportar" usa ▾. Use o mesmo ▾ nos dois: `.bc3-filt>summary::after`, igual a `.bc3-exp summary::after` (`estilo.css:383`).
- 🟡 P3: a caixa "Ignorar fora da base" é um `<a role="checkbox">`. A barra de espaço não marca, e o `title` explica o sistema. Pode ficar como link, mas tire o `role` (ou trate a barra de espaço) e troque o `title` por "Pedidos internos". Em `_bc3_cab.html:35-36`.

### 2.2 Farol de Entregas

- 🔴 P1: **18 colunas na grade, com rolagem lateral até a 1920.** A grade × popup está em §3.2, com o popup aberto pela NF.
- 🟡 P1: a 1366, as "Pendências dos meses anteriores" (largura toda) comem metade da altura, e a tabela de cima mostra só 5 linhas. Com a grade enxuta (sem quebra de linha) as duas cabem. Se ainda faltar altura, deixe as Pendências fechadas por padrão, com a contagem no título.
- 🟡 P2: CLIENTE vem como "900001 - CLIENTE FICTICIO 01". Mostre só o nome na grade e o código no popup (mesma regra do Pedidos: um nome de cliente só).

### 2.3 Farol de Inadimplência

**Abas de tabela**

- 🔴 P1: Títulos (18 colunas) e Por cliente (17) rolam para o lado a 1366. A grade × popup está em §3.3.
- 🟡 P1: as abas de tabela ficam **sem números e sem o filtro BAP/AM/PA** na faixa: só o título (G6).
- 🟡 P2: as colunas SITUAÇÃO, FAIXA e STATUS são selos (`cobranca.COLUNAS_CHIP`), mas aparecem como texto na fixture. Confira com o pacote real.

**Cobrar no WhatsApp**

- 🟡 P1: título repetido ("Farol de Inadimplência · Cobrar no WhatsApp" logo abaixo da faixa e da aba ativa), em `_fila.html:21`. Saem o `<h1>` e o "5 clientes", que já estão na aba ("Cobrar no WhatsApp · 5"). O link "já tratados hoje" vai para a barra das abas.
- 🟡 P1: a faixa azul-clara "Situação do PC até … O que você marcar aqui chega ao PC às 08h ou 14h" fica **acima** da faixa verde e explica o sistema (`farol.html:6`). Ela vira uma linha curta dentro da faixa, ao lado da data: "PC: 24/11 08:07 · envios voltam às 08h e 14h".
- 🟡 P2: a página rola (a fila tem 10 cartões). Aceitável por ser fila de trabalho. No PC, use 6 por página, ou 2 colunas que caibam em 1366×768.
- 🟢 Um só botão principal por cartão ("Abrir WhatsApp"); "Pular" é neutro. Os selos A COBRAR / ENVIADO têm texto.

**Barra lateral**

- 🟡 P3: "Farol de Inadimplência" quebra em 2 linhas na lateral de 190 px (a 1366). Use 200 px, ou o nome curto "Inadimplência" na lateral (ver §4).

### 2.4 Farol de Visita

**Barra das abas**

- 🔴 P1: Por vendedor (20 colunas), Cliente a cliente (23), Prospecção (14) e Aderência (16) rolam para o lado. A grade × popup está em §3.4.
- 🟡 P1: **8 abas não cabem com a busca a 1366.** As ações descem para uma segunda linha (~50 px perdidos). Use nomes curtos: Supervisor · Vendedor · Dia a dia · Aderência · Cliente a cliente · Prospecção · Indicação. Abaixo de 1500 px, a busca vira ícone e abre ao clicar.

**Avisos e páginas**

- 🟡 P1: o aviso "Sem filtro por estado: esta tabela mostra a BAP inteira." aparece em **todas** as abas, numa linha própria, explicando o sistema (`main.py:354`, `tabelas.py:51`). Se o filtro de estado não aparece, o aviso não ajuda a agir: tire-o. O mesmo vale para o do Resumo ("os cartões mostram a BAP inteira").
- 🔴 P1: Cliente a cliente pagina de 100 em 100 (G5).

### 2.5 Farol de Metas Equipe

- 🟢 As tabelas de equipe cabem no PC sem rolagem lateral, e os grupos FATURAMENTO / POSITIVAÇÃO estão claros.
- 🟡 P1: no PC real são 10 abas (com Bairro, Zona e Família), que não cabem numa linha a 1366. Use nomes curtos: Equipe · Top 30 · UF · Cidade · Bairro · Segmento · Zona · Categoria · Família.
- 🔴 P1 (celular): as 3 tabelas rolam para o lado (% ATING. cortado) → M3 (G4).
- 🟡 P2: o rótulo da faixa "FATURAMENTO · DESAFIO COMERCIAL" tem 3 linhas no celular. Use "Faturamento" com o detalhe "desafio comercial".

### 2.6 Solicitação BAP (aba do Pedidos)

- 🟢 As sub-abas cabem, e os CSV do Protheus ficaram dentro do Exportar.
- 🟡 P2: as sub-abas são "pílulas" verdes, um 3º estilo de aba além das abas e do filtro de estado. Use o mesmo controle segmentado do filtro de estado (`.bc3-uf`) em fundo claro.
- 🟡 P1: a faixa perde os números (G6).

### 2.7 Painel Executivo (`/painel`)

- 🔴 P1: fora do BC3 (G1). Sem barra lateral; com o rodapé "BAP Central web v0.3.0".
- 🔴 P1: as **12 abas** rolam para o lado tanto a 1366 quanto no celular ("Itens p…" cortado). Há também "Painel · produtividade" e "Produtividade", com nomes quase iguais.
- 🟡 P1: o título "Painel do Diretor · resultado" é diferente do nome no menu ("Painel Executivo").
- 🟡 P1: a página rola a 1366×768 (846 px) e chega a 1.940 px no celular.

A proposta completa está em §5.

### 2.8 Página inicial (`/`)

- 🔴 P1: a grade de quadrados brancos fica fora do BC3. É 1 clique a mais para tudo, porque a barra lateral já faz esse papel.
- 🟡 P2: o texto do quadro sem dado ("ainda não disponível na web") difere do da lateral ("Sem dados no último pacote") e não diz o que fazer.

### 2.9 Login e Trocar senha

- 🟡 P1: a tela é limpa, mas o logo "b" do topo é diferente da marca da lateral BC3 (quadrado verde). Leve ao **design-de-marca**: um logo só.
- 🟡 P2: o título "Entrar" repete o botão "Entrar". Use o título "BAP Central", com "BAP AUTOPARTS" pequeno; o botão fica "Entrar".
- 🟡 P2: o erro de login (`login.html:6`) e o de senha (`senha.html:7`) não têm `role="alert"`, então o leitor de tela não anuncia.
- 🟡 P3: "Nova senha (mínimo 10 caracteres)" pode ficar. Na troca obrigatória, a frase "Defina uma senha nova para continuar." vai no subtítulo, não como aviso amarelo.

### 2.10 Usuários (`/usuarios`)

**Botões**

- 🔴 P1: **3 botões verdes principais por linha** ("Desativar", "Trocar senha" e, embaixo, "Criar"). "Desativar" é ação de perigo, tem cara de principal e não pede confirmação. Correção:
  - "Desativar" como texto vermelho (nível perigo) com `confirm()`;
  - "Trocar senha" como neutro, abrindo o campo só na linha clicada (`<details>`);
  - um só principal na tela: "Novo usuário", na barra do topo.

**Textos e estados**

- 🟡 P1: o perfil aparece como código ("pos_venda", "pre_venda"). Use os rótulos Admin · Diretor · Gerente · Pré-venda · Pós-venda · Vendas.
- 🟡 P1: a situação aparece em minúsculas ("ativo"), sem selo. Use os selos Ativo (verde) · Desativado (cinza) · Troca de senha pendente (amarelo).
- 🟡 P2: o formulário "Novo usuário" fica abaixo da dobra a 1366. Ele abre pelo botão "Novo usuário" do topo.
- 🟡 P2 (celular): a tabela rola para o lado (606/371). No M3: uma linha por usuário (nome + selo), e as ações dentro.

### 2.11 Parcial (`/farol/<rid>/parcial`) e Editar

- 🟡 P1: a Parcial usa o cabeçalho antigo (`parcial.html:5`) dentro do shell BC3. Ela vira faixa BC3 ("Parcial · Farol de Pedidos"), com o seletor Acumulado / D-1 / Hoje no lugar das abas. "Baixar imagem" é o único principal.
- 🟢 O estado vazio da Parcial ("A parcial ainda não chegou do PC.") tem uma frase só.
- 🟡 P2: a frase de rodapé do Editar explica o sistema: "…gravada pela mesma função da tela do PC" (`editar.html:42`). Encurte para "Chega ao PC em até 30 min."

### 2.12 Acessibilidade e toque (todas as telas BC3)

- 🟡 P1: a busca tem `outline:0` e nenhum foco visível (`estilo.css:379`). Acrescente `.bc3-busca:focus-within{box-shadow:0 0 0 2px #2F7D32}`, mais um `:focus-visible` geral para links, abas e botões.
- 🟡 P1 (celular): alvos com menos de 44 px:
  - as abas: ~31 px (`estilo.css:428`, `padding:7px`);
  - o filtro de estado: ~24 px (`.bc3-uf a`, `:366`);
  - os itens do menu: ~34 px (`:353`).

  Em `@media(max-width:700px)`: `min-height:44px` nos três.
- 🟡 P2 (celular): o menu ☰ não fecha ao tocar fora nem com Esc (`bc3.js:9-15`). Acrescente o clique no fundo e o Esc.
- 🟡 P3: o menu lateral usa `transition:.2s` sem respeitar o "reduzir movimento" (`estilo.css:418`). Acrescente `@media(prefers-reduced-motion:reduce){.bc3-lado{transition:none}}`.
- 🟡 P3: o popup tem `role="tooltip"`, mas o link não tem `aria-describedby="pop-pedido"` (`_grade.html:15`).
- 🟢 As cores dos selos e faróis vêm sempre com texto (número, %, "LIBERADO"), e os contrastes dos selos estão em 5:1 ou mais.

### 2.13 Textos de tela

- 🟡 P1 (G9): a mesma dica de busca, "Buscar pedido, cliente ou produto", aparece em todos os faróis (`_bc3_cab.html:46`). A dica passa a vir por farol:

  | Farol | Dica |
  |---|---|
  | Pedidos | "Buscar pedido ou cliente" |
  | Entregas | "Buscar NF ou cliente" |
  | Inadimplência | "Buscar cliente ou NF" |
  | Visita | "Buscar vendedor ou cliente" |
  | Metas | "Buscar nome" |

- 🟡 P2: o estado vazio da lateral é só um `title` ("Sem dados no último pacote"); na página inicial é "ainda não disponível na web". Use um texto só, visível: "Sem dados hoje".

---

## 3. Grade × popup por farol (base da tarefa do "ajuste fino")

Regras:

1. Cada tabela de cima tem **uma coluna-chave** sublinhada. Ao passar o mouse ou focar nela, abre o popup; no Pedidos, o clique filtra as de baixo.
2. A grade tem **no máximo 10 a 11 colunas a 1366** (de 1.142 px úteis), sem quebra de linha.
3. O popup mostra **só o que não está na grade**, em blocos com título.
4. No celular (M3), a linha fechada mostra chave · nome · selo · valor; aberta, mostra o popup inteiro.
5. O Excel continua com todas as colunas.

Implementação sugerida (dono: `modulo-web`):

- `tabelas.py`: trocar `NO_POPUP` por `GRADE = {titulo: {"chave": col, "grade": (...), "cel": (nome, selo, valor)}}`. Tudo que não está em `grade` vai ao popup.
- `popup_pedido.js`: generalizar para "popup da linha". Os itens do Analítico continuam só no Pedidos.

### 3.1 Pedidos

| Tabela | Grade (ordem) | Popup |
|---|---|---|
| Pedidos | DT. PED · FATURAR ATÉ · **PEDIDO** · FANTASIA · UF · CIDADE · R$ VENDA · % DESC. · SLA · % ATENDIDO · ANÁLISE CRÉDITO · SITUAÇÃO · VENDEDOR (13; hoje já cabe a 1366) | **Cliente:** RAZÃO SOCIAL, CÓD. · **Crédito:** LIMITE, DISP., ATRASO, COND. PAGTO · **Pedido:** PED. MÁX. (se diferente do pedido), VOL., R$ TABELA, FILIAL, PRAZO · **Nota:** NF, DT. NF · **Itens** (do Analítico) |
| Gerar ID de separação CD | PEDIDOS · **CÓD. PROD.** · QTD · COLETAR EM · FILIAL DEST. (sigla) | DATA, DESCRIÇÃO, FORN., UF, CIDADE |
| Gerar reversa de lojas | igual à de cima | igual |
| Analítico por pedido | **PEDIDO** · CÓD. PROD. · QTD · FALTA · VALOR FALTANTE | DATA, DESCRIÇÃO, FILIAL, EST. FRW, PEDIDOS ANTES, DISP. P/ ESTE, ATENDIDO |

Celular: PEDIDO · FANTASIA · SLA · R$ VENDA (já é assim).

### 3.2 Entregas

| Tabela | Grade | Popup |
|---|---|---|
| Entregas (hoje 18 colunas) | **NF** · CLIENTE (só o nome) · CIDADE · UF · SITUAÇÃO · SLA · DT. PREVISTA · ETAPA · TRANSPORTADORA · VLR NF (10) | **Datas:** DT. PED, DT. NF, DT. REAL · **Frete:** VLR FRETE, TBL FRETE, VLR REAL FRETE, RESPONSÁVEL · **Outros:** código do cliente, FILIAL, PRAZO (chip) |
| Pendências dos meses anteriores | MÊS · **NF** · CLIENTE · SITUAÇÃO · SLA · DT. PREVISTA · ETAPA · VLR NF (8) | o mesmo popup da de cima, mais UF e CIDADE |

Celular: NF · CLIENTE · SLA · VLR NF.

Coluna Editar (admin): fica à esquerda, como hoje.

### 3.3 Inadimplência

| Tabela | Grade | Popup |
|---|---|---|
| Títulos (18) | **NOME** · NF · PARC. · VENCIMENTO · DIAS ATRASO · FAIXA · SALDO · SITUAÇÃO · STATUS · VENDEDOR (10) | CLIENTE (código), VALOR, EMISSÃO, FILIAL, CIDADE, UF, SUPERVISOR, CONDIÇÃO |
| Por cliente (17) | **NOME** · SITUAÇÃO · FAIXA · TÍTULOS VENCIDOS · EM ATRASO · MAIOR ATRASO · A VENCER · STATUS · VENDEDOR (9) | CLIENTE (código), CIDADE, UF, SUPERVISOR, PRÓX. VENCIMENTO, LIMITE, PEDIDO EM ABERTO, ÚLTIMA COMPRA |
| Por vendedor / supervisor / filial / UF (12) | **NOME** · CARTEIRA ABERTA · A VENCER · EM ATRASO · % INADIMPL. · CLIENTES INADIMPL. (6) | **Atraso por faixa:** 1–15, 16–30, 31–60, 61–90, 91–180, +180 dias |
| Dia a dia (9) | igual a hoje (cabe) | — |

Celular: NOME · FAIXA (selo) · EM ATRASO (ou SALDO).

### 3.4 Visita

| Tabela | Grade | Popup |
|---|---|---|
| Por supervisor (21) | **SUPERVISOR** · REPRES. · META · VISIT. · % META · % CONV. · % FORA DE ROTA · CAD. C/ COMPRA · PROSP. · JORNADA LÍQ. (10) | **Cadastro:** CAD. · **Jornada:** INÍCIO, ÚLT. ATIV., DIAS < JORN. LÍQ., INTERV. ALMOÇO, DIAS ALMOÇO > MÁX. · **Tempo:** TMA, TMD · **Rota:** KM, KM/CLIENTE |
| Por vendedor (20) | **VENDEDOR** · META · VISIT. · % META · % CONV. · % FORA DE ROTA · CAD. C/ COMPRA · PROSP. · JORNADA LÍQ. · KM/CLIENTE (10) | SUPERVISOR (há filtro) + o mesmo popup de cima |
| Dia a dia (21) | DATA + DIA ("03/11 TER") · **VENDEDOR** · SITUAÇÃO · META · VISIT. · % META · % CONV. · % FORA DE ROTA · INÍCIO · ÚLT. ATIV. (10) | SUPERVISOR e o resto das métricas |
| Aderência dia a dia (2 + N + 1) | **VENDEDOR** · um quadradinho de ~38 px por dia útil (só o %, na cor do farol, com o cabeçalho "03" sobre "TER") · % ACUM. Cabe com até 23 DU a 1366. | SUPERVISOR; no quadradinho, um `title` com a data completa e o % |
| Cliente a cliente (23) | DATA · VENDEDOR · **CLIENTE** (fantasia) · SITUAÇÃO · STATUS · CURVA · DIAS S/ COMPRA · PEDIDO NO DIA · VALOR PEDIDO · JUSTIFICATIVA (com reticências) (10) | DIA, SUPERVISOR, CÓD., razão social, SEGMENTO, BAIRRO, CIDADE, ATRASO · **Roteiro:** SEQ. PREV., SEQ. REAL, INÍCIO, FIM, ATEND. · JUSTIFICATIVA inteira |
| Prospecção (14) | DATA · VENDEDOR · **ESTABELECIMENTO** · SEGMENTO · CIDADE · STATUS · RESULTADO (7) | HORA, DIA, SUPERVISOR, FONTE, UF, LINHAS DE INTERESSE, OBSERVAÇÃO |
| Indicação (14) | DATA · VENDEDOR · CLIENTE QUE INDICOU · **INDICADO** · CIDADE · SITUAÇÃO · VISITADA EM (7) | DIA, SUPERVISOR, CÓD. QUEM INDICOU, BAIRRO, SEGMENTO, OBSERVAÇÃO, REGISTRADO EM |

Celular: VENDEDOR (ou CLIENTE / ESTABELECIMENTO) · selo de % META ou SITUAÇÃO · VISIT.

### 3.5 Metas Equipe e Solicitação BAP

- **Metas** (Equipe, Top 30, UF, Cidade, Bairro, Segmento, Zona, Categoria, Família): a grade fica como está, porque cabe. Sem popup no PC. Celular: nome · selo de % ATING. · REAL, e o resto ao abrir.
- **Solicitação BAP:** grade como está nas sub-abas de até 7 colunas. Na "Detalhado por pedido" (a mais larga), use a mesma regra das 10 colunas, com a chave PEDIDO.

---

## 4. Cabeçalho padrão (todas as telas)

Uma faixa só, **sempre da mesma altura** no PC: 88 px a 1366 e 96 px a 1920, igual em todas as abas.

```
┌─ faixa verde (fundo #1F5A23 → #17401A, sem o canto claro) ─────────────────────────────┐
│ Farol de Pedidos   24/11/2026 08:30                              [BAP|AM|MA|PA]         │
│ SLA MÉDIO  PEDIDOS  R$ EM ABERTO  FATURAR (100%)  MAIS DE 4 DIAS  VOLUME               │
│ 3,6 dias   21       R$ 112 mil    10              10              401 un.               │
└────────────────────────────────────────────────────────────────────────────────────────┘
 Resumo  Pedidos·21  Solicitação BAP                 [Filtros▾] [🔍 Buscar pedido…] [Exportar▾]
```

**Conteúdo da faixa**

- **Linha 1:** título + data (sem "Dados de"; o `title` diz "Dados de 24/11/2026 08:30, horário de Manaus") + filtro de estado à direita.
- **Linha 2:** até 6 números (os do farol), em **todas** as abas. Quando o filtro tira os números, eles ficam e ganham o detalhe "sem o filtro", em vez de sumir.

**Telas sem números**

- **Usuários:** a faixa leva Ativos · Desativados · Troca pendente.
- **Trocar senha** e **Parcial:** a faixa só com o título, mesma altura.

**Cores**

- Rótulos `#E3F0E4` e números `#FFFFFF`.
- Tons alerta / atenção / ok com contraste ≥ 3:1 sobre o fundo novo: alerta `#FFC2B8`, atenção `#FFE7A3`, ok `#BDEBC0` (conferir com o design-de-marca).

**Lateral e celular**

- **Lateral:** 200 px. Nomes curtos dentro do grupo: Pré-venda › Pedidos; Pós-venda › Entregas, Inadimplência; Vendas › Visita, Metas Equipe. O título da faixa mantém o nome completo.
- **Celular:** a faixa com o título e a data, o filtro de estado com 44 px e os números em 3 colunas; as abas num segmentado sem rolagem: até 3 abas + "Mais ▾".

---

## 5. Página inicial = Painel Executivo no formato dos faróis (especificação)

### 5.1 Entrada

- `/` leva cada perfil à tela dele (redirecionamento 302):

  | Perfil | Tela inicial |
  |---|---|
  | admin, diretor, gerente | `/painel` |
  | pre_venda | `/farol/pv_pedidos` |
  | pos_venda | `/farol/pl_entregas` |
  | vendas | `/farol/vc_visitas` |

- A grade de quadrados (`home.html`) deixa de existir: a barra lateral é o menu.
- Na barra lateral, "Painel Executivo" vem no topo, no grupo **Diretoria**. Seguem Pré-venda, Pós-venda, Vendas e **Conta** (Usuários, Trocar senha, Sair).
- Sem pacote: a faixa mostra o título e a frase "Sem dados ainda. A primeira atualização chega às 06h30."

### 5.2 PC (BC3), 1366×768 sem rolagem da página

```
┌lateral──────┐┌─ faixa verde ─────────────────────────────────────────────────────────────┐
│BAP Central  ││ Painel Executivo  24/11/2026 08:30 · nov até 19/11 · 13 de 19 DU  [BAP|AM|MA|PA|RR]│
│DIRETORIA    ││ FATURAMENTO PROJ.     POSITIVAÇÃO PROJ.   PEDIDOS FAT. PROJ.                 │
│▌Painel Exec.││ R$ 165 mil · 100%     66 · 93%            85                                 │
│PRÉ-VENDA    │└───────────────────────────────────────────────────────────────────────────┘
│ Pedidos     │ Resultado  Produtividade  Por DU  Resumo  Faturamento  Volume  Visitas
│PÓS-VENDA    │ Positivação  Itens  Markup  Preço  Inadimplência               [Exportar▾]
│ Entregas    │┌Faturamento líquido───┐┌Positivação──────────┐┌Pedidos faturados────┐
│ Inadimplênc.││ MTD 11% ◔  MÊS 100% ●││ MTD 40% ◔  MÊS 93% ◕││                     │
│VENDAS       ││ out +11% set −31% jul││ out +11% set −31% … ││ out +11% set −31% … │
│ Visita      ││ ▇  █  ▆  ▁           ││ ▇  █  ▆  ▁          ││ ▇  █  ▆  ▁          │
│ Metas Equipe││ PA MA AM RR          ││ PA MA AM RR         ││ PA MA AM RR         │
│CONTA        │└──────────────────────┘└─────────────────────┘└─────────────────────┘
│ Usuários    │
│ AD admin Sair│
└─────────────┘
```

**Faixa e abas**

- **Faixa:** os 3 números de cabeça da aba (os do cartão RRM do PC, sem recalcular; o número do Diretor bate com o farol de origem) e o % do desafio comercial como detalhe. Nas abas de painel (Faturamento, Volume…), a faixa mostra os cartões `kpis` da aba.
- **Abas curtas, sem rolagem lateral:** Resultado · Produtividade · Por DU · Resumo · Faturamento · Volume · Visitas · Positivação · Itens · Markup · Preço · Inadimplência.
  - "Produtividade" do painel de visitas vira "Visitas" (acaba a duplicidade).
  - Se não couber a 1366, as 8 últimas vão para "Indicadores ▾".
- **Filtro de estado:** em aba só da BAP, o segmentado fica cinza (desabilitado), com `title` "Esta aba é só da BAP inteira". Some o aviso `AVISO_SO_BAP` do corpo.

**Cartões e textos**

- **Cartões:** sem o número grande, que subiu para a faixa (uma informação, um lugar). Ficam o título, os anéis MTD / MÊS, a faixa de variação e as barras por estado.
  - A altura sai do `min-height:540px` (`estilo.css`, `.rc`) e passa a ocupar o que sobra da tela (`flex:1`), como a tabela de cima dos faróis.
- **Textos:** "Painel do Diretor · resultado" sai; o nome é "Painel Executivo", e a aba diz qual visão é. O "como ler" vai para um ícone ⓘ com `title`, sem linha própria.

### 5.3 Celular (M3)

```
┌ BAP Central                       ☰ ┐
│┌ faixa ─────────────────────────────┐│
││ Painel Executivo · 24/11 08:30      ││
││ [BAP|AM|MA|PA|RR]  (44 px)          ││
││ FATUR. PROJ.  POSIT. PROJ.  PED. FAT.││
││ R$ 165 mil    66            85       ││
│└────────────────────────────────────┘│
│ [Resultado][Produtividade][Mais ▾]   │  ← segmentado, sem rolagem
│ ▾ Faturamento líquido   100% ●       │  ← aberto
│   MTD 11% · MÊS 100%                 │
│   out +11% · set −31% · jul −74%     │
│   PA ███░░ 9%                        │  ← barras deitadas por estado
│   MA ██████ 110%                     │
│   AM █████ 95%                       │
│ ▸ Positivação            93% ◕       │  ← fechado: título + % + selo
│ ▸ Pedidos faturados      85          │
└──────────────────────────────────────┘
```

- Primeiro cartão aberto e os outros fechados. Barras por estado deitadas (cabem em 390 px sem rolagem lateral).
- "Mais ▾" abre uma lista com as 10 outras abas (alvos de 44 px).

### 5.4 Estados

| Estado | O que aparece |
|---|---|
| Vazio (sem painel no pacote) | Faixa + "Sem dados do painel hoje." |
| Aba só da BAP com estado escolhido | Segmentado desabilitado (sem aviso no corpo) |
| Erro ou pacote velho (mais de 26 h) | Selo âmbar "Desatualizado" ao lado da data, na faixa |

### 5.5 Quem faz

- Dono: `modulo-web`.
- **Arquivos:**
  - `main.py`: rota `/` com redirecionamento; `pagina()` com `bc3=True` em todas as telas logadas e `rid="painel"` no `/painel`;
  - `templates/painel.html`: a faixa via `_bc3_cab.html`;
  - `home.html`: removido;
  - `estilo.css`: `.rc` sem `min-height`, mais as regras M3 do painel.
- Antes do PR: simulação PNG (antes/depois, 1366, 1920 e 390) para o Alexandre (regra 10).
- Validação do **design-de-marca** (logo único e tons da faixa).

---

## 6. Ordem sugerida do "ajuste fino"

1. **P1 rápido, só CSS e JS:**
   - G3 (mover a linha 466 para dentro de `@media(min-width:701px)`);
   - foco visível;
   - alvos de 44 px no celular;
   - cabeçalho com a mesma altura em todas as abas (G6);
   - contraste da faixa (G7).
2. **P1 de grade:** tabela `GRADE` em `tabelas.py`, popup genérico e M3 genérico (G2, G4, §3); rolagem por dentro sem páginas e contagem certa (G5).
3. **P1 de telas:** Painel Executivo e página inicial no BC3 (§5); Usuários, Login, Senha e Parcial no shell BC3 (G1); os avisos que explicam o sistema saem (Visita, Cobrar).
4. **P2/P3:** popup sem repetir a grade; textos (busca por farol, "Ver mais", Editar); selos de Usuários; reduzir movimento.

Cada lote com simulação antes (regra 10). Reteste em 1366×768, 1920×1080 e 390×844, com o critério "`scrollWidth` da caixa ≤ `clientWidth`" em toda tabela (o `ux_png.mjs` já mede).
