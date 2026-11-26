# Inventário PC × site da BAP Central e proposta de tarefas (T-0033 em diante)

Autor: engenheiro-software · 26/11/2026 (Manaus) · só leitura: nenhum arquivo do repositório foi alterado.
Pedido: R-20261126-174334-alexandre ("migrar TUDO", página inicial no Painel Executivo no formato dos faróis, "melhore o que achar que precisa"). Decisões que valem: R-20261126-171559-alexandre (BC3/M3; diretor só Resumo nos faróis novos; TOTAL A PAGAR só para admin, gerente e diretor; Fretes na próxima leva; champions_config.json pela web só admin, gravado pelo robô). Passagem: R-20261126-173917-po.

**Base lida:** `origin/main` = **8cda492**. O #124 (T-0032) **já entrou** depois do c8f6004 que o pedido cita. Lidos também os PRs abertos #89, #91, #97, #102, #103, #105, #106, #93, #98, #100, #107 e #82, por `git diff origin/main...origin/<branch>`.

**Como contei o PC:**
- `bap_central.QUADRADOS` e os botões do quadrado do Analista;
- os botões do cabeçalho de `bap_relatorios._BaseRelatorio`, as janelas auxiliares e `relatorios_nucleo.CATALOGO` + `LEGADO`;
- as abas, geradas com `rn.montar` sobre as bases congeladas, numa cópia de trabalho do main fora do repositório;
- `bap_analista.MODULOS`, `CADASTROS_PAINEIS` e `PAINEIS`, mais as abas do `bap_planner`, do `bap_meta` e do `bap_oportunidade`.

**Estados usados:**
- **site**: já no main e no ar;
- **PR #n**: em PR aberto;
- **falta**: ainda não começou;
- **PC**: fica no PC, com o motivo na seção 2;
- **não migrar**: saiu do PC ou foi substituído, com o motivo na seção 2.

**Perfis:**
- Perfis do site (`web/app/usuarios.PERFIS`): admin, diretor, gerente, pre_venda (Juliana), vendas (Mayara), pos_venda (Estefanie).
- O PC tem também o quadrado do Analista (Leandro, controlado pelo `bap_acesso.json`) e o de Trade, cuja vaga está aberta. **O site não tem perfil "analista" nem "trade".**

---

## 1. Inventário (uma linha por item do PC)

### 1.1 Entrada e acesso

| # | Item | Arquivo/função no PC | Quem usa | Estado | Observação |
|---|---|---|---|---|---|
| 1 | Tela dos quadrados (BAP Central) | `bap_central.Central` | todos | site (parcial): `/` = `home.html` (lista de botões) | **Falta o pedido do Alexandre:** abrir no Painel Executivo no BC3/M3 (T-0034). Tk. |
| 2 | Quem vê o quadrado do Analista | `bap_central.ve_analista` + `bap_acesso.json` (usuário do Windows) | analista | não migrar (substituído) | No site, o acesso é por perfil e login (`usuarios.py`). Falta o perfil "analista" (T-0036). |
| 3 | Horários de envio de cada área (ENVIOS) | `bap_central.ENVIOS` | assistentes | falta | Texto fixo. Melhoria: mostrar no cabeçalho do grupo do menu lateral (T-0034). |
| 4 | Trocar senha / usuários | — (no PC é o login do Windows) | todos / admin | site (`/senha`, `/usuarios`) | Fora do BC3: passo 3 da passagem (T-0034). |

### 1.2 Quadrado Faturamento (Juliana · pre_venda)

| # | Item | Arquivo/função no PC | Quem usa | Estado | Observação |
|---|---|---|---|---|---|
| 5 | Farol de Pedidos · Resumo e aba Pedidos | `rn.farol_pedidos` (`pv_pedidos`) | pre_venda, gerência | site (T-0021/28/29/30/31) | BC3. A caixa "Ignorar fora da base" segue a RN-GER-013. |
| 6 | Detalhe do pedido + autorização de venda | `bap_relatorios.DetalhePedido`, `autorizacoes.gravar` | pre_venda (no site, só admin) | site (popup T-0028, edição T-0021) | **Grava dado digitado** (`_AUTORIZACOES`) pelo robô (RN-GER-012). O PC fica só leitura (`AUTORIZA_EM = ()`). |
| 7 | Aba Solicitação BAP (7 sub-abas: Lojas, CD, FRW, Manual, Detalhado, Produtos e Filiais excluídos) | `bap_relatorios.AbaSolicitacaoBap` | pre_venda | site (leitura) | Corte do pacote: só as linhas em aberto quando o pacote passa do teto. |
| 8 | Trocar loja de coleta (Solicitação BAP) | `bap_relatorios.DialogoTrocaColeta` → `solicitacao_bap` | pre_venda | **falta** | **Grava:** ProdutosExcluir + linha nova + CSV. Na web, sairia como edição via robô (T-0040). |
| 9 | Parcial Pedidos (Acumulado/D-1/Hoje, PNG/PDF) | `DialogoParcial("pedidos")`, `parcial_imagem` | pre_venda | site (T-0026, botão T-0032) | O PNG vem pronto do PC. |
| 10 | CSVs do Protheus (autorizações) | `pv_pedidos` | pre_venda, admin | site (T-0021) | — |
| 11 | Excel/PDF por aba | `_menu_exportar` | todos | site (`/farol/{rid}/exportar`) | O PDF exporta só uma aba por vez no site. |
| 12 | Painel de indicadores (4 abas) | `rn.painel_indicadores` (`pv_indicadores`) | pre_venda | PR #89/#91/#97 (T-0024) | Gráficos viram blocos de barras. Filtros MÊS, FILIAL, VENDEDOR, SEGMENTO: só o mês do pacote. |
| 13 | Farol de Estoque FRW (aba Estoque FRW) | `rn.estoque_frw` (`pl_frw`) | pre_venda, pos_venda | PR #89/#91/#97 (T-0024) | 1.534 linhas (0,28 MB). |
| 14 | Farol DDR · Faturamento | `rn.farol` (`farol_pv`), `farol_ddr.gravar_marcacoes` | pre_venda | PR #93/#98/#100/#107 (T-0025, refazer) | **Grava** STATUS/MOTIVO (marcações) pelo robô. |

