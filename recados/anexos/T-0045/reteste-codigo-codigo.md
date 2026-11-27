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
