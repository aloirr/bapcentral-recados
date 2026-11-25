# Parecer de UX — T-0017, entregas 3 a 5 (sim6: abas de Pedidos, Entregas e Visita no site)

- **Revisor:** designer-ux · **Data:** 25/11/2026 (Manaus)
- **Objeto:** os 28 PNGs de `scratchpad/sim6/` (todos abertos um a um), os HTML de `sim6/html/`, o código da branch `modulo-web/T-0017-tres-farois` no **head c86b9ff** (`web/app/templates`, `web/app/static/estilo.css`, `web/app/main.py`, `web/app/tabelas.py`, `web/tests/farol_fixture.py`).
- **Referência:** sim4-* (Inadimplência, entrega 2) e sim5-* (Resumo dos três faróis), já aprovadas.
- **Conferências extras feitas por mim:**
  - Largura a 390 px: abri os 18 HTML num iframe de 390 px no Chrome headless. Em todos, `scrollWidth == clientWidth`, ou seja, **sem rolagem horizontal da página**. As tabelas largas rolam dentro do quadro: `.rolagem` de 356 px com conteúdo de 574 a 1.954 px.
  - Página inteira no PC (1366 px) de 01, 02, 05 e 11. Essas capturas estão em `scratchpad/uxchk/full_*.png`. Elas mostram o que os PNGs do sim6 cortam: as juntas de Pedidos, a junta Pendências de Entregas e a paginação do Cliente a cliente.
  - Contraste dos selos: verde `#2F7D32`/`#E5F3DF` = 4,44:1 · amarelo `#8A5A00`/`#FFF1C7` = 5,27:1 · vermelho claro `#B3261E`/`#FDECEA` = 5,72:1 · vermelho cheio branco/`#B3261E` = 6,54:1.

## Veredito

**Ainda não mandar ao Alexandre.** São 3 🔴, todos de correção rápida (dois na fixture e um de CSS). Junto deles vão os 🟡 Y1, Y3, Y4 e Y5, que mudam o que ele vai ver. Depois disso, gerar de novo os PNGs e pedir o reteste.

---

## 🔴 Corrigir antes de mostrar

### R1. Dia da semana errado em todas as tabelas de Visita, e o recorte "dia útil" mostra fim de semana
- **PNGs:**
  - `sim6-09-visita-dia-a-dia-sem-visita-vendas-pc/cel`: 01/11/2026 aparece como "TER", mas é domingo; 07/11 (sábado) e 15/11 (domingo) aparecem no recorte **"Sem visita em dia útil"**; e há linhas "SEM VISITA" com VISIT. 12 a 20 e % META de 95% a 112%.
  - `sim6-10-visita-aderencia-admin-pc/cel`: os títulos "03/11 SEG", "06/11 QUI" e "09/11 TER" estão deslocados um dia (03/11/2026 é terça). As datas das colunas estão certas; só o rótulo erra.
  - `sim6-11-visita-cliente-a-cliente-admin-pc`: 01/11/2026 aparece como "SEG".
  - `sim6-12-visita-prospeccao-admin-pc`: todas as linhas mostram "SEG".
- **Por que é 🔴:** o pedido de revisão exige a conferência "Datas em Manaus". O Alexandre conhece o calendário de novembro e vai achar que o site erra o dia útil.
- **Origem:** a fixture, não o código do site.
- **Correção (modulo-web, `web/tests/farol_fixture.py`):**
  - Calcular o dia pela data real: `["SEG","TER","QUA","QUI","SEX","SÁB","DOM"][date(2026, 11, d).weekday()]`, nas linhas 350, 364, 386 e 406 (hoje `DIAS_SEM[dia % 5]`, `DIAS_SEM[(d - 3) % 5]`, `DIAS_SEM[i % 5]` e `"SEG"`).
  - No Dia a dia, usar só dias úteis (seg a sex, fora 02/11 e 15/11), como o próprio `range` da Aderência já faz.
  - Nas linhas "SEM VISITA", usar VISIT. = 0 e % META = 0%.