### 1.3 Quadrado CRM e Pós-venda (Mayara · vendas)

| # | Item | Arquivo/função no PC | Quem usa | Estado | Observação |
|---|---|---|---|---|---|
| 15 | Farol de Metas Equipe · Resumo + 9 abas | `rn.acompanhamento_meta` (`vc_meta`) | vendas, gerência | site (T-0022) | Desafio comercial em tudo (regra 8). |
| 16 | Farol de Metas · aba "Acomp. RH" | `vc_meta` | analista, gerente | **falta** | É a meta RH: só pode aparecer no "Exportar para o RH" e na parcial de RV (regra 8). Proposta: só admin/gerente (T-0038). |
| 17 | Farol de Metas · Exportar para o RH (PDF/Excel) | `_BaseRelatorio.exportar_rh`, `rn.exportar_rh` | analista, gerente | **falta** | Leva RV e nome de vendedor: perfil restrito (decisão do Alexandre). |
| 18 | Farol de Metas · Enviar Parcial via e-mail | `email_parcial` (Outlook clássico por COM, `.eml` de reserva) | analista | PC (o envio) / falta (o PDF de cada pessoa para baixar) | **Outlook local + e-mail do Planner.** Ver a seção 2. |
| 19 | Farol Roteirização (8 abas, com Calendário) | `rn.resumo_planner` (`vc_planner`), `CalendarioVisitas`, `DiaDoCalendario` | vendas | PR #89/#91/#97 (T-0024) | **"Por cliente" tem 7.116 linhas (3,9 MB).** A aba Calendário é um desenho próprio no PC (`t["calendario"]`): o PR a trata como tabela livre; conferir na simulação. |
| 20 | Roteirização · Enviar Rota da semana por e-mail | `EnvioRota`, `email_rota` (Outlook) | analista, vendas | PC (o envio) / falta (o PDF por vendedor no site) | Outlook local. |
| 21 | Farol de Clientes (8 abas) | `rn.base_e_oportunidades` (`vc_base`) | vendas | PR #89/#91/#97 (T-0024) | **"Clientes" tem 3.017 linhas, com nome, cidade e bairro**: só RN-GER-011 e `COLUNAS_FORA`. |
| 22 | Farol de Visita · Resumo + 7 abas | `rn.farol_visitas` (`vc_visitas`) | vendas | site (T-0017/26/31) | O "Cliente a cliente" é a 2ª coisa cortada quando o pacote passa do teto. |
| 23 | Farol de Visita · Parcial Visitas e Conversão | `DialogoParcial("visitas")` | vendas | site | — |
| 24 | Farol de Visita · Atualizar visitas | `visitas_maxima` (login na Máxima), `prospeccao_forms` (Excel do Forms no OneDrive) | vendas | PC | **Segredo** (login da Máxima) + arquivo sincronizado do OneDrive. Ver a seção 2. |
| 25 | Campanhas BAP (7 abas) | `rn.bap_champions` (`vc_champions`) | vendas, gerência | PR #98/#100/#107 (T-0025, refazer) | **Falta:** TOTAL A PAGAR só para admin/gerente/diretor (permissão por coluna, mecanismo novo) e diretor só Resumo. |
| 26 | Campanhas · Parâmetros das campanhas | `DialogoChampions` → `champions_config.json` | analista | **falta** | **Dado digitado (regra 7)**, autorizado pela web só para o admin e gravado pelo robô (26/11). |
| 27 | Campanhas · Exportar campanha (Excel da premiação) | `_BaseRelatorio.exportar_campanha` | analista | PC | **Leva CPF, CNPJ e e-mail** (RN-GER-011 / regra 6). |
| 28 | Farol de Giro de Produtos (7 abas) | `rn.giro_produtos` (`pl_giro`) | vendas | PR #89/#91/#97 (T-0024) | **"Todos os produtos" tem 17.592 linhas (3,7 MB).** |
| 29 | Farol DDR · CRM | `farol_vc` | vendas | PR (T-0025, refazer) | Grava marcações pelo robô. |

