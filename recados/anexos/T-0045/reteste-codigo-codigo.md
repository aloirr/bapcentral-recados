# T-0045 — reteste de código (revisor-codigo), 27/11/2026

Este reteste confere as correções contra o parecer `revisao-codigo-codigo.md`. Ele vale só para os heads abaixo.

| Branch | Head revisado | Parecer |
|---|---|---|
| `modulo-rota/T-0045-visitas-nucleo` | `f75d2072` (passando pelo `c82ce92`) | **0 🔴 · 1 🟡 novo · 1 🟢** |
| `modulo-web/T-0045-visitas` | `134efc88` (web 0.6.0) | **0 🔴 de código** (o W2, simulação, fica com o gerente) **· 2 🟡 · 2 🟢** |
| `engenheiro-software/T-0045-contrato-v1-1` | `3ffcc06` | confere com a web (o 422 já usa `achados`) |

**Conferências gerais:**
- `verificar --por-commit` OK nas duas branches. O diff da rota contra o main mexe só no `visitas_nucleo.py`.
- `VERSAO = 27`.
- `compileall` limpo.
- Testes:
  - web: 460 passed;
  - `tests/test_T0045_visitas_nucleo.py` (branch `testes/T-0045-testes`, eb6e145): 17 passed no `c82ce92` e no `f75d207`.
- Nenhum segredo e nenhum dado digitado tocado.

---

## A pergunta do gerente: o `ler_espelho` do f75d207 muda o que o PC grava?

**Não muda nos dados reais. Por isso não é 🔴.**

- **Comparação:** rodei o `ler_espelho` do `origin/main` e o do `f75d207` em todos os Espelhos reais das bases: 1.622 arquivos em `RELATORIOS/Visitas/ANALITICO` (a outra cópia, em `.claude/worktrees`, tem os mesmos arquivos). O script só contou linhas e não imprimiu nenhum valor.
- **Resultado:**

  | Arquivos | Linhas no main | Linhas no f75d207 | Arquivos com diferença |
  |---|---|---|---|
  | 1.622 | 13.571 | 13.571 | 0 |

  A saída do `ler_espelho` saiu igual nos dois, arquivo por arquivo, em todos os campos.
- **A fixture dos testes da rota também passa:** 17 passed, inclusive `ler_espelho` igual antes e depois do filtro.

**🟡 R9 — `visitas_nucleo.py:755` (`_linha_de_cliente`): a regra estreita a leitura do PC sem precisar.**
- O critério antigo do `ler_espelho` era "código ou cliente não vazio". O novo é "data válida ou código de 6 a 8 dígitos".
- Num Espelho fictício, as linhas sem data com:
  - só o nome do cliente,
  - código de 5 dígitos,
  - código em número decimal (`1234568.0`)

  somem. Resultado: main = 4 clientes e 4 visitados; f75d207 = 2 e 2. Uma linha dessas com `INICIO` preenchido conta como visita no main (`c["visitado"] = data or inicio`, e o dia cai no dia do arquivo).
- Hoje isso não acontece em nenhuma das 13.571 linhas reais. Mas se a Máxima mudar o formato, o PC passa a perder visita sem aviso.
- **Correção:** a regra única deve ser **a antiga**, `_texto(reg["codigo"]) or _texto(reg["cliente"])`.
  - Ela já resolve o R2, porque o rodapé e o total no meio da lista não têm código nem cliente.
  - E não muda nada no PC.
  - Acrescentar um teste com essas 3 linhas fictícias: o `ler_espelho` tem de contar as 3, e o `ler_espelho(destino)` tem de ser igual ao `ler_espelho(origem)`.

---

## Rota: os achados do parecer