### R2. Celular: a 1ª coluna fixa corta o nome e as linhas ficam iguais
- **PNGs:**
  - `sim6-08-visita-por-supervisor-gerente-cel`: as 3 linhas mostram "SUPERVISOR F…" e não dá para saber quem é quem.
  - `sim6-08-visita-por-vendedor-gerente-cel` e `sim6-10-visita-aderencia-admin-cel`: mesmo corte. Além disso, a coluna que fica fixa é a SUPERVISOR, mas quem identifica a linha é o VENDEDOR, e ele some ao rolar para o lado.
- **Correção 1 (`web/app/static/estilo.css`, bloco `@media(max-width:600px)` do T-0017):**
  - Trocar `.tab-dados th:first-child,.tab-dados td:first-child{max-width:7.5rem;overflow:hidden;text-overflow:ellipsis}`
  - por `.tab-dados th:first-child,.tab-dados td:first-child{max-width:9.5rem;white-space:normal;overflow-wrap:anywhere}`. O nome passa a quebrar em até 2 linhas, sem reticências.
- **Correção 2 (`web/app/tabelas.py` + `_grade.html`):**
  - Criar um índice `fixa` por tabela (padrão 0). Em "Por vendedor", "Dia a dia", "Aderência dia a dia" e "Cliente a cliente", a coluna fixa passa a ser a **VENDEDOR**.
  - No `_grade.html`, aplicar `class="fixa"` à célula desse índice e trocar o `:first-child` do CSS por `.fixa`.

### R3. Cores dos selos da fixture diferentes das do PC
- **PNGs:** `sim6-01-…-pc/cel` e `sim6-02-…-pc` (SLA), `sim6-08-…` e `sim6-09-…` (% META).
- **O que está errado:**
  - **SLA:** o site mostra 2 e 3 sem selo e 4 em amarelo. No PC, `relatorios_nucleo.CHIP_SLA()` pinta 1 de verde, 2 de amarelo, 3 e 4 de vermelho claro (`#FBDDDA`) e acima de 4 de vermelho cheio.
  - **% META:** o site pinta 78% de amarelo. No PC, `FAIXA_PCT_META` pinta de vermelho tudo abaixo de 80%.
  - **% ATENDIDO:** as cores da barra também diferem de `BARRA_ATENDIDO` (`#D9534F`/`#E0A526`/`#62BB47`).
- **Por que é 🔴:** o Alexandre compara com o PC e vai perguntar por que "4 dias" está amarelo. O site em si só desenha o que o robô manda; o erro está apenas na simulação.
- **Correção (`web/tests/farol_fixture.py`, linhas 86 a 89):** copiar exatamente `CHIP_SLA()`, `BARRA_ATENDIDO` e `FAIXA_PCT_META` de `relatorios_nucleo.py` (linhas 1534, 1540 e 19094), ou importá-los de lá.

---

## 🟡 Ajustes

**Recomendo corrigir antes de mostrar: Y1, Y3, Y4 e Y5.**

### Y1. Texto curto quebrando em 3 a 5 linhas no PC, com linhas muito altas
- **PNGs:**
  - `sim6-05-entregas-entregas-pos_venda-pc` e `sim6-06-…-PA-admin-pc`: CLIENTE fica "900001 / - / CLIENTE / FICTICIO / 01", com o "-" sozinho numa linha. Cabem só 4 linhas por tela.
  - `sim6-01-…-pc`: FANTASIA em 3 linhas.
  - `sim6-08-…-vendedor-pc`, `sim6-09-…-pc`, `sim6-10-…-pc` e `sim6-11-…-pc`: VENDEDOR, BAIRRO e CÓD. ("900001-/01") quebrando.
- **Correção (`estilo.css`):**
  - Usar `.tab-dados td{white-space:nowrap}`. Como a tabela já rola de lado, não há motivo para espremer as colunas.
  - Só o texto livre quebra: `.tab-dados td.livre{white-space:normal;min-width:14rem;max-width:26rem}`.
  - A classe `livre` sai de uma marca na coluna em `tabelas.py`: OBSERVAÇÃO, JUSTIFICATIVA, RESULTADO, LINHAS DE INTERESSE e DESCRIÇÃO do Analítico.

