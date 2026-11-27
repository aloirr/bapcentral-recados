# Revisão de código — T-0053 (RN-GER-019), branch `modulo-farois/T-0053-cadastro-do-pedido`

- Head revisado: **b56f1211191c697b789f530e6c403787b6f60047** (sem PR). Commit novo = revisão nova.
- Escopo: só `relatorios_nucleo.py` (+158/−32). Base do diff: `85bc589` (a branch está 3 commits atrás de `origin/main` 6ebdb6f; nenhum deles toca `relatorios_nucleo.py` nem `tests/`).
- Método: leitura do diff, RN-GER-019 de `origin/gerente-projetos/T-0053-regras`, testes da função pura e comparação base × head de 7 relatórios (`farol_pedidos`, `pedidos_em_aberto`, `pedidos_excluidos`, `entregas`, `fretes`, `devolucoes`, `saldo_desconto`) nas bases congeladas, com hoje = 27/11/2026.

## Parecer: NÃO APROVADO (2 🔴, 3 🟡, 4 🟢)

### 🔴 bloqueia
1. **`relatorios_nucleo.py:8145-8148` (fretes) e `:7337-7338` (entregas antigas): a loja não identificada fica com cidade vazia, e `bd.e_frete("")` dá False. A nota vira LOCAL e sai do Farol de Fretes.** Nas bases congeladas, **21 NFs (R$ 280.318) saem**:
   - Fretes "Notas com frete": 661 → 641; R$ 3.255.436 → 2.976.438; "% do faturado" 65% → 60%; frete estimado R$ 162.726 → 148.776.
   - Por estado: Belém 264 → 248, São Luís 258 → 253, Manaus 12 → 13 (este +1 é a correção legítima: a loja certa tem cidade com frete).
   - Entregas: cartão "Frete" R$ 162.789 → 148.839 (Belém e São Luís); 22 linhas trocam FRETE → LOCAL.

   A RN-GER-019 diz "os cartões e o filtro por estado não mudam". Além disso, o pedido era o Farol de Pedidos, e "sem cidade" passou a valer como "sem frete", o que afirma um dado que não se sabe.
   **Correção:** quando a loja não é identificada, a classificação frete/local não pode cair em LOCAL só por falta de cidade. Opções: (a) manter `ctx.cliente(cod)` só para `e_frete` em `fretes`/`entregas`; (b) frete se todas as lojas do código na UF (ou do código) forem frete. A decisão de regra é do po. Os totais de Fretes e Entregas devem voltar a 661 / R$ 3.255.436, ou a diferença deve ser explicada linha a linha.
2. **Sem teste da RN-GER-019** (regra inegociável 2; checklist "o check novo cobre a mudança"). O commit não traz nenhum `test_RN_GER_019_*`, e não há branch de testes da T-0053 (`tests/` é do `testes`). Não fazer o merge sem o lote do `testes` cobrindo:
   - os 5 casos de borda de `cadastro_do_pedido`;
   - `analise_credito` com `credito_apurado False` → `CREDITO_NAO_APURADO`, entrando no recorte "Crédito a analisar" (`:2312`);
   - a igualdade dos cartões e dos totais por filial (Farol de Pedidos, Fretes, Entregas, Excluídos) entre a base e o head.

### 🟡 corrigir antes do merge
1. **`relatorios_nucleo.py:1807` (Pedidos excluídos, cartão "Clientes")**: conta `len({l[5]})`, ou seja, o nome mostrado. Agora o mesmo código aparece com dois nomes (loja da filial × "(loja não identificada)"). Resultado: **399 → 400** nas bases congeladas. Isso é um agregado por cliente que mudou por engano. Contar por código (`i0["cliente"]`), não pelo texto. Conferir também as tabelas "Por cliente" de excluídos e de devoluções (`:8017`, chave `nome_cliente(cod, fil)`): um código pode se dividir em duas linhas. Nas bases congeladas o número de linhas não mudou, mas a chave está frágil.
2. **`relatorios_nucleo.py:1507` (`detalhe_pedido`, subtítulo)**: continua `ctx.nome_cliente(i0['cliente'])`, sem a filial. Na consulta de pedido, o subtítulo mostra o nome da outra loja, e o campo "Cliente" (`:1451`) mostra a loja da filial. É o mesmo defeito da T-0053, na mesma tela. Passar `i0["filial"]`.
3. **`relatorios_nucleo.py:751` (`HERDA_LOJA_UNICA`)**: o comentário ainda diz "[SUPOSICAO] do modulo-farois", mas a RN-GER-019 já fixou a regra ("código com uma loja só usa essa loja"). Além disso, a constante é uma chave que nunca muda. Tirar a constante e o ramo condicional, ou ao menos o rótulo de suposição. A regra fica na RN, não numa chave do código.