| Achado | Situação | Como conferi |
|---|---|---|
| 🔴 R1 valor de célula em `colunas_fora` | **fechado** | A célula sem rótulo (`"solta"`) é descartada, e o `_rotulo_seguro` recusa 4 ou mais dígitos seguidos e dado pessoal. O probe do parecer agora dá `colunas_fora: ['OBSERVACAO']`, sem o nome nem o CPF. Há teste: `test_RN_VIS_007_colunas_fora_so_leva_nomes_nunca_valor` |
| 🟡 R2 rodapé gera falso achado | **fechado** | O probe "Pagina 1 de 2" na coluna DATA não gera mais achado. Ver o R9 sobre o critério usado |
| 🟡 R3 número em coluna de texto | **fechado** | Pelo `_na_rede(s, ("cnpj", "cpf", "telefone"))`. Há teste: `test_RN_VIS_007_cpf_e_telefone_como_numero_em_coluna_de_texto` |
| 🟡 R4 lista de permitidas copiada | **fechado** | Ela agora sai das tabelas do `ler_espelho`, menos `_FORA_DO_ESPELHO`. Há teste comparando com as tabelas |
| 🟡 R5 dia fechado duplicado | **fechado** | O `dia_fechado(raiz, d)` usa o `dia_fechado_no_indice`, e o `plano` chama o `dia_fechado`. Há teste: `test_RN_VIS_002_dia_fechado_usa_a_regra_unica` |
| 🟡 R6 sem teste | **fechado se o merge for junto** | `testes/T-0045-testes` (eb6e145), 17 testes com o nome da RN. Os PRs da rota e dos testes têm de entrar no mesmo lote |
| 🟢 R7 laço repetido | **fechado** | O `_eventos_espelho` é usado pelo `ler_espelho` e pelo `filtrar_espelho`, e o `_abrir_excel` também é um só |

**🟢 R10** — O empate da nuvem tem teste só na rota (`test_RN_VIS_002_juntar_baixado_fuso_e_empate_e_um_lado_so`). A paridade com a web está no W11, abaixo.

---

## Web 134efc88

| Achado | Situação | Como conferi |
|---|---|---|
| 🔴 W1 empate com o PC | **fechado** | O `juntar_baixado` usa `n >= p`, com a mesma assinatura do núcleo e declarado como espelho no cabeçalho do módulo. Probe: web = núcleo = `origem: "nuvem"`, com `erros_vendedor: 2`. Há teste na web |
| 🔴 W2 tela sem simulação | **com o gerente** | Não reconferi |
| 🟡 W3 leitura do zip fora do contrato e sem teto total | **fechado** | (1) No máximo `ZIP_MEMBROS_MAX = 64` membros. (2) A soma do `file_size` vai até `DESCOMPRESSAO_MAX = 50 MB`, por arquivo e por lote (orçamento compartilhado), com 413 `DESCOMPRESSAO_TETO`. (3) A leitura roda em `run_in_threadpool` (`main.py`, rota do lote). (4) Lê `<v>` e faz `html.unescape`. (5) O contrato v1.1 registra a conferência, o 413 e o 422 `achados`. Probe: o zip de 200 membros que antes inflava 1,6 GB agora dá 413 em 0,0 s, e um CPF numérico é achado |
| 🟡 W4 regex copiado | **aberto** | Ver W11 |
| 🟡 W5 diagnóstico fora da tela | **fechado** | `diagnostico_linhas`: tempos, pico e só as contagens (colunas, células limpas, achados); nenhum nome |
| 🟡 W6 período reescrito | **fechado** | O `periodo_padrao` usa o espelho de `dias_a_baixar` |
| 🟢 W7 `sem_token` copiado | **fechado** | `bearer(request, esperado)` |
| 🟢 W9 acréscimos fora do contrato | **fechado** | No contrato v1.1, §2 e §3.4 |

