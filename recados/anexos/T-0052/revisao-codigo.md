# T-0052: parecer do revisor-codigo

- Web: `modulo-web/T-0052-painel-cartoes`, head **73dbbbe1ff71f0328a97eaf1d52fafa18c6a4b03**. Revisei também os heads f141851, 2878e17 e o merge ae1a5d5. O 73dbbbe só tira 2 linhas em branco do `render.py`.
- Testes: `testes/T-0052-painel-cartoes`, head **6dbce3b978d1d6208f434be1d72295a6a18d6efa** (#181).
- Pedido: R-20261127-093750-alexandre e R-20261127-094731-alexandre.
- **Parecer: sem 🔴 nos dois heads. Há 1 🟡 de processo (pareceres de tela) antes do merge.** O parecer vale só para os SHAs acima.

## Conferido sem achado
- **O pedido foi atendido, sem mudança a mais:**
  - todo cartão RRM tem o `rc-valor`;
  - a estrutura é a mesma em todos: título, valor, legenda reservada, faixa (ou `rc-faixa vazia`) e gráfico;
  - as seções têm altura fixa só em `.rrm:not(.rrm-recorte)`;
  - a faixa do topo da aba RRM vai sem números (`faixa_ks=[]` em `main.py`, na rota `/painel`). Isso vale para Resultado, Produtividade e Por DU.
- **A web não calcula nada:**
  - `cartao()` repassa o `valor` do pacote;
  - `legenda_do_cartao` só filtra o texto (sem dígito, sai vazio). É a mesma regra que antes ficava dentro de `faixa_painel`: foi movida, não reescrita;
  - `faixa_painel(tela_f)` continua servindo às 9 abas de painel (forma farol) com `kpis_da_faixa`. Quem trava isso é `test_painel_cartoes_comuns_das_abas_vao_para_a_faixa_e_os_ricos_ficam`.
- **Não sobrou código morto:** `NA_FAIXA`, `na_faixa` e o parâmetro `tela` de `faixa_painel` não aparecem mais em `web/`.
- **CSS:**
  - `.rc-rot`, `.rc-valor`, `.rc-leg`, `.rc-id` e `.rc-faixa` só aparecem em `painel.html`. Farol, parcial e `kpi-est` (que usam só `.rc-barras`) não mudaram;
  - o `@media(max-width:600px)` desfaz as reservas, que é o 🟡 da UX.
- **Versão:** 0.10.1 sobre o main 0.10.0, já com o merge do 57cf6fa. O 0.8.1 do f141851 estava atrás do main e foi corrigido no ae1a5d5. Os 3 testes de versão foram ajustados.
- **Testes que travam o pedido** (`web/tests/test_T0034_pagina_inicial.py`):
  - `bc3-ks` ausente no `/painel` e `rc-valor` em todo cartão;
  - a faixa e a legenda reservadas (`test_T0052_todo_cartao_tem_valor_legenda_reservada_e_faixa`);
  - o CSS do celular e o teto de 22 px;
  - `test_T0052_legenda_so_com_numero_proprio`.
- **#181:** a troca condicional pela presença de `bc3-ks` é correta. Ela exige o mesmo caso nas 3 abas e, no caso T-0052, confere o `rc-valor` × o `valor` do PC em todo cartão. Isso garante que o número do Diretor bate com o painel de origem.
- **Dados digitados, `bap_dados.py`, configs `.json` e `tests/`:** o diff da web não toca neles. O `tests/` da web é igual ao main.
- **Segredos e dado pessoal:** nada no diff; as fixtures são fictícias.
- **`verificar --por-commit`:** sem violação nas duas branches. O diário do testes entra como exceção do protocolo. O merge entre as duas branches sai sem conflito.

## Testes rodados (cópias descartáveis em scratchpad)
- `compileall` em `web/app` (73dbbbe): ok.
- `pytest web/tests -q`:
  - 2878e17: **602 ✅**;
  - main 57cf6fa: **599 ✅**;
  - f141851: 577 ✅.
- `tests/test_T0034_painel_comparacoes.py` do #181 com a web 2878e17: **6 ✅**, nenhum pulado. Com a web do main 57cf6fa: 6 ✅ (os dois casos passam).
- `tests/` (Python 3.12 com tkinter e xvfb):
  - os 14 arquivos que usam a web, no 73dbbbe com o arquivo do #181: **396 ✅**, 0 pulados;
  - a suíte inteira com `-x --deselect` no RN_PAINEL_011 parou aos 62% por um sinal externo (a máquina estava carregada com outra sessão), sem nenhuma falha até ali. Ela não foi refeita.
  - Com o Python 3.13 (sem tkinter), só `test_T0021_edicao_web_robo.py::test_RN_GER_012_...` falha, por ambiente.
  - Além do RN_PAINEL_011, não vi nenhum outro teste de `tests/` quebrado pela T-0052.
- **`web/tests/test_T0045_visitas.py::test_lote_ok_idempotente_e_entra_no_indice`:** não reproduzi a falha. Passou na suíte inteira tanto no head quanto no main. O diff da T-0052 não toca `visitas.py` nem as fixtures de visitas, então a falha não veio da T-0052. [SUPOSIÇÃO] É instabilidade antiga, ligada à ordem ou ao estado do disco, e merece uma tarefa própria do testes.

## 🟡 corrigir antes do merge
1. **Pareceres de tela no head errado.** Os pareceres de UX (`revisao-ux.md`) e de marca (`revisao-marca.md`) valem para o **2df92cd**. Depois dele, a tela mudou:
   - o valor passou a `clamp(1.125rem,5.2vw,1.375rem)`, com 20–22 px;
   - o celular ganhou regras próprias;
   - a grade do recorte passou a `grid-auto-rows:auto`;
   - a legenda sem número some (2878e17), e "projeção do mês" deixa de aparecer em Faturamento líquido, Pedidos e Peças. Os prints de `sim/` (14h10) são anteriores a essa mudança.
   - **Pronto quando:** UX e marca reconfirmarem no 73dbbbe e a simulação depois (PC e celular) for refeita nesse SHA, para a aprovação do po (regra 10).

## 🟢 sugestões
- `web/app/render.py`, docstring de `faixa_painel`: ela ainda descreve a aba RRM, que já não passa pela função (o `[]` está em `main.py`). Basta dizer "aba de painel (forma farol)".
- `web/app/templates/_painel_cab.html:1-3`: o comentário diz "faixa com os números da aba", mas a aba RRM vai sem números.
- `web/tests/test_T0034_pagina_inicial.py`: a decisão vale para Resultado e Produtividade, mas o `bc3-ks` ausente só é conferido em `/painel` (Resultado). Vale incluir `?aba=produtividade`.
- `legenda_do_cartao`: no mês fechado, o PC manda "fechamento do mês", sem dígito, e a legenda também some. O DU da faixa ("· mês fechado") cobre isso; é só um aviso ao po.
- `.rc-rot` com `height:2.5em;overflow:hidden`: um título com 3 linhas fica cortado sem "…" (o 🟢 da UX, ainda em aberto).
