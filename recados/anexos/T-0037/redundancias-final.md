# T-0037 · Farol de Fretes · parecer final do corretor-redundancias

- **Data:** 27/11/2026 (Manaus). **Revisor:** corretor-redundancias.
- **Heads revistos** (vale só para eles; commit novo pede reteste):

| Branch | Head |
|---|---|
| `testes/T-0037-fretes` | 97eb8c7 |
| `engenheiro-software/T-0037-desenho` | cbe9747 |
| `modulo-web/T-0037-fretes` | 2274cb2 (web 0.9.0) |
| `modulo-farois/T-0037-fretes` | 48c6577 |
| `modulo-robo/T-0037-fretes` | 91e6f8a (já contém o 48c6577 dos faróis) |

- **Como:** clone de rascunho fora do repositório com o `main` + os 5 heads (merge limpo). Telas tiradas da fixture (`simular_farol.paginas` + Playwright, 1366 e 390 px): Resumo, Notas, Cidade e Transportadora. Testes da T-0037 rodados da raiz: `tests/test_T0037_*` 46 passaram e `web/tests/test_T0037_fretes.py` 20 passaram.
- **Numeração:** RD-0192 a RD-0199 e, depois, RD-0202 a RD-0205. Os RD-0182 a 0191 são da T-0050, e os RD-0200 e 0201 são da T-0045.
- **Veredito: não liberado.** Há 13 achados em aberto: 7 médios e 6 baixos. Só o RD-0205 (título de teste) não segura o lote.

## O que já está resolvido
- **O `_rotulo_sem_fretes_web` saiu do robô.** Nenhuma ocorrência no código combinado. O Resumo usa o rótulo pronto do PC (`relatorios_nucleo.rotulo_agrupa_fretes`).
- **Os rótulos "Sem …" estão iguais no Resumo e nas abas**, sem "(sem)" nem barra solta. O cartão "Sem transportadora" (1) é igual à linha da tabela (1).
- **O `EDICOES_WEB` do robô** passou a usar uma entrada só (`_ED_ENTREGAS_WEB`) para os 3 lugares da aba ENTREGAS.
- **O `_grade.html` não escreve mais a mensagem da nota sem chave por extenso.** Ela vem de `edicoes.msg_sem_chave`.
- **As frases do Resumo** não repetem mais os números da tabela (A4 da UX).

## Achados

### RD-0192 · As frases do Resumo vão duas vezes no pacote · rotina/código · baixa
- **Onde:** `bap_automation.py:7012-7015` (`blocos_resumo_fretes_web` acrescenta o bloco `insights`) e `:7049-7050` (`selecionar_farol_web` copia as mesmas frases em `insights_painel`).
- **O que se repete:** as 2 frases vão no bloco `insights` "Resumo gerencial" e também em `insights_painel` (2 cópias).
  - A web só lê o bloco quando o `insights_painel` vem vazio (`web/app/render.py:725`, `_insights(insights_painel) or ins_blocos`).
  - No Fretes o `insights_painel` sempre vem cheio, então o bloco nunca é lido.
  - O título "Resumo gerencial" da tela vem do template (`_resumo.html:20`), não do bloco.
- **Impacto:** manutenção. As duas cópias precisam ficar iguais, e um teste confere só isso (`test_T0037_fretes_resumo.py:111`).
- **Proposta (o bloco sai, o `insights_painel` fica):**
  - robô: antes, `if frases: blocos.append({"tipo": "insights", "titulo": "Resumo gerencial", ...})`. Depois, as 3 linhas saem e a função devolve `(blocos, frases)` com as barras e as 3 tabelas.
  - contrato §10.12.2: o item 3 vira "**frases** (`insights_painel`), até 2 frases `info` …", e a linha "As mesmas frases vão em `insights_painel` …" sai. No `docs/desenho/T-0037.md:110`, a parte "1 `insights` … repetidas em `insights_painel`" vira "2 frases em `insights_painel`".
  - testes: `test_T0037_fretes_resumo.py:59` passa a `tipos.count("insights") == 0`, e as linhas 110 e 112 (`ins = …` e `fr == …ins["linhas"]`) saem.
  - fixture: segue sozinha se o RD-0194 entrar. Senão, as 2 linhas do bloco saem do `blocos_resumo_web`.