### Y2. PC: a barra de rolagem lateral fica só no fim da tabela
- **PNGs:** 01, 02, 05, 06, 08, 09, 10 e 11 no PC. As últimas colunas aparecem cortadas ("% A", "ETAPA EM TRÁ", "INTER") e não há nenhuma dica. A barra horizontal só aparece depois da última linha (119 pedidos; 100 linhas por página no Cliente a cliente).
- **Correção (`estilo.css`):**
  - Limitar a altura do quadro: `.rolagem:has(.tab-dados){max-height:75vh;overflow:auto}`, ou uma classe `rolagem-dados` no `_grade.html:4`.
  - Fixar o cabeçalho: `.tab-dados thead th{position:sticky;top:0;z-index:2}` e `.tab-dados thead th:first-child{z-index:3}`. A Inadimplência já tem o mesmo comportamento no `.tb-rol`.
  - Mostrar a dica também no PC: tirar `@media(min-width:1000px){.dica-rolagem{display:none}}`, ou mostrar só quando `tabela.cols|length > 12`.

### Y3. "Com filtro, os cartões seguem só no PC." não está claro e deixa 5 a 6 cartões vazios
- **PNGs:**
  - `sim6-02-…-AM-gerente-pc`: 6 cartões com "—".
  - `sim6-06-entregas-entregas-PA-admin-pc`: 5 cartões com "—". Ali o usuário só escolheu o estado PA, não "filtrou", então "com filtro" nem descreve a situação.
- **Correção 1 (`web/app/tabelas.py:46`):**
  - Trocar o texto por `AVISO_CARTOES = "Cartões só para a BAP inteira, sem recorte nem filtro. Os números do estado estão no Resumo gerencial."`
- **Correção 2 (`_tabela.html:16`):**
  - Trocar `{% if kpis is defined %}` por `{% if kpis is defined and not aviso_kpis %}`. Assim os cartões vazios não aparecem e fica só a linha do aviso.

### Y4. Solicitação BAP mostra Estado e cartões que não têm relação com a aba
- **PNGs:** `sim6-03-pedidos-solicitacao-cd-pre_venda-pc/cel` e `sim6-03-…-detalhado-…-pc/cel`.
  - O desenho (D5) diz "Solicitação sem estado", mas a tela mostra os botões BAP inteira/AM/MA/PA.
  - Os 6 cartões são os do Resumo de Pedidos (119 pedidos, 82 em aberto), não os do arquivo.
  - No celular, a tabela só começa em ~750 px.
- **Correção (`web/app/main.py`, `farol_abas`, linhas 288 a 311):**
  - Quando `t.get("subabas")`, passar `ufs=[]` e não montar `kpis`. No template, trocar `{% if kpis is defined %}` por `{% if kpis %}`.

### Y5. Rótulos crus do arquivo na Solicitação BAP
- **PNGs:** `sim6-03-*`. As sub-abas mostram "Solicitacao CD" (sem acento), "DETALHADO_PEDIDO", "ProdutosExcluir" e "FiliaisExcluir". Os cabeçalhos mostram "FILIAL_DESTINO", "COD_PRODUTO" e "DESCRICAO".
- **Correção (`tabelas.subabas_para_tela`, só na exibição; o contrato continua usando o nome do arquivo):**
  - Mapa de sub-abas: Lojas · CD · FRW · Manual · Detalhado por pedido · Produtos excluídos · Filiais excluídas.
  - Cabeçalhos: trocar `_` por espaço e aplicar `{"COD":"CÓD.","DESCRICAO":"DESCRIÇÃO","JA":"JÁ"}`.

### Y6. Celular: a tabela de Visita fica fora da primeira tela
- **PNGs:** `sim6-08/09/10/11-*-cel`. As 8 abas ocupam 4 linhas, o aviso 2 linhas e os 5 cartões grandes 3 linhas. Em `sim6-11-…-cel` não aparece nenhuma linha da tabela.
- **Correção 1 (`estilo.css`, `@media(max-width:600px)`):**
  - Abas mais compactas: `.abas a{padding:.35rem .7rem;font-size:.92rem;min-height:44px;display:inline-flex;align-items:center}`.
- **Correção 2 (`main.py:310`):**
  - Nas abas de tabela, usar sempre cartões em faixa fina: `faixa=True`. Isso também resolve o Y7.

