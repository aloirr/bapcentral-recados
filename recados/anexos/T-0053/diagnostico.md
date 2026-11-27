# Diagnóstico T-0053 (R-20261127-095026-alexandre): "cliente RR-1" com muitos pedidos no Farol de Pedidos

Só leitura. Bases congeladas de `RELATORIOS/` (formato, não os dados de 27/11). Sem dado pessoal.

## 1. De onde vêm as linhas
- Fonte única: `TABELA_BAP.xlsx`, aba `ftPedidos` (robô: Relatório Movimentação_Protheus_BAP, `bap_automation.py:80`). Lida em `bap_dados.py:568 _ler_pedidos`: uma linha da aba = um ITEM.
- Em aberto (TIPO=VEA), o "número do pedido" é `NUM_PEDIDO` (cai em `D2_DOC` só se vazio) (`bap_dados.py:600`). Na base congelada nenhum VEA tem `NUM_PEDIDO` vazio (0 de 36).
- `relatorios_nucleo.py:1224 _pedidos` agrupa os itens por (filial, pedido) para VEA/EXC e por (filial, NF, série) para VND/DEV. `farol_pedidos` (1794) cria UMA LINHA POR PEDIDO (1857-1869), com valor e volume somados dos itens.
- Não há merge. SOLICITACAO_BAP aparece só no rótulo de fonte (1805) e na área de Solicitação. O farol não a cruza. `ftPedidos` e TABELA_BAP são a mesma coisa: "comparar com a TABELA BAP" = conferir as linhas VEA da `ftPedidos`, pelo par `D2_FILIAL` + `NUM_PEDIDO`. A chave existe (`CHAVE_FIL_PED`), mas na base congelada o valor sai quase vazio (`0101002|0`). Use `NUM_PEDIDO`.
- Conclusão: o farol NÃO multiplica linhas. Se há ~30 linhas do cliente RR-1, há ~30 números de pedido VEA distintos na ftPedidos para ele. Hipóteses (b) e (c) derrubadas pelo código.

## 2. Hipóteses
- (a) CONFIRMADA COMO PADRÃO REAL na base congelada: o ERP cria rajadas de pedidos distintos, quase idênticos, em poucos segundos. Em `ftPedidos` (EXC), de 850 pedidos excluídos, 12 combinações cliente-dia têm 4 ou mais pedidos. Exemplos:
  - cliente X-1 (filial MA, 04/11): 13 pedidos entre 21:43:18 e 21:43:27, 32 itens, 3 produtos distintos, mesmo vendedor, números 000582 a 000598 com saltos (os saltos são de outros clientes);
  - cliente X-2: 7 pedidos com o mesmo conjunto de itens (produto + quantidade) em 16 s;
  - cliente X-3: 6 pedidos idênticos em 6 s;
  - cliente X-4: 7 pedidos com 1 conjunto de itens em 16 s.
  Em 7 das 12 rajadas o conjunto de itens é o mesmo em todos os pedidos (provável reenvio ou duplicação na digitação ou integração).
  - Os mesmos clusters aparecem em `SOLICITACAO_BAP.xlsx` › `DETALHADO_PEDIDO` (cliente X-1: 14 números, um a mais que os 13 do EXC). Isso mostra que eles chegaram a ficar EM ABERTO (VEA) antes de serem excluídos.
  - Filial RR (0101004): mediana de 1 pedido/dia e máximo de 3 na base congelada. Quase 43 números num dia é fora do normal. Isso aponta para criação em lote, não para pedidos comerciais independentes.
- (d) bonificação/troca/garantia: a ftPedidos tem `TIPO` (VND, VEA, EXC, DEV, TRF). O loader descarta TRF (4.778 linhas) e só lê VND, VEA, EXC e DEV. Não há coluna de natureza do pedido (bonificação etc.) no loader; não dá para provar nem derrubar sem o pacote real.
- Padrão do print (desconto 0,0%, SLA 1, 100% atendido): as linhas de EXC das rajadas têm desconto fixo e % atendido 0. No VEA das rajadas a cobertura 100% é possível; não dá para afirmar.
- Duplicidade de linha (mesmo pedido+produto repetido): 26 casos em EXC e 7 em VND. Isso é item repetido, não pedido repetido.

## 3. Cartões do topo (relatorios_nucleo.py:1930 cartoes_bi)
- Todos contam linhas do farol (1 linha = 1 pedido): "Pedidos" = `len(ls)` (1940), "R$" = soma do valor (1941), "Faturar" = linhas com % atendido ≥ 99,99 (1934), "Volume" = soma de unidades (1944).
- Se os ~30 pedidos forem duplicatas, os quatro cartões ficam inflados na mesma proporção. Um cartão não é maior que a tabela: a tabela e os cartões usam as mesmas linhas, já sem "fora da base" (RN-GER-013).
- Aba Pedidos: 31 linhas, ~30 do cliente RR-1. Então os cartões estão dominados por esse cliente.

