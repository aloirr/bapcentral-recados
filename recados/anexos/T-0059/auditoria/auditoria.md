# Auditoria "MENOS É MAIS" (R-20261127-174849-alexandre): web da BAP Central

- Código: origin/main 7375c1fd1c99ce872ca15baa27974d971461b3cb (destacado, sem worktree, sem edição).
- Como: uvicorn local com pacote fictício montado das fixtures de web/tests (painel22 + farol_fixture + analista pacote_coerente), admin com senha gerada na hora, BAP_WEB_COOKIE_SEGURO=0. Prints a 1366 px e 390 px (`<pagina>-pc.png` / `<pagina>-cel.png`, página inteira).
- Critérios: (a) linha que não enche a largura antes de descer · (b) tamanho fora do padrão entre páginas · (c) redundância · (d) marca.
- Nenhuma página passa da largura a 390 px (scrollWidth = 390 em todas).

| Página | Crit. | Grav. | Onde | Correção proposta (1 linha) | Esforço |
|---|---|---|---|---|---|
| Painel · Produtividade | a | 🟡 | `.rrm` usa `repeat(auto-fill,minmax(340px,1fr))` (estilo.css:118): com 1 cartão sobram 2/3 da linha vazios a 1366 | trocar para `auto-fit` (o cartão estica) ou fixar o nº de colunas no nº de cartões da aba | pequeno |
| Painel · Resultado/Produtividade | c | 🟡 | legenda "atingimento da meta do mês (projeção ÷ meta)" repetida no rodapé de cada cartão | dizer uma vez só, acima da grade (ou no `title`) | pequeno |
| Painel × faróis | b | 🟡 | cartão do Painel `.rc` min-height 540 px (barras ~300 px) × gráfico do farol 280 px (`.bc3 .graficos .graf`); à 1366 o Painel ocupa a tela toda com uma linha | um token único `--altura-grafico` (ex.: 280 px) para barras do Painel e dos faróis | médio |
| Entregas · Resumo | a | 🟡 | `.bc3 .graficos` com `auto-fit,minmax(165px,1fr)` (estilo.css:650) e a tabela ocupando a linha inteira: as 6 trilhas ficam vivas e o "SLA por estado" sai com 180 px, 5/6 da linha vazia; o cartão da tabela tem altura fixa com ~110 px em branco embaixo | gráficos numa grade própria `auto-fit,minmax(340px,1fr)` e a tabela fora dela, com altura pelo conteúdo | médio |
| Entregas · Resumo | c | 🟡 | "R$ 52 mil · 410 notas" na faixa e de novo na linha TOTAL da tabela (R$ 52.000 · 410) | tirar a linha TOTAL do Resumo (a faixa já diz) ou tirar o número da faixa | pequeno |
| Entregas · celular | UX | 🔴 | tabela "Frete por estado" espremida: cabeçalho quebra letra a letra ("NO/TA/S") e valor quebra no meio ("R$ 1.250./000") | `white-space:nowrap` nos números + rolagem lateral com a 1ª coluna fixa (ou a lista `bc3-item` dos outros faróis) | pequeno |
| Inadimplência | a | 🟡 | cartão "Em atraso" sozinho numa linha (`section.kpis` `auto-fill,minmax(200px)` → 1/5 da largura a 1366; metade a 390) | levar "Em atraso / acima de 90 dias" para a faixa como os outros KPIs, ou `auto-fit` para encher a linha | pequeno |
| Inadimplência | UX | 🟡 | "Vencido × a vencer": rótulos de valor girados 90° (PC e celular); "Em atraso por vendedor" com metade do cartão em branco | valor só no `title`/popup ou barras empilhadas sem rótulo girado; cartões da linha com a altura do conteúdo | médio |
| Inadimplência / Visitas | d | 🟡 | série única em verde vivo #62BB47 (vem do pacote do PC) × Painel em cinza-verde #8FA79A: verde aqui não significa "ok" | o render normalizar série neutra para `--grafico-3` (#8FA79A), como já faz com #4F6D7A (estilo.css:327) | pequeno |
| Visitas · Resumo | b | 🟢 | gráfico de 3 barras na largura toda: barras finas e rótulos S1/S2/S3 alinhados à esquerda, longe da barra | centrar o rótulo sob a barra (`.gb-rot` centrado na coluna) | pequeno |
| Visitas | c | 🟢 | "Sem filtro por estado" escrito na faixa (os outros faróis só omitem o seletor de UF) | tirar o texto; a ausência do seletor já diz | pequeno |
| Usuários | a/b | 🟡 | botão "Novo usuário" solto numa linha própria, à esquerda; nos faróis a ação fica à direita, na linha das abas | pôr o botão à direita, na mesma linha (padrão `.bc3-sub`/`.bc3-acoes`) | pequeno |
| Pedidos · Resumo | — | 🟢 | enche a largura; só o "Resumo gerencial" (1 linha) e a página acaba em 280 px | ok pela regra; avaliar gráfico/sinal no Resumo para não ficar só texto | — |
| Analista · Saldo · Resumo | — | 🟢 | igual a Pedidos: enche a largura, só o resumo | ok | — |
| Login | — | ok | caixa central 420 px (padrão de mercado para login) | ok | — |
| Global (todas) | d | 🔴 | texto do corpo em #1B2430 (azul-ardósia, estilo.css:110), bordas de campo #ADB5BD e legendas #6B7075 (cinzas azulados), `--verde-marca` #59BA61 (paleta: #4FA236/#62BB47), `--alerta` #B42318 (paleta: #B3261E), `--borda` #E3E8E4 (paleta: #D5DAD4) | trocar pelos tokens da paleta (`--texto` #1E2722 etc.); consolidação MC-0006 com o design-de-marca | pequeno (CSS) + decisão de marca |
| Global (todas) | b | ok | largura útil igual em todas (1134 px a 1366 com lateral de 200 px; 362 px a 390); faixa 88 px; título 21 px PC / 20 px celular; abas do mesmo estilo | manter | — |

Observações: o pacote é fictício; os números repetidos entre cartões do Painel (barras por UF iguais, faixa out/set/jul do Visitas igual à do Faturamento) são da fixture, não da tela.