- **Dono:** modulo-robo, com engenheiro-software (contrato e desenho), testes e modulo-web.

### RD-0193 · Os rótulos "Sem …" estão escritos à mão no robô · código (regra repetida PC × robô) · média
- **Onde:** os textos nascem em `relatorios_nucleo.py:8013-8017` (`rotulo_agrupa_fretes`). O robô compara com os mesmos textos copiados em `bap_automation.py:6997` (`!= "Sem UF"`) e em `:7005-7006` (`not in ("Sem transportadora", "Sem acompanhamento")`).
- **O que se repete:** os 3 textos estão no PC e no robô (2 cópias). A fixture da web tem uma 3ª cópia (RD-0194).
- **Impacto:** decisão. Se o PC trocar o texto (por exemplo, "Sem transp."), o robô deixa de pular a linha, e a frase do Diretor passa a dizer "Sem transportadora leva 40% do valor.". Nenhum teste pegaria isso, porque os testes usam os mesmos textos copiados.
- **Proposta:**
  - **faróis (`relatorios_nucleo.py`):** criar as constantes `SEM_UF = "Sem UF"`, `SEM_CIDADE = "Sem cidade"`, `SEM_TRANSP = "Sem transportadora"`, `SEM_ACOMP = "Sem acompanhamento"` e usá-las no `rotulo_agrupa_fretes`.
  - **robô:** antes, `x[0] != "Sem UF"` e `x[0] not in ("Sem transportadora", "Sem acompanhamento")`. Depois, `x[0] != _rn.SEM_UF` e `x[0] not in (_rn.SEM_TRANSP, _rn.SEM_ACOMP)`.
- **Dono:** modulo-farois (constantes) e modulo-robo (uso).

### RD-0194 · A fixture da web copia a função do robô e a do PC · teste/código · média
- **Onde:** `web/tests/fretes_fixture.py:110-122` (`rotulo_agrupa`, cópia do `relatorios_nucleo.rotulo_agrupa_fretes`), `:145` (`TABELAS_RESUMO`, cópia do `_TABELAS_RESUMO_FRETES_WEB`) e `:148-197` (`blocos_resumo_web`, cópia linha a linha do `bap_automation.blocos_resumo_fretes_web`, com 50 linhas).
- **O que se repete:**
  - a montagem do Resumo, com a regra das frases e a do TOTAL (2 cópias);
  - o rótulo "Sem …" (2 cópias);
  - nenhum teste confere a cópia contra o original;
  - a docstring do `blocos_resumo` (`:201`) diz que a entrada "passa pela mesma função pura do robô", o que não é verdade: passa pela cópia.
- **É redundância útil?** Não. A fixture já importa um módulo do PC (`relatorios_nucleo`). Medi que `import bap_automation` só carrega a biblioteca padrão no topo e funciona no passo de testes da web do CI, que roda no mesmo job do `pip install` da raiz. A cópia pode ser trocada pela chamada da função. Conferi na entrada da fixture: blocos e frases iguais aos do robô 91e6f8a, e rótulos iguais aos do PC nas 9 notas.
- **Impacto:** manutenção. Cada mudança no robô (A2, A3, A4 e barra solta) já pediu uma rodada à mão para refazer o espelho.
- **Proposta:**
  - `blocos_resumo()`:
    - antes: `blocos, frases = blocos_resumo_web({...})`;
    - depois: `import bap_automation as ba` e `blocos, frases = ba.blocos_resumo_fretes_web({...})`;
    - a `blocos_resumo_web` sai inteira, e a docstring fica como está (passa a ser verdade).
  - `_resumo()`:
    - antes: `rotulo_agrupa(col, ln, nb)`;
    - depois: `rn.rotulo_agrupa_fretes({"UF": 7, "CIDADE": 6, "TRANSPORTADORA": 11}[col], list(ln) + ["" if ln[nb.index("ETAPA")] == SEM_AC else "CHAVE"])`;
    - a `rotulo_agrupa` sai. A linha da fixture tem os mesmos índices do PC, menos a 17ª célula, a CHAVE.
  - `TABELAS_RESUMO`: passa a ser `ba._TABELAS_RESUMO_FRETES_WEB`.
