# T-0017, entregas 3 a 5 — todas as abas do PC de Pedidos, Entregas e Visita no site (desenho)

- **Autor:** engenheiro-software · **Data:** 25/11/2026 (Manaus) · **Sem código de produção.**
- **Decisões de origem:** R-20261124-223741-alexandre (Pedidos, "Quero todas"), R-20261124-223958-alexandre ("1 B", Entregas e Visita), regras das tabelas da Inadimplência R-20261124-192008-alexandre ("1 A", "2 A", "6 A"), RN-GER-006.
- **Contrato:** `.coord/contratos/relatorio.md` §10.7 (novo), §3.2 (tipo `hora`), notas no §10.1 e §10.6. **ADR 0001, adendo 5.** Branch `engenheiro-software/T-0017-abas-tres-farois` (sem PR).
- **Base medida:** `main` em `2d182bd`, `relatorios_nucleo.montar(rid, raiz, hoje=20/11/2026, params={"ANO": "2026", "MÊS": "11"})` nas bases congeladas do repositório, num clone descartável. Só nomes de colunas, contagens e tamanhos; nenhum valor de célula foi impresso.

---

## 1. Inventário das abas do PC

Legenda: (o) = coluna oculta no PC (vai no pacote; a web não desenha). "Grava" = o que fica só no PC, sem botão no site.

### 1.1 Farol de Pedidos (`pv_pedidos`) — `relatorios_nucleo.farol_pedidos`

| Aba do PC | Origem | Linhas (NOV/26) | Colunas | Saem | Grava (só PC) | Estado (RN-GER-006) |
|---|---|---|---|---|---|---|
| Resumo gerencial | `painel` (`_painel_pedidos`): 1 insights, 11 barras, 1 hbarras; 8 cartões em faixa | — | — | — | — | cartões por filial da nota (já na branch do robô) |
| **Pedidos** | `tabela("Pedidos")` | **119 no mês** (2.216 nos 12 meses que o PC carrega; o filtro MÊS é oculto e segue o Mês/Ano de cima) | 33 (lista no §10.7.3) | nenhuma; limpar CPF/CNPJ em RAZÃO SOCIAL e FANTASIA | autorização de venda (no "Ver pedido", duplo clique; `autorizacoes.gravar`); botão EDITAR NO EXCEL (`editar` = ACOMPANHAMENTO_POS_VENDA.xlsx) | filial da nota (coluna FILIAL → `uf_do_nome_da_filial`) |
| ↳ junta "Gerar ID de separação CD" | `_solicitacoes_pendentes` | 19 | 10 | nenhuma | — | segue a `liga` (PEDIDOS ↔ PEDIDO) |
| ↳ junta "Gerar reversa de lojas" | `_solicitacoes_pendentes` | 9 | 10 | nenhuma | — | segue a `liga` |
| ↳ junta "Analítico por pedido" | `_analitico_produto` | 34 | 16 | nenhuma; CLIENTE é "código - nome": limpar só o nome | — | segue a `liga` (PEDIDO) |
| **Solicitação BAP** | não é do `montar`: a tela lê `RELATORIOS/SOLICITACAO_BAP.xlsx` (`solicitacao_bap.ler`), 7 sub-abas | 4.370 no total: Lojas 877, CD 654, FRW 404, Manual 6, DETALHADO_PEDIDO 2.147, ProdutosExcluir 272, FiliaisExcluir 10 (só pedido EM ABERTO: 82 + as 2 listas) | as do cabeçalho do arquivo (10 a 23 por aba) | nenhuma; CLIENTE (DETALHADO_PEDIDO) é quase sempre só o código: limpar mesmo assim | **troca de loja de coleta** (duplo clique: ProdutosExcluir + linha nova + CSV, `solicitacao_bap.trocar_coleta`); "Abrir no Excel" | sem estado |