### 🟢 sugestões
1. `pedidos_faturados` (`:1654`, `cli = ctx.cliente(cod)`, `:1721`) e `farol_markup` (`:10497`) são visões por pedido/NF e ainda usam a loja de maior limite. Fica inconsistente com as outras visões. Ou entram na RN-GER-019 (cuidado com o `e_frete` de `:1717`, que tem o mesmo risco do 🔴1), ou o po registra que ficam fora.
2. `cadastro_do_pedido` (`:793-795`): sem nenhuma loja na UF, o nome é testado em **todas** as lojas do código. A RN fala em "lojas dessa UF". O comportamento é razoável, mas precisa constar na RN (po) ou no teste.
3. `lojas_do_codigo` (`:1107-1115`): o fallback monta o mesmo dict do laço. Extrair um `_loja_do_cadastro(d, g)` evita as duas cópias.
4. `:2383`: linha com mais de 79 colunas (`ctx.filial(it["filial"]), it["p_venda"] * falta ...`), fora do padrão do arquivo.

## Itens pedidos pelo gerente
1. **Função pura `cadastro_do_pedido` (`:754`)**: conferida com dicts sintéticos (sem dado pessoal).
   - Uma loja na UF: escolhe essa loja; com saldo, crédito apurado. Sem saldo (loja que não é a de maior limite): "Crédito não apurado", conforme a RN.
   - Nenhuma loja na UF (2 lojas): UF da filial, sem cidade, limite nem saldo; nome = "(loja não identificada)", ou o nome comum quando é igual em todas.
   - Várias lojas na UF com nomes diferentes: "(loja não identificada)".
   - Loja única com UF diferente: herda a loja (UF dela, não a da filial), conforme a RN.
   - Código sem cadastro: a pura devolve não identificada; o `ctx.cadastro_do_pedido` devolve `{}`, o que mantém o comportamento antigo (fora da base / "Sem Limite").
   - Filial desconhecida: UF vazia; com 1 loja, herda; com 2 ou mais, não identificada.
   - Filial com prefixo "4" funciona (`uf_da_filial` pega os 7 últimos dígitos).
   - UF em minúscula no cadastro é normalizada.
2. **Os ~12 lugares**:
   - Farol de Pedidos: cartões, total e cartões por filial iguais. Mudam só as células UF (18), CIDADE (55), RAZÃO (45), FANTASIA (51), LIMITE (51), DISP./ATRASO (44); 38 linhas "(loja não identificada)": 16 entregues, 16 excluídas, 6 devolvidas.
   - Pedidos em aberto: idêntico (os 10 VEA congelados estão todos identificados).
   - Saldo de desconto e devoluções: cartões e totais iguais; só nomes e cidades.
   - Excluídos: cartão "Clientes" mudou (🟡1).
   - Fretes e entregas: totais mudaram (🔴1).
   - Carteira, positivação e inadimplência não foram tocadas (não chamam `cliente_do_pedido`).
3. **"Crédito não apurado"**:
   - Entra em "Crédito a analisar" (`:2312`, `!= CREDITO_OK`), no tom "atencao" (`:2090`), no alerta de pendência de crédito do painel (`:19116`), na parcial (`:11632`, via `analise_credito`) e em Pedidos em aberto (`:1565`, em caixa alta: "CRÉDITO NÃO APURADO", a mesma convenção caixa-alta daquela tela).
   - A parcial do vendedor (`:16292-16295`) trata qualquer valor diferente de "OK" com `.lower()` → "crédito não apurado". Não quebra.
   - Grep no repositório inteiro (PC, `bap_automation.py`, `web/`, `scripts/`): nenhum consumidor compara com "Com Limite"/"Sem Limite"/"SEM LIMITE" fixos fora de `relatorios_nucleo.py`. A web só declara a coluna "ANÁLISE CRÉDITO" (`web/app/tabelas.py:210`, `:1170`); a fixture usa valores próprios. Sem quebra.