**🟡 W11 — o teste de paridade na raiz não existe.**
- O contrato v1.1 (§3.1) e o cabeçalho de `web/app/visitas.py` dizem que "um teste de paridade na raiz (`tests/`) confere que as duas dão o mesmo resultado".
- Nenhuma branch tem esse teste: nem `testes/T-0045-testes`, nem a web, nem a rota. Hoje o empate é testado separadamente nos dois lados, e os regex só "com o contrato" (`test_paridade_minima_dos_regex_com_o_contrato`).
- **Dono:** testes. Arquivo `tests/test_T0045_paridade_web_nucleo.py`, com a fixture `web_app` (o padrão de `tests/test_T0017_pacote_tres_farois.py`).
- **O que comparar entre `app.visitas` e `visitas_nucleo`:**
  - `juntar_baixado`, `dia_fechado_no_indice` e `dias_a_baixar` na mesma tabela de casos: maior, empate, só um lado, sem fuso, virada do dia;
  - `RE_PESSOAL` com `_REDE` (padrões);
  - `TIPOS_ACHADO`;
  - `COLUNAS_PROIBIDAS` com `_FORA_DO_ESPELHO`;
  - `RE_NOME_ARQ` contra `_RX_ARQ_ANALITICO`, nos nomes válidos.

**🟡 W12 — `web/app/templates/editar.html:27`: mudança fora do escopo, na tela de edição da T-0021.**
- O campo de data passou de `type="date"` (com `min` e `max`) para texto `dd/mm/aaaa`.
- O servidor continua conferindo: `edicoes.py:236` aceita `dd/mm/aaaa` e recusa a data fora das opções da linha. O `test_T0021_edicao.py:158` foi ajustado.
- Mas é tela de outra tarefa (regra 10: simulação antes) e tira o calendário do celular.
- O gerente já avisou de um 🔴 de UX nesse campo. Ou isso sai deste PR, ou vai com simulação própria.

**🟢 W13** — `main.py:657-658`: `atual_iso`, `min` e `max` continuam sendo montados para o `editar.html`, mas o template não usa mais. Se a W12 ficar, tirar. Se voltar o `type=date`, eles voltam a servir.

**🟢 W8** (continua) — o `RE_NOME_ARQ` é uma cópia mais restrita do `_RX_ARQ_ANALITICO`. Entra na W11.

**Nota (sem achado):** o `achar_no_excel` agora lê `<v>`. Um número decimal com exatamente 11 ou 14 dígitos seguidos pode dar falso `cpf`/`cnpj`. O cron aplica a mesma rede (`_na_rede` em `str(float)`), então os dois lados erram igual e pausam com `DADO_PESSOAL`. É risco de pausa à toa, não de vazamento. Fica para a conferência de 5 dias.

---

## Pronto quando
- **Rota:** o R9 volta ao critério antigo e ganha o teste das 3 linhas fictícias. Revisão nova no head novo.
- **Web:** a W12 é resolvida (sai do PR ou vai com simulação); a W11 é entregue pelo `testes`. Revisão nova no head novo, que o gerente vai avisar.

---

# Reteste final, 27/11/2026: rota 84052835 · web d1e0034 · contrato 8208616

| Branch | Head | Parecer |
|---|---|---|
| `modulo-rota/T-0045-visitas-nucleo` | `84052835` | **1 🔴 · 2 🟡** |
| `modulo-web/T-0045-visitas` | `d1e0034f` (web 0.6.0) | **aprovado no código** (sem 🔴 nem 🟡; o W2, simulação, fica com o gerente) · 2 🟢 |
| `engenheiro-software/T-0045-contrato-v1-1` | `8208616d` | confere com a web; falta ajustar a tabela de formatos (R12) |

**Conferências gerais:**
- `verificar --por-commit` OK nas duas.
- `VERSAO = 27`.
- `compileall` limpo.
- Testes:
  - web: 461 passed;
  - paridade `tests/test_T0045_paridade_visitas_web.py` (testes 9498312): 4 passed com estes heads de rota e web;
  - `tests/test_T0045_visitas_nucleo.py`: **1 failed**, 16 passed.

## Rota 84052835

**O R9 está resolvido no PC.** Com o critério antigo, o `ler_espelho` dá o mesmo resultado do main nos 1.622 Espelhos reais (13.571 = 13.571 linhas, 0 arquivos diferentes). As 3 linhas fictícias voltam a contar (main 4/4, 84052835 4/4).