## 4. Outros clientes
- Na base congelada, 12 de 850 pedidos EXC são de rajadas; em VND, 83 cliente-dias têm 2+ pedidos (sem rajada). Hoje o farol não detecta nem avisa. Qualquer cliente pode ter o problema.

## 5. O que não dá para confirmar sem o pacote de 27/11 09h39
- Se os pedidos 000241 a 000283 do cliente RR-1 têm o mesmo conjunto de itens (produto + quantidade) e horas em poucos segundos (rajada) ou se são pedidos legítimos pequenos.
- Se são de tipo/natureza diferente (bonificação etc.): coluna que o ERP não traz hoje.
- Como confirmar: o robô ou o Alexandre listam, da `ftPedidos` de 27/11 09h39, para o cliente RR-1 (código mascarado) com TIPO=VEA: `NUM_PEDIDO`, `C5_XHORA`, `D2_COD`, `D2_QUANT`, `VALOR TOTAL`, `C5_VEND1`. A consulta no Protheus (SC5) diria se os 43 números existem como pedido separado ou se o relatório os quebra. Uma conta simples: pedidos distintos / conjuntos de itens distintos / janela de hora.

## 6. Correção proposta (não implementada)
- Se for rajada de duplicatas: o defeito é de dado (digitação ou integração), não do farol. No farol, adicionar o aviso na área de Alertas (nunca pintar a linha): "N pedidos do mesmo cliente com os mesmos itens em X minutos".
- Função pura `pedidos_suspeitos_de_duplicidade(itens_por_pedido, janela_s=...)` em `relatorios_nucleo.py` (dono: modulo-farois), com teste escrito antes (`test_RN_PED_001_...`) e a nova RN em `docs/produto/03-regras.md` (nome sugerido RN-GER-014; dono do doc: po/engenheiro-software). Decisão de negócio pendente do Alexandre: continuar contando os suspeitos nos cartões ou tirá-los (hoje contam).
- Pedido de dado ao engenheiro-dados: coluna de natureza do pedido (bonificação/troca) e identificador de origem (app, API), se existirem no Protheus.
- Simulação em PNG antes de qualquer mudança de tela (regra 10).

---
# COMPLEMENTO (R-20261127-095245-alexandre): visão RR mostra 1 pedido, visão BAP mostra 000241 a 000283

Só leitura. A nova hipótese (pedidos de outra filial com nome e UF do cliente RR-1 por junção só pelo código) é a principal e é consistente com o código. A confirmação final depende do pacote real (item 5).

## 1. Qual visão bate com a TABELA BAP
- Chave de cada pedido na TABELA BAP: `D2_FILIAL` + `NUM_PEDIDO` (+ `D2_CLIENTE`). O farol agrupa por (filial, pedido) (`relatorios_nucleo.py:1233`) e grava a FILIAL em cada linha (`:1852`, coluna FILIAL).
- O recorte RR do site usa a coluna FILIAL da linha: `bap_automation.py:7581` (`("pv_pedidos","Pedidos"): ("FILIAL","filial")`) e `:8184` (`uf_linhas` pelo nome da filial). A visão RR respeita a regra "estado = filial da nota" e bate com a TABELA BAP.
- A visão BAP mostra todas as linhas. O nome e a UF vêm do cadastro (item 2). Se o print mostra UF=RR nos pedidos 000241 a 000283, essa UF NÃO é a filial do pedido.
- Para provar: no pacote de 27/11 09h39, listar para 000241 a 000283 o par (`D2_FILIAL`, `D2_CLIENTE`). Se `D2_FILIAL` não for 0101004, a hipótese está provada. A visão RR com 1 pedido (000109) já indica isso, porque o filtro é por filial.

## 2. Causa, com arquivo:linha
- `D2_LOJA` NÃO existe na `ftPedidos` (cabeçalho com 45 colunas, conferido). O pedido só traz o código `D2_CLIENTE`, sem a loja (`bap_dados.py:612`, `cliente: cod6(g(r,"D2_CLIENTE"))`).
- O cadastro é indexado só pelo código: `_ler_clientes_tabela` (`bap_dados.py:~700-715`) guarda uma loja por código, a de maior limite ("o codigo tem varias lojas: fica a de maior limite"). `ctx.cliente(cod)` (`relatorios_nucleo.py:1019-1030`) e `ctx.tabela["clientes"].get(cod)` devolvem esse registro único.
- `farol_pedidos.linha()` (`relatorios_nucleo.py:1824-1845`) monta nome, fantasia, UF e cidade, limite, saldo e atraso desse registro único. A coluna FILIAL vem do pedido (`:1852`).
- Efeito: um pedido de uma loja do mesmo código, ou feito numa filial diferente da do cadastro, aparece com o nome, a UF e o limite da loja de maior limite (ex.: RR). O filtro por estado usa a filial e o tira. É a mesma linha, vista por duas chaves.
- O limite e o saldo da linha também ficam da loja errada, e a análise de crédito (`analise_credito`, `:1864`) usa esse limite.