- Pop-up "Ver pedido" (`detalhe_pedido`, duplo clique): não é aba. Itens, saldo e a caixa de autorização (grava). Decisão D4.
- `tons` com cor (o `pv_pedidos` está em `LINHA_PINTADA`): grave 17, alerta 189, atencao 1, ok 1.182, sem cor 827.
- Selos: SLA com faixas (`CHIP_SLA()`), % ATENDIDO com barra (`BARRA_ATENDIDO`).
- Recortes: "Faturar (100% atendidos)", "Mais de 4 dias", "Crédito a analisar", "Acima de 15% sem autorização" (callables → índices prontos no pacote). Analítico: "Com falta", "Sem nenhuma unidade".
- Cartões da aba "Pedidos" no PC: `kpis_de` com o filtro padrão (SITUAÇÃO = EM ABERTO) → os 6 cartões do BI (SLA, Pedidos, R$, Faturar, > 4 dias, Volume), diferentes dos 8 do Resumo. Vão prontos em `kpis_padrao`.

### 1.2 Farol de Entregas (`pl_entregas`) — `relatorios_nucleo.entregas`

| Aba do PC | Origem | Linhas | Colunas | Saem | Grava (só PC) | Estado |
|---|---|---|---|---|---|---|
| Resumo gerencial | `_painel_entregas_exec`: insights, bloco **tabela** "Frete por estado" (7 colunas, 3 linhas, sem cliente), 5 hbarras, 1 barras; 7 cartões | — | — | — | — | cartões pela UF do cliente (branch do robô) |
| **Entregas** | `tabela("Entregas")` | **59 no mês** (1.390 nos 12 meses; o filtro MÊS é visível, padrão = mês) | 22 (a linha tem 23 células: a última é a chave e sai) | nenhuma; CLIENTE é "código - nome" (1.250 de 1.390): limpar só o nome (19 com documento no começo, 4 com CPF no fim); RESPONSÁVEL = motorista (D6) | **edição da entrega** (duplo clique: ETAPA, TRANSPORTADORA, DT. PREVISTA, DT. REAL, RESPONSÁVEL, VLR FRETE REAL → `ACOMPANHAMENTO_POS_VENDA.xlsx`/`_EDICOES_POS_VENDA`); EDITAR NO EXCEL | UF do cliente (coluna UF) |
| ↳ junta "Pendências dos meses anteriores" | mesma função | 0 hoje (varia: entregas de meses antigos não concluídas) | 22, MÊS visível | idem | edição (junta `editavel`) | UF do cliente |

- `tons` todos `""` (fora de `LINHA_PINTADA`); PRAZO (oculta) com selo por texto; SLA com selo pela linha (`chip_tom` → TOM SLA). `cores_celulas` é só Excel/PDF: não vai.
- Sem recortes. Cartões da aba = `cartoes_mes` com o filtro padrão (= os do Resumo). Na branch `modulo-farois/T-0017-hoje-fora-du` o `cartoes_mes` aceita `filtro` de UF para as pendências (`chamar_kpis_de`).

### 1.3 Farol de Visita (`vc_visitas`) — `relatorios_nucleo.farol_visitas`

| Aba do PC | Linhas (NOV/26 até 19/11) | Colunas | Saem | Grava (só PC) |
|---|---|---|---|---|
| Resumo gerencial (16 barras; 10 cartões) | — | — | — | **"Atualizar visitas"** (botão, `visitas_maxima`); botão ABRIR (`abrir`) |
| **Por supervisor** | 3 | 21 | nenhuma | — |
| **Por vendedor** | 9 | 24 | nenhuma | — |
| **Dia a dia** | 171 | 25 | nenhuma | — |
| **Aderência dia a dia** | 9 | 2 + N dias + 1 (16 hoje; muda com o mês) | nenhuma | — |
| **Cliente a cliente** | **1.441** (mês cheio: cerca de 2.200) | 24 | nenhuma; CLIENTE (198 documento no começo, 30 CPF no fim) e NOME FANTASIA (29) limpos; JUSTIFICATIVA (D6) | — |
| **Prospecção** | 44 | 18 → 14 | **CNPJ, CONTATO, TELEFONE, FOTO** (o nome do arquivo da foto traz o CNPJ: 13 de 44); OBSERVAÇÃO, RESULTADO, LINHAS DE INTERESSE (D6) | — |
| **Indicação** | 0 hoje | 17 → 14 | **CONTATO, TELEFONE, CNPJ**; OBSERVAÇÃO (D6) | — |

