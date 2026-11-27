# T-0052 — auditoria de redundância (corretor-redundancias)

- Head revisado: `f141851697117b7f0dfbf50b7c17c9c88bba6170` (`modulo-web/T-0052-painel-cartoes`), diff `origin/main...f141851`.
- Evidência: prints e `MEDICAO.md` da simulação (Resultado e Produtividade, PC 1366 e celular 390), `revisao-ux.md`.
- Faixa de IDs: RD-0238 a RD-0243 (usados RD-0238 a RD-0241).

## Parecer: **4 achados em aberto, que seguram o lote** (RD-0238, RD-0239 e RD-0240). RD-0241 é baixa e só em comentário ou título: entra no lote seguinte.

### Sem achado
- **Número repetido na tela:** cada valor aparece uma vez só. "R$ 165 mil" e os outros valores ficam só no cartão; a faixa do topo leva só a data, o DU e o selo (RD-0063 revisto, R-20261127-094731). "13 de 19 DU" aparece uma vez. Faixas "out/set/jul" iguais em todos os cartões: é a fixture, não a tela real.
- **CSS:** nada duplicado nem morto. `.rc-id` é nova e única. As regras do celular (`height:auto`, `:empty`, `.vazia`) só desfazem as reservas do PC. `.rrm-recorte .rc-topo{flex:1}` e `.rrm:not(.rrm-recorte) .rc-topo{flex:none}` não se sobrepõem.
- **Faixa vazia reservada no PC** ("Desconto comercial", "Km por visita"): a área vazia é o preço do alinhamento entre os cartões. Fica como redundância útil (`manter?` resolvido pelo revisor-ux: "está bom"). No celular ela some.
- **`NA_FAIXA` / `na_faixa`:** não sobrou referência nenhuma no repositório.

### Achados

| ID | Onde | Tipo | O que se repete | Impacto | Sev. | Proposta (antes → depois) | Dono |
|---|---|---|---|---|---|---|---|
| RD-0238 | Painel Executivo › Resultado, cartões "Faturamento líquido · proj.", "Pedidos faturados · proj." e "Faturamento de peças · proj." (origem `painel_rrm.py:390`, `leg_proj`; usado nas linhas 395, 413 e 425) | texto | O título já diz "· proj." e a legenda repete "projeção do mês": 3 cartões, o mesmo fato 2 vezes em cada um. Antes da T-0052, essa legenda sem número não aparecia (a regra do `NA_FAIXA` a escondia). Agora ela aparece na web. Ao lado, "Positivação 45 · projeção do mês 66" usa a mesma frase com outro sentido (lá, o valor grande é o real), o que confunde. | leitura | média | `leg_proj = "projeção do mês" if corre else "fechamento do mês"` → `leg_proj = "" if corre else "fechamento do mês"`. A linha da legenda continua reservada no PC (T-0052) e some no celular (`.rc-leg:empty`). Fixtures que imitam o texto (só alinhar, sem obrigação): `web/tests/conftest.py:45,49` e `tests/test_T0014_recortes_web.py:22`. Mexe em tela do PC: precisa de simulação antes (CLAUDE.md, regra 10). | modulo-farois |
| RD-0239 | `web/app/render.py:124-135` (`faixa_painel`) e `web/app/main.py:321,328,334` | código | O parâmetro `tela` de `faixa_painel(tela, tela_f)` não é mais lido, e a chamada `faixa_painel(tela, None)` sempre devolve `[]`. O lugar do `NA_FAIXA` ficou com 4 linhas em branco (2 sobrando). | manutenção | baixa | `def faixa_painel(tela, tela_f): if tela_f: return kpis_da_faixa(tela_f["kpis"]); return []` → `def faixa_painel(tela_f: dict \| None) -> list[dict]: return kpis_da_faixa(tela_f["kpis"]) if tela_f else []`. Em `main.py`: 321 e 328 → `render.faixa_painel(tela_f)`; 334 → `faixa_ks=[]` (com o comentário "aba RRM: faixa sem números, RD-0063"). Teste `test_T0034_pagina_inicial.py:178` → `render.faixa_painel(None) == []`. Tirar as 2 linhas em branco que sobraram. | modulo-web |
| RD-0240 | `web/tests/test_T0034_pagina_inicial.py:29,32`, `:158` e `:175-178` | teste | `'class="bc3-ks"' not in h` aparece em 3 testes e `h.count("R$ 165 mil") == 1` em 3 testes, sempre com o mesmo pacote. O 3º teste ainda repete o `faixa_painel(...) == []`. | manutenção | baixa | Fica só em `test_painel_no_bc3_com_faixa_abas_e_cartoes` (linhas 29 e 32). Em `test_cartoes_alem_dos_3_primeiros_...`, linha 158 sai inteira. Em `test_T0052_todo_cartao_...`, sai a linha 177 e o laço das linhas 175-176 fica `assert h.count("R$ 7,00") == 1`. Fica o `faixa_painel(None) == []` (RD-0239) como único teste de unidade da faixa vazia. | modulo-web |
| RD-0241 | `web/tests/test_T0034_pagina_inicial.py:147` (título) e `:201` (comentário) | teste | O título `test_cartoes_alem_dos_3_primeiros_mantem_numero_e_legenda` e o comentário "(o número do 4º cartão em diante é o maior)" falam de uma divisão "3 primeiros × resto" que a T-0052 desfez. | manutenção | baixa (só comentário e título: não segura o lote) | Título → `test_os_10_cartoes_do_resultado_mostram_numero_e_legenda`; comentário → `# U10: enquanto o template usar rc-valor e rc-leg, o CSS tem as duas regras`. | modulo-web |