4. **Desempenho**: há índice. `_lojas_idx` é montado uma vez por `Contexto`, a partir de `protheus_lojas` (4.459 lojas). Depois, a consulta por código é um dict. `cadastro_do_pedido` para os 7.985 itens custa 0,05 s. O(n), sem risco de O(n²). Farol de Pedidos: 0,56 s na base × 0,48 s no head.
5. **Cache**: `bap_dados.VERSAO = 27`. `bap_dados.py` não foi tocado, e a forma do dado em cache não mudou (só leitura de `protheus_lojas` e `clientes`, que já existiam). Não precisa de marca nova.
6. **Segredos e dados pessoais**: nenhum no diff. Os testes desta revisão usaram dicts sintéticos; nenhum nome, CNPJ ou contato aparece aqui.
7. **Dados digitados** (`_EDICOES_POS_VENDA`, `_NCC`, `_GARANTIAS`, `_AUTORIZACOES`, os 3 configs): intocados. `bap_dados.py` está intocado.
8. `compileall` OK. `node scripts/coord.mjs verificar --base origin/main` no head: OK, nenhuma violação (1 arquivo, dono `modulo-farois`).
9. **Tela**: o diff muda o texto visível (UF, nome, "(loja não identificada)", "Crédito não apurado"). Pela regra 10, a simulação em PNG/PDF tem de existir antes do PR. Há `anexos/T-0053/sim/` (c4dd7a7). Esta revisão não conferiu as imagens; isso fica para o `designer-ux`.

## Testes no head (`pytest tests/ -q`, xvfb, /usr/bin/python3.12)
- **1.005 passed, 10 skipped, 2 xpassed, 0 failed.** Rodado arquivo por arquivo, porque a suíte inteira numa só chamada foi derrubada por tempo, com a CPU dividida com outras sessões.
  - O `test_T0024_lote2_robo_web.py` foi interrompido na 1ª passada e repetido sozinho: 6 passed, 2 skipped.
  - Nenhuma falha nova. A suíte não tem nenhum teste da RN-GER-019 (🔴2): verde aqui não prova a mudança.
- Árvore limpa depois dos testes (`git status` vazio no worktree do head). `RELATORIOS/painel_diretor_hist.json` intocado.
- Comparação base × head: scripts e saídas em `/tmp/claude-0/-home-user/4f3da797-8ad2-51e5-b58d-a720ae0afc4c/scratchpad/T-0053/` (`rev_dump.py`, `rev_cmp.py`, `rev_cmp2.py`, `rev_fretes.py`). Os scripts só leem as bases congeladas e não ficam no repositório.

## Para a próxima revisão (commit novo)
- Os totais de Fretes e Entregas voltam aos da base (661 notas / R$ 3.255.436; frete R$ 162.789), ou a diferença vem explicada e aprovada pelo po.
- O cartão "Clientes" de excluídos volta a 399.
- O teste do `testes` (`test_RN_GER_019_*`) cobre os casos de borda e a igualdade dos cartões por filial.

---

# Reteste no head b4006e7a76936b57f4b317e262da570cb44ca007 (delta desde b56f121)

- Delta: só `relatorios_nucleo.py` (+25/−28). Base do diff ainda `85bc589`.
- RN-GER-019 lida no head atual de `origin/gerente-projetos/T-0053-regras`: o escopo é a família do Farol de Pedidos, com "Saldo Não Apurado" e a fantasia igual ao nome.

## Parecer: SEM 🔴 de código e SEM 🟡. Merge segue bloqueado só pelo 🔴2 (teste da RN-GER-019 com o `testes`, branch `testes/T-0053-cadastro-do-pedido`, ainda a revisar)