- Estado: **sem recorte** (RN-GER-006: as tabelas não têm a UF do cliente; a branch do robô já manda sem `recortes` e com o aviso "Sem filtro por estado: os cartões mostram a BAP inteira.").
- Parciais (e-mail e imagem da parcial de visitas) ficam no PC.
- `tons` todos `""`; % META com faixas (`FAIXA_PCT_META`). Tipo `hora` (texto pronto, ex. "08:15") em 9 colunas: acrescentado ao §3.2.
- Recortes: Dia a dia (3), Cliente a cliente (8), Prospecção (3), Indicação (2). `total` e `total_de` em Por supervisor, Por vendedor, Dia a dia e Aderência.
- Filtros de cima SUPERVISOR/VENDEDOR/COMPARATIVO (parâmetros do PC): o robô monta com o padrão (todos; acumulado até a data).

---

## 2. Proposta de contrato (resumo do §10.7)

- `relatorios[rid]["tabelas"]`: lista de `TabelaWeb7`, uma por aba, independentes (cai uma, as outras seguem).
- `TabelaWeb7` = `TabelaWeb` do §10.6.2 + `juntas` (Pedidos 3, Entregas 1, com `liga` e `mostrar`), `subabas` (Solicitação BAP, 7), `kpis_padrao` (cartões da aba no filtro padrão), `recortes_linhas` (índices prontos por rótulo), `uf_linhas` (UF de cada linha pela RN-GER-006), `zebra`, `inteira`. Formas de selo novas: `chip` por faixa, `barra`, `chip_tom` (pelo **nome** da coluna oculta).
- Lista exata de colunas por tabela (§10.7.3); "Aderência dia a dia" por padrão de nome; "Solicitação BAP" pelo cabeçalho do arquivo, com a lista de colunas proibidas.
- Colunas que nunca vão: TELEFONE, CELULAR, WHATSAPP, CNPJ, CPF, E-MAIL, EMAIL, CONTATO, FOTO, ENDEREÇO. Nome de cliente limpo por `relatorios_nucleo.sem_documento` / `cliente_sem_documento` (proposta RN-GER-011).
- O PC confere aba por aba e deixa fora só a que não bate (com aviso); a web recusa o pacote torto inteiro.
- Abas da web por chave na URL: `pedidos`, `solicitacao`; `entregas`; `supervisor`, `vendedor`, `dia`, `aderencia`, `cliente`, `prospeccao`, `indicacao`.

### 2.1 Tamanho do pacote (limite `BAP_WEB_PACOTE_MAX_MB = 25`, `render.yaml`)

| Parte | Linhas | KB (JSON compacto) |
|---|---|---|
| `vc_painel` | — | 41 |
| `pl_inadimplencia` com tabelas e cobrança | 732 | 287 |
| Pedidos, só o mês (12 meses: 745 KB) | 119 | 42 |
| 3 juntas de Pedidos | 62 | 12 |
| Solicitação BAP inteira (só EM ABERTO: ~25 KB) | 4.370 | 830 |
| Entregas, só o mês + pendências (12 meses: 259 KB) | 59 | 16 |
| Visita: Cliente a cliente (mês cheio ~620 KB) | 1.441 | 406 |
| Visita: as outras 6 abas | 236 | 50 |
| recortes_linhas, uf_linhas, kpis_padrao e a forma "farol" dos 3 faróis [SUPOSIÇÃO] | — | ~150 |

**Total no fim do mês com as recomendações: ~2,2 MB (2,5 MB com o `json.dumps` padrão do robô), 10% do teto.** Pior caso (D2 B + D3 A): ~3,5 MB. Disco: 7 pacotes ≈ 25 MB. Trava do robô `WEB_PACOTE_TETO_MB = 20` com corte em 3 passos (§10.7.8).

