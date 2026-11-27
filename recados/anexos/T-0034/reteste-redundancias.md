# T-0034 · Reteste de redundância (corretor-redundancias)

- **Escopo:** `git diff b60cae1..aae27cc` da branch `modulo-web/T-0034-pagina-inicial` (20 arquivos, +211 −145), lido no estado do head. Só leitura: a branch do clone não foi trocada.
- **Head SHA retestado:** `aae27cc`.
- **Testes no head:** `pytest web/tests` com 364 testes verdes (cópia do head por `git archive`, com `.coord/contratos` junto). `pylint` e `vulture` não estão instalados.
- **Fora do lote (aceitos pelo gerente):** os 3 títulos de teste do RD-0067 e o RD-0044.
- **Resultado:** **não libera.** 6 achados fechados (RD-0038, RD-0059, RD-0063, RD-0064, RD-0067 e RD-0068), 2 com item em aberto (RD-0065 e RD-0066) e 3 novos, todos de gravidade baixa (RD-0069 a RD-0071). Dono de todos: modulo-web.

## 1. Situação dos achados

| RD | Situação | Prova no head `aae27cc` |
|---|---|---|
| RD-0038 | **Fechado** | Saiu `render.TITULOS`, e `aba_para_tela` não devolve mais `titulo`. `PAINEIS` tem os nomes curtos ("Visitas", "Itens"…), e `PAINEL_CURTO` ficou só com as 3 abas RRM. A docstring de `render.py:1` foi corrigida. Teste: `test_nomes_das_abas_do_painel_numa_tabela_so`. |
| RD-0059 | **Fechado** | Os 2 "Voltar ao farol" saíram de `parcial.html`, e a regra `.bc3-corpo>p>.bc3-bt` saiu do CSS. O estado vazio tem uma frase só. Teste: `test_parcial_sem_repetir_a_lateral` (`"Voltar ao farol" not in h`). |
| RD-0063 | **Fechado** | `painel.html` não tem mais `rc-valor` nem `rc-leg`. Em `render.faixa_painel`, o detalhe só aparece quando a legenda tem número, e os anéis ficam só no cartão. Teste: `"MTD" not in faixa` e `h.count("R$ 165 mil") == 1`. A sobra de CSS está no RD-0069. |
| RD-0064 | **Fechado** | `base.html:34` usa a frase do contrato. `painel.html` só avisa "O painel não veio no último pacote do PC." quando há pacote. Teste: `h.count("Sem dados ainda") == 1`. O teste antigo ficou duplicado: ver o RD-0070. |
| RD-0065 | **Aberto (2 itens)** | Feito: `_faixa.html` com `quando`, `selo_velho`, `filtro_uf`, `filtro_uf_off`, `numeros` e `faixa_simples`, usados pelos 2 cabeçalhos e pelas telas simples. `painel.html:7` passou a usar `faixa_simples`. O `title` do seletor desligado tem um texto só. `kpis_da_faixa` é usada por `faixa_painel` e por `_bc3_cab.html`. Falta: (a) `render.kpis_do_corpo` está registrada como global (`main.py:96`), mas nenhum template a usa (só `test_regra_cartao_comum…` a chama). `_resumo.html:5` ainda filtra por conta própria (`selectattr("estados")…rejectattr("estados")|selectattr("linhas")`). A regra segue em 2 lugares e a função está morta. (b) A barra de abas com "3 no celular + Mais" continua escrita 2 vezes, com lógicas diferentes: `_painel_cab.html:18-20` (`vis_cel`) e `_bc3_cab.html:32-34` (`vis`). Esse item estava na lista do achado, mas faltou na proposta anterior; a proposta vai abaixo. |
| RD-0066 | **Aberto (1 item, CSS)** | Feito: saíram `AVISO_SO_BAP` e `RELATORIO` (agora `PAINEL_RID`, usado em `:158` e `:280`). `no_painel` é calculado uma vez só. `mainclass2` agora é usado por `painel.html` e `parcial.html`. O parâmetro `quando` saiu. Saíram `.sair`, os 4 `main{…}`, `main.larga`, `.selo-velho`, `.aviso.info.faixa-pc` e o `margin-left` duplicado. O comentário de `render.py:193` foi corrigido. Falta: continuam 3 blocos `@media(max-width:700px)` (`estilo.css:483`, `:581` e `:593`; o `:593` é novo). A proposta era um bloco só. `.bc3-k em` é declarado 2 vezes na mesma largura (`:494` `{white-space:nowrap;overflow:hidden;text-overflow:ellipsis}` e `{display:block;margin:0}`; `:588` `{display:block;margin:0;white-space:normal}`). O `:588` anula o `nowrap` do `:494`, e `display:block;margin:0` aparece 2 vezes. |
| RD-0067 | **Fechado** (sem os 3 títulos, fora do lote) | Saíram os 4 testes repetidos. `com_painel` está só em `conftest.py:113`. Em `test_T0022_painel_meta.py:58-69`, cada resposta é buscada uma vez e reusada. A sobra está no RD-0070. |
| RD-0068 | **Fechado** | `usuarios.html:29` só mostra o selo "Desativado". Teste: `test_usuarios_sem_selo_ativo_em_toda_linha`. |