**🔴 R11 — o teste do lote falha, então o CI fica vermelho.**
- O teste que falha é `test_RN_VIS_007_rodape_no_meio_da_lista_nao_gera_falso_achado`: a linha `[None, "Total: 12", None]`, com o "total" na coluna CODIGO, volta a ser lida como cliente e dá `{'coluna': 'CODIGO', 'tipo': 'formato'}`.
- **Correção (conferida numa cópia, sem alterar a branch):**

  ```python
  def _linha_de_cliente(reg):
      return bool(_texto(reg.get("cliente"))
                  or _RX_CODIGO_CLIENTE.fullmatch(_texto(reg.get("codigo"))))
  ```

  Com ela: 17 passed; o `ler_espelho` fica igual ao do main nos 1.622 reais; e as 3 linhas do R9 (só nome, código de 5 dígitos, código decimal) continuam contando, porque todas têm nome.

**🟡 R12 — falso `formato` nos dados reais: a nuvem pausaria quase todo dia.**
- Rodei o `filtrar_espelho` nos 1.622 Espelhos reais, contando só os achados (sem valor): **146 arquivos (9%) teriam achado**. São dois casos:
  - `ORD PREV`, 439 células no formato `99999` (5 dígitos, mascarado);
  - `ATEND`, 19 células no formato `-99:99:99` (duração negativa).
- Nenhum dos dois é dado pessoal. Mas com cerca de 15 vendedores por dia, quase todo dia teria um Excel com achado, o que dá `DADO_PESSOAL` e pausa (RN-VIS-007). Isso vale desde o `c82ce92`; eu não tinha rodado o filtro nos dados reais nos retestes anteriores.
- **Correção:**
  - contrato §3.6, tabela de formatos (engenheiro-software; formato não é coluna permitida, então é v1 com aviso): `ORD *` até 5 dígitos; `INICIO`, `FIM`, `ATEND` e `PER` com sinal opcional;
  - `_RX_FORMATO` (modulo-rota): `"ord": ^\d{1,5}$` e `"hora": ^-?\d{1,3}:\d{2}(:\d{2})?$`;
  - um teste (testes) que rode o filtro numa fixture com esses 2 formatos e exija `achados == []`.
- **Pronto quando:** o filtro der 0 achados nos 1.622 reais.

**🟡 R13 — o "teste das 3 linhas" do R9 não está em branch nenhuma.** Não está em `testes/T-0045-testes` (9498312), e a rota não tem teste. Dono: testes. O teste deve conferir que linha só com o nome, com código de 5 dígitos e com código decimal entram no `ler_espelho` e no `ler_espelho(destino)`.

## Web d1e0034
- **W12 fechado:** `editar.html` e `test_T0021_edicao.py` estão iguais ao main (voltou o `type=date` com `min`/`max`), e com isso a W13 também sai.
- **W11:** o teste de paridade existe (testes 9498312) e passa. Ele cobre o índice: empate, sem fuso, hoje e intervalo.
- **🟢 W14:** a paridade ainda não prende os regex, o `TIPOS_ACHADO` nem o `COLUNAS_PROIBIDAS` × `_FORA_DO_ESPELHO`. Vale acrescentar ao mesmo arquivo de paridade.
- **🟢 W15:** a docstring de `web/app/visitas.py` diz que o teste de paridade "AINDA VAI SER CRIADO". Ele já existe; atualizar no próximo commit.
- O resto confere: o espelho bate com o núcleo no empate; a bomba de 200 membros dá 413 `DESCOMPRESSAO_TETO` na hora; o diagnóstico fica em `<details>`; o `PODEM_PEDIR`/`SO_ADMIN` é uma constante só.

---

# Releitura final antes dos PRs, 27/11/2026

| Branch | Head | Parecer |
|---|---|---|
| `engenheiro-software/T-0045-contrato-v1-1` | `3a245916` | **aprovado** |
| `modulo-rota/T-0045-visitas-nucleo` | `75312711` | **aprovado** |
| `modulo-web/T-0045-visitas` | `b7e37d09` | **aprovado no código** (o W2, simulação, continua com o gerente) |
| `testes/T-0045-testes` | `fe0ef55f` | **aprovado** |
| `modulo-robo/T-0045-plano` | `35a28dd1` | **🟡 R14**: o código está aprovado, mas a branch carrega o `visitas_nucleo.py` antigo |