### Y7. Tamanho dos cartões muda entre os faróis nas abas de tabela
- **PNGs:** `sim6-01-…-pc` usa a faixa fina (78 px); `sim6-05-…-pc` e `sim6-08-…-pc` usam o cartão grande (120 px, borda de 2 px).
- **Correção:** a mesma do Y6, `faixa=True` nas abas de tabela. O Resumo continua como o PC.

### Y8. O mesmo aviso de estado aparece em duas cores
- **PNGs:** `sim6-13-visita-resumo-diretor-cel` mostra o aviso **amarelo** ("os cartões mostram a BAP inteira"); `sim6-08-…` mostra o aviso **azul** ("esta tabela mostra a BAP inteira").
- **Correção (`render.farol_para_tela`, `web/app/render.py:409`):** levar o aviso do robô que começa com "Sem filtro por estado" para `aviso_uf`, que já é desenhado como `aviso info` (azul) em `farol.html:28`. Amarelo fica para o que pede ação.

### Y9. "Filtros" parece título, não botão
- **PNGs:** `sim6-01`, `05`, `08-vendedor`, `11`, `12-prospeccao` e `12-indicacao` (todos `-pc`). O `display:flex` em `.filtros-det summary` tira o triângulo do `<details>`. O problema vale também para a Inadimplência.
- **Correção (`estilo.css`):** `.filtros-det summary::before{content:"▸";margin-right:.45rem}` e `.filtros-det[open] summary::before{content:"▾"}`.

### Y10. Links com a cor padrão do navegador (azul e sublinhado)
- **PNGs:**
  - "Limpar" em `sim6-02`, `06` e `09` (`-pc`).
  - "Voltar ao menu" em `sim6-04-pedidos-aba-403-diretor-pc`.
- **Correção (`estilo.css`):**
  - `.filtros-tab a,.caixa a{color:var(--azul);font-weight:600}`.
  - "Limpar" com cara de botão neutro e 44 px de altura no celular: `.filtros-tab a{min-height:44px;display:inline-flex;align-items:center;padding:0 .6rem}`.

### Y11. PRODUTO com seleção múltipla sem instrução
- **PNG:** `sim6-02-…-pc`. O `<select multiple size=4>` exige Ctrl + clique, que ninguém descobre sozinho, e ainda desalinha a linha dos filtros.
- **Correção (`_tabela.html:37-41`):** acrescentar `{% if f.multi %}<small>Ctrl + clique marca mais de um</small>{% endif %}` abaixo do campo, ou trocar por caixas de marcar dentro de um `<details>`.

### Y12. Plural errado em "1 linhas"
- **Onde:** na junta "Gerar reversa de lojas" do HTML 02 (fora do PNG).
- **Correção (`_tabela.html:7` e `:56`):** `{{ n }} {{ 'linha' if n == 1 else 'linhas' }}`.

### Y13. Estado vazio fala em "filtro" quando não há filtro
- **PNG:** `sim6-12-visita-indicacao-vazia-admin-pc` mostra "Nenhuma linha neste filtro." com tudo no padrão.
- **Correção (`_tabela.html:48`):** `grade(tabela, base, fq, "Nenhuma linha neste mês." if tabela.padrao else "Nenhuma linha neste filtro.")`.

### Y14. Fixture com números que não fecham, que o Alexandre pode estranhar
- **PNGs e casos:**
  - `sim6-08-…-supervisor-pc`: linha TOTAL com 9 representantes, meta 20, 12 visitas e 112%.
  - `sim6-04-…-resumo-diretor-*`: Resumo com "Pedidos 119 · Mais de 4 dias 9", contra 21 e 10 na aba Pedidos de `sim6-01`.
  - Junta Pendências (página inteira de 05): linhas "SET/26" com datas de outubro.
  - Resumo só com "Frase fictícia.".
- **Correção (`farol_fixture.py`):** somar o TOTAL das linhas; alinhar os cartões do Resumo com os da aba; casar MÊS e data nas pendências; reaproveitar no Resumo a fixture do sim5 (frases e gráficos).

### Y15. Os PNGs mostram só a primeira tela
- Juntas (01 e 05) e paginação "Página 1 de 3" (11) não aparecem em nenhum PNG, embora o desenho, na seção 4, prometa mostrá-las.
- **Correção:** gerar também a versão de página inteira de 01-pc e 05-pc, como os `sim5-*-inteira`.