- **Dono:** modulo-web.

### RD-0195 · A troca da cor do PC pela da marca está em dois lugares, e eles já divergem · código · média
- **Onde:** `web/app/marca.py:20-23` (`COR_PC`, novo, usado em `render._cor`) e `web/app/static/estilo.css:319-321` (seletores `[style*="1F4FD1"]`, `"C98A00"`, `"B7791F"` e `"4F6D7A"` com `!important`, que já estão no `main`).
- **O que se repete:** a mesma troca da cor do PC por um token da marca (2 lugares). Depois do `_cor`, o HTML não leva mais o 1F4FD1, o C98A00 nem o 4F6D7A, então essas regras do CSS ficam mortas. Para o B7791F, a regra só vale nas barras e na legenda, não nas `hbarras`.
- **Evidência:**
  - Renderizei um farol fictício com as 7 cores do PC em barras, legenda e `hbarras` e comparei a cor calculada, sem as 3 linhas do CSS e com `"#b7791f": TOKENS["--grafico-2"]` no `COR_PC`.
  - Deram iguais 27 de 28 barras.
  - A única diferença é a `hbarras` em #B7791F: hoje sai #B7791F, porque o CSS não cobre o `.hb-trilho` para esse hex, e passaria a sair #D8B56E, igual às barras e à legenda.
- **Impacto:** manutenção e coerência visual (o mesmo âmbar sai em duas cores).
- **Proposta:**
  - `estilo.css`: as 3 linhas `.gb-b i[style*="1F4FD1" i]…`, `.gb-b i[style*="C98A00" i]…` e `.gb-b i[style*="4F6D7A" i]…` saem.
  - `marca.py`: antes, `COR_PC = {…, "#4f6d7a": TOKENS["--grafico-3"]}`. Depois, `COR_PC = {…, "#4f6d7a": TOKENS["--grafico-3"], "#b7791f": TOKENS["--grafico-2"]}`.
  - Um só lugar: o `COR_PC`.
  - A cor da `hbarras` âmbar passa a ser igual à das barras; o design-de-marca confirma.
- **Dono:** modulo-web (cc design-de-marca).

### RD-0196 · `render._blocos` repete a conta de `vert`/`rotv` do `_bloco_barras` · código · média
- **Onde:** `web/app/render.py:466-472` (`_bloco_barras`) e `:629-637` (o laço "A1" do `_blocos` refaz as duas fórmulas quando tira o `larga`).
- **O que se repete:** as fórmulas `vert = 8 < nbarras and not denso` e `rotv = (n > 5 and maxrot > 5) or (n > 8 and maxrot > (3 if denso else 4))` (2 cópias). A 2ª conta as barras de outro jeito (`len(cols[0]["barras"])` em vez de `len(series)`).
- **Impacto:** manutenção. Quem mexer numa das cópias muda o gráfico dos outros faróis só em metade dos casos.
- **Proposta:**
  ```python
  def _disposicao(cols, n_series, denso, larga) -> tuple[bool, bool]:
      n, maxrot = len(cols), max([len(c["rot"]) for c in cols] or [0])
      vert = 8 < n * max(n_series, 1) and not denso and not larga
      rotv = not larga and ((n > 5 and maxrot > 5) or (n > 8 and maxrot > (3 if denso else 4)))
      return vert, rotv
  ```
  - `_bloco_barras`: `vert, rotv = _disposicao(cols, len(series), denso, larga)`.
  - `_blocos`: `x["larga"] = False; x["vert"], x["rotv"] = _disposicao(x["cols"], len(x["cols"][0]["barras"]) if x["cols"] else 1, x["denso"], False)`.
- **Dono:** modulo-web.

