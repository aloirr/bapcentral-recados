---
id: R-20261127-001426-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: revisao
prioridade: normal
tarefa: T-0033
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T00:14:26-04:00
---
# Parecer do revisor-codigo na T-0033 (7 branches): web com 🔴 de conflito, em correção

Origem: subagente revisor-codigo desta sessão, gravado pelo gerente (decisão 3 A). Os 🔴 e 🟡 já estão com os donos.

## Contexto
Revisão da T-0033 antes dos PRs, nos heads de origin em 27/11: contrato 04c38e5, web 3c6419d, farois cf473a4 (inclui 403036f), rota ca97773, robo 4fa2aae, posvenda aa3fc77 (PR #127), testes e2e815a. Combinado montado em /tmp (main 767a389 + as 7 branches) e apagado depois; nada gravado no clone.

Resultado no combinado (Python 3.12 com tkinter): compileall ok; `pytest tests` 596 ok e 5 falhas; `pytest web/tests` 342 ok. No main, `pytest tests` dá 552 ok e nenhuma falha. `bap_dados.VERSAO` = 27. Nenhum arquivo de `RELATORIOS/` nem `.json` nos diffs. `verificar <dono> --base origin/main` ok nas 7 branches. Em `--por-commit`, o #127 acusa o painel_diretor_hist.json em ea6a003 e aa3fc77, mas o diff líquido é zero: com squash, passa.

## Parecer por branch
- engenheiro-software/T-0033-contrato-bc3 04c38e5: aprovado.
  - 🟡 Fora desta branch: o `relatorio.md:788` (§10.7.6) ainda lista o `AVISO_CARTOES`, que a web tirou.
  - 🟡 O `relatorio.md:730` (Aderência) não prevê o `chip` nas colunas pct.
  - 🟢 A §12.1 usa `--vermelho`/`--amarelo` e candidatos antigos (`--suave` #69736D); vale alinhar aos nomes e hex do manual 4.2.
- modulo-web/T-0033-revisao-geral 3c6419d:
  - 🔴 Conflita com o main da T-0035 (web 0.4.0). Precisa do merge de origin/main mantendo:
    - `web/app/main.py:446` com `par["arquivo"].read_bytes()`;
    - `web/app/main.py:511` com `ind.gerado_em(rid)`;
    - `_bc3_cab.html:19-20` com o selo "Desatualizado";
    - o `.bc3-selo` em tokens no `estilo.css`;
    - VERSAO ≥ 0.4.0 (sugestão: 0.5.0).
  - 🔴 Deixa o CI vermelho: `tests/test_T0017_pacote_tres_farois.py:953` espera o `tabelas.AVISO_CARTOES`, que a branch tirou. O `testes` atualiza o teste e o `engenheiro-software` o §10.7.6, no mesmo lote.
  - 🟡 Cores que o manual 4.2 tira (falha `test_RN_GER_009_site_sem_as_cores_que_o_manual_tira`):
    - `estilo.css:72,95,96`: `--c-e7edf5`, `--c-fff3bf` e `--c-fff8e1`, usados nas linhas 166, 237, 238, 247, 266, 267, 307 e 555;
    - `estilo.css:354`: o `62BB47`;
    - `render.py:328`: `#b3261e` (passa a `--alerta` #B42318).
  - 🟡 São 66 tokens `--c-<hex>` no `:root`: é hex com outro nome, não token (tela-bc3 §12). Use os tokens do manual.
  - 🟢 `main.py:373`: o detalhe "BAP inteira" (§13.1 pede "BAP").
  - 🟢 Falta um teste de 403 do `/farol/<rid>/linhas` por perfil. Conferi à parte: o corte está certo nos 6 perfis, nos 3 faróis e nas abas da Inadimplência.
  - XSS: `data-pop` com `tojson|forceescape`; o popup e o "carregar mais" usam `textContent`/`importNode`. Ok.
- modulo-farois/T-0033-aderencia-cor cf473a4:
  - Só cor e texto. `tom_aderencia` mantém o 80/50.
  - 🟡 Constantes fora do manual 4.2 (falham 3 testes do `testes`):
    - `bap_visual.py:73`: SUAVE #69736D, deve ser #5E6B63;
    - `bap_visual.py:68`: CINZA_LINHA #D5DAD4, deve ser #E3E8E4;
    - `bap_visual.py:89`: FUNDOS alerta #FCEFEE e atencao #FFF8E6, devem ser #FDECEA e #FFF4D6;
    - `bap_visual.py:1312`: o "cinza" com #69736D.
- modulo-rota/T-0033-marca ca97773: aprovado.
- modulo-robo/T-0033-marca 4fa2aae: aprovado no texto.
  - 🟡 A cor da Aderência não chega ao site: `bap_automation.py:7708` monta as colunas pct da Aderência com `selo=None`, e o `_selo_web` descarta o `chip` que o PC agora manda (`relatorios_nucleo.py:14531-14533`). Falta `selo="faixa"` nessas colunas, e o contrato precisa prever isso.
  - Essa mudança só entra depois da web e do PC: robô novo com PC antigo derruba a tabela (`_TabelaTortaWeb("selo")`).
- modulo-posvenda/T-0033-marca aa3fc77 (#127): segue aprovado e entra sem conflito.
- testes/T-0033-marca-aderencia e2e815a: os testes estão certos e pegam os 🟡 acima. Só entra junto ou depois da web e do farois.
  - 🟢 Os nomes `test_RN_GER_009_aderencia_*` deveriam citar a RN da Aderência (RN-VIS-001, se for criada).

## Ordem de merge
1. #127 posvenda, rota e robo (marca).
2. Contrato, com o §10.7.6 e a Aderência no relatorio.md.
3. Web (depois do merge de origin/main e das correções).
4. Farois.
5. Testes (com o test_T0017 ajustado).
6. Por último, o robo com o `selo="faixa"` da Aderência.

## Pronto quando
Os 🔴 e 🟡 resolvidos em heads novos e re-revisados. Com commit novo, a revisão é nova.

[SUPOSIÇÃO] A simulação PNG da tela foi aprovada (commit 588bb6b: "12 achados do parecer de UX"); não vi os PNG.
