# T-0052: revisão de UX (designer-ux)

- Branch `modulo-web/T-0052-painel-cartoes`, head **2df92cd** (só `web/app`; o commit de testes e versão que ainda vem não muda a tela).
- Simulação própria, toda com dado fictício (fixture `conftest`): abas Resultado, Produtividade e Por DU e o recorte AM.
- Larguras: 390×844, 1024×768, 1366×768, 1600×900 e 1920×1080, com a tela real do PC (`uma-tela`), não a página inteira.
- Casos-limite: valor longo ("R$ 1.165 mil"), legenda longa e título longo.

## Parecer: aprovado com 1 🟡

O pedido do Alexandre (R-20261127-093750) está atendido:
- os 8 cartões do Resultado têm o valor grande;
- todos seguem a mesma estrutura (título, valor, legenda, faixa, gráfico);
- a faixa de comparação e o gráfico começam na mesma altura em toda linha, nas medições:
  - 1024 px: 2 por linha;
  - 1366 e 1600 px: 3 por linha;
  - 1920 px: 4 por linha, como no print;
- o mesmo vale para Produtividade e Por DU;
- não há valor encostando nos anéis, faixa estourada nem página mais larga que a tela (390 px = 390).

Decisão RD-0063 (a faixa do topo sem os 3 números): **de acordo**.
- Cada número aparece uma vez só, e o Faturamento Líquido abre a 1ª linha.
- No recorte por estado, a mudança ainda corrige um defeito do `main`: na faixa, os textos da legenda se sobrepunham ao número seguinte (`ux-recorte-am-1366x768.png`).

"Desconto comercial" e "Km por visita" sem faixa, no PC: o bloco vazio reservado **está bom**.
- Visualmente parece o cabeçalho um pouco mais alto, não um defeito.
- É o que o PC desenha (`painel_rrm.py` traça a linha da faixa e reserva a altura mesmo sem comparação).
- Sem ele, o gráfico desse cartão sairia do nível dos outros, que é justamente o que o Alexandre pediu para corrigir.

## 🟡 corrigir antes do merge
1. **Celular (≤ 600 px, um cartão por linha): espaço vazio sem motivo.**
   - O problema: a altura fixa do cabeçalho (138 px) e a faixa vazia reservada (78 px) também valem no celular, onde não há linha para alinhar.
   - Efeito: "Desconto comercial" mostra ~120 px de verde vazio e "Ticket médio"/"Markup", ~40 px. Isso é estado vazio aparecendo.
   - A legenda longa também fica cortada com "…", e o `title` não abre no toque.
   - Correção: no bloco `@media(max-width:600px)`, `.rrm:not(.rrm-recorte) .rc-topo{height:auto}`, `.rc-leg{height:auto;-webkit-line-clamp:unset}`, `.rc-leg:empty{display:none}` e `.rc-faixa.vazia{display:none}`.
   - A estrutura e a ordem ficam as mesmas.
   - Antes: `ux-celular-antes.png`. Depois sugerido: `ux-celular-depois-sugerido.png`.

## 🟢 para depois
- **Título e legenda repetem a mesma coisa:**
  - "Faturamento líquido · **proj.**" e "Pedidos faturados · **proj.**" têm a legenda "projeção do mês", que repete o título.
  - Ao lado, "Positivação 45 / projeção do mês 66" usa a mesma frase com outro sentido (lá, o valor é o real).
  - O texto vem do PC (`painel_rrm.py`, `leg_proj`) e é igual à referência. Sugestão ao dono do PC: legenda sem número = nenhuma legenda (a linha continua reservada).
- **Valor longo:** `.rc-valor` é `nowrap`, sem reduzir a fonte.
  - Hoje cabe ("R$ 1.165 mil" fica a 8 px do anel no celular).
  - Um "R$ 12.345 mil" encostaria no anel. O PC reduz a fonte até caber; na web, por exemplo, `font-size:clamp(1.1rem,4.2vw,1.5rem)` ou `text-overflow:ellipsis`.
- **Título com mais de 2 linhas:** é cortado sem "…" (`.rc-rot` com `overflow:hidden`). Usar o mesmo `line-clamp` da legenda. Nenhum título real chega a 3 linhas hoje.
- **1366×768 (notebook):** o cabeçalho mais a faixa ocupam 216 dos 380 px do cartão, e o gráfico fica com ~110 px úteis.
  - Ainda dá para ler. Se o Diretor achar baixo, `grid-auto-rows:minmax(420px,1fr)` em `body.uma-tela .painel-corpo .rrm`.
- **Recorte por estado no PC (já era assim no `main`):** os cartões têm 380 px de altura só com título, valor e legenda, o que deixa muito verde vazio.
  - Correção: `body.uma-tela .painel-corpo .rrm-recorte{grid-auto-rows:auto}`.
- **Informativo:** 4 cartões por linha só a partir de ~1640 px. A 1600 px ficam 3, o que é aceitável: o grid não mudou neste PR.

## Anexos (dado fictício)
`ux-resultado-1920.png`, `ux-resultado-1366x768.png`, `ux-por-du-1366x768.png`, `ux-recorte-am-1366x768.png`, `ux-celular-antes.png`, `ux-celular-depois-sugerido.png`.

## Reteste no head 73dbbbe (27/11/2026): aprovado

- Conferi os `sim/depois-*` do po (2878e17, mesma tela) e regerei no **73dbbbe** com a fixture fictícia (`--lang=pt-BR`): Resultado, Produtividade, Por DU e o recorte AM, a 320, 390, 600, 1024, 1366, 1600 e 1920 px.
- **O 🟡 do celular está resolvido.**
  - Até 600 px, o topo do cartão fica na altura do conteúdo, e a legenda e a faixa vazias somem (altura 0).
  - O "Desconto comercial" vai do valor direto ao gráfico, sem o verde vazio.
  - A legenda longa aparece inteira, sem "…".
  - Nenhuma largura passa da tela (390 = 390, 320 = 320).
- **No PC, o alinhamento continua igual.**
  - O topo tem 138 px e a faixa 78 px em todo cartão.
  - A faixa e o gráfico começam na mesma altura em cada linha (1366: 310/392, 704/786 e 1098/1180).
  - A linha da legenda vazia continua reservada.
- **Legenda (RD-0238):** "projeção do mês" sem número sumiu do Faturamento líquido e dos Pedidos. "Projeção do mês 66" fica, porque tem número próprio. O 🟢 de título repetido está resolvido.
- **Valor:** 18 px a 320, 20,3 px a 390 e 22 px a partir de 600 (no máximo 22 px, como pediu a marca). Mesmo o "R$ 1.165 mil" fica a 8 px do anel. O 🟢 de valor longo está resolvido.
- **Recorte por estado no PC:** com `grid-auto-rows:auto`, o cartão baixou de 380 para 196 px (1366).
- **Marca:** nenhum hex novo em `estilo.css` nem em `painel.html` em relação ao `main`. Só `var(--…)`.
- 🟢 para depois (não bloqueia):
  - no recorte, os cartões ainda esticam até encher a tela (296 px a 1920);
  - `align-content:start` em `body.uma-tela .painel-corpo .rrm-recorte` deixaria cada cartão na altura do conteúdo.
- Anexos (dado fictício): `ux-reteste-celular-73dbbbe.png`, `ux-reteste-recorte-am-1366-73dbbbe.png`.
