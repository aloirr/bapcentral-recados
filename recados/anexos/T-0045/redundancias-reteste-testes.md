# T-0045 · Reteste de redundâncias · PR do testes

## Rodada 3: head b1a0533 (vale esta)
- **Branch:** `testes/T-0045-testes`, head **b1a0533cadc01e262adafa10906263e11b12469c**
- **Base:** `origin/main` @ 4728880, que é também o merge-base. O merge do main entrou na branch (7d8c19e).
- **Escopo:**
  - o RD-0168 e o RD-0169;
  - o delta do testes em fd6aeef..b1a0533. É só o b1a0533: `tests/test_T0045_paridade_visitas_web.py` (−8), `tests/test_T0045_plano.py` (−1) e uma linha no `.coord/diario/testes.md`. O 7d8c19e só traz o main, que já tinha sido revisto no PR #151.
- **Evidência:**
  - Rodei `pytest` no head b1a0533 nos 3 arquivos da T-0045: 30 ✅ e 1 pulado (o plano: o `visitas_maxima` do main ainda não tem `indice_do_pc`).
  - Conferi com `ast` que nenhum dos 3 arquivos ficou com import sem uso (o `pytest`, o `datetime` e o `rn` continuam usados).
  - Procurei `skip`, `Pulado`, `branch` e `modulo-` nos 3 arquivos. Só sobrou a guarda do robô, que ainda vale.

| RD | Situação | Evidência |
|---|---|---|
| RD-0168 | **fechado** | Na paridade saíram as 2 guardas da web: a do `exists()` e a do `hasattr` na fixture `web_app`. Saíram também o `_ROTA`, que tinha ficado sem uso, e a frase "Pulado, com motivo, enquanto a web…" da docstring. Os 7 testes da paridade rodam contra a web do main. |
| RD-0169 | **fechado** | Saiu o `assert rn.hoje_manaus() == datetime.now(vn.FUSO_MANAUS).date()` do `test_RN_VIS_002_sem_hoje_usa_manaus`. O que o teste prova do `plano` sem `hoje` continua lá. A fonte do `hoje_manaus` fica no `test_RN_GER_007_hoje_manaus_e_a_data_no_fuso_de_manaus` (T-0017). |

**Achado novo:** nenhum no delta fd6aeef..b1a0533.

**Resultado: libera.** Nenhum achado em aberto, de nenhuma gravidade.
- Os RD-0149, RD-0150 (as 2 partes), RD-0154, RD-0155, RD-0168 e RD-0169 estão fechados.
- Vale para **b1a0533cadc01e262adafa10906263e11b12469c** (testes), contra o main **472888058e870ef3e1864358045ac59e53a94a47**.

---

## Rodada 2: head fd6aeef (histórico)