## Para fechar
- **RD-0238** (modulo-farois): legenda vazia quando `corre`, com simulação do Painel no PC e na web.
- **RD-0239 e RD-0240** (modulo-web): no mesmo PR da T-0052.
- **Reteste:** novo head SHA com `pytest web/tests/test_T0034_pagina_inicial.py` verde e print do Resultado sem "projeção do mês" sob os títulos "· proj.".

## Reteste no head `2878e171838948f8bd02854c3cf78edd55ca59ce` (2026-11-27)

- Escopo: o commit `2878e17` (correções) e o diff `origin/main...2878e17`. O `ae1a5d5` é o merge do `main` (T-0050) e não mexe nos arquivos da T-0052 além do `VERSAO`.
- Evidência: `pytest web/tests/test_T0034_pagina_inicial.py web/tests/test_web.py`: 69 passaram. `pytest tests/test_T0014_recortes_web.py`: 5 passaram. Leitura do diff.

| ID | Situação | Evidência |
|---|---|---|
| RD-0238 | **fechado na web** | `render.legenda_do_cartao` (`render.py:72-75`) é usada só em `cartao()`. "projeção do mês" sem número some, e "projeção do mês 66" e "R$ 190 mil" ficam (`test_T0052_legenda_so_com_numero_proprio`). A regra "só com número próprio" está num lugar só: não há outro `isdigit` de legenda na web. No PC, os únicos textos sem número que essa regra corta são `leg_proj` ("projeção do mês" e "fechamento do mês"). O "mês fechado" já está no DU da faixa ("22 DU · mês fechado"), então não se perde informação. |
| RD-0239 | **aberto (resíduo)** | O parâmetro morto saiu: `faixa_painel(tela_f)`, e `main.py` passa `faixa_ks=[]` na aba RRM e `faixa_painel(None) == []` no teste. **Faltou** tirar as 2 linhas em branco a mais: `render.py:128-131` continuam com 4 linhas em branco entre `abas_no_celular` e `faixa_painel`. Antes → depois: 4 linhas em branco → 2. Baixa, dono modulo-web. |
| RD-0240 | **fechado** | `bc3-ks not in h` e `count("R$ 165 mil") == 1` ficaram só em `test_painel_no_bc3_com_faixa_abas_e_cartoes`. O teste dos 10 cartões e o `test_T0052_todo_cartao_...` não repetem mais essas checagens. |
| RD-0241 | **fechado** | O título virou `test_todos_os_cartoes_do_resultado_mostram_numero_e_legenda`, e o comentário U10 ficou sem a divisão "4º cartão em diante". |

### Novo
- **RD-0242 · texto · média · modulo-farois · fora do lote da T-0052** (não segura este PR, porque não está no diff da web e já existia antes).
  - Onde: no PC (Tkinter), o Painel do Diretor, aba Resultado, continua com "Faturamento líquido · proj." / "Pedidos faturados · proj." / "Faturamento de peças · proj." e a legenda "projeção do mês" logo abaixo. O texto vem de `painel_rrm.py:390` (`leg_proj`).
  - A web passou a filtrar a legenda (RD-0238), mas a fonte segue mandando o texto repetido.
  - Proposta (para o backlog, com simulação): `leg_proj = "projeção do mês" if corre else "fechamento do mês"` → `leg_proj = ""`. Feito isso, `render.legenda_do_cartao` fica sem efeito e pode sair, e a regra volta a ter um lugar só, a fonte.
- Mais nada: o merge não trouxe CSS, texto nem teste repetido nos arquivos da T-0052.

### Parecer do reteste
- **1 achado em aberto no lote:** RD-0239 (resíduo), baixa, em código. Pela regra de liberação, segura o lote até tirar as 2 linhas em branco.
- RD-0242 fica no catálogo para o PC e não entra neste lote.