### Y16. Regra do "antes e depois" (R-20261120-102406-alexandre)
- A regra pede UMA imagem com o antes (PC) e o depois (site) lado a lado; a seção 4 do desenho também promete o antes. Nenhum PNG do sim6 tem o antes.
- **Correção:** montar o pacote final como 1 imagem de painéis, com o PC (Tkinter, fictício) à esquerda e o site à direita, ou pelo menos mandar o antes junto de 01 e 05.

### Y17. Rótulo da aba diferente da Inadimplência (baixo)
- O rótulo é "Resumo gerencial" aqui e "Resumo" na Inadimplência.
- **Correção (`tabelas.py:33`):** usar `RESUMO = ("resumo", "Resumo")`. É mais curto, cabe melhor no celular e o título da seção já diz "Resumo gerencial".

### Y18. Data sem ano (baixo)
- Pedidos, Entregas e as juntas mostram "02/11"; Solicitação e Visita mostram "02/11/2026". Na junta Pendências, o ano faz falta quando a pendência vem de dezembro e o mês corrente é janeiro.
- **Correção:** o formato `data` em `tabelas.py` passa a sair sempre como dd/mm/aaaa.

---

## 🟢 OK
- **Largura no celular:** nenhuma página rola de lado em 390 px (medido nos 18 HTML). As tabelas rolam dentro do quadro com a 1ª coluna fixa e a dica "Role para o lado…".
- **Corte e sobreposição:** nada sobreposto nos 28 PNGs. Os cortes à direita são da rolagem interna, que é o esperado; o resto está em R2 e Y1.
- **Perfil:**
  - O diretor vê só o Resumo, sem barra de abas, em `sim6-04-*`, `sim6-07-*` e `sim6-13-*`.
  - A URL de aba devolve a página 403 "Acesso negado · Você não tem acesso a esta página.", em português claro.
  - Com o robô antigo (`sim6-14`), o admin vê só o Resumo, sem aba quebrada.
- **3 toques:**
  - Menu → farol → aba = 2 a 3 toques. Recorte ou sub-aba é +1, ainda dentro do limite.
  - Barra de abas, sub-abas, recortes e aviso de estado têm estado ativo claro: aba laranja, chip verde, sub-aba azul.
- **Coerência com a Inadimplência:**
  - Mesma barra de abas, mesmos chips de Estado e Recorte, mesmo `.selo`.
  - Mesmos tons de linha: alerta `#fdecea`, atenção `#fff8e1`, ok `#f1f8ee`, grave `#f6c9c4`.
  - Mesma faixa "Dados de … (horário de Manaus)" e mesmo rodapé "BAP AUTOPARTS".
  - A cor sempre vem com texto ou número.
- **Dado pessoal:**
  - Só "CLIENTE/VENDEDOR/SUPERVISOR/MOTORISTA/FORNECEDOR FICTICIO nn", códigos 9xxxxx e logins sim.*.
  - Prospecção e Indicação sem CNPJ, CONTATO, TELEFONE e FOTO.
- **Datas e hora:** "Dados de 24/11/2026 08:30 (horário de Manaus)" e "Baixado do ERP em 24/11/2026 08:10" estão certas. O erro de dia da semana está no R1.
- **Juntas (página inteira de 01 e 05):** títulos claros, contagem ao lado e estado vazio "Nenhuma linha ligada às linhas de cima.".

## Observações fora deste PR (para o design-de-marca, já existentes e aprovadas na Inadimplência)
- Texto branco na aba ativa laranja (`#E8590C`): 3,58:1, abaixo de 4,5:1 para texto de 16 px.
- Selo verde `#2F7D32` sobre `#E5F3DF`: 4,44:1, quase no limite. É a cor do PC.

## PNGs recomendados para o Alexandre (máx. 8, depois das correções)
1. `sim6-01-pedidos-pedidos-admin-pc.png` (de preferência a versão de página inteira, com as 3 juntas)
2. `sim6-01-pedidos-pedidos-admin-cel.png`
3. `sim6-03-pedidos-solicitacao-cd-pre_venda-pc.png`
4. `sim6-05-entregas-entregas-pos_venda-pc.png` (página inteira, com Pendências)
5. `sim6-06-entregas-entregas-PA-admin-pc.png` (estado + aviso dos cartões)
6. `sim6-08-visita-por-vendedor-gerente-cel.png` (prova da 1ª coluna fixa no celular)
7. `sim6-09-visita-dia-a-dia-sem-visita-vendas-pc.png`
8. `sim6-04-pedidos-resumo-diretor-cel.png` (o diretor vê só o Resumo)