### RD-0197 · CSS do gráfico largo no celular: 4 declarações mortas ou repetidas · código · baixa
- **Onde:** `web/app/static/estilo.css`, no bloco "T-0037 (UX A1)", `@media(max-width:700px)` (linhas 720 e seguintes).
- **O que se repete:**
  - `.graf-larga{padding-left:6px;padding-right:6px}` é sempre vencida por `.bc3 .graficos .graf.graf-larga{…12px}`;
  - o `gap:1px` de `.gb.gb-larga` é vencido por `.bc3 .graf .gb.gb-larga{gap:6px}`, que tem mais peso (no celular medi 6 px);
  - `.gb-larga .gb-rot{font-weight:600;letter-spacing:-.02em}` repete o que já está em `.bc3 .graf .gb.gb-larga .gb-rot{…}`;
  - o `.gb-larga .gb-rot` de `.gb-larga .gb-rot,.gb-larga .gb-txt{font-size:11px}` também repete.
- **Evidência:** o PNG do Resumo sai idêntico, byte a byte, a 1366 e a 390 px, com e sem as 4 declarações.
- **Proposta (o bloco depois da mudança):**
  ```css
  @media(max-width:700px){
    .gb.gb-larga{grid-auto-columns:minmax(0,1fr)}
    .gb-larga .r-l{display:none}.gb-larga .r-c{display:inline}
    .gb-larga .gb-txt{font-size:11px}
    .bc3 .graf .gb.gb-larga .gb-rot{font-size:11px;overflow:visible;font-weight:600;letter-spacing:-.02em}
    .bc3 .graf .gb.gb-larga{overflow:visible}
    .bc3 .graficos .graf.graf-larga{padding-left:12px;padding-right:12px}
    .gb-larga .gb-col:nth-last-child(even) .gb-rot{visibility:hidden}      /* um rótulo sim, um não, do último mês para trás */
  }
  ```
- **Dono:** modulo-web.

### RD-0198 · A coluna MÊS repete "NOV/26" em todas as linhas das abas UF, Cidade e Transportadora · texto/layout · média
- **Onde:** na web, as abas UF, Cidade e Transportadora (print da Cidade: 5 linhas, todas "NOV/26").
- **O que se repete:** o pacote só leva o mês (P1 A), e o filtro MÊS já vai oculto (`bap_automation._tabela_web7`, `_so_mes_web`). A coluna mostra o mesmo valor em todas as linhas (5 vezes na Cidade e 5 na Transportadora). A aba Notas do mesmo farol e o "Entregas" já levam o MÊS oculto na web.
- **Impacto:** leitura (uma coluna que não diferencia nada) e coerência entre as abas do mesmo farol.
- **Proposta (o PC não muda: lá o filtro "(todos)" mostra os 12 meses e a coluna serve):**
  - contrato §10.7.3 (`pl_fretes`), nas 3 abas: antes, `` `MÊS` texto · `UF` texto · …``. Depois, `` `MÊS` texto (o) · `UF` texto · …``. O mesmo nas linhas do §10.12.3 (ou só a remissão, ver o RD-0204).
  - robô `_COLUNAS_TABELAS_WEB["pl_fretes"]`, nas 3 abas: antes, `(_c("MÊS", "texto"), _c("UF", "texto"))`. Depois, `(_c("MÊS", "texto", True), _c("UF", "texto"))`. É o mesmo padrão do "Entregas" (`:7763`).
  - web `tabelas.COLUNAS_RID[("pl_fretes", …)]`, nas 3 abas: antes, `[_c("MÊS"), _c("UF")]`. Depois, `[_c("MÊS", "texto", True), _c("UF")]`.
- **Dono:** engenheiro-software (contrato), depois modulo-robo e modulo-web. Os testes de colunas (robô × contrato e robô × web) mostram se os três ficaram iguais.

