---
id: R-20261126-180502-gerente-projetos
de: gerente-projetos
para: [po]
cc: [alexandre]
tipo: pergunta
prioridade: normal
tarefa: T-0032
responde_a: null
encerra: false
contrato: null
criado_em: 2026-11-26T18:05:02-04:00
---
# T-0032: simulação da correção do celular (PR #126) antes do merge

# T-0032: correção do celular (PR #126) — simulação antes do merge

O #124 entrou no ar sem simulação. No celular (390 px), o botão "Parcial Pedidos" empurrava a página para 448 px e cortava o Exportar. O PR #126 corrige: os botões do cabeçalho quebram linha, e o Exportar fica à direita, com o menu inteiro na tela.

Imagens com dados fictícios, em `recados/anexos/T-0032/pr126/`:
- `pedidos-390.png` e `pedidos-360.png`: Farol de Pedidos com o menu do Exportar aberto, inteiro na tela;
- `entregas-390.png` e `visita-390.png`: o mesmo em Entregas e Visita;
- `pedidos-1366.png`: o PC não muda;
- `antes-menu-entregas-390.png`: a primeira versão da correção, barrada pelo revisor porque o menu abria cortado.

Conferências:
- revisor-codigo aprovou no head 986c6af;
- CI verde;
- só `web/app/static/estilo.css`, no bloco do celular.

## Decisão
1. PR #126: (A) pode fazer o merge (corrige o que está no ar) · (B) ajustar antes.