**Proposta para o que falta no RD-0065:**
- `_resumo.html:5`: **antes:** `{% set ricos = tela.kpis|selectattr("estados")|list + tela.kpis|rejectattr("estados")|selectattr("linhas")|list %}` → **depois:** `{% set ricos = kpis_do_corpo(tela.kpis) %}`.
- Barra de abas: uma função pura `render.abas_no_celular(chaves, ativa) -> list[int]` (a 1ª, a 2ª e a aberta; senão as 3 primeiras), usada por `_painel_cab.html` (no lugar de `vis_cel`) e por `_bc3_cab.html` (no lugar das 3 linhas `{% set vis … %}`). Fica uma regra só de "quais abas aparecem no celular".

**Proposta para o que falta no RD-0066:**
- As regras de `estilo.css:582-589` e a regra `.d-pc{display:none}.d-cel{display:inline}` de `:593` entram no bloco `@media(max-width:700px)` de `:483`. Os blocos de `:581` e `:593` saem.
- Em `:494`, as 2 declarações `.bc3-k em{…}` viram uma só: `.bc3-k em{display:block;margin:0;white-space:normal}`. O `.bc3-k em{…}` de `:588` sai. Nada muda na tela, porque hoje o `:588` já vence.

## 2. Achados novos (criados pela correção)

### RD-0069 · CSS do número grande do cartão RRM ficou morto
- **Onde:** `estilo.css:116` `.rc-valor{…}` e `:117` `.rc-leg{…}`.
- **Tipo:** código.
- **O que se repete:** nenhum template, JS ou `.py` usa mais essas classes. O RD-0063 tirou `rc-valor` e `rc-leg` de `painel.html`, e o teste confere `"rc-valor" not in h`.
- **Impacto:** manutenção (regra vencida, a mesma origem do RD-0036 e do RD-0045).
- **Severidade:** baixa.
- **Proposta:** as linhas `:116` e `:117` saem.

### RD-0070 · Testes: o mesmo caso "painel sem pacote" em 2 testes e um import morto
- **Onde:**
  - `test_web.py:162` `test_sem_pacote_aviso` e `test_T0034_pagina_inicial.py:48` `test_painel_sem_pacote_diz_quando_chega`. Os 2 chamam `admin.get("/painel")` sem pacote e conferem "Sem dados ainda…". O da T-0034 confere o mesmo e mais: a contagem 1 e a faixa;
  - `test_T0034_pagina_inicial.py:7` `from painel22_fixture import pacote_completo`: não é mais usado, porque a fixture `com_painel` foi para o `conftest.py`.
- **Tipo:** teste.
- **Impacto:** manutenção (a troca de texto do RD-0064 obrigou a mexer nos 2 testes).
- **Severidade:** baixa.
- **Proposta:** `test_web.py:162-164` sai, e o da T-0034 fica. A linha `:7` de `test_T0034_pagina_inicial.py` sai.

### RD-0071 · Formatação "dd/mm hh:mm" escrita 2 vezes
- **Onde:** `main.py:63-66` `fmt_manaus_curto` (`f[:5] + " " + f[-5:]`) e `main.py:69-72` `hhmm` (o `else` repete `f[:5] + " " + f[-5:]`).
- **Tipo:** código (formatação de data reimplementada).
- **Impacto:** manutenção.
- **Severidade:** baixa.
- **Proposta:** em `hhmm`, **antes:** `… else f[:5] + " " + f[-5:]` → **depois:** `… else fmt_manaus_curto(iso)`.

## 3. Sem achado novo (conferido)
- **Macros de `_faixa.html`:** cada peça da faixa está escrita uma vez. Os 2 cabeçalhos e `faixa_simples` usam os mesmos macros, e nenhum template guarda cópia da marcação. O `_faixa_simples.html` saiu, e as 5 telas importam de `_faixa.html`.
- **`conftest.py`:** `com_painel` está definida só lá. A T-0022 e a T-0034 não a redefinem. A única sobra é o import do RD-0070.
- **Texto do seletor desligado:** o `title` tem um texto só ("Esta aba mostra a BAP inteira"), num lugar só (`_faixa.html:20`), e o teste da T-0022 confere esse texto. O `aria-label` ("Filtro por estado (esta aba é da BAP inteira)") fica como `manter?`, porque é acessibilidade. Sugestão opcional, que não segura o lote: alinhar para "Filtro por estado: esta aba mostra a BAP inteira".
- **Data em `d-pc` e `d-cel`:** as 2 estão no HTML, mas só uma aparece por largura (a outra fica com `display:none`, fora da leitura de tela). É `manter`.
- **"Como ler" do RRM:** saiu do rodapé (`<p class="como">`) e foi para o ⓘ do título. Continua num lugar só.

## 4. Para liberar
- Corrigir o que falta no RD-0065 e no RD-0066, mais o RD-0069, o RD-0070 e o RD-0071.
- Reteste: o novo head SHA, `pytest web/tests` verde e o print `painel-admin` no celular 390 (a regra de abas no celular e o CSS de 700px).

## Premissas
- [SUPOSIÇÃO] Sem PNG novo neste reteste: os itens de tela (RD-0059, RD-0063, RD-0064 e RD-0068) foram fechados pelo template e pelos testes do head. As mudanças de CSS propostas não mudam a tela.
- [SUPOSIÇÃO] Para dizer que um CSS está morto, as classes foram buscadas em `web/app` (templates, JS e `.py`).
- [SUPOSIÇÃO] Os 3 títulos de teste do RD-0067 e o RD-0044 (`render.BC3` e o comentário de `render.py:183-185`) não foram reabertos, porque o gerente os aceitou fora do lote.
- [SUPOSIÇÃO] `web/RENDER.md:66-101` ainda fala em "Painel · resultado / produtividade". Esse arquivo não está no diff da T-0034. Fica como observação para o próximo lote, não como achado deste.