## 3. Cartões do topo
- Pedidos, R$, Faturar e Volume somam linhas por (filial, pedido) (`:1930-1945`). Não dependem do cadastro. Na visão BAP, os pedidos contam todos, mesmo com UF/nome trocados. O total está certo (as linhas existem na TABELA BAP).
- O que fica errado é a atribuição: o cliente RR-1 parece ter os pedidos, e "Crédito a analisar" (recorte em `:2091`) usa o limite da loja errada.
- Por estado (RR): o cartão e as linhas saem pela filial (`bap_automation.py:7581`), então estão corretos. Os cartões por estado de AM, MA, etc. incluem esses pedidos corretamente. Só a visão BAP, na coluna UF/CLIENTE, mostra o cliente errado.
- Se os pedidos forem duplicatas (diagnóstico acima), os cartões ficam inflados na filial de origem. As duas hipóteses podem valer ao mesmo tempo.

## 4. Quantos clientes e filiais (bases congeladas, contagem, sem nomes)
- `dClientesBap` (sem linhas apagadas): 4.154 códigos; 172 códigos com mais de 1 loja; destes, 58 com UF diferente entre as lojas e 106 com nome diferente. 0 códigos com filial de cadastro diferente.
- `ftPedidos` (VEA+EXC+VND, pedidos únicos por filial+pedido+código): 583 clientes; 15 compraram em mais de uma UF de filial.
- Pedidos cuja filial (UF) é diferente da UF de qualquer loja do cadastro: 40 EXC e 8 VND; mais 4 EXC e 9 VND só com a loja de maior limite diferente. 36 pedidos (19 EXC e 17 VND) são de códigos com lojas em UF distinta (6 códigos). 5 EXC sem cadastro. Nos 8 VEA da base congelada: 0.
- Ou seja, o problema não é só do cliente RR-1; o padrão existe em dezenas de pedidos da base congelada e o farol não avisa.

## 5. Não confirmado sem o pacote de 27/11 09h39
- Quais `D2_FILIAL` e `D2_CLIENTE` têm 000241 a 000283. Se é um código só ou vários, e quantas lojas tem o código na `dClientesBap` (A1_COD com várias A1_LOJA, A1_EST).
- Se o cliente é uma loja do grupo comprando em várias filiais (um código, muitas filiais, rajada em um dia).
- Como confirmar: o Alexandre ou o robô mostram, para esses pedidos, FILIAL, `D2_CLIENTE`, e para o código no cadastro: A1_LOJA, A1_EST, A1_MUN, A1_FILIAL. Sem nome, CNPJ ou contato.

## 6. Correção proposta (não implementada)
- Função pura `cadastro_do_pedido(filial, cod_cliente, lojas_do_codigo)` em `relatorios_nucleo.py` (dono: modulo-farois). Escolhe a loja do código cuja UF é a da filial do pedido (`uf_da_filial`, `:112`); sem casamento, devolve vazio e a coluna mostra "(loja não identificada)", sem herdar UF, limite ou saldo de outra loja. Usada em `farol_pedidos.linha()` para nome, UF, cidade e limite.
- RN nova, `docs/produto/03-regras.md` [SUPOSIÇÃO: RN-GER-014, o número depende do que o po reservar; a duplicidade do bloco acima pode ser RN-GER-015]: "o pedido herda do cadastro só a loja cuja UF é a da filial da nota; sem casar, não herda UF, limite nem saldo".
- Teste antes: `test_RN_GER_014_pedido_nao_herda_uf_de_outra_loja`, com um código de 2 lojas (UF AM e RR) e pedidos em filiais AM e RR, e `test_RN_GER_014_codigo_sem_loja_da_filial`. Fixtures sintéticas, sem dado pessoal.
- Dados: pedido ao `engenheiro-dados` para o robô incluir `D2_LOJA` na `ftPedidos` (hoje ausente) e a chave (cod, loja) no cadastro; é o único jeito de casar a loja certa sem adivinhar pela UF. Dono de `bap_dados.py`: conferir com `node scripts/coord.mjs dono bap_dados.py`.
- Simulação em PNG antes de qualquer mudança visível (regra 10). A coluna "UF" do farol deve mostrar a UF da filial da nota (regra "estado = filial da nota").
