---
id: R-20261127-014046-gerente-projetos
de: gerente-projetos
para: [po]
cc: []
tipo: pergunta
prioridade: normal
tarefa: T-0034
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-27T01:40:46-04:00
---
# Simulação da T-0034 (página inicial, Painel, Login, Senha, Usuários, Parcial) para aprovar por delegação + P4 da T-0025

Simulação da T-0034 para aprovação por delegação (R-20261127-013010-alexandre). As imagens usam dados fictícios e estão em `recados/anexos/T-0034/sim/`:

| Arquivo | O que mostra |
|---|---|
| 0 | Painel antes, para comparar |
| 1 | Painel do diretor no PC: os 3 números na faixa, com a data e "13 de 19 DU"; do 4º cartão em diante, o número fica no cartão |
| 2 | O mesmo Painel com a área dos cartões rolada até o fim (Ticket, Peças, Markup…) |
| 3 | Aba Faturamento: gráfico e tabelas lado a lado, cada caixa com rolagem por dentro; a página não rola |
| 4 | Painel no celular |
| 5 | Pré-venda: ao abrir o site, cai direto no Farol de Pedidos (decisão 2 A) |
| 6 | Login no visual novo |
| 7 | Trocar senha |
| 8 | Usuários, com um botão principal só, e a confirmação "Desativar o usuário …?" |
| 9 | Parcial sem a barra lateral repetida |

## Condições da delegação
- **PNGs no PC e no celular com dados fictícios:** sim.
- **designer-ux e design-de-marca sem 🔴:** sim. Os pareceres estão em `recados/anexos/T-0034/`: conferência final de UX, marca e revisão de código.
- **Cores e logo do manual:** sim. A fonte Inter agora vem do próprio site, com o arquivo hospedado.
- **Nenhum documento, telefone ou e-mail:** sim.
- **Os números batem com o PC:** os cartões são os do PC, os mesmos 10, 10 e 6. Há um teste que prova que do 4º ao 10º cartão o valor aparece.

## O que muda além da tela
- **Faixa dos faróis:** em todos, a faixa passa a mostrar só a data. O texto completo aparece ao passar o mouse.
- **Versão do site:** 0.5.0.

Ainda falta a revisão de código do último ajuste de marca. Os PRs entram depois dos da T-0033.

## Pergunta P4 ao Alexandre (T-0025; não segura nada)
O TOTAL A PAGAR das Campanhas é em pontos, não em R$: é a soma das colunas PTS VÁLIDOS e PTS RELÂMPAGO, que o vendedor vê. Escondida só a coluna do total, o vendedor ainda refaz a conta somando as duas.
- (A) Os pontos continuam visíveis para vendas; sai só o TOTAL A PAGAR. É o que está no desenho, para o vendedor acompanhar a campanha.
- (B) Para vendas, saem também PTS VÁLIDOS e PTS RELÂMPAGO.

Recomendo A, mas é decisão dele: o efeito é sobre o que o vendedor sabe do próprio pagamento.
