# Revisão de código · T-0034 · delta `84106c5..8393321` (head `83933216d144af2e730c7641b51a229e759eec0a`)

**Parecer: aprovado.** Sem 🔴 e sem 🟡. Ficam 3 🟢.

Este parecer vale só para o head `8393321`. Um commit novo pede uma revisão nova.

## O que conferi

| Ponto | Resultado | Como conferi |
|---|---|---|
| **woff2 oficiais** | **conforme** | Os SHA-256 de `Inter-400/600/700.woff2` são iguais, byte a byte, aos de `package/files/inter-latin-{400,600,700}-normal.woff2` do `@fontsource/inter@5.3.0` baixado do npm. Os mesmos arquivos estão no 5.2.8 e no 5.2.7 (só o 400 e o 600). Todos começam com `wOF2` |
| **Licença OFL** | **conforme** | `fontes/OFL.txt` é idêntico ao `package/LICENSE` do 5.3.0 (SHA-256 `3b0a5fca…`): copyright do Inter Project e a SIL OFL 1.1 inteira. O teste confere que o arquivo é servido |
| **CSP e fonte** | **conforme** | O CSP não tem `font-src`, então vale o `default-src 'self'`. A fonte vem de `/static/fontes/`, a mesma origem, e é aceita. `/static` está em `ISENTAS_FUSO`, então o 503 do fuso nunca cai na fonte |
| **MC-0020 a 0024** | **conforme**, igual ao pedido em `marca.md` | São 3 `@font-face` (400, 600 e 700) com `font-display:swap` antes do `:root`, e a pilha `--fonte` segue igual. O login ficou com `96×122` e `padding:13px`. O rótulo branco das barras é `.rc-barras .barra .rot-b{background:var(--cartao)…}`. Não sobrou nenhum `font-weight:800` (o teste confere no CSS já mesclado). O selo cinza ficou com `.selo-cinza{background:var(--borda)}`, igual ao `PALETA_TOM["cinza"]` de `tabelas.py` |
| **Print** | **conforme** | `sim/6-login__pc1366.png` mostra o logo com o respiro novo. `sim/1-painel-diretor__pc1366.png` mostra o % em rótulo branco (9 %, 110 %, 95 %) |
| **Merge `8393321`, resolução** | **conforme** | `git show --remerge-diff` mostra que os 4 conflitos foram resolvidos sem código novo, só com a escolha dos lados (−22/+3 linhas). **`main.py`:** ficaram os dois lados (`manaus_curto`, `kpis_da_faixa`, `kpis_do_corpo` e `abas_no_celular` da T-0034, e `livres` da T-0024). **`render.py`:** ficou o `GRUPOS_MENU` do lote 2, e o `BC3` continua fora (G1 da revisão 2), sem nenhuma referência que sobrou. **`_resumo.html`:** ficou o `kpis_do_corpo(...)` da T-0034 e voltou o macro `barras_cols` com o bloco `periodos` da T-0033, sem duplicar |
| **A1 na T-0034** | **conforme** | `_bc3_cab.html:12` ficou `ks_todos if (e_tab and kpis_da_aba is defined and kpis_da_aba) else kpis_da_faixa(ks_todos)`. O `render.kpis_da_faixa` é exatamente o `rejectattr('estados')\|rejectattr('linhas')` do lado da T-0033, então a regra continua numa função só (RD-0065), sem reescrever. `main.py:416-427` liga o `kpis_da_aba` só com `kpis_padrao` e sem pedido. Quem cobre é o `test_abas.py::test_A1_aba_sem_kpis_padrao_leva_na_faixa_os_mesmos_numeros_do_resumo` |
| **Faróis do lote 2** | **conforme** | `web/tests/test_T0024_farois_lote2.py` dá 403 no `pl_frw` para o perfil vendas e no `pl_giro?aba=todos-os-produtos` para o diretor. O `sem_uf` respeita `livres`. O menu tem os 5 faróis no grupo certo |
| **Escopo** | **conforme** | `origin/main...8393321` só mexe em `web/`. Os arquivos de fora (`bap_automation.py`, `tests/`, `.coord/`) chegam pelo merge e já estão no `main` (`0bb251b` é ancestral). Não muda nada além do pedido |
| **Dado digitado e configs** | intocados | Nenhum `_EDICOES_POS_VENDA`, `_NCC`, `_GARANTIAS` ou `_AUTORIZACOES`, e nenhum `.json` da raiz no delta |
| **Segredos** | nenhum | O grep no diff só achou "senha" de rota e de rótulo, e `TOKENS` de cor |
| **`bap_dados.VERSAO`** | 27 | |
| **Número do Diretor** | sem mudança | O delta só mexe em CSS e na resolução do merge. `NA_FAIXA` e `faixa_painel` não mudaram |
| **`verificar --por-commit origin/main..8393321`** | OK | 16 commits conferidos, nenhuma violação. Os merges não entram |

## Testes (numa cópia do head feita com `git archive`, fora do clone)
- `python -m compileall -q web/app`: OK.
- `pytest web/tests`: **395 passed**.
- `pytest tests/test_T0024_lote2_robo_web.py tests/test_T0024_pacote_real_lote2.py tests/test_T0024_robo_lote2.py tests/test_T0017_tres_farois.py`: **44 passed**.

## 🟢 Sugestões
- **G1, `web/app/main.py:123-124`:** o `immutable` de um ano vai para tudo o que fica sob `/static/fontes/`, inclusive um 404. Também não há versão no nome do arquivo. A sugestão tem duas partes:
  - aplicar o cabeçalho só quando `r.status_code == 200`;
  - escrever no comentário que trocar a fonte pede um nome novo (ex.: `Inter-400.v2.woff2`).
- **G2, `web/tests/test_T0034_pagina_inicial.py:186`:** a fonte só carrega porque o CSP cai no `default-src 'self'`. Se alguém apertar o `default-src` no futuro, a Inter some sem que nenhum teste quebre. A sugestão: conferir no teste que o CSP aceita `'self'` para fonte, ou pôr `font-src 'self'` explícito no CSP.
- **G3, print:** as PNGs de `sim/` (05:40) são do `c3c3064`, de antes do merge. Não há print de uma aba sem `kpis_padrao` depois do A1. A cobertura vem do teste A1, e a conferência da tela no head fica com o reteste do designer-ux.
- Os itens da revisão 2 seguem como estavam:
  - **T34-G1:** o CSS ainda é conferido por trecho literal;
  - **T34-G3:** `main.py:27` ainda tem `[SUPOSIÇÃO] os 3 veem o painel`, e isso já é a decisão 2 A.

## [SUPOSIÇÃO]
- O `@fontsource/inter@5.3.0` baixado do registro npm é o pacote oficial.
- Este arquivo não teve commit, nem recado ou linha no diário, porque o gerente pediu: "não altere nada".
