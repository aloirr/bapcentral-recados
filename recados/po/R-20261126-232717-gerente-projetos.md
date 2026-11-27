---
id: R-20261126-232717-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pergunta
prioridade: normal
tarefa: T-0033
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-26T23:27:17-04:00
---
# T-0033: simulação da revisão geral de todos os faróis (antes/depois) — aprovação

# T-0033: simulação da revisão geral de todos os faróis (marca, UX e redundância) — aprovação

É a primeira tarefa da migração (R-20261126-174334-alexandre), com o manual da marca aprovado (R-20261126-182227). Imagens ANTES (o site de hoje) e DEPOIS, com dados fictícios, em `recados/anexos/T-0033/sim/`:

| Imagem (antes- e depois-) | O que mudou |
|---|---|
| admin-pedidos-pedidos__pc1366 | logo inteiro da BAP AUTOPARTS na placa preta; faixa nas cores do manual, com texto branco legível; sem o botão "Cobrar no WhatsApp" (7 A); tabela de até 10 colunas, com o resto no popup; tabelas de baixo lado a lado, sem rolagem |
| admin-pedidos-pedidos__cel390 | celular: lista que abre (M3) |
| admin-entregas-entregas__pc1366 / pos-entregas-entregas__cel390 | Entregas sem rolagem para o lado, nos dois tamanhos |
| admin-inad-titulos__pc1366 / admin-inad-cobrar__pc1366 | Inadimplência: sem título e hora repetidos |
| admin-pedidos-solicitacao__pc1366 | Solicitação BAP com os nomes legíveis |
| dir-pedidos-resumo__pc1366 | o diretor só no Resumo |
| admin-metas-equipe__pc1920 | Metas na tela larga |
| pc-maquete-antes / pc-maquete-depois | PC (BAP Tools): "BAP AUTOPARTS" e as cores do manual. É uma maquete do cabeçalho e do Farol de Pedidos, porque a tela Tkinter não abre na nuvem |

## O que mais entra junto
- Os 31 achados de redundância (contagem que aparecia 3 vezes, avisos repetidos, CSS e regra duplicados): os de prioridade alta e média estão resolvidos.
- "BAP AUTOPARTS" em todos os materiais: mensagem do WhatsApp e e-mail da inadimplência (PR #127), telas do PC e e-mail da parcial, e-mail da rota, robô.
- 318 testes da web passam. Há um teste novo que garante que as cores do site são as do manual.

## Ainda em ajuste (não muda o que você vê nas imagens)
O designer-ux pediu 12 retoques antes do merge, sobretudo no celular:
- abas que quebram em 2 linhas;
- rótulos cortados;
- o aviso "Sem filtro por estado" que voltou à faixa do Visita;
- a ordem da coluna NF no Entregas.

Estão sendo corrigidos agora.

O Painel Executivo, a página inicial e Usuários ainda estão no visual antigo nas imagens. Eles mudam na T-0034, que vem a seguir.

## Decisão
1. Simulação da T-0033: (A) aprovada; os PRs entram depois dos 12 retoques e da revisão · (B) ajustar antes (diga o quê).