**Conferências gerais:**
- `verificar --por-commit` OK nas 5 branches.
- `VERSAO = 27`.
- `compileall` limpo.
- Testes, na árvore combinada (rota 7531271 + web b7e37d0 + `visitas_maxima.py` 35a28dd + `tests/` fe0ef55):
  - `test_T0045_visitas_nucleo.py`, `test_T0045_paridade_visitas_web.py` e `test_T0045_plano.py`: **33 passed**;
  - web: **461 passed**.

## Dados reais (bases congeladas; só contagens, nenhum valor impresso)

| Conferência | Resultado |
|---|---|
| `ler_espelho` main × 7531271 nos 1.622 Espelhos | 13.571 = 13.571 linhas, **0** arquivos diferentes: o PC não perde visita |
| `filtrar_espelho` 7531271 nos 1.622 Espelhos | **0** achados: o R12 fechou (`ORD` até 6 dígitos, hora com sinal) |
| As 3 linhas fictícias do R9 (só nome, código de 5 dígitos, código decimal) | main 4/4, 7531271 4/4 |
| `plano` main × 35a28dd na pasta `RELATORIOS` (80 casos, com e sem `refazer`, 484 dias) | **idêntico** |

## Fechados
- **🔴 R11:** a regra única ficou `cliente não vazio ou código de 6 a 8 dígitos`. Teste: `test_RN_VIS_007_rodape_total_na_coluna_codigo_nao_gera_achado`.
- **🟡 R12:** o contrato §3.6 traz a tabela de formatos igual ao `_RX_FORMATO`. Testes: `test_RN_VIS_007_formato_aceita_ord_de_5_digitos_e_atend_negativo` e `..._sem_achado_no_espelho`.
- **🟡 R13:** `test_RN_VIS_007_linhas_so_nome_codigo_curto_e_decimal_continuam`.
- **🟢 W14:** a paridade agora cobre a rede de dado pessoal, o `TIPOS_ACHADO` e o `_FORA_DO_ESPELHO`/permitidas.
- **🟢 W15:** a docstring foi corrigida, e o `dia_data` sem uso saiu.
- **R5 (o `plano` pela regra única):** o `plano` usa `vn.dias_a_baixar(indice_do_pc(...))`, com `hoje` de Manaus. Testes: `test_RN_VIS_002_plano_igual_nas_bases_congeladas`, `..._sem_hoje_usa_manaus`.

## 🟡 R14 — `modulo-robo/T-0045-plano` partiu da rota antiga
- A branch traz os commits da rota até 8405283. O `visitas_nucleo.py` dela tem o critério de linha e o `_RX_FORMATO` **anteriores** ao 7531271 (`git diff origin/modulo-rota/T-0045-visitas-nucleo origin/modulo-robo/T-0045-plano -- visitas_nucleo.py`).
- Depois do squash da rota no main, o PR do robô vai dar conflito nesse arquivo ou, se o conflito for resolvido errado, **desfazer o R11 e o R12**. Também fere o "um PR por dono", porque leva commits do modulo-rota.
- **Pronto quando:** depois do merge da rota, o modulo-robo faz merge do `origin/main` na branch dele (sem rebase do main), e `git diff origin/main...origin/modulo-robo/T-0045-plano --stat` mostra **só** `visitas_maxima.py`. Revisão nova nesse head.

## Ordem de merge
1. **contrato** (`3a24591`)
2. **rota** (`7531271`)
3. **web** (`b7e37d0`), depois da simulação aprovada pelo po (W2). Pela ADR §9, a web vai ao ar antes da parte do PC.
4. **robô** (`35a28dd`), só depois do R14: atualizado sobre o main, e com diff só no `visitas_maxima.py`.
5. **testes** (`fe0ef55`) por último. A paridade importa `web/app/visitas.py` e o `plano` do robô, então o CI dessa branch tem de ficar verde depois de um merge do main com os 4 anteriores.