### 1.4 Quadrado Logística de Entrega e Qualidade (Estefanie · pos_venda)

| # | Item | Arquivo/função no PC | Quem usa | Estado | Observação |
|---|---|---|---|---|---|
| 30 | Farol de Entregas · Resumo + Entregas + Pendências | `rn.entregas` (`pl_entregas`), `Edicao`, `pos_venda.gravar_edicoes` | pos_venda | site (edição só admin, T-0021) | **Dado digitado** `_EDICOES_POS_VENDA` pelo robô. O PC fica só leitura (`EDICAO_SO_WEB`). |
| 31 | Farol de Entregas · Parcial Entregas | `DialogoParcial("entregas")` | pos_venda | site (só quem vê a tabela) | — |
| 32 | Farol de Garantias (4 abas) + janela da garantia | `rn.garantias`, `DialogoGarantia`, `garantias` | pos_venda | PR #102/#103/#105/#106 (T-0023, refazer) | **Dado digitado** `_GARANTIAS` pelo robô. "Histórico de compra" tem 4.949 linhas (1,4 MB). |
| 33 | Farol de Devolução e Reembolsos (5 abas) | `rn.devolucoes`, `Edicao` | pos_venda | PR (T-0023, refazer) | Edição de Devoluções = `_EDICOES_POS_VENDA`. |
| 34 | Farol de Inadimplência · Resumo + 7 abas | `rn.farol_inadimplencia` | pos_venda | site (T-0017/26) | RN-POS-004. |
| 35 | Inadimplência · Cobrar no WhatsApp | `cobranca_whatsapp.janela` | pos_venda | site (`cobranca.py`, RN-POS-001..003) | Diário só acrescenta (`COBRANCA_WEB.csv` pelo robô). |
| 36 | Inadimplência · Enviar por e-mail (carteira de cada vendedor) | `email_inadimplencia` (Outlook) | pos_venda | PC (o envio) / falta (o PDF de cada pessoa) | Outlook local. |
| 37 | Farol de NCC (5 abas) | `rn.farol_ncc`, `ncc_controle.gravar` | pos_venda | PR (T-0023, refazer) | **Dado digitado** `_NCC` pelo robô. |
| 38 | Farol DDR · Pós-venda | `farol_pl` | pos_venda | PR (T-0025, refazer) | Grava marcações pelo robô. |
| 39 | Fretes (4 abas, edição de Notas com frete) | `rn.fretes` (`pl_fretes`, id do LEGADO) | pos_venda | **falta** (próxima leva, decisão de 26/11) | **Dado digitado** `_EDICOES_POS_VENDA`. Até lá, a edição fica no PC. Não está nos QUADRADOS: abre pelo atalho. |

### 1.5 Quadrado Trade Marketing (vaga)

| # | Item | Arquivo/função no PC | Quem usa | Estado | Observação |
|---|---|---|---|---|---|
| 40 | Farol de Expositores (4 abas, cadastro de linha nova) | `rn.farol_expositores`, `expositores.gravar_edicoes` | trade (hoje admin/gerente) | PR (T-0025, refazer) | Grava `ACOMPANHAMENTO_EXPOSITORES.xlsx` pelo robô. Sem perfil trade no site. |

### 1.6 Quadrado Analista Comercial (Leandro · sem perfil no site)