## Para o dono (modulo-web)
- R1, R3 e Y14 ficam em `web/tests/farol_fixture.py`.
- R2, Y1, Y2, Y6, Y9 e Y10 ficam em `web/app/static/estilo.css`.
- Y3, Y5, Y17 e Y18 ficam em `web/app/tabelas.py`.
- Y4 e Y6/Y7 ficam em `web/app/main.py`.
- Y8 fica em `web/app/render.py`.
- Y3, Y11, Y12 e Y13 ficam em `web/app/templates/_tabela.html`.
- O reteste é feito por mim, nos PNGs gerados de novo e no head SHA novo.

---

## Reteste 3b7a627 (25/11/2026, Manaus)

### O que foi conferido
- **Código:** o diff c86b9ff..3b7a627 em `web/app/` e em `web/tests/farol_fixture.py`.
- **PNGs abertos:** os 8 que recomendei, mais o 11-pc e mais 02 (novo), 08-supervisor-cel, 12-indicacao e 13-cel.
- **Largura no celular:** medi de novo os 19 HTML a 390 px. Nenhum rola de lado (`scrollWidth == clientWidth` em todos).
- **Página inteira:** o recado diz que 01-pc, 05-pc e 11-pc são de página inteira, mas **os 28 PNGs continuam com o tamanho da tela** (2732×1800 e 780×1688). Por isso gerei eu mesmo, a partir do HTML novo, `scratchpad/uxchk2/full_01-pedidos-admin.png`, `full_05-entregas-pos_venda.png` e `full_11-cliente-a-cliente-admin.png` (1366 px).

### Situação de cada achado
| Item | Situação | Prova |
|---|---|---|
| R1 dia da semana | ✅ resolvido | sim6-09-pc: 03/11 TER, 16/11 SEG, 06/11 SEX, 19/11 QUI (todos conferidos com o calendário). O recorte "Sem visita em dia útil" só tem dias úteis, com VISIT. 0 e selo 0%. A Aderência usa as datas reais. |
| R2 1ª coluna no celular | ✅ resolvido | sim6-08-supervisor-cel e sim6-08-vendedor-cel: o nome quebra em 2 linhas e fica legível. VENDEDOR é a 1ª coluna fixa em Por vendedor, Dia a dia, Aderência e Cliente a cliente. |
| R3 cores dos selos | ✅ resolvido | HTML 01: SLA 0–1 verde, 2 amarelo, 3–4 `#FBDDDA`, 5+ vermelho cheio (= `CHIP_SLA`). HTML 08: % META abaixo de 80 vermelho claro, 80–99 amarelo, 100 ou mais verde (= `FAIXA_PCT_META`). |
| Y1 quebra de texto | ✅ | sim6-05-pc e sim6-11-pc: CLIENTE numa linha só; só o texto livre quebra. |
| Y2 rolagem lateral no PC | ✅ | Dica visível no PC, quadro com 75vh e cabeçalho fixo (página inteira de 11). |
| Y3 aviso dos cartões | ✅ | sim6-02 e sim6-06: uma linha de aviso clara, sem os cartões vazios. |
| Y4 Solicitação sem estado e sem cartões | ✅ | sim6-03-cd-pc: a tabela começa logo abaixo das sub-abas. |
| Y5 rótulos | ✅ | Sub-abas Lojas · CD · … · Filiais excluídas; cabeçalhos CÓD. PRODUTO, DESCRIÇÃO, JÁ SOLICITADO. |
| Y6 tabela de Visita no celular | ✅ | Abas em 3 linhas e cartões em faixa fina; a tabela já aparece na 1ª tela do sim6-08-cel. |
| Y7 tamanho dos cartões | ✅ | Faixa fina em todas as abas de tabela. |
| Y8 cor do aviso de estado | ✅ | sim6-13-cel: aviso azul, igual ao das abas. |
| Y9 Filtros com seta | ✅ | ▸ quando fechado, ▾ quando aberto. |
| Y10 links | ✅ (resíduo) | "Limpar" e o 403 em azul da marca. **Resíduo:** "Próxima »" da paginação ainda usa o azul padrão. Correção: incluir `.paginas a` na regra de cor em `estilo.css`. |
| Y11 Ctrl + clique | ✅ | sim6-02. |
| Y12 plural | ✅ | Corrigido no código (`_tabela.html` :7 e :56). Não há caso de "1 linha" na fixture para ver no PNG. |
| Y13 estado vazio | ✅ | sim6-12-indicacao: "Nenhuma linha neste mês.". |
| Y14 números da fixture | ✅ (resíduo) | TOTAL fecha (60 / 45 / 75%), os cartões do Resumo do diretor são iguais aos da aba e as pendências SET/26 têm datas de setembro. **Resíduo:** nas abas de Visita os cartões dizem "Visitas 180 · 84,0%", enquanto o TOTAL da tabela diz 45 · 75%, e isso aparece na mesma tela de sim6-08-supervisor. Correção: em `farol_fixture.py`, `kpis_padrao` de Visita = TOTAL do Por vendedor. |
| Y17 rótulo "Resumo" | ✅ | |
| Y18 data com ano | ✅ | dd/mm/aaaa em todas as tabelas. |
| Y15 / Y16 | Não feitos (informado pela web) | Ver abaixo. |

