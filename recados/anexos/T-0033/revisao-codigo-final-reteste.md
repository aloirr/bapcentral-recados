# T-0033 — reteste da revisão de código final (revisor-codigo)

- **Data:** 27/11/2026 (Manaus).
- **Repositório:** `aloirr/bapcentral` (conferido com `git remote -v`). Base: `origin/main` em `a32b610` (o `767a389` + o quadro da T-0046, #136, só doc).
- **Escopo:** só os commits novos depois do parecer `revisao-codigo-final.md`. As faixas `chip` do PC (`CHIP_SLA`, `FAIXA_PCT_META`, `#E5F3DF` em faixa) ficam para a T-0047.
- **Vale para os heads abaixo.** Commit novo pede revisão nova daquele branch.

| Parte | Branch | Antes → agora | Parecer |
|---|---|---|---|
| Contrato | `engenheiro-software/T-0033-contrato-bc3` | `9ff2851` → `a36dfc1` | C1 fechado · C2(a) fechado · **C2(b) 🟡 aberto** (R1) |
| Web | `modulo-web/T-0033-revisao-geral` | `3165af2` → `9716248` | W2 e W3 fechados · **W1 🟡 aberto** (R1) · 🟢 2 |
| Faróis | `modulo-farois/T-0033-aderencia-cor` | `7de029b` → `80daf25` | F1 fechado · **🟡 1** (R2) · 🟢 1 |
| RN-VIS-001, rota, robô, pós-venda, testes | sem mudança | `046a4db`, `f39e389`, `ff6e7f0`, `aa3fc77`, `f91c265` | parecer anterior vale |

**Resultado: nenhum 🔴. Dos 6 🟡, 4 fecharam (W2, W3, F1, C1). W1 e C2 continuam abertos como um só achado (R1): a web e o contrato foram corrigidos em sentidos opostos. Entrou 1 🟡 novo (R2): o print do selo novo.**

## Os 6 🟡 do parecer anterior
| 🟡 | Situação | Como |
|---|---|---|
| W1 | **parcial** | A marca agora vai sempre, também com `detalhe` do PC (`web/app/main.py:395-397`, "BAP inteira · {detalhe}" e "sem o filtro · {detalhe}"), com teste novo `web/tests/test_abas.py::test_cartao_com_detalhe_do_pc_tambem_diz_de_onde_vem_o_numero`. Mas a regra da web contradiz o contrato novo. Ver R1. |
| W2 | fechado | `web/app/templates/base.html:6`: `<title>… · BAP AUTOPARTS</title>`, igual ao manual §7. É o único `<title>` dos templates. |
| W3 | fechado | `web/app/tabelas.py:187-190`: `ok` = `--ok-claro`/`--verde-escuro`, `alerta` = `--alerta-claro`/`--alerta`. Teste de tela ajustado (`test_abas.py:658-659`). |
| F1 | fechado | `bap_visual.py:1309-1313`: os 4 pares do manual. |
| C1 | fechado | `.coord/contratos/relatorio.md:688`: os 4 pares do manual, com o nome do token e a lista dos hex que não valem. |
| C2 | (a) fechado · (b) **aberto** | (a) `tela-bc3.md:371`: `<title>` "· BAP AUTOPARTS". (b) Os dois contratos agora concordam entre si, mas na regra que a web tirou. Ver R1. |

## A paleta do `chip_tom` (pedido 2)
| Tom | Contrato (`relatorio.md:688`) | PC (`bap_visual.py:1309-1313`) | Web (`tabelas.PALETA_TOM`, valor de `marca.TOKENS`) | Manual (`docs/marca/manual.md` do main) | Contraste |
|---|---|---|---|---|---|
| ok | #F0F7EC / #2F7D32 | #F0F7EC / #2F7D32 | `--ok-claro` #F0F7EC / `--verde-escuro` #2F7D32 | `--ok-claro` / `--ok` (= `--verde-escuro`), §4.3 | 4,69:1 |
| atenção | #FFF4D6 / #8A5A00 | #FFF4D6 / #8A5A00 | `--atencao-claro` / `--atencao-texto` | §4.3 | 5,41:1 |
| alerta | #FDECEA / #B42318 | #FDECEA / #B42318 | `--alerta-claro` / `--alerta` | `--erro` sobre `--erro-claro`, §4.3 | 5,75:1 |
| cinza | #E3E8E4 / #5E6B63 | #E3E8E4 / #5E6B63 | `--borda` / `--suave` | os dois tokens existem; o par não está na §4.3 | 4,50:1 (calculado) |

**Resultado: igual nos três lugares e nos tokens do manual.** Nenhuma combinação proibida da §4.4.

## 🟡 Corrigir antes do merge

**R1. Web × contrato: com filtro, recorte ou estado, a web mantém os cartões da aba com a marca; o contrato manda tirar os cartões e mostrar o `AVISO_CARTOES`.** (W1 + C2(b))
- **O contrato (`a36dfc1`) escolheu o `AVISO_CARTOES`:**
  - `.coord/contratos/relatorio.md:670` (`kpis_padrao`), `:792` (§10.7.6) e `:821` (D5): "os cartões da aba saem, e fica o aviso `AVISO_CARTOES`";
  - `.coord/contratos/tela-bc3.md:86` (§4.2) e `:268` (tabela do §9): "Aba com `kpis_padrao` e filtro, recorte ou estado → o `AVISO_CARTOES` no lugar dos cartões".
- **A web (`9716248`) faz o contrário:**
  - `web/app/main.py:390-397`: os `kpis_padrao` ficam e ganham "sem o filtro" ou "BAP inteira";
  - `web/tests/test_abas.py:561-575`, `:578-580` e `:893-897` exigem isso, e o `:894` exige `"Cartões sem filtro" not in h`;
  - `web/app/tabelas.py:198`: o `AVISO_CARTOES` ficou definido e sem uso. Só existe para o `tests/test_T0017_pacote_tres_farois.py:947-953`, que confere o texto do contrato.
- **Por que passou nos testes:** nenhum teste liga as duas pontas. A web testa o próprio comportamento, e o `test_T0017` confere só o texto da constante.
- **O que pesa na escolha:** a regra que a web segue é a do parecer de UX (`revisao-ux-geral.md`, l. 266: os números "ficam e ganham o detalhe 'sem o filtro', em vez de sumir"). O parecer do gerente (`R-20261127-001426-gerente-projetos`, l. 25 e 35) também pedia ao `engenheiro-software` para tirar o `AVISO_CARTOES` do §10.7.6.
- **Correção [SUPOSIÇÃO: vale a regra da UX e do gerente; o gerente decide]:**
  - `engenheiro-software`: nas 5 linhas acima, trocar o `AVISO_CARTOES` por "os cartões da aba ficam e ganham a marca 'sem o filtro' (filtro ou recorte) ou 'BAP inteira' (estado), também com `detalhe`", e tirar o `AVISO_CARTOES` do §10.7.6;
  - `modulo-web`: apagar o `tabelas.AVISO_CARTOES` (`tabelas.py:198`);
  - `testes`: trocar o `tests/test_T0017_pacote_tres_farois.py:947-953` pela regra nova.
- **Se valer o contrato:** a web implementa o aviso e reescreve os 3 testes citados.

**R2. Faróis e web: a tela mudou e não há print.**
- O selo `alerta` do `chip_tom` era vermelho cheio com texto branco (`#B42318`/`#FFFFFF`). Agora é fundo claro com texto vermelho (`#FDECEA`/`#B42318`). O `ok` também clareou. O SLA atrasado do Farol de Entregas fica bem menos forte, no PC e no site.
- Não achei print dessa mudança no pacote (`recados/anexos/T-0033/`).
- **Correção:** um PNG do Entregas no PC e na web, com os 4 tons (ok, atenção, alerta, cinza), para o `designer-ux` e o `design-de-marca` conferirem antes do merge (checklist e regra 10).

## 🟢 Sugestões (não bloqueiam)
- **Faróis, `bap_visual.py:1309-1313`:** o dicionário do `chip_tom` ainda usa hex soltos. Já existem as constantes `VERDE_ESCURO`, `VERMELHO`, `VERMELHO_CLARO`, `AMARELO_CLARO`, `CINZA_LINHA` e `SUAVE` (l. 65-78). Faltam `OK_CLARO` e `AMARELO_TEXTO`. Isso cabe na T-0047.
- **Testes:** nenhum teste confere que o `chip_tom` do PC é igual ao `tabelas.PALETA_TOM` e ao manual. O PC não tem teste de cor, e a web testa só `ok` e `alerta` (`test_abas.py:658-659`). Para isso, o `bap_visual` precisa expor a paleta numa constante, o que também cabe na T-0047.
- **Web:** nenhum teste fixa o `<title>` "· BAP AUTOPARTS" (manual §7).
- **Marca:** o par `--suave` sobre `--borda` (selo cinza) dá 4,50:1, no limite do AA. Vale o `design-de-marca` pôr o par na tabela §4.3 do manual.
- **Testes de `tests/` com cor antiga:** não há nenhum. O único hex antigo é `#B3261E`, em `tests/test_T0033_marca.py:141` (`SAEM_DO_SITE`). Essa é a lista das cores que o manual tira, então ela está certa.

## Conferências dos 3 branches novos
- **Segredos e dados pessoais:** não há.
- **Dado digitado e pastas congeladas:** fora do diff.
- **`bap_dados.VERSAO`:** continua 27.
- **Governança:** fora do diff.
- **Número do Diretor:** nenhuma conta mudou.
- **Donos:** `node scripts/coord.mjs verificar --por-commit origin/main..<branch>` deu OK nos três (contrato com 5 commits; web e faróis com 7 cada).

## O combinado: os 8 heads mesclados num branch local descartável
- **A mescla:** os 8 heads entraram por cima do `origin/main` `a32b610`, sem conflito. A ordem: #127 → rota → robô → contrato → #135 → web → faróis → testes.
- **Python:** 3.12.3, no venv do scratchpad (com `tkinter` e as dependências do CI).
- **Resultados:**
  - `python -m compileall -q .`: sem erro;
  - `pytest tests/`: **609 passed, 2 xpassed**;
  - `pytest web/tests`: **344 passed** (antes eram 343; o novo é o teste do W1);
  - `RELATORIOS/painel_diretor_hist.json` ficou intacto e não precisou de `git restore`;
  - os smokes não foram rodados.
- **Limpeza:** o branch descartável foi apagado. Nada foi alterado nem enviado.

## Ordem de merge
Não mudou: **#127 → rota → robô → contrato → #135 → web → faróis → testes.** Os faróis nunca entram antes da web. Se o R1 for pela regra da UX, o contrato, a web e o `testes` corrigem no mesmo lote, para o `test_T0017_pacote_tres_farois.py:947-953` não ficar vermelho.
