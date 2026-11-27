# T-0033 e T-0034 · Revisão de código, rodada 2 (revisor-codigo)

- **T-0033:** `modulo-web/T-0033-revisao-geral`, delta `94b3440` (aprovado) → **`f188d731684c13592885848a0357f08ed38bce6f`**.
- **T-0034:** `modulo-web/T-0034-pagina-inicial`, delta `9ad9ae9` → **`84106c57a2772a7dbd1b8209ea59f35e083ee727`**.
  - O pedido citava o `cf93690` como base. O parecer anterior (`revisao-codigo.md`) foi dado no `9ad9ae9`, e o `cf93690` já é o commit da correção do R1.
  - Por isso revisei o delta inteiro `9ad9ae9..84106c5`: `cf93690`, `dc81c24`, o merge `39c1d6c` e o `84106c5`.
- **Régua:** `.coord/contratos/relatorio.md` §10.7.2 (`kpis_padrao`), §10.7.6 (`AVISO_CARTOES`), §10.7.7 e D5 (§10.7.9). Para a T-0034, também o meu parecer anterior e `conferencia-final-ux.md` (U10, U11, U12).
- O parecer vale só para estes dois heads. Commit novo pede revisão nova.

## Resultado
- **T-0033 `f188d73`:** não aprovado. **0 🔴, 1 🟡 (A1)**, 1 🟢.
- **T-0034 `84106c5`:** não aprovado. **0 🔴, 1 🟡 (o A1, que entra pelo merge `39c1d6c`)**, 3 🟢. R1, Y1, Y2, G1, G2 e G4 estão resolvidos.

## O que foi rodado
- **Cópias fora do clone:** `git archive` de `94b3440`, `f188d73` e `84106c5` no scratchpad. O clone não mudou de branch e nada foi alterado nele.
- **`python -m compileall -q web/app`:** limpo no `84106c5`.
- **Testes:**
  - `pytest web/tests` no **`84106c5`**: **371 passed**, 1 warning (deprecação do starlette);
  - no `f188d73`: **346 passed**, 1 warning.
- **Donos** (`node scripts/coord.mjs verificar --por-commit origin/main..<branch>`):
  - T-0034: "OK — 15 commit(s), nenhuma violação";
  - T-0033: "OK — 9 commit(s), nenhuma violação".
  - Os commits novos trazem `Agente: modulo-web`, e o diff fica todo em `web/`.
- **Regras:** `bap_dados.VERSAO = 27`. Nenhuma base, config `.json` da raiz ou dado digitado no diff. Nenhum segredo.
- **Merge `39c1d6c`:** o `git diff --stat dc81c24 39c1d6c` é igual ao delta da T-0033 (main.py +1, `_bc3_cab.html`, test_abas.py +21). No conflito do `_bc3_cab.html` ficou a função `kpis_da_faixa` da T-0034 no lugar do `rejectattr` da T-0033, com a mesma semântica. Nada se perdeu.
- **Prova do A1:** um teste avulso, só nas cópias, lê os `<small>/<b>` da faixa com `cobranca_fixture.pacote_cobranca()` e `pacote_tres_farois()`. Resultado abaixo.

## T-0033 · `f188d73`

### Defeito 1 (Visita sem número na faixa): corrigido
- **O que mudou:** `_bc3_cab.html:12`, `ks = ks_todos if e_tab else kpis_da_faixa(ks_todos)`. Na aba de tabela, o cartão com `linhas` agora vai à faixa.
- **Contra o contrato:** bate com o §10.7.2. O `kpis_padrao` é o "cartão inteiro, como os do Resumo", com `linhas` quando o PC põe.
- **Filtro, recorte e estado:** continuam saindo e dando lugar ao `AVISO_CARTOES` (`main.py:409-411`, sem mudança), como pedem o §10.7.6 e o D5.
- **Teste:** `test_faixa_da_aba_leva_o_cartao_com_linhas_no_padrao` põe `linhas` em todos os `kpis_padrao` de Pedidos e confere o número de cartões na faixa, sem o aviso. Cobre o defeito.