### Novo achado
- 🟡 **N1. Os 4 recortes de Pedidos sumiram da fixture.** O 3b7a627 tirou o `recortes_linhas` de `tabela_pedidos`, então sim6-01 e sim6-02 não mostram mais a linha "Recorte" (Faturar 100%, Mais de 4 dias, Crédito a analisar, Acima de 15% sem autorização). No site real, eles vêm do robô. A Visita (sim6-09 e sim6-11) ainda mostra o componente, mas o Pedidos fica diferente do que vai para produção.
  - **Correção:** recolocar a lista `rec` e `recortes_linhas=` em `farol_fixture.py`.
- 🟢 Com a 1ª coluna fixa no celular, DT. PED fica larga (`min-width:8rem`). Não atrapalha a leitura.

### O que ficou aberto impede mostrar ao Alexandre?
**Não.** Não há 🔴. Os resíduos não impedem:
- Y10: a cor do link da paginação.
- Y14: os cartões de Visita não batem com o TOTAL. O desencontro não aparece nos 8 PNGs recomendados (em sim6-08-vendedor-cel o TOTAL fica fora da tela).
- N1: os recortes de Pedidos. O componente já aparece em Visita.
- Y15: o Resumo já foi aprovado no sim5; esta rodada é das abas.
- Y16: o sim5 foi aprovado sem o "antes". Ainda assim, recomendo uma frase no recado: "no PC é a mesma tabela; o antes é a aba do PC".

**Recomendado, se houver 5 minutos:** N1 e Y14 na fixture.

**Para mandar:** usar as páginas inteiras que gerei, e não os PNGs do tamanho da tela, para 01-pc e 05-pc (juntas) e 11-pc (paginação).

### Os 8 PNGs finais
1. `scratchpad/uxchk2/full_01-pedidos-admin.png` (Pedidos + 3 juntas, PC)
2. `scratchpad/sim6/sim6-01-pedidos-pedidos-admin-cel.png`
3. `scratchpad/sim6/sim6-03-pedidos-solicitacao-cd-pre_venda-pc.png`
4. `scratchpad/uxchk2/full_05-entregas-pos_venda.png` (Entregas + Pendências, PC)
5. `scratchpad/sim6/sim6-06-entregas-entregas-PA-admin-pc.png`
6. `scratchpad/sim6/sim6-08-visita-por-vendedor-gerente-cel.png`
7. `scratchpad/sim6/sim6-09-visita-dia-a-dia-sem-visita-vendas-pc.png`
8. `scratchpad/sim6/sim6-04-pedidos-resumo-diretor-cel.png`

A paginação do 11 (página inteira em `scratchpad/uxchk2/full_11-cliente-a-cliente-admin.png`) fica como reserva. Se o gerente quiser mostrá-la, ela entra no lugar do item 5.