| # | Item | Arquivo/função no PC | Quem usa | Estado | Observação |
|---|---|---|---|---|---|
| 41 | Painel Executivo: Painel · resultado, produtividade e por dia útil (RRM) | `rn.painel_executivo`, `painel_rrm`, `painel_cartoes`, `painel_diretor.calcular` | admin, diretor, gerente | site (T-0013/14/22) | **Não está no BC3** (passo 3 da passagem). Filtro só por estado. |
| 42 | Painel Executivo: 9 painéis (Resumo gerencial ... Inadimplência) | idem | idem | site (T-0022) | — |
| 43 | Painel Executivo: 17 tabelas "só exportar" (Faróis, Por filial ... Executivos · analítico) | idem (`so_exportar`) | analista, diretor | **falta** | Excel do Painel (T-0039). |
| 44 | Painel Executivo: filtros gerais (cidade, supervisor, vendedor, segmento, categoria, sistema, família, linha, produto) e "Somar pedidos em aberto" | idem (`parametros`) | analista, diretor | **falta** (o site só filtra por estado) | O site não calcula (ADR 0001). Cada visão a mais aumenta o pacote. Proposta: supervisor e "com pedidos" (T-0039). |
| 45 | Painel Executivo: Metas executivas (cadastro) | `bap_meta.py --executivas` | analista | **falta** | **Grava** a config do Gerador de Meta: via robô, com o "autorizo" do Alexandre (T-0042). |
| 46 | Painel Executivo: Exportar para o RH (resumo + analítico por indicador) | `DialogoRHExecutivo` | analista | **falta** | Perfil restrito (T-0038). |
| 47 | Farol de Saldo (4 abas) | `rn.saldo_desconto` (`vc_saldo`) | analista | **falta** | O detalhe do pedido só lê. 1.587 linhas. |
| 48 | Farol de Markup (11 abas) | `rn.farol_markup` | analista | **falta** | **9.541 linhas (2,5 MB).** |
| 49 | Farol de Preço (5 abas, com Pesquisa de mercado do BAP Ajuda) | `rn.farol_preco` | analista | **falta** | A pesquisa vem de `respostas_bap_ajuda` (texto livre: RN-GER-011). |
| 50 | Divergências clientes Planner × Protheus (3 abas) + Exportar para correção | `rn.divergencias_clientes` | analista | **falta** | **A aba "Sem coordenada / endereço" lista endereço**: só o código e a cidade podem ir. O Excel de correção sairia como download só para o admin. |
| 51 | Campanhas BAP (o mesmo do #25) | — | analista | PR (T-0025) | — |
| 52 | Kits promocionais | `bap_oportunidade.py --kits` | analista | **falta** | Ver #58. |
| 53 | Parcial BAP (pedidos + visitas) | `DialogoParcial("bap")`, `rn.parcial_bap` | analista → grupo de vendas | **falta** | PNG pronto do PC, como as outras parciais (T-0038). |
| 54 | Atualizar dados | `bap_dados.atualizar_tudo` | analista | PC | Arquivos locais e cache. No site: a hora de cada fonte (T-0043). |
| 55 | BAP Tools (janela do robô) | `bap_janela.py` → `bap_automation` | analista | PC | Rede interna + cofre. No site: só o estado da rodada (T-0043). |
| 56 | Abrir o BAP Analista | `bap_analista.Analista` | analista | falta (ver #57 a #64) | Tk. |

### 1.7 BAP Analista (cadastros que o quadrado abre)

| # | Item | Arquivo/função no PC | Quem usa | Estado | Observação |
|---|---|---|---|---|---|
| 57 | Roteirização / Planner: 8 abas (Resumo, Vendedores e supervisores, Zonas, Rota por cidade, Analítico da rota, Base cliente, Exportar Protheus, Parâmetros) | `bap_planner.App` (7.147 linhas, **lógica dentro da tela Tk**) | analista | **falta** | **Grava:** `planner_config.json`, `SISTEMA BAP/PLANNER_MESES`. O Recalcular usa `geografia` (pesado). O JSON da Máxima/Protheus pode virar download. Leitura: T-0041. Edição: T-0042. |
| 58 | Kits promocionais / Oportunidades: 7 abas | `bap_oportunidade.Oportunidades` (3.410 linhas) | analista | **falta** | Grava `oportunidade_config.json`. |
| 59 | Metas e RV: 6 abas (Parâmetros, Painel de meta, Acompanhamento, Metas executivas, Quem conta na meta, Imprimir/exportar) | `bap_meta.Meta` (4.232 linhas) | analista | **falta** | Grava `meta_config.json`. **Meta RH:** o painel de meta mostra a meta RH: só admin/gerente. |
| 60 | Agenda de cidades dos supervisores | `agenda_cidades` (dentro do Planner) | supervisores, analista | **falta** | Grava a agenda do mês (T-0042). |
| 61 | Meta de saldo (por UF, dividida por vendedor) | `bap_analista` + `saldo_meta` | analista | **falta** | Grava `meta_saldo_config.json`. |
| 62 | Expositores (trade): cadastro | `bap_analista` (`_ex_*`) + `expositores` | analista | PR (T-0025, cadastro de linha nova) | Grava `expositores_config.json` / ACOMPANHAMENTO pelo robô. |
| 63 | Entrega: Transportadoras (% frete, mínimo, cidades) + SLA por filial/cidade | `bap_analista` + `transportadoras` | analista | **falta** | **`transportadoras_config.json` é dado digitado (regra 7):** precisa do mesmo "autorizo" do champions. |
| 64 | Farol DDR: abrir / gerar o do mês / gerar o próximo + cadastro da rotina | `bap_analista`, `farol_ddr`, `farol_ddr_config.json`, `gerar_farol_ddr.bat` | analista | **falta** (cadastro) / PC (gerar) | Gerar o mês cria um .xlsx local: o robô gera e o site mostra. |
| 65 | Relatórios do time (lista do que cada assistente vê) | `bap_analista` (PAINEIS) | analista | não migrar (substituído) | O menu do site, por perfil, é esta lista. |

### 1.8 Recursos comuns das telas do PC

| # | Item | Arquivo/função no PC | Quem usa | Estado | Observação |
|---|---|---|---|---|---|
| 66 | Parâmetro MÊS/ANO (ver um mês anterior) | `parametros` de cada farol | todos | **falta** (o site mostra só o mês do pacote) | Proposta: só o mês anterior fechado, no Painel e no Metas (T-0039). O resto segue no mês corrente (tamanho). |
| 67 | Filtros, recorte, busca, ordenar por coluna | `VistaTabela` | todos | site (filtros, recortes, busca, rolagem por dentro) | Ordenar por coluna: conferir na revisão (T-0033). |
| 68 | Abrir / Editar no Excel | `_BaseRelatorio.abrir_excel` | assistentes | PC | Arquivo local + Excel. No site é o Exportar Excel. |
| 69 | Observações do farol (ⓘ avisos) | `desenhar` | todos | site (avisos) | Na revisão: avisos repetidos (corretor). |

### 1.9 Programas e rotinas que não são tela de relatório

| # | Item | Arquivo | Estado | Observação |
|---|---|---|---|---|
| 70 | Robô (downloads do ERP, TABELA/ESTOQUE/BASE_CLIENTE, Solicitação BAP, pacote web, edições da web) | `bap_automation`, `executar_bap.bat`, `tarefa_bap.xml` | PC | Seção 2. |
| 71 | Pop-up "arquivo em aberto" (Continuar/Cancelar) | `aviso_arquivo` (COM do Excel) | PC | Parte do robô. |
| 72 | Coordenadas dos clientes (OSM, Google, TomTom) | `geocodificar`, `atualizar_coordenadas*.bat` | PC | Chaves só na produção (regra 5). |
| 73 | Sincronização do BAP Ajuda (respostas) | `respostas_bap_ajuda`, `BAP Ajuda 2.0/sincronizar_bap.py` | PC | Usa Git no PC. |
| 74 | Conferência da Solicitação BAP | `conferir_solicitacao.py` (console, chamado pelo robô) | PC | Saída do robô. Pode virar aviso no Farol de Pedidos. |
| 75 | Instaladores e atualização da produção | `instalar_bap.bat`, `ATUALIZAR_DO_GITHUB.bat`, `atualizar_do_github.py --diario` | PC | ADR 0002. |
| 76 | Testes no PC | `RODAR_TESTE_BAP.bat`, `smoke_*.py` | PC/CI | — |
| 77 | Conta de e-mail M365 (msal + Graph) | `conta_email.py` | não migrar | **Regra 9.** Nenhum `.py` importa o arquivo: propor a remoção ao corretor (T-0045). |
| 78 | Painel do Diretor antigo (16 cartões + Leitura/Ações/Compromisso) | `painel_diretor` (aba) + `painel_diretor_config.json` | não migrar | Saiu do PC em 10/11 ("A"). O cálculo continua como base do RRM, que já está no site. |
| 79 | IDs antigos: Pedidos em aberto, Pedidos faturados, Pedidos excluídos, Indicadores Executivos, Resumo Indicadores | `rn.LEGADO` | não migrar | Substituídos em 16/10 (estão dentro do Farol de Pedidos e do Painel Executivo). Fretes (#39) é a exceção e vai. |

### Totais (79 linhas, estado principal de cada uma)

| Estado | Quantas | Itens |
|---|---|---|
| no site | **19** | 1 (parcial: lista em vez do Painel), 4, 5, 6, 7, 9, 10, 11, 15, 22, 23, 30, 31, 34, 35, 41, 42, 67, 69 |
| em PR aberto | **15** | 12, 13, 14, 19, 21, 25, 28, 29, 32, 33, 37, 38, 40, 51 (= 25), 62 |
| falta | **25** | 3, 8, 16, 17, 26, 39, 43, 44, 45, 46, 47, 48, 49, 50, 52, 53, 56, 57, 58, 59, 60, 61, 63, 64, 66 |
| fica no PC | **15** | 18, 20, 36 (o envio), 24, 27, 54, 55, 68, 70, 71, 72, 73, 74, 75, 76 |
| não migrar | **5** | 2, 65, 77, 78, 79 |

Itens com duas partes:
- 18, 20 e 36: o envio fica no PC e o PDF de cada pessoa **falta** no site (T-0038).
- 64: o cadastro falta no site e o "gerar o mês" fica no PC (o robô executa).

---

## 2. O que fica no PC: justificativa ao Alexandre

O Alexandre disse "tudo". Fica no PC **só o que não pode ir**, cada caso com o motivo.

1. **O robô e os downloads do ERP** (`bap_automation`, BAP Tools, `executar_bap.bat`, a tarefa agendada, o pop-up de arquivo aberto, a conferência da Solicitação BAP).
   - O robô entra no site BAP Tools da rede interna (`172.19.20.76:8501`), que o Render não alcança.
   - A senha está no cofre do Windows (regra 5).
   - O resultado são as planilhas da pasta de produção que todos os faróis leem.
   - **No site:** o estado da rodada e a hora dos dados (T-0043) e, se o Alexandre quiser, um "pedir rodada" que o robô atende na volta de 30 min.
2. **Atualizar dados** (`bap_dados.atualizar_tudo`). O cálculo usa arquivos locais e o cache da pasta de produção, e a web não monta relatório (ADR 0001, modelo M2). O pedido pode sair do site (T-0043); a conta é do PC.
3. **Atualizar visitas** (`visitas_maxima`, `prospeccao_forms`).
   - Entra na Máxima com o login do Alexandre: é segredo (regra 5).
   - A prospecção vem do Excel do Forms sincronizado pelo OneDrive. A saída sem Graph foi escolhida para cumprir a regra 9; ler isso do Render exigiria o Graph.
4. **Envio de e-mail** (Parcial via e-mail, Inadimplência por e-mail, Rota da semana).
   - O envio é feito pelo Outlook clássico do computador, por COM (`win32com`).
   - Enviar do Render exigiria o Graph/SMTP da conta Microsoft 365, ou seja, registro de aplicativo (regra 9) ou a senha de uma caixa no servidor (regra 5).
   - **Vai ao site:** o conteúdo. O PDF de cada pessoa sai para baixar (T-0038); o botão de enviar continua no PC.
5. **Exportar campanha** (Excel da premiação). Leva CPF, CNPJ e e-mail de cada pessoa, e documento e contato não vão ao site (regra 6, RN-GER-011). **No site:** o fechamento sem documento, como relatório.
6. **Abrir / Editar no Excel.** Abre a planilha da pasta de produção no Excel da máquina. No site já existe o "Exportar Excel". O dado digitado continua gravado só pelas funções do PC (regra 7).
7. **A gravação das edições** (autorizações, pós-venda, NCC, garantias, expositores, DDR, champions e, adiante, as configs). A tela de edição vai para o site, mas **quem grava é o robô no PC**, com a mesma função da tela, só acrescentando linha (regra 7, RN-GER-012).
8. **Coordenadas dos clientes** (`geocodificar`, `atualizar_coordenadas*.bat`). As chaves do Google e do TomTom ficam só na pasta de produção, e os agentes nem podem ler esses configs (regra 5).
9. **Os cálculos pesados das telas de cadastro**: Recalcular Planner, Gerar o Farol DDR do mês, dividir a meta de saldo, o Gerador de Meta. A web não calcula (ADR 0001). O pedido e o parâmetro saem do site e o robô executa (T-0042). Na prática, o usuário faz no site; o processamento é do PC.
10. **Sincronização do BAP Ajuda.** Usa Git na pasta de produção, como parte da rodada do robô.
11. **Instaladores e rotina diária** (`instalar_bap.bat`, `ATUALIZAR_DO_GITHUB.bat`, `atualizar_do_github.py --diario`). É a infraestrutura do próprio PC (ADR 0002, regra 11).
12. **Testes locais** (`RODAR_TESTE_BAP.bat`, smokes). Ferramenta do time, não do usuário.
13. **Não migrar, nem no PC nem no site:**
    - `conta_email.py`: msal + Graph, a regra 9 proíbe e nenhum `.py` importa o arquivo;
    - o Painel do Diretor antigo: saiu em 10/11;
    - os IDs do LEGADO, menos Fretes: substituídos em 16/10;
    - `bap_acesso.json`: trocado pelo perfil do site;
    - "Relatórios do time": é o próprio menu do site.

---

## 3. Proposta de tarefas (na ordem)

**Tamanho em horas de agente:** P ≤ 3 h · M 4–8 h · G > 8 h. Toda tela passa pela simulação (PNG antes/depois, regra 10). "Dado digitado" = edição gravada pelo robô no PC (regra 7, RN-GER-012).

| Ordem | Tarefa | Donos | Tam. | Depende de | Simulação | Dado digitado / governança |
|---|---|---|---|---|---|---|
| 1 | **T-0033 Revisão geral de todos os faróis do site + correções** (corretor-redundancias, design-de-marca, designer-ux/revisor-ux sobre Pedidos, Visita, Entregas, Inadimplência, Metas e Painel). Inclui o ajuste fino grade × popup por farol (passo 2 da passagem, `tabelas.NO_POPUP`) e o contrato visual `.coord/contratos/tela-bc3.md` (engenheiro-software): cabeçalho, faixa, popup, rolagem, M3 e nomes. Cada leva nova passa por ele sem precisar de outra revisão do zero. | modulo-web (+ modulo-robo/modulo-farois quando o texto vem do PC), engenheiro-software (contrato), testes | M (8 h) | — | sim | não |
| 2 | **T-0034 Página inicial = Painel Executivo no BC3 (PC) / M3 (celular)**, com o menu lateral de todos os faróis por perfil, Usuários e Senha no BC3 (passo 3) e os horários de envio por área no menu. **Decisão ao Alexandre:** os perfis que não veem o Painel (pre_venda, vendas, pos_venda) abrem no primeiro farol do quadrado deles (recomendação) ou num resumo da área. | modulo-web, testes | M (6 h) | T-0033 (contrato BC3) | sim | não |
| 3 | **T-0035 Pacote por farol (ADR 0003)**: o robô manda um arquivo por farol (com gzip); a web guarda só o índice em memória e lê o farol do disco quando a página pede; teto por farol; medição de memória no `/saude`. É uma nova versão do contrato §10 + recado aos consumidores. | engenheiro-software (ADR, contrato), modulo-robo, modulo-web, testes | G (10 h) | — (pode correr junto da T-0033) | não (sem tela) | governança: o `render.yaml` só se o teto mudar ("autorizo") |
| 4 | **T-0024 (em andamento) Faróis do lote 2**: rebase sobre o main. **O `FAROIS_WEB` da branch do robô perdeu o `vc_meta`.** Falta também o BC3, a aba Calendário e o tamanho do pacote medido. Sem a T-0035, cortar "Todos os produtos" (Giro) e "Por cliente" (Roteirização) no `_cortar_pacote_web`. | modulo-web, modulo-robo, testes | M (5 h) | T-0035 ou o corte novo | sim | não |
| 5 | **T-0023 (refazer sobre o main, branches -v2) Garantias, Devoluções e NCC**: diretor só Resumo; edição só do admin. | modulo-web, modulo-robo, modulo-farois (PC só leitura), testes | M (8 h) | T-0024 no main (o mesmo `FAROIS_WEB`/`_TABELA_RECORTE_WEB`) | sim | **sim**: `_GARANTIAS`, `_NCC`, `_EDICOES_POS_VENDA` |
| 6 | **T-0025 (refazer sobre o main, -v2) DDR ×3, Campanhas e Expositores** + TOTAL A PAGAR só admin/gerente/diretor (permissão por coluna, mecanismo novo em `tabelas.py`) + **Parâmetros das campanhas** (`champions_config.json`, só admin, gravado pelo robô). | modulo-web, modulo-robo, modulo-farois (`bap_champions`, `farol_ddr`), modulo-posvenda (`expositores`), testes | G (12 h) | T-0023 no main | sim | **sim**: marcações do DDR, expositores, `champions_config.json` (autorizado em 26/11) |
| 7 | **T-0026 #82 (testes das parciais)**: atualizar com o main e fazer o merge. | testes | P (1 h) | — | não | não |
| 8 | **T-0036 Faróis do Analista**: Saldo, Markup, Preço e Divergências (sem endereço; "Exportar para correção" para baixar, só admin) + **perfis novos "analista" e "trade"** (decisão do Alexandre; o Expositores passa ao trade quando a vaga entrar). | modulo-robo, modulo-web, testes | M (8 h) | T-0035 (Markup tem 2,5 MB) | sim | não |
| 9 | **T-0037 Farol de Fretes com edição** (próxima leva, decisão de 26/11); PC só leitura em "Notas com frete". | modulo-web, modulo-robo, modulo-farois, modulo-posvenda (`pos_venda.gravar_edicoes`), testes | M (6 h) | T-0023 no main (mesmo módulo `pos_venda`) | sim | **sim**: `_EDICOES_POS_VENDA` |
| 10 | **T-0038 Parciais e exportações que faltam:** Parcial BAP; aba "Acomp. RH" e Exportar para o RH (Metas e Painel), só admin/gerente; o PDF de cada pessoa da Parcial por e-mail, da Inadimplência por e-mail e da Rota da semana para **baixar** (o envio continua no PC). | modulo-robo, modulo-farois (função pura do PDF por pessoa, se precisar), modulo-rota (`email_rota`), modulo-web, testes | M (8 h) | T-0035 | sim (PNG/PDF) | não; a decisão sobre quem vê a meta RH é do Alexandre |
| 11 | **T-0039 Painel Executivo completo:** Excel das 17 tabelas "só exportar"; filtro por supervisor (deixado para depois na T-0014); "Somar pedidos em aberto"; o **mês anterior fechado** no Painel e no Metas. | modulo-robo, modulo-web, testes | M (8 h) | T-0034, T-0035 | sim | não |
| 12 | **T-0040 Trocar loja de coleta pela web** (Solicitação BAP, só admin), gravada pelo robô com `solicitacao_bap`. | modulo-web, modulo-robo, testes | M (5 h) | T-0021 (fila de edições, já no main) | sim | edição via robô (mesmo padrão da RN-GER-012); não está na lista da regra 7 |
| 13 | **T-0041 Cadastros do Analista em leitura no site:** Planner (8 abas; o JSON Protheus/Máxima para baixar), Metas e RV (meta RH só admin/gerente), Kits/Oportunidades, Meta de saldo, Transportadoras/SLA, rotina do DDR. **Antes, tirar a regra das telas Tk para funções puras** (regra 2) nos núcleos (`planner_nucleo`, `meta_nucleo`, `oportunidade_nucleo`): as telas hoje fazem conta dentro do Tk. | modulo-rota, modulo-metas, modulo-posvenda (transportadoras), modulo-robo, modulo-web, testes; engenheiro-software (desenho) | G (16 h) | T-0035 | sim | não (só leitura) |
| 14 | **T-0042 Cadastros do Analista com edição pela web** (só admin, gravados pelo robô): Metas executivas, Meta de saldo, Planner (parâmetros, zonas, vendedores, agenda de cidades), Kits, Transportadoras/SLA, rotina do DDR; e o "Recalcular"/"Gerar" como pedido que o robô executa. **Um "autorizo" do Alexandre por arquivo**, como o do champions. | os mesmos da T-0041 | G (16 h) | T-0041 | sim | **sim**: `transportadoras_config.json` (regra 7) e as configs de produção. Os `.json` da raiz do repositório continuam governança; a rotina diária não leva config, então o robô não sobrescreve nada. |
| 15 | **T-0043 Página "Dados e robô" no site**: a hora de cada fonte, a última rodada e os erros (sem dado pessoal); opcional, "pedir rodada"/"pedir Atualizar visitas" (admin), que o robô atende na volta de 30 min. | engenheiro-software (desenho), modulo-robo, modulo-web, testes | M (6 h) | T-0035 | sim | não. É a decisão pendente do R-20261123-102515 ("rodar o robô pelo site") |
| 16 | **T-0044 Fim da migração:** desligar no PC, farol a farol, o que ficou 2 semanas igual ao site (fase 6 do roadmap); remover o `conta_email.py` e os IDs do LEGADO sem uso. | modulo-farois, engenheiro-software, corretor-redundancias, testes | P (3 h) | T-0033 a T-0043 | sim (o PC sem os botões) | não; cada desligamento só com o "ok" do Alexandre |

**Totais:**
- tarefas novas: T-0033 a T-0044, 12 tarefas, cerca de 100 h de agente;
- PRs em andamento: T-0023, T-0024, T-0025 e #82, cerca de 26 h;
- **total: cerca de 126 h.**

**Caminho crítico:** T-0033 → T-0034, com T-0035 em paralelo → T-0024 → T-0023 → T-0025 → as levas novas.

**Ordem dos merges que mexem no `bap_automation.FAROIS_WEB`:** T-0024, depois T-0023-v2, depois T-0025-v2, depois T-0036/T-0037. Uma branch por vez sobre o main, para não repetir o conflito da T-0021 v1.

---

## 4. Riscos

1. **Tamanho do pacote (teto 25 MB na web, 20 MB no robô) e memória do Render (512 MB). É o maior risco.**
   - Nas bases congeladas, só as linhas das tabelas dos 23 faróis do CATALOGO somam **17 MB** de JSON:
     - Roteirização: 3,9 MB;
     - Giro: 3,7 MB;
     - Markup: 2,5 MB;
     - Garantias: 1,4 MB;
     - Clientes: 1,2 MB;
     - Painel: 0,9 MB;
     - Pedidos: 0,9 MB.
   - A isso se somam as parciais em PNG (até 3 MB cada), os recortes por estado e os painéis.
   - **Com a T-0024 e a T-0036, o pacote passa do teto.** O `_cortar_pacote_web` só conhece os faróis antigos, então os novos estouram e dão 413.
   - Na web, o `ultimo.get()` faz `json.loads` do pacote inteiro, e o `por_sha` carrega um pacote antigo na cobrança. O dicionário Python ocupa 5 a 10 vezes o JSON, ou seja, 150 a 300 MB num processo de 512 MB.
   - **Mitigação:** T-0035 (pacote por farol, leitura sob demanda) antes da T-0036. Até lá, a T-0024 corta as duas tabelas grandes e mede o pacote no teste.
2. **Perfis e permissões finas.**
   - O site tem 6 perfis; o PC tem também Analista e Trade, que não existem no site.
   - As decisões de 26/11 pedem permissão **por coluna** (TOTAL A PAGAR), que o `tabelas.VE_TABELAS` não tem, porque decide por aba.
   - A meta RH (Acomp. RH, Exportar RH, painel de meta) não pode vazar para vendas nem para o diretor fora do Exportar RH (regra 8).
   - Hoje toda edição é só do admin (`edicoes.EDITA`): com os cadastros, o Leandro precisaria do perfil admin, ou o Alexandre libera a edição ao perfil "analista".
   - **Mitigação:** uma tabela única de permissão (perfil × farol × aba × coluna) no contrato, com teste por RN.
3. **Dados pessoais (RN-GER-011, regra 6).**
   - Os faróis "livres" da T-0024 passam as colunas que o PC monta e só bloqueiam a lista negra `COLUNAS_FORA` (TELEFONE ... ENDERECO).
   - **Nº, BAIRRO, CEP, coordenadas e o nome do cliente passam.** Nº foi acrescentado no PR; os outros, não.
   - Pontos sensíveis:
     - a aba "Sem coordenada / endereço" da Divergências;
     - o "Clientes" (3.017 linhas) e a Roteirização "Por cliente";
     - o texto livre da Pesquisa de mercado e das garantias;
     - o Exportar campanha (CPF/CNPJ), que fica no PC.
   - **Mitigação:** nos faróis novos, lista **positiva** de colunas por tabela (como os de T-0017), não negativa; teste com fixture sintética para cada farol novo; o revisor-codigo confere a lista no PR.

Riscos menores:
- **Conflito entre os PRs:** os três lotes mexem no mesmo `FAROIS_WEB`, e a branch da T-0024 já está atrás do main.
- **Telas Tk com regra de negócio dentro** (Planner, Meta, Oportunidades): a T-0041 depende de extrair funções puras antes. É o maior bloco de horas.
- **Ver um mês anterior:** cada mês a mais multiplica o pacote.
- **Desligar o PC cedo demais:** a T-0044 só com 2 semanas iguais e o "ok" do Alexandre.

### Suposições
- [SUPOSIÇÃO] O tamanho real em produção é igual ou maior que o das bases congeladas (as bases são de um mês já fechado).
- [SUPOSIÇÃO] O Render segue no plano starter de 512 MB (`render.yaml`).
- [SUPOSIÇÃO] As horas por tarefa valem para um agente em Opus médio, sem contar a espera pela aprovação da simulação.
- [SUPOSIÇÃO] "Tudo" inclui os cadastros do BAP Analista, porque o quadrado do Analista abre o BAP Analista.