### Defeito 2 (Solicitação BAP com `&uf=`): corrigido
- **O que mudou:** `main.py:382` recalcula o `topo` sem estado quando a aba é a Solicitação.
- **Contra o contrato:** bate com o §10.7.7 e o D5. A Solicitação não tem estado e mostra a BAP inteira. O seletor fica desligado (`ufs=[]`, `ufs_off`), e os links das abas não levam o `&uf=`.
- **Teste:** `test_solicitacao_bap_ignora_o_estado_tambem_nos_cartoes_de_cima` compara a faixa com e sem `&uf=AM` e exige que ela não fique vazia. Na minha prova, `94b3440` mostrava os 2 cartões de AM e `f188d73` mostra os da BAP. Cobre o defeito.

### 🟡 A1 · A faixa das abas de tabela que usam os cartões do Resumo passou a levar também os cartões com barras por estado ou `linhas`
- **Onde:** `web/app/templates/_bc3_cab.html:12` (`f188d73`, e a mesma linha no `84106c5`).
- **O que acontece:** o `ks_todos if e_tab` vale para **toda** aba de tabela, não só para as que têm `kpis_padrao`. As abas que caem nos `kpis` do Resumo também mudaram:
  - as abas de tabela da Inadimplência (`main.py:732`);
  - a Solicitação BAP;
  - as abas de Pedidos e Entregas sem `kpis_padrao`.
- **Efeito:** o cartão que o RD-0065 deixa no corpo do Resumo (`render.kpis_da_faixa`, `kpis_do_corpo`) agora aparece na faixa dessas abas.
- **Prova** (fixture fictícia da Inadimplência, com "Em atraso" com `linhas`):

| Tela | `94b3440` | `f188d73` / `84106c5` |
|---|---|---|
| Resumo | 4 números | 4 números (o "Em atraso" fica no corpo) |
| aba Títulos | 4 números | **5** (entra "Em atraso R$ 1,20 mi") |
| aba Cobrar (fila, `e_tab` falso) | 4 números | 4 números |

  - A faixa muda de conteúdo entre abas do mesmo farol. Em Pedidos aconteceu o mesmo: com `linhas` no 1º cartão do Resumo, a Solicitação passou de 5 para 6 números.
- **Por que é 🟡:**
  - é mudança além dos 2 defeitos, que eram só o `kpis_padrao` com `linhas`;
  - não foi declarada no commit;
  - não tem teste;
  - contraria o comentário do próprio template ("a fila e a Solicitação levam os do Resumo"), porque a fila segue filtrada e a Solicitação não.
  - O número em si está certo: é o da BAP inteira, e o Diretor só vê o Resumo.
- **Correção (uma das duas):**
  - **(a)** limitar o "cartão inteiro" ao `kpis_padrao`. Por exemplo, `main.py` passa `render.kpis_da_faixa(topo["kpis"])` no ramo sem `kpis_padrao` (linha 413) e na linha 732. Ou o template decide por uma marca `kpis_da_aba` em vez de `e_tab`. A regra continua num lugar só (`kpis_da_faixa`);
  - **(b)** se o designer-ux/po quiserem esses cartões na faixa das abas, declarar a decisão, alinhar a fila (linha 750) e o comentário, e pôr um teste.
- **Teste novo:** a faixa da aba Títulos da Inadimplência e a da Solicitação BAP têm os mesmos números da faixa do Resumo (com a), ou o conjunto decidido (com b).

### 🟢
- **T33-G1:** `main.py:371` diz "uma vez só", mas na Solicitação o `farol_para_tela` roda duas vezes (`:371` e `:382`). Dá para ler `t = por_chave[aba]` e `solicitacao` antes e chamar uma vez só, com `None` na Solicitação.

## T-0034 · `84106c5`