### RD-0199 · O teste do pacote monta as abas de resumo com a regra antiga do rótulo · teste (regra repetida) · média
- **Onde:** `tests/test_T0037_fretes_robo.py:154`, `k = (x[0], x[i] or "(sem)")`, no `_farol`.
- **O que se repete:** uma cópia, já vencida, da regra do rótulo (o "(sem)" e a cidade sem " / UF"). O PC usa a `rn.rotulo_agrupa_fretes`. A cópia esconde a divisão entre "Sem transportadora" e "Sem acompanhamento": o teste espera 3 linhas na "Por transportadora" de NOV, e com a regra do PC são 4.
- **Proposta:**
  - linha 154: antes, `k = (x[0], x[i] or "(sem)")`. Depois, `k = (x[0], rn.rotulo_agrupa_fretes(i, x))`.
  - linha 190: antes, `zip(tabs[1:], (3, 4, 3))`. Depois, `zip(tabs[1:], (3, 4, 4))`. As 4 linhas da "Por transportadora" são TRANSPORTADORA FICTICIA 1, TRANSPORTADORA FICTICIA 2, Sem transportadora e Sem acompanhamento.
- **Dono:** testes.

### RD-0202 · O teste de rótulos reescreve o critério do cartão "Sem transportadora" · teste (regra repetida) · baixa
- **Onde:** `tests/test_T0037_fretes_rotulos.py:52-63` (`test_RN_POS_009_sem_transportadora_bate_com_o_cartao`).
- **O que se repete:** `cartao = sum(1 for ln in ls if ln[COL_CHAVE] and not ln[COL_TRANSP])` copia a regra de `rn.kpis_fretes` (`relatorios_nucleo.py:8048`). O teste compara o rótulo com essa cópia, e não com o cartão de verdade.
- **Proposta:**
  - `_l`: depois de `ln = [""] * 17`, acrescentar `ln[8] = ln[9] = 0.0`.
  - Antes: `cartao = sum(1 for ln in ls if ln[COL_CHAVE] and not ln[COL_TRANSP])`.
  - Depois: `cartao = int(next(k["valor"] for k in rn.kpis_fretes(ls, {}) if k["rotulo"] == "Sem transportadora"))`.
- **Dono:** testes.

### RD-0203 · Dois testes passam pelo mesmo ramo · teste · baixa
- **Onde:** `tests/test_T0037_fretes_resumo.py:176` (`test_T0037_uma_uf_sem_frase_de_uf`, uma linha "PA") e `:234` (`test_T0037_so_sem_uf_nao_tem_frase_de_uf`, uma linha "Sem UF").
- **O que se repete:** os dois só cobrem o `len(ufs) > 1` com uma linha (2 testes para o mesmo caso). Com "Sem UF" sozinha também cai no `len == 1`, e não no `ufs_ok` vazio. Esse caso não acontece, porque o PC agrupa no máximo uma linha "Sem UF" por mês.
- **Proposta:**
  ```python
  @pytest.mark.parametrize("rotulo", ["PA", "Sem UF"])
  def test_T0037_uma_linha_no_por_uf_sem_frase_de_uf(rotulo):
      _, fr = ba.blocos_resumo_fretes_web({"tabelas": [_tab_uf([["NOV/26", rotulo, 5, 100.0, 1.0]])]})
      assert fr == []
  ```
  Esse teste substitui os dois.
- **Dono:** testes.

### RD-0204 · O contrato escreve as mesmas listas duas vezes · doc · baixa
- **Onde:** `.coord/contratos/relatorio.md`. A §10.7.3 (`pl_fretes`, linhas 742-747) e a tabela da §10.12.3 (linhas 1602-1605) repetem as 16 colunas de "Notas com frete", os filtros e as 3 × 5 colunas das abas de resumo (2 cópias). A §10.12.3, item "Tela", repete à mão a `web/app/tabelas.GRADE[("pl_fretes", "Notas com frete")]` (9 colunas, `cel` e `blocos`), e nenhum teste compara as duas.
- **Impacto:** manutenção. A lista que o teste lê é a da §10.7.3 (`test_T0017_colunas_robo_igual_contrato_1073`). A da §10.12.3 pode mudar sem que ninguém perceba, como no Y2 do revisor-codigo.
- **Proposta:**
  - tabela da §10.12.3: a coluna "Colunas depois do corte (nome · tipo)" vira "§10.7.3 (`pl_fretes`)" nas 4 linhas. As colunas Filtros e Edição continuam.
  - item "Tela": antes, a lista das 9 colunas, `blocos` e `cel`. Depois, "A grade é a `web/app/tabelas.GRADE[("pl_fretes", "Notas com frete")]` (fonte única): até 10 colunas, chave NF, as 4 editáveis (ETAPA, TRANSPORTADORA, ENTREGAR ATÉ, ENTREGUE) na grade e o RESPONSÁVEL no popup."