- **Branch:** `testes/T-0045-testes`, head **fd6aeef83823e37bcc837155d73a4a0b3922d546**. A rodada anterior foi no 38b1329.
- **Base:** `origin/main` @ 4728880. Ele já tem a rota (PR #150, d58b12f) e a web (PR #151) da T-0045. O merge-base da branch é o 98f87db, de antes do #151.
- **Escopo:** `git diff origin/main...origin/testes/T-0045-testes`:
  - `tests/test_T0045_paridade_visitas_web.py`
  - `tests/test_T0045_visitas_nucleo.py`
  - `tests/test_T0045_plano.py`
  - `.coord/diario/testes.md`
- **Evidência:** juntei o head fd6aeef com o `origin/main` 4728880 numa cópia local, sem commit. O merge não deu conflito.
  - `tests/test_T0045_visitas_nucleo.py`, `tests/test_T0045_paridade_visitas_web.py` e `tests/test_T0045_plano.py` juntos: 30 ✅ e 1 pulado.
  - A paridade agora roda contra a web do main.
  - O plano continua pulado, porque o robô (`indice_do_pc`) ainda não está no main.
- **Numeração:** o RD-0156 ao RD-0167 já foram usados por outro corretor, em `anexos/T-0023/redundancias-final.md`. Os novos começam no **RD-0168**.

### Situação por RD
| RD | Situação | Evidência |
|---|---|---|
| RD-0149 | **fechado** | Saíram a `paridade:213` (a disjunção) e a frase da docstring. O `test_RN_VIS_007_colunas_fora_do_espelho_iguais_na_rota_e_na_web` agora só compara `COLUNAS_PROIBIDAS == _FORA_DO_ESPELHO` (e as permitidas da web, se um dia existirem). Os outros asserts da paridade comparam núcleo × web. |
| RD-0150 (títulos, testes) | **fechado** | Fechado na rodada anterior (`núcleo:253` e `:277` no head novo, "ord de até 6 dígitos"). |
| RD-0150 (comentário, modulo-web) | **fechado** | Em `web/app/visitas.py:12-13` @ 4728880 (main, PR #151), o texto agora é "O teste de paridade (`tests/test_T0045_paridade_visitas_web.py`) prende as cópias ao núcleo.", sem o nome da branch. |
| RD-0154 | **fechado** | `núcleo:120` `assert set(vn._COLUNAS_ESPELHO) - col == set(vn._FORA_DO_ESPELHO)`. A disjunção do `nomes_que_o_site_espelha` saiu. A lista literal fica só em `núcleo:225`. |
| RD-0155 | **fechado** | Saíram a guarda `_FUNCOES` e o skip do núcleo, a guarda da rota na paridade e o skip do `_rede_rota` (que virou `tuple(vn._REDE)`). As docstrings não citam mais a branch da rota. |

### Achados novos

#### RD-0168 · Com a web no main (#151), as guardas "web ainda não está no main" da paridade viraram código morto
| Campo | Conteúdo |
|---|---|
| Onde | `tests/test_T0045_paridade_visitas_web.py` @ fd6aeef: o `:33-35` (`if not (RAIZ / "web" / "app" / "visitas.py").exists(): pytest.skip(...)`), o `:45-46` na fixture `web_app` (`if not all(hasattr(visitas, n) for n in _ROTA): pytest.skip(...)`) e a docstring `:18` ("Pulado, com motivo, enquanto a web (`web/app/visitas.py`) não estiver no main.") |
| Tipo | código (teste) · doc (comentário) |
| O que se repete | É o mesmo caso do RD-0155, agora do lado da web. No main 4728880, `web/app/visitas.py` existe e tem `juntar_baixado` (`:200`), `dia_fechado_no_indice` (`:221`), `dias_a_baixar` (`:227`), `RE_PESSOAL`, `TIPOS_ACHADO` e `COLUNAS_PROIBIDAS`. As 2 guardas nunca disparam. As mensagens de skip citam a branch `modulo-web/T-0045-visitas`, que já entrou no main (o padrão do RD-0150). Na rodada anterior elas ainda valiam, porque o #151 não tinha entrado. |
| Impacto | manutenção e leitura. Se uma função da web mudar de nome, a paridade é pulada em silêncio em vez de reprovar. É justo a quebra que o arquivo existe para pegar. |
| Severidade | baixa. A parte de código segura o lote; a da docstring sozinha não seguraria. |
| Proposta | Saem o `if not (...).exists(): pytest.skip(...)` (`:33-35`) e o `if not all(hasattr(visitas, n) …): pytest.skip(...)` da fixture (`:45-46`). Com isso o `_ROTA` (`:31`) fica sem uso e sai também. Na docstring, sai a linha `:18`, e a `:19` fica "Datas fictícias, sem dado de cliente." O `pytest` continua importado, por causa do `@pytest.fixture`. |
| Dono | testes |

#### RD-0169 · O teste do plano volta a testar o `relatorios_nucleo.hoje_manaus`, que já tem teste próprio
| Campo | Conteúdo |
|---|---|
| Onde | `tests/test_T0045_plano.py:73` @ fd6aeef (`assert rn.hoje_manaus() == datetime.now(vn.FUSO_MANAUS).date()`, em `test_RN_VIS_002_sem_hoje_usa_manaus`) × `tests/test_T0017_tres_farois.py:591-597` no main (`test_RN_GER_007_hoje_manaus_e_a_data_no_fuso_de_manaus`) |
| Tipo | teste |
| O que se repete | "`hoje_manaus()` = a data de agora no fuso de Manaus" está provado 2 vezes, em 2 arquivos. O teste da T-0017 é a fonte e protege a virada da meia-noite com o `antes`/`depois`. A linha nova compara um instante só. O resto do teste novo (o `plano` sem `hoje` vai até hoje em Manaus, `:74-83`) é a parte própria da T-0045 e fica. Ele já usa o `antes`/`depois`. |
| Impacto | manutenção. Uma mudança no `hoje_manaus` exige editar 2 testes. |
| Severidade | baixa |
| Proposta | Sai o `:73`. Na docstring `:69-72`, "pelo `relatorios_nucleo.hoje_manaus` (RD-0147: um só)" fica, porque explica a fonte da data. |
| Dono | testes |

### Sem achado
- O `test_T0045_plano.py`, fora o `:73`:
  - a guarda do robô (`:23-25`) ainda vale, porque o `visitas_maxima` do main não tem `indice_do_pc`;
  - o teste novo do `plano` sem `hoje` não repete o `:64`, que passa o `hoje` explícito.
- O diário do testes: só acrescenta linha. O conflito da rodada anterior sumiu com o merge do main (4beedfc).

### Resultado
**Não libera** o head fd6aeef.
- **Fechados:** RD-0149, RD-0150 (as 2 partes), RD-0154 e RD-0155.
- **Seguram o lote do testes:**
  - RD-0168: as guardas da web, mortas depois do #151;
  - RD-0169: o `hoje_manaus` testado de novo no plano.

Vale para **fd6aeef83823e37bcc837155d73a4a0b3922d546** (testes), contra o main **472888058e870ef3e1864358045ac59e53a94a47**.