### Itens do parecer anterior
| Item | Situação | Conferido |
|---|---|---|
| 🔴 R1 | **resolvido** | `render.NA_FAIXA = 3` é usado por `faixa_painel` (`[:NA_FAIXA]`) e por `aba_para_tela` (`na_faixa: i < NA_FAIXA`). O corte é um só, também no recorte por estado (a mesma lista de `cartoes`). `painel.html:28` mostra `rc-valor`/`rc-leg` só quando `not c.na_faixa`. O teste `test_cartoes_alem_dos_3_da_faixa_mantem_numero_e_legenda` usa 10 cartões e confere 7 `rc-valor`, o 4º e o 10º com valor e legenda, e "R$ 165 mil" uma vez só, na faixa. O número do Diretor volta a aparecer para todos os cartões do PC (10/10/6), sem nada recalculado |
| 🟡 Y1 | **resolvido** | `web/app/__init__.py`: `VERSAO = "0.5.0"`. O `main` e a T-0033 seguem em `0.4.0`. O `test_T0035` foi ajustado |
| 🟡 Y2 | **resolvido** | `render.VEEM_PAINEL` é usado em `pagina_inicial`, e `main.VERES = render.VEEM_PAINEL` protege `/painel` e a lateral. O teste é `test_perfis_do_painel_numa_constante_so` |
| 🟢 G1 | resolvido | `render.BC3` saiu, junto com a linha do `test_T0030`. Não sobrou nenhuma referência |
| 🟢 G2 | resolvido | Com `trocar_senha`, `nav = []` (`main.py:176`). O teste `test_troca_obrigatoria_mostra_so_a_casca_sem_menu` confere |
| 🟢 G3 | em aberto (lote futuro) | O DU segue lido do texto `sub`. Ver U11 |
| 🟢 G4 | resolvido | O comportamento está explicado na docstring de `abas_no_celular` |

### Ajustes de UX
- **U10:** voltaram `.rc-valor` e `.rc-leg` (1,5rem/700 e .85rem), iguais ao `conferencia-final-ux.md` U10.
- **U11:** `_DU_FECHADO = r"fechado \((\d+) dias úteis\)"` bate com o texto do PC, `painel_rrm.py:623` (`f"{MESES_L[mes]} fechado ({ndm} dias úteis)"`). Devolve "22 DU · mês fechado", só lido, sem recálculo (regra 4). O mês aberto segue primeiro, e o teste cobre os dois textos.
- **U12:** `grid-auto-rows:minmax(380px,1fr);overflow:auto` no `.rrm`, igual ao proposto. O `grid-template-rows` antigo saiu.

### 🟡 (herdado da T-0033)
- O **A1** entra na T-0034 pelo merge `39c1d6c`, em `_bc3_cab.html:12`.
- Corrigido na T-0033, ele chega à T-0034 com um novo merge. Ou se corrige nas duas, se a T-0034 for ao `main` primeiro.

### 🟢
- **T34-G1:** o `test_dias_uteis_do_mes_fechado_e_o_css_do_numero_do_cartao` confere o CSS por trecho literal (`"font-size:1.5rem;font-weight:700"`, `"minmax(380px,1fr)"`). Qualquer reformatação quebra o teste sem mudar a tela. Basta conferir a presença das regras `.rc-valor{` e `.rc-leg{`. O valor fica com o print do designer-ux.
- **T34-G2:** não há print do head `84106c5`. Os PNGs `conferencia-final-ux/sugerido-*` são a simulação do U10–U12, feita sobre o `dc81c24`. A conferência da tela no head fica com o reteste do designer-ux, que é requisito de pronto.
- **T34-G3:** `main.VERES` virou só um apelido de `render.VEEM_PAINEL`. Mantém o comentário "[SUPOSIÇÃO] os 3 veem o painel", que já não é suposição: é a decisão 2 A. Dá para usar `render.VEEM_PAINEL` direto ou ajustar o comentário.

## [SUPOSIÇÃO]
- Que a Inadimplência e o Pedidos do PC mandam cartões de cima com `linhas` ou `estados`. Na fixture, a Inadimplência manda ("Em atraso"), e o `bap_automation.py:6893-6911` põe `estados` nos cartões do farol. Não rodei o PC.
- Este arquivo não teve commit, nem recado ou linha no diário, a pedido do gerente ("não altere nada").