### Itens do parecer anterior
- **🔴1 Fretes/Entregas: resolvido.** Os `rev_cmp*.py` comparam a base 85bc589 com o head b4006e7 (bases congeladas, hoje = 27/11/2026). Fretes, Entregas, Devoluções e Saldo de desconto ficaram **idênticos ao main**: mesmas linhas, mesmos cartões, mesmos cartões por filial, nenhuma célula diferente.
  - Fretes: 661 notas, R$ 3.255.436, frete R$ 162.726. Nenhuma nota saiu ou entrou.
  - Entregas: cartão Frete R$ 162.789.
  - Nos hunks do `git diff 85bc589 b4006e7` sobraram só `cadastro_do_pedido`, `Contexto`, `detalhe_pedido`, `pedidos_em_aberto`, `pedidos_excluidos`, `analise_credito`/`CREDITO_*`, `farol_pedidos` e `_pedidos_abertos_da_parcial`. `_analitico_produto`, `_historico_de_compra`, `entregas`, `devolucoes`, `fretes` e `saldo_desconto` voltaram ao main.
- **🔴2 teste RN-GER-019: em aberto.** Está com o `testes`; vou revisar quando publicar.
- **🟡1 cartão "Clientes" (`:1805`): resolvido.** Conta pelo código (`split(" - ")[0]` de `nome_cliente`), e dá **399 = main**. Os cartões de Excluídos ficaram todos iguais.
- **🟡2 subtítulo da consulta (`:1505`): resolvido.** Passa `i0['filial']`.
- **🟡3 `HERDA_LOJA_UNICA`: resolvido.** A constante saiu (`hasattr` dá False), e o ramo de loja única ficou incondicional, conforme a RN.
- **🟢 do parecer anterior:**
  - O 1 (faturados e markup) ficou fora por decisão da RN ("os outros faróis seguem como antes").
  - O 2 (nome entre todas as lojas) entrou na RN.
  - O 3 (fallback duplicado em `lojas_do_codigo`) continua como sugestão.
  - O 4 (`:2383`) saiu com a reversão do analítico.

### Números no head (família do Farol de Pedidos)
- **Farol de Pedidos**: 2.216 linhas. Cartões, total e cartões por filial iguais ao main.
  - Mudam só as células UF (18), CIDADE (55), RAZÃO (45), FANTASIA (51), LIMITE (51), DISP./ATRASO (44).
  - 38 linhas com "(loja não identificada)": 16 entregues, 16 excluídas, 6 devolvidas.
  - "ANÁLISE CRÉDITO" dos 10 em aberto igual ao main: 4 Com Limite, 3 Sem Limite, 2 em Atraso, 1 Parcial. Nenhum VEA congelado cai em "Saldo Não Apurado".
- **Pedidos em aberto**: idêntico ao main (10 pedidos, 27 itens faltantes).
- **Excluídos**: 830 linhas, cartões iguais (399 clientes). Mudam CIDADE (34), UF (18) e CLIENTE (31). Na tabela "Por cliente", 603 linhas, com 14 nomes trocados.

### Função pura (dicts sintéticos)
- Os mesmos 8 casos do parecer anterior batem com a RN nova.
- Sem loja única, `fantasia = nome`: "(loja não identificada)" ou o nome comum.
- Crédito sem saldo, ou sem loja identificada: `analise_credito` dá **"Saldo Não Apurado"**. Em Pedidos em aberto sai em caixa alta, "SALDO NÃO APURADO". A parcial do vendedor (`.lower()`) mostra "saldo não apurado".
- Nenhum resto de "Crédito não apurado" no código. O grep dos consumidores continua sem comparação de string fixa fora de `relatorios_nucleo.py`.

### Conferências
- `bap_dados.VERSAO = 27`; `bap_dados.py` intocado; sem marca de cache nova (não precisa).
- Nenhum segredo nem dado pessoal no delta. Dados digitados e configs intocados.
- `compileall` OK. `node scripts/coord.mjs verificar --base origin/main` OK (1 arquivo, dono `modulo-farois`).
- `pytest tests/ -q` com xvfb, arquivo por arquivo: **1.005 passed, 10 skipped, 2 xpassed, 0 failed**. Árvore limpa depois; `RELATORIOS/painel_diretor_hist.json` intocado.

### 🟢 novas (não bloqueiam)
1. `:769` e `:1505` passam de 79 colunas. As linhas `:807`, `:816`, `:841` e `:1083` já passavam no main.
2. Excluídos (`:1805`): a contagem por código depende do formato "cod - nome" do `nome_cliente`. Um `{i0["cliente"]}` guardado na linha seria mais robusto. O resultado de hoje está certo.
