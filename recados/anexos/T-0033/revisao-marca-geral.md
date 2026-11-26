# Revisão geral de marca BAP AUTOPARTS: site BAP Central (todos os faróis e telas)

- **Pedido:** R-20261126-174334-alexandre (frente 1). Referências: R-20261125-174000-alexandre (visual C com as cores e o logo da BAP AUTOPARTS) e R-20261126-171559-alexandre (BC3 no PC, M3 no celular).
- **Commit revisado:** `c8f6004` (main da T-0031), extraído com `git archive` para `.../revisao-geral/marca-src/`. Nenhum arquivo do repositório foi alterado.
- **Telas:** a pasta `revisao-geral/telas/` do corretor-redundancias ainda estava vazia. Gerei as capturas com a fixture fictícia (`simular_farol.paginas` + Chromium), em 1366 px e 390 px: `.../revisao-geral/marca-telas/*.png` (login, home, painel, usuários, senha, os 5 faróis, a tabela de Pedidos e a parcial).
- **Base da marca:** `docs/marca/` **não existe** (ver MC-0012). Usei a paleta de `bap_visual.py` (VERDE #62BB47, VERDE_ESCURO #2F7D32, TEXTO #1E2722, SUAVE #69736D, VERMELHO #B3261E, AMARELO #B7791F e os tons claros), o logo `SISTEMA BAP/recursos/logo_bap.png` (o "b" verde em círculo), o logo embutido no CSS do visual C (`estilo.css:219`) e as decisões acima.

## Resumo
| | Qtde | Onde |
|---|---|---|
| 🔴 | 3 | logo falso e nome ausente na casca BC3; "BAP Auto Parts" na mensagem de cobrança ao cliente; PDF da tabela sem a marca |
| 🟡 | 10 | duas cascas; contraste da faixa; cores soltas; botão do WhatsApp; fontes; nome do Painel; favicon; nome errado no PC; manual; teste |
| 🟢 | 4 | rótulo do estado; cor do número na faixa; tela Parcial; Poppins na web |

**Parecer: segura.** A casca BC3, que hoje veste todos os faróis, troca o logo aprovado por um quadrado verde e não mostra "BAP AUTOPARTS" em nenhum lugar da tela. Isso fere a decisão de 25/11 e a regra 8.

## Achados

### 🔴 MC-0001: casca BC3 sem o logo e sem "BAP AUTOPARTS"
| Campo | Conteúdo |
|---|---|
| Onde | Os 5 faróis (Pedidos, Entregas, Inadimplência, Visita, Metas Equipe), a Parcial e o Editar, no PC e no celular. `web/app/templates/base.html:15` e `:28`, `web/app/static/estilo.css:350` |
| Tipo | logo · aplicação |
| Fere | R-20261125-174000 ("cores e o logo da BAP AUTOPARTS"); regra 8 ("BAP AUTOPARTS" nos materiais) |
| Gravidade | alta: o Diretor e a equipe veem a marca errada em todas as telas de farol |
| O que se vê | `.bc3-marca i{...background:#2F7D32}` desenha um quadrado verde liso no lugar do símbolo "b". O texto é só "BAP Central". O nome "BAP AUTOPARTS" fica apenas no `<title>` da aba. No visual C (login, home, painel) o logo certo aparece (`.marca::before`) |
| Correção | (1) Tirar o logo do data URI e publicar como ativo: `web/app/static/logo_bap_56.png` (o mesmo PNG de 56×55 px do `estilo.css:219`). (2) `estilo.css:350`: `.bc3-marca i{width:24px;height:24px;border-radius:7px;background:#2F7D32}` → `.bc3-marca i{width:28px;height:28px;flex:none;background:url(/static/logo_bap_56.png) center/contain no-repeat}`, sem raio e sem fundo, com o logo nunca recolorido. (3) `base.html:15` e `:28`: `<i aria-hidden="true"></i>BAP Central` → `<i aria-hidden="true"></i><span>BAP Central<small>BAP AUTOPARTS</small></span>`, com `small{display:block;font-size:10.5px;font-weight:600;color:#69736D;letter-spacing:.04em}` (SUAVE). Tamanho mínimo do símbolo: 24 px |
| Dono | modulo-web |

### 🔴 MC-0002: "BAP Auto Parts" na mensagem de cobrança que o site manda ao cliente
| Campo | Conteúdo |
|---|---|
| Onde | Farol de Inadimplência → "Cobrar no WhatsApp". O texto vem pronto do PC no pacote: `cobranca_whatsapp.py:36` (`MODELO`) |
| Tipo | voz · aplicação |
| Fere | regra 8 |
| Gravidade | alta: marca errada visível ao **cliente** |
| Correção | `"Aqui é do financeiro da BAP Auto Parts.\n\n"` → `"Aqui é do financeiro da BAP AUTOPARTS.\n\n"`. Conferir os testes que citam o texto. A web só repassa a mensagem e não muda nada |
| Dono | modulo-posvenda |

### 🔴 MC-0003: PDF "desta tabela" exportado pelo site sem a marca
| Campo | Conteúdo |
|---|---|
| Onde | Exportar → "PDF desta tabela", em todos os faróis. `web/app/exportar.py:236-240` (título, rodapé e faixa do cabeçalho), `web/app/main.py:498` (rodapé) |
| Tipo | aplicação · cor |
| Fere | regra 8; o PDF do PC (`bap_visual.py:3793-3810`) sai com logo e faixa PRETO_BAP |
| Gravidade | alta: material que sai do site para o Diretor e a equipe sem o nome da empresa |
| Correção | (1) `main.py:498`: `rod = f"{render.FAROIS[rid][0]} · ..."` → `rod = f"BAP AUTOPARTS · {render.FAROIS[rid][0]} · ..."`. (2) Faixa do cabeçalho em `exportar.py:240`: `0.18 0.36 0.23 rg` (#2E5C3B, fora da paleta) → `0.184 0.490 0.196 rg` (VERDE_ESCURO #2F7D32). (3) Excel em `exportar.py:125`: `FF2F5D3A` → `FF2F7D32`. (4) Numa segunda etapa, o logo no canto do PDF (o `pdf_imagem` já embute PNG), com simulação antes |
| Dono | modulo-web |

### 🟡 MC-0004: duas cascas no mesmo site
| Campo | Conteúdo |
|---|---|
| Onde | O login, a home, o Painel Executivo, os Usuários e o Trocar senha usam a casca do visual C (barra branca no topo, logo real, rodapé "BAP AUTOPARTS · BAP Central web"). Os faróis usam a casca BC3 (barra lateral). `web/app/main.py:145` (`render.BC3 = set(FAROIS)`) |
| Tipo | aplicação |
| Fere | R-20261126-171559 ("padrão BC3 em todos os faróis e telas") |
| Correção | BC3 em todas as telas logadas. O login ganha a versão BC3 centralizada, com o logo grande e "BAP AUTOPARTS". Isso já está na frente 2 de R-20261126-174334 (página inicial no Painel Executivo, no formato dos faróis). Simulação antes |
| Dono | modulo-web (designer-ux no layout) |

### 🟡 MC-0005: contraste do texto pequeno na faixa verde
| Campo | Conteúdo |
|---|---|
| Onde | A faixa BC3 de todos os faróis: "Dados de …" (12 px) e os rótulos dos números (11 px). `estilo.css:361`, `:364`, `:369`, `:370` |
| Tipo | cor (contraste) |
| Medido | #D2E7D3 sobre o início do gradiente (medido nos prints: #307934 no PC, #348438 no celular) dá **4,1:1 e 3,6:1**. O mínimo para texto pequeno é 4,5:1 |
| Correção | Início do gradiente `#3C9440` → `#2F7D32` (VERDE_ESCURO, que já é da paleta): `radial-gradient(120% 140% at 0% 0%,#2F7D32 0%,#1B4D1F 70%)`. Texto pequeno da faixa (`.bc3-quando`, `.bc3-k small`, `.bc3-k em`, `.bc3-aviso-k`): `#D2E7D3` → `#FFFFFF`, o que dá 5,1:1 no pior ponto. A hierarquia fica pelo peso e pelo tamanho, não pela cor |
| Dono | modulo-web |

### 🟡 MC-0006: cores soltas e "quase iguais", sem constante
| Campo | Conteúdo |
|---|---|
| Onde | `estilo.css`. Há 7 verdes diferentes para o mesmo papel: #2F7D32, #2f7d32, #2b8a3e (`:1`), #1e8e3e (`:159`), #4FA236 (`:234`, `:243`, `:290`), #3C9440 (`:361`) e #7DB46A (`:260`). O farol amarelo tem #E0A43A × AMARELO #B7791F. Restos do visual antigo: `:root{--azul:#0b3a6b;--lar:#e8590c…}` (`:1`), `.aviso.atencao #fff3bf`, `.aviso.alerta #ffc9c9`, `.aviso.info #d0ebff` (`:10`), `.faixa-pc #a5d8ff` (`:168`), `.selo-*` (`:150`) |
| Tipo | cor |
| Fere | Checklist A: só a paleta, por constante; nada "quase igual" |
| Correção | Um bloco `:root` com as constantes de `bap_visual.py`: `--verde:#62BB47; --verde-escuro:#2F7D32; --verde-claro:#E5F3DF; --texto:#1E2722; --suave:#69736D; --fundo:#F3F4F2; --vermelho:#B3261E; --vermelho-claro:#FBE3E1; --amarelo:#B7791F; --amarelo-claro:#FFF4D6; --grade:#ECEEEB`. O CSS passa a usar `var(--…)` no lugar do hex. Trocas: #2b8a3e, #1e8e3e e #4FA236 → `var(--verde-escuro)`; #E0A43A → `var(--amarelo)`; #fff3bf → `var(--amarelo-claro)`; #ffc9c9 → `var(--vermelho-claro)`. Apagar `--azul` e `--lar`. As cores que o Alexandre viu e aprovou nas simulações (barras #7DB46A, #D8B56E, #8FA79A; faixa #1B4D1F; números da faixa #FFB4A9, #FFE08A, #A6E3A9) ganham constante própria e entram no manual (MC-0012). Sem troca de tom, para não mudar o que ele aprovou |
| Dono | modulo-web |

### 🟡 MC-0007: botão "Cobrar no WhatsApp" fora da paleta e com contraste baixo
| Campo | Conteúdo |
|---|---|
| Onde | Fila de cobrança (`_fila.html`, `.cob-link.botao`); `estilo.css:159-160` |
| Tipo | cor |
| Medido | branco sobre #1e8e3e = 4,2:1 (o mínimo é 4,5:1) |
| Correção | `.botao{background:#1e8e3e}` → `#2F7D32` (5,1:1). `.cob-enviado` com borda e texto `#1e8e3e` → `#2F7D32` |
| Dono | modulo-web |

### 🟡 MC-0008: três pilhas de fonte
| Campo | Conteúdo |
|---|---|
| Onde | `estilo.css:3` (`system-ui,Segoe UI,Roboto`), `:216` (`"Segoe UI",system-ui,Roboto`) e `:346` (`Inter,"Segoe UI",system-ui`). A Inter não é carregada nem foi aprovada: aparece só em quem a tem instalada |
| Tipo | tipografia |
| Correção | Uma pilha só, num lugar: `body{font-family:"Segoe UI",system-ui,-apple-system,Roboto,sans-serif}`. Tirar a `Inter` do `:346` |
| Dono | modulo-web |

### 🟡 MC-0009: o Painel com dois nomes
| Campo | Conteúdo |
|---|---|
| Onde | O menu e a aba do navegador dizem "Painel Executivo"; o título da tela diz "Painel do Diretor · resultado" (`painel.html:24`, `tela.titulo` vindo do pacote) |
| Tipo | voz (nome de produto) |
| Correção | No site, um nome só: "Painel Executivo", que é o termo do Alexandre em R-20261126-174334. Título: `Painel Executivo · resultado`. O ajuste é na exibição (`render`), sem mexer no pacote do PC |
| Dono | modulo-web |

### 🟡 MC-0010: sem favicon nem ícone de atalho
| Campo | Conteúdo |
|---|---|
| Onde | `base.html:3-9`: não há `<link rel="icon">`. A aba do navegador e o atalho na tela do celular ficam sem marca |
| Tipo | ícone |
| Correção | O símbolo "b" verde (recorte do `logo_bap.png`, só o círculo) em `static/favicon-32.png` e `static/apple-touch-icon-180.png`, mais `<link rel="icon" href="/static/favicon-32.png">` e `<link rel="apple-touch-icon" href="/static/apple-touch-icon-180.png">`. Conferir que fica reconhecível em 16 px |
| Dono | modulo-web |

### 🟡 MC-0011: nome errado da empresa no PC (fora do site, mesma regra 8)
| Onde | Texto | Dono |
|---|---|---|
| `email_parcial.py:214`, `:324` | "BAP Auto Parts · Farol de Metas" (assinatura do e-mail) | modulo-farois |
| `email_inadimplencia.py:406`, `:433` | "BAP Auto Parts · Farol de Inadimplência" | modulo-posvenda |
| `bap_visual.py:359` | "BAP AUTO PARTS · {ÁREA}" (cabeçalho das telas Tkinter) | modulo-farois |
| `bap_visual.py:2851` | "BAP AUTO PARTS · …" (A1 do Excel) | modulo-farois |
| `bap_visual.py:3793` | `author="BAP Auto Parts"` (propriedades do PDF) | modulo-farois |
| `bap_automation.py:6099` | "BAP AUTO PARTS · TRADE" (HTML de alterações de preço) | modulo-robo |

- **Correção:** trocar por "BAP AUTOPARTS" nos seis pontos.
- **Não mexer** em `meta_nucleo.py:2818` e `bap_dados.py:413`: ali o texto serve para achar o CNPJ interno pelo nome (regra de negócio), não é marca.

### 🟡 MC-0012: o manual da marca não existe
- **Onde:** `docs/marca/` não existe no repositório.
- **Tipo:** governança da marca.
- **Correção:** eu monto o rascunho do `docs/marca/manual.md` e do `decisoes.md` só com o que já tem "aprovo" registrado: a paleta do `bap_visual.py`, o visual C (25/11), o BC3 e o M3 (26/11) e o logo `logo_bap.png`. O Alexandre aprova pelo po, e só então o rascunho vira manual.
- **Dono:** design-de-marca, com o "aprovo" do Alexandre.

### 🟡 MC-0013: o teste de marca não pega o logo falso
- **Onde:** `web/tests/test_T0020_visual.py:74`. O teste só confere que o data URI existe no CSS, e continua verde com a casca BC3 sem o logo.
- **Correção:** criar o teste `test_T0020_casca_bc3_tem_logo_e_nome`, que abre um farol logado e exige o logo em `.bc3-marca` e o texto "BAP AUTOPARTS" no HTML.
- **Dono:** modulo-web (com o `testes`).

### 🟢 MC-0014: o mesmo filtro com dois rótulos
- **Onde:** o filtro de estado diz "BAP" na faixa BC3 (`_bc3_cab.html:17`) e "BAP inteira" no painel (`painel.html:14`).
- **Correção:** um rótulo só, "BAP", quando o painel for para o BC3.
- **Dono:** modulo-web.

### 🟢 MC-0015: cor do número de farol na faixa
- **Onde:** o número "alerta" da faixa (#FFB4A9, salmão) lê como laranja, não como vermelho. Exemplos: "% da meta 75,0%" e "Mais de 4 dias".
- **Correção:** sugiro número branco com o ponto de farol antes do rótulo, como já se faz em `.kpi-rot::before`. Muda o visual aprovado, então só com simulação e "aprovo".
- **Dono:** designer-ux, depois modulo-web.

### 🟢 MC-0016: tela Parcial fora do padrão BC3
- **Onde:** `parcial.html`. Tem a barra lateral, mas não a faixa verde; o título fica solto e o aviso amarelo é o antigo #fff3bf.
- **Correção:** a faixa BC3 com "Parcial · {farol}" e o aviso em AMARELO_CLARO #FFF4D6.
- **Dono:** modulo-web.

### 🟢 MC-0017: a fonte da marca não chega à web (proposta, não ajuste)
- **Onde:** a Poppins é a fonte do catálogo e dos PDFs do PC (`SISTEMA BAP/recursos/Poppins-*.ttf`, `bap_visual.py:3740`). A web não a usa.
- **Proposta:** títulos e números da faixa em Poppins, hospedada no próprio site. Mexe na marca, então segue a regra 10: 2 opções em imagem, depois o "aprovo" do Alexandre.
- **Dono:** design-de-marca (proposta).

## O que está conforme
- As imagens da parcial já saem com "BAP AUTOPARTS" (T-0027, #94).
- O login, a home, o painel e os usuários mostram o logo certo, sem distorção, e "BAP AUTOPARTS" no topo e no rodapé.
- O verde, o amarelo e o vermelho de farol aparecem só para estado: linhas, pontos, SLA e anéis.
- Não há marca de terceiros nem grafismo cultural.
- No celular, o M3 segue a decisão: a lista abre e as tabelas de baixo são recolhíveis.

## Fora do meu escopo (encaminhar, não catalogado)
- **Farol de Inadimplência (PC):** há um vão grande vazio entre a faixa e o cartão "Em atraso". É layout: vai ao designer-ux.

## Pendências
- Ainda não enviei recado aos donos nem gravei parecer em `docs/marca/pareceres/`: o pedido não tem número de tarefa e foi "só auditoria". Quando o gerente abrir as tarefas, mando um recado por dono com as correções acima.
- O reteste é feito nos prints depois da correção, no head SHA do PR.