### 2.2 Perfis por farol e por aba (corte no servidor)

| Perfil | Pedidos (Resumo · Pedidos · Solicitação BAP) | Entregas (Resumo · Entregas) | Visita (Resumo · 7 abas) |
|---|---|---|---|
| admin | tudo | tudo | tudo |
| gerente | tudo (sem telefone já, sem botão já) | tudo | tudo |
| pre_venda | **D1** (rec.: tudo) | não vê o farol | não vê o farol |
| pos_venda | não vê o farol | **D1** (rec.: tudo) | não vê o farol |
| vendas | não vê o farol | não vê o farol | **D1** (rec.: tudo) |
| diretor | só Resumo | só Resumo | só Resumo |

(Quem vê cada farol é o `web/app/render.FAROIS` de hoje: Pedidos admin/diretor/gerente/pre_venda; Entregas admin/diretor/gerente/pos_venda; Visita admin/diretor/gerente/vendas.)

### 2.3 Decisões para o Alexandre (com recomendação)

| | Pergunta | Opções | Recomendação |
|---|---|---|---|
| D1 | O perfil de cada farol vê as tabelas? | A: sim (pre_venda/pos_venda/vendas, como o pós-venda na Inadimplência) · B: só admin e gerente · C: A, mas vendas sem Cliente a cliente, Prospecção e Indicação | **A** |
| D2 | Quantos meses de linhas? | A: só o mês do pacote, como o PC abre (pendências de entrega na junta) · B: os 12 meses, com filtro MÊS no site (+1 MB) | **A** |
| D3 | Solicitação BAP: quais linhas? | A: as 7 abas inteiras (830 KB; corte automático se passar da trava) · B: só pedido EM ABERTO (~25 KB) · C: só no PC | **A** |
| D4 | "Ver pedido" (pop-up do duplo clique) | A: fica no PC nesta entrega · B: detalhe pronto dos pedidos do mês, só leitura (+~300 KB) | **A** |
| D5 | O estado de cima filtra as linhas? | A: sim, pela regra dos cartões (Pedidos: filial da nota; Entregas: UF do cliente); Visita e Solicitação com aviso · B: não, tabelas da BAP inteira | **A** |
| D6 | Texto livre (JUSTIFICATIVA, OBSERVAÇÃO, RESULTADO, LINHAS DE INTERESSE) e o motorista (RESPONSÁVEL) | A: vão, com telefone/e-mail/CPF/CNPJ trocados por "[removido]" · B: ficam só no PC | **A** |

Resposta pronta para copiar (com as recomendações): "D1 A, D2 A, D3 A, D4 A, D5 A, D6 A".

---

## 3. Plano por dono (arquivos e funções)

### 3.1 modulo-farois — `relatorios_nucleo.py` (branch `modulo-farois/T-0017-hoje-fora-du`, mesmo PR)
Funções puras, sem Tk, sem mudar tela do PC:
- `sem_documento(texto) -> str`: CPF/CNPJ no começo (a regex de `cobranca_whatsapp._DOC_INICIAL`), no fim (`\s*\d{11}$`, `\s*\d{14}$`, formatados) e formatado no meio.
- `cliente_sem_documento(texto) -> str`: mantém `^\d{6}(-\d{2})? - ` e limpa o resto com `sem_documento`.
- `texto_sem_contato(texto) -> str` (D6 A): telefone (8 a 13 dígitos com DDD/55, com ou sem máscara), e-mail e CPF/CNPJ → `"[removido]"`.
- `linhas_padrao(t) -> list[int]`: índices das linhas visíveis com os filtros `padrao` da tabela, sem recorte e sem busca (a mesma regra de `bap_relatorios.VistaTabela._filtradas` no estado inicial; §11 pedia essa regra no núcleo). Teste que compare com a tela.
- `recortes_em_linhas(t) -> list[dict]`: `[{"rotulo", "linhas": [i...]}]` para os recortes por função (ignora `{"top"}` e devolve aviso).
- Já na branch: `chamar_kpis_de`, `hoje_manaus`, pendências por UF.