- **Dono:** engenheiro-software.

### RD-0205 · Título de teste cita outra regra · teste (título) · baixa · **não segura o lote**
- **Onde:** `tests/test_T0037_fretes_robo.py:100`, `test_RN_GER_006_fretes_na_uf_do_cliente_sem_linhas`.
- **O que acontece:** o teste confere que, sem linhas, sai "0" e "—". Não tem nada da UF do cliente.
- **Proposta:** antes, `test_RN_GER_006_fretes_na_uf_do_cliente_sem_linhas`. Depois, `test_RN_POS_009_sem_notas_zero_e_traco`.
- **Dono:** testes (entra no lote seguinte).

## Redundância útil (fica)
- **As listas de colunas do contrato §10.7.3, do robô (`_COLUNAS_TABELAS_WEB`, `_RESUMO_FRETES_WEB`) e da web (`COLUNAS`, `COLUNAS_RID`, `_RESUMO_FRETES`):** é a ponte entre dois processos, e os testes de colunas (robô × contrato e robô × web) conferem as três.
- **`marca.COR_PC` com o hex do PC escrito à mão:** a web no Render não importa o PC. `manter?`: falta um teste da raiz que confira as chaves com `relatorios_nucleo.AMARELO` e `CINZA` e com o ardósia. Fica como sugestão ao testes, sem segurar o lote.
- **O TOTAL nas 3 tabelas do Resumo (`manter?`, decisão do po):**
  - O 9 / R$ 85.950 / R$ 2.565 aparece 3 vezes, e os cartões da faixa também mostram 9, R$ 86 mil e R$ 2,6 mil. Pela regra 1 ("uma informação, um lugar"), a repetição existe.
  - Mesmo assim fica, por 3 motivos:
    - é a conferência do RN-POS-009 que o Diretor vê: o TOTAL bate com o cartão, e o cartão arredonda;
    - o designer-ux decidiu manter;
    - o contrato e os testes amarram os 3 totais.
  - Opção, se o po preferir: TOTAL só na "Por UF" (robô, contrato §10.12.2, `test_RN_POS_009_totais_iguais_nas_3_tabelas` e o teste Y5 da web).
- **O "Aguardando o PC" no Fretes e no Entregas (`edicoes.IRMAOS`):** a mesma linha do PC aparece em dois faróis. O aviso é útil.

## Fora do lote (já estão no `main`; sugiro tarefa, não seguram a T-0037)
- **`web/app/templates/editar.html:33`:** "Apague a data para voltar à calculada pelo PC." sai em todo campo de data. Na edição do Fretes aparece 2 vezes, e na DT. REAL não faz sentido (regras 1 e 3; já era o 🟢 6 da UX).
  - Antes: `{% if not novo %}`.
  - Depois: `{% if not novo and c.campo == "prevista_manual" %}`.
  - Vale também para o Entregas. Dono: modulo-web.
- **`estilo.css:637` (T-0024):** `.bc3 .graficos .graf{min-height:280px}` deixa cerca de 85 px vazios no cartão "Por UF (NOV/26)" no PC, que tem 3 linhas e TOTAL. A mesma coisa acontece em toda tabela curta do Resumo.
  - Proposta: `.bc3 .graficos .graf-tab{min-height:0}`.
  - Afeta outros faróis: precisa de revisão do designer-ux. Dono: modulo-web.

## Catálogo
- Os RD-0192 a 0199 e 0202 a 0205 vão para o `docs/redundancias/catalogo.md` no próximo PR do corretor. O arquivo ainda não existe no `main`, e este parecer saiu sem commit, como foi pedido.

## Reteste
- Ao corrigir, cada dono avisa o head novo. O reteste:
  - RD-0197 e RD-0195: PNG e cor calculada iguais;
  - RD-0194: os testes da web passam sem a `blocos_resumo_web`;
  - RD-0198: print da aba Cidade sem a coluna MÊS;
  - o resto: diff e testes da T-0037.
