# T-0036: medição da §15 (tela-bc3), no BC3 do `main` (T-0033)

Chromium (Playwright), deviceScaleFactor 2. PC = 1366×768; celular = 390×844. Pacote: `analista_fixture.pacote_coerente()`
(dados fictícios, 40 linhas por tabela, números que fecham entre si; a faixa sai das somas das tabelas). Perfil `analista`
nos 4 faróis e no menu; perfil `trade` na página inicial.

| Tela | Largura | Rolagem lateral da página (§15.1) | Rolagem lateral da tabela | A página rola (§15.2) | Altura da faixa | Números na faixa | Altura da barra das abas | Abas à vista | Colunas da grade (§15.4) |
|---|---|---|---|---|---|---|---|---|---|
| saldo (Pedido) | 1366 | 0 | 0 | não | 88 px | 4 | 44 px (1 linha) | 5 | 10 |
| saldo (Pedido) | 390 | 0 | 0 | lista (M3) | 187 px | 4 | 50 px | 3 + Mais | lista |
| markup (Pedido) | 1366 | 0 | 0 | não | 88 px | 6 | 44 px (1 linha) | 12 | 10 |
| markup (Pedido) | 390 | 0 | 0 | lista (M3) | 190 px | 6 | 50 px | 3 + Mais | lista |
| preco (Categoria) | 1366 | 0 | 0 | não | 88 px | 6 | 44 px (1 linha) | 6 | 10 |
| preco (Categoria) | 390 | 0 | 0 | não | 190 px | 6 | 50 px | 3 + Mais | lista |
| divergencias (Divergentes) | 1366 | 0 | 0 | não | 88 px | 6 | 44 px (1 linha) | 4 | 8 |
| divergencias (Divergentes) | 390 | 0 | 0 | lista (M3) | 187 px | 6 | 50 px | 3 + Mais | lista |
| menu do analista (Saldo, Resumo) | 1366 | 0 | — | não | 88 px | 4 | 44 px | 5 | — |
| menu do analista (☰ aberto) | 390 | 0 | — | não | 187 px | 4 | 50 px | 3 + Mais | — |
| início do trade | 1366 | 0 | — | não | sem faixa | 0 | — | — | — |
| início do trade | 390 | 0 | — | não | sem faixa | 0 | — | — | — |

- A faixa tem 88 px em todas as telas do PC (a mesma altura do `main`, §15.3). O 7º número do Markup e das Divergências fica no Resumo.
- O Markup (12 abas) cabe numa linha a 1366, com a busca em ícone.
- No celular, a página rola só pela lista que abre (M3, §7.4 do contrato e §8).

## Ajustes da revisão de UX e marca (27/11/2026)

PNGs refeitos (saldo, markup, preço, divergências, menu do analista e início do trade, PC e celular), com o relógio do
servidor em 24/11/2026 09:00 de Manaus (o dia do pacote; sem isso a faixa mostra o selo "Desatualizado"). A tabela acima
já traz as medidas novas.

- Saldo (Pedido a pedido e grupos): o % sobre a tabela virou "DESC. S/ TABELA"; o valor em reais segue "DESC. COMERCIAL".
  No Markup o "% DESC." também é "DESC. S/ TABELA"; no Preço o "VAR. FAT. R$" virou "DIF. FAT." (ao lado de "VAR. FAT.").
  Teste: nenhuma tabela do Analista fica com dois rótulos de mesma base.
- Menu: o grupo do próprio perfil abre a barra (analista: "Analista Comercial" logo abaixo de "Diretoria"; trade: "Trade").
  Os outros perfis seguem a ordem de sempre.
- Faixa no celular: o valor não quebra linha (`white-space:nowrap`); valor com mais de 9 caracteres ("R$ 1.353.501") sai
  em 15 px. Medido: nenhum valor passa da sua coluna a 390 px. "Vendedor diferente" = "Vend. dif.".
- Divergências no celular: o selo da linha usa o rótulo curto (Vend. dif. / Sem vendedor / Fora da base); o texto inteiro
  aparece no detalhe aberto.
- Início do trade: título da aba "Início" e a frase "Os faróis do Trade Marketing ainda não estão no site."

## Redundâncias da revisão (RD-0003 a RD-0007, 27/11/2026)

PNGs refeitos só do início do trade (PC 1366 e celular 390, deviceScaleFactor 2; rolagem lateral 0 nos dois).

- Início do trade: sem a faixa com "BAP Central" (o nome já está na marca da barra); fica só a frase. O aviso
  "Ainda não chegou nenhum pacote do PC" sai pela flag `sem_pacote_ok` do `base.html`, não mais pelo nome do farol.