### 3.2 modulo-robo — `bap_automation.py` (branch `modulo-robo/T-0017-tres-farois`, mesmo PR)
- `_COLUNAS_TABELAS_WEB`: `{rid: {titulo: ((nome, tipo, oculta, selo), ...)}}` com as listas do §10.7.3; `_ADERENCIA_WEB` (padrões); `_JUNTAS_WEB` (título do quadro → título da tabela, `liga`, `mostrar`); `_COLUNAS_FORA_WEB`; `_COLUNAS_LIMPAS_WEB` (`sem_documento` × `cliente_sem_documento`) e `_COLUNAS_TEXTO_LIVRE_WEB`.
- `tabela_web7(rid, t, mes_rot) -> dict | None` (pura): corta colunas e células a mais; filtra o mês (D2 A); limpa nomes e texto livre; converte selo (`chip` lista/dict, `barra`, `chip_tom` índice → nome); `kpis_padrao` (`chamar_kpis_de(t["kpis_de"], linhas_padrao)`); `recortes_linhas` (antes do corte, com os índices do PC remapeados depois do filtro do mês); `uf_linhas`; confere com a lista; `None` = aba fora.
- `tabelas_farol_web(rid, r, raiz) -> (list, avisos)`: as abas na ordem do §10.7.1, com juntas e, no Pedidos, `solicitacao_web(raiz)`.
- `solicitacao_web(raiz) -> dict | None`: lê `solicitacao_bap.ler`; tipos pela regra da tela (pedir ao modulo-farois para expor a regra de `AbaSolicitacaoBap.carregar` como função pura `bap_relatorios.tipos_solicitacao(colunas, linhas)`, ou o robô a replica com teste de igualdade [SUPOSIÇÃO: replicar com teste é mais simples, porque `bap_relatorios` importa Tk]).
- `selecionar_farol_web`: põe `tabelas` nos 3 `rid`; o `_AVISO_SO_PC_WEB` passa a tirar só o aviso da pasta de fotos (a Prospecção agora vai).
- `WEB_PACOTE_TETO_MB = 20` e `_cortar_pacote_web(pacote) -> pacote` (pura): os 3 passos do §10.7.8, com aviso.
- `simular_pacote_farol`: aceita os 3 `rid` com tabelas (para a simulação com dados reais **só no PC/scratch**, nunca no repositório).

### 3.3 modulo-web — `web/app/` (branch `modulo-web/T-0017-tres-farois`, mesmo PR)
- `web/app/tabelas.py` (novo): `ABAS = {rid: ((chave, titulo), ...)}`; `COLUNAS` (o §10.7.3); `VE_TABELAS = {rid: perfis}` (D1); `validar(rid, r) -> list[str]` (a lista de recusa do §10.7.6); `tabela_para_tela(t, consulta, uf=None, pagina_tam=100)` **genérica** (filtros com `padrao`/`oculto`/`multi`, ordenação, `recortes_linhas`, estado por `uf_linhas`, paginação, juntas pela `liga` sobre todas as linhas filtradas, sub-abas, `kpis_padrao` só na visão padrão); `fmt_celula` com `dia`, `hora`, `pct`, `pct1`, `num`, `num1`, `valor`; selos `chip` (dict e faixa), `barra`, `chip_tom`.
- `web/app/cobranca.py`: `tabela_para_tela` passa a chamar a genérica (sem mudar o que a Inadimplência mostra).
- `web/app/pacotes.py`: `PROIBIDAS` deixa passar `tabelas` nos 3 `rid` (e `juntas` só dentro de `tabelas`), chamando `tabelas.validar`.
- `web/app/main.py`: `GET /farol/{rid}?aba=&sub=&uf=&pag=...` com 403 por perfil e aba; `no-store`, `noindex`; `registrar_acesso`.
- `web/app/templates/farol.html` e `static/estilo.css`: barra de abas; tabela com rolagem lateral e 1ª coluna fixa no celular; juntas abaixo; sub-abas; aviso de estado.
- `VERSAO` nova no `/saude`. Testes em `web/tests/` (perfil × aba = 403; recusa de pacote torto; tabela igual ao fixture).
- `web/simular_png.mjs` e `web/tests/farol_fixture.py`: os PNGs da §4 com dados fictícios.

