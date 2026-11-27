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