### 3.4 testes — `tests/test_T0017_abas_tres_farois.py`, `docs/testes/T-0017.md` (branch `testes/T-0017-testes-tres-farois`, mesmo PR)
- `test_RN_GER_011_sem_documento_comeco_fim_meio`, `..._cliente_mantem_codigo`, `..._texto_livre_sem_contato`.
- Lista de colunas: robô == web == §10.7.3 (lê a lista dos dois módulos).
- Pacote real (bases congeladas): nenhuma coluna proibida; nenhum CPF/CNPJ (regex) em nenhuma célula de `tabelas`; igualdade célula a célula com o PC depois do corte e da limpeza; `kpis_padrao` == `chamar_kpis_de(kpis_de, linhas_padrao)`; `recortes_linhas` == recorte do PC; `uf_linhas` pela RN-GER-006; aba torta fica fora sozinha; tamanho < 20 MB e corte em 3 passos.
- Número do cartão bate com o farol de origem (Pedidos aberto no mês = linhas EM ABERTO do mês).

### 3.5 Outros
- **gerente-projetos:** RN-GER-011 em `docs/produto/03-regras.md`; quadro; levar D1–D6 ao Alexandre (pelo po).
- **modulo-posvenda (recomendação, não bloqueia):** `cobranca_whatsapp.nome_sem_documento` passar a usar `relatorios_nucleo.sem_documento` (CPF no fim do nome também na Inadimplência).

### 3.6 Ordem dos PRs
1. **engenheiro-software** — contrato §10.7 + ADR 0001 adendo 5 (esta branch), depois das respostas D1–D6.
2. **modulo-farois** — funções puras + hoje fora do DU (já na branch).
3. **testes** — pode abrir junto com 2 e 4 (testes das funções puras e do pacote), merge depois deles.
4. **modulo-web** — aceita e desenha as tabelas; simulações aprovadas pelo Alexandre **antes** do PR; merge = deploy (adendo 4); `/saude` com a versão nova.
5. **modulo-robo** — por último no merge; "instale" no PC só com o `/saude` novo (regra 11 do `CLAUDE.md`).

Com robô novo antes da web nova, a web recusa o pacote inteiro e o Painel também para: a ordem 4 → 5 é obrigatória.

---

## 4. Simulações PNG (dados fictícios; PC 1366 px e celular 390 px)

Cada uma com o "antes" (PC, Tkinter, fictício) e o "depois" (site), regra do R-20261120-102406-alexandre.

| # | Farol | Tela | Perfil | PC | Celular |
|---|---|---|---|---|---|
| 1 | Pedidos | aba Pedidos (linhas pintadas, SLA em faixa, % ATENDIDO em barra, cartões do BI) com as 3 juntas abaixo | admin | x | x |
| 2 | Pedidos | aba Pedidos com recorte "Mais de 4 dias" e estado AM (cartões "—", aviso) | gerente | x | |
| 3 | Pedidos | aba Solicitação BAP, sub-aba "Solicitacao CD" e "DETALHADO_PEDIDO" | pre_venda (D1 A) | x | x |
| 4 | Pedidos | só Resumo, sem barra de abas; URL da aba → 403 | diretor | x | x |
| 5 | Entregas | aba Entregas (SLA com selo pela linha, ETAPA inteira) + junta Pendências com linhas | pos_venda (D1 A) | x | x |
| 6 | Entregas | aba Entregas com estado PA (linhas e pendências do PA) | admin | x | |
| 7 | Entregas | só Resumo (com o bloco tabela "Frete por estado") | diretor | | x |
| 8 | Visita | Por supervisor e Por vendedor (% META em faixa, linha TOTAL) | gerente | x | x |
| 9 | Visita | Dia a dia com recorte "Sem visita em dia útil" | vendas (D1 A) | x | x |
| 10 | Visita | Aderência dia a dia (colunas de dias, rolagem lateral) | admin | x | x |
| 11 | Visita | Cliente a cliente (página 1 de N, nomes fictícios, sem documento) | admin | x | x |
| 12 | Visita | Prospecção (sem CNPJ, contato, telefone e foto) e Indicação vazia | admin | x | |
| 13 | Visita | só Resumo com o aviso "Sem filtro por estado" | diretor | | x |
| 14 | Os 3 | robô antigo (sem `tabelas`): só Resumo | admin | x | |

Fixture: `web/tests/farol_fixture.py` (modulo-web), nomes "CLIENTE FICTICIO nn", "VENDEDOR FICTICIO nn", códigos 9xxxxx; nenhum dado das bases.

---

## 5. Riscos

- **R1 Dado de cliente no Render:** mitigado pelo corte por perfil, colunas proibidas, limpeza com teste (RN-GER-011) e recusa do pacote torto. Resta o texto livre (D6).
- **R2 Coluna nova no PC derruba a aba:** por desenho (lista exata). O aviso aparece no site; o PR do contrato vem antes.
- **R3 Ordem de publicação:** robô antes da web derruba o pacote inteiro. Conferir `/saude` antes do "instale".
- **R4 Cartões com filtro:** o site não refaz `kpis_de` (M2). Mostra os cartões da aba só no filtro padrão; com filtro, "—" e aviso. Diferente do PC por desenho.
- **R5 Crescimento da Solicitação BAP:** o arquivo acumula. A trava de 20 MB corta primeiro essa aba.
- **R6 Celular:** tabelas de 24 a 33 colunas. Rolagem lateral com 1ª coluna fixa; as simulações 1, 10 e 11 provam.

## 6. Achados no caminho (fora do escopo, para o gerente)

1. `cobranca_whatsapp.nome_sem_documento` apaga código no começo ("001234 - NOME" → "NOME") e não vê CPF no fim; na Inadimplência hoje não há caso nas bases, mas a regra é frágil (recomendação ao modulo-posvenda, §3.5).
2. `web/app/config.py` usa 2 MB como padrão de `BAP_WEB_PACOTE_MAX_MB` quando a variável falta; o `render.yaml` põe 25. Sem a variável, o pacote de ~2,5 MB seria recusado (413). Sugestão ao modulo-web: padrão 25, ou teste que falhe se o `render.yaml` perder a chave.
3. ADR 0001, adendo 3, ainda diz "Cabe no BAP_WEB_PACOTE_MAX_MB de 2 MB": é histórico; o adendo 5 cita os 25 MB atuais.
4. Branch do robô: `_TABELA_RECORTE_WEB["vc_visitas"] = "Por vendedor"` não é usado (Visita sem recortes); e o `_AVISO_SO_PC_WEB` (Prospecção) precisa mudar quando a aba for ao site.
5. Recado antigo em aberto na caixa do engenheiro-software: R-20261120-120939-alexandre (T-0013, já entregue); cabe ao gerente encerrar.

## 7. Premissas

- [SUPOSIÇÃO] Os perfis que veem cada farol são os de `web/app/render.FAROIS` na branch `modulo-web/T-0017-tres-farois`.
- [SUPOSIÇÃO] As bases congeladas (até 20/11/2026) representam o volume típico; "Cliente a cliente" no mês cheio estimado por regra de três (1.441 linhas em 13 dias úteis → ~2.200 em 20).
- [SUPOSIÇÃO] "Todas as abas" não inclui o pop-up "Ver pedido" (D4) nem as janelas que gravam.
- [SUPOSIÇÃO] Os 150 KB de `recortes_linhas`, `uf_linhas`, `kpis_padrao` e forma "farol" são estimativa, não medida.
