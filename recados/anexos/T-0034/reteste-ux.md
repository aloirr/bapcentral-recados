# T-0034 · Página inicial e telas de conta no BC3: reteste de UX

- **Revisor:** designer-ux · **Data:** 27/11/2026 (Manaus)
- **Head revisado:** `modulo-web/T-0034-pagina-inicial` em `aae27cc74ff186857ca47040fb0bb14c4fcc9d70` (diff contra `b60cae1`, 20 arquivos).
- **Régua:** o parecer anterior (`T-0034/revisao-ux.md`, U1 a U7), o contrato `tela-bc3` v1, o manual de marca e as duas decisões do gerente (1: a faixa mostra só a data; 2: no PC nada rola e as caixas rolam por dentro, no celular rolar é aceitável).
- **Telas:** abri as 30 PNGs de `sim-t0034/depois2` (fixture fictícia). Também medi as **12 abas do Painel** a 1366, 1920 e 390, no mesmo código (`git archive aae27cc`, servidor da simulação, nada no repositório). A simulação só mede o `documentElement`. Por isso conferi também a rolagem do `.bc3-corpo` e de cada caixa.

## Veredito

**Não aprovado ainda: 0 🔴, 2 🟡 (novos, pequenos), 7 🟢.** Os U1 a U7 estão **fechados**. Nada estoura a largura e, no PC, nada rola nas 12 abas. A regra dos 3 toques e as cores estão certas. Faltam duas coisas: o DU volta a ficar visível na faixa do Painel (U8, decisão abaixo) e o espaço entre a faixa e o formulário do Trocar senha (U9).

## U1 a U7, um a um

| # | Situação | Conferido |
|---|---|---|
| U1 | **Fechado** | Os cartões RRM perderam o `rc-valor` e o `rc-leg` (`painel.html`). Ficam o título, os anéis, a variação e as barras. A faixa perdeu os anéis no detalhe (`faixa_painel`), e o número aparece uma vez só. |
| U2 | **Fechado** | Resultado a 1366: 768 × 768 e `.bc3-corpo` sem rolagem. O "Como ler" virou ⓘ no título (`title` + `aria-label`). |
| U3 | **Fechado** | Nas 12 abas, a 1366 e a 1920, `docH` = altura da janela e o `.bc3-corpo` não rola. Gráfico e tabelas ficam em caixas lado a lado (Faturamento: gráfico + 3 tabelas). Com a fixture, nenhuma caixa precisou rolar. Com dado real, a caixa `.graf` rola por dentro. |
| U4 | **Fechado** | A faixa entrou no `<main>` (`base.html`). O topo fica a 14 px a 1366 e a 16 px a 1920 em todas as telas logadas, com margem e cantos iguais aos dos faróis. As três faixas saem do mesmo `_faixa.html` (RD-0065). |
| U5 | **Fechado** | "Usuários" e "Trocar senha" ficam ativos na lateral, com `aria-current="page"` (`render.menu_lateral` e `base.html:20`). |
| U6 | **Fechado** (ver U8) | A faixa mostra só "24/11/2026 08:30" no PC e "24/11 08:30" no celular. O texto inteiro vai no `title`. O mesmo vale nos faróis (`_bc3_cab.html`), e assim não nascem dois padrões. No celular, a faixa do Resultado caiu de 229 px para 213 px. |
| U7 | **Fechado** | O "Voltar ao farol" saiu nos dois estados. A Parcial foi simulada com dados: seletor Acumulado / D-1 / Hoje, "Baixar imagem" como único botão principal, "Copiar imagem" e "Baixar PDF" neutros. A imagem rola por dentro da caixa, e a página não rola a 1366 nem a 1920. |

Os 🟢 anteriores também andaram:
- o 3: o selo "Ativo" saiu;
- o 6: entrou o `aria-disabled="true"`.

## Conferências

- **Nada cortado, sem rolagem lateral:** `scrollWidth` = largura nas 30 telas e nas 36 medições do Painel. Nenhum elemento da faixa é cortado. Nenhuma caixa rola de lado.
- **Rolagem:** no PC, nenhuma tela rola. No celular rolam o Painel (Resultado com 1.880 px, Faturamento com 1.295 px) e Usuários. Isso é aceito pela decisão 2.
- **3 toques:**
  - Painel → qualquer aba: 1 toque (2 pelo Indicadores/Mais);
  - Painel → farol: 1 toque no PC, 2 no celular;
  - Desativar: Usuários → Desativar → confirmar = 3;
  - Farol → Parcial → Baixar imagem = 2;
  - Parcial → farol: 1 toque (Pedidos ativo na lateral).
- **Cores:** só tokens no CSS novo. A faixa usa `--faixa-ok/atencao/alerta`, as barras RRM ficam em cinza-verde e os selos da tabela passaram para fundo claro com texto escuro (`PALETA_TOM`: `--ok-claro`/`--alerta-claro`). Nada de azul-marinho nem de laranja. O nome é "BAP AUTOPARTS" na lateral, no login e no `<title>`.

## 🟡 Corrigir antes do merge

| # | Tela | Elemento | Regra quebrada | Correção proposta |
|---|---|---|---|---|
| U8 | Painel · faixa (PC e celular) | Dias úteis | Hierarquia: o contexto do número principal some. No celular não há `title` (toque não tem *hover*), e o "13 de 19 DU" fica inalcançável para o Diretor | Mostrar `24/11/2026 08:30 · 13 de 19 DU` no PC e `24/11 08:30 · 13 de 19 DU` no celular, em **todas** as abas do Painel (a linha não muda entre abas, §4.2). Usar o `caller()` do macro `quando`, como o farol já faz com "· Sem filtro por estado". "Visão absoluta", "nov até 19/11" e "variação × mês fechado" continuam no `title`. Mês fechado: `19 DU · mês fechado` |
| U9 | Trocar senha (1366, 1920, 390) | Formulário | Um só estilo por componente: o cartão encosta na faixa, com 0 px entre os dois. Nos faróis e no Painel o espaço é de ~12 px (as abas). Em Usuários, ~10 px (`.u-novo{margin:10px …}`, remendo local). A causa: `.bc3-corpo .caixa{margin:0}` com a faixa agora dentro do `<main>` | Uma regra na casca, `.bc3-corpo>.bc3-faixa{margin-bottom:12px}` (a mesma distância da faixa às abas), e tirar o `margin-top` do `.u-novo`. Conferir também `editar.html` e `erro.html`, que usam a mesma faixa simples |

## Decisão: o DU volta a ficar visível na faixa do Painel

**Volta, como em U8.** Os motivos:

1. **É o contexto do número principal.** Os números da faixa do Resultado e do Produtividade são **projeções** ("· PROJ."), e a projeção = real ÷ DU fechados × DU do mês (regra 4). Com 3 de 19 DU, a projeção é frágil; com 17 de 19, é firme. O Diretor precisa disso para ler o número, e não para entender o sistema. Por isso o DU não cai no §1.5, ao contrário de "visão absoluta" e "variação × mês fechado", que explicam a conta e ficam no `title`.
2. **O `title` não existe no celular.** O Diretor usa o celular, e ali o DU sumiria por completo. No PC, ele só aparece depois de parar o mouse sobre a data, o que ninguém faz.
3. **Não reabre a decisão 1.** Ela tirou o rótulo "Dados de", um texto redundante com a data. O DU não é um segundo carimbo de hora: é um dado de negócio, como o "· Sem filtro por estado" que a faixa do farol já mostra no mesmo lugar e com o mesmo macro. Não nasce componente novo.
4. **Custo baixo.** São 12 caracteres. A 1366, a linha 1 tem espaço sobrando até o filtro de estado. A 390, "24/11 08:30 · 13 de 19 DU" cabe numa linha (~190 px de ~330 px).

**De onde vem o número:** hoje o DU chega só dentro do texto `sub` do PC (`painel_rrm.py:622`, `ndp`/`ndm`). O caminho limpo é o pacote mandar os campos (ex.: `du: {fechados, mes}`), num recado ao dono do `painel_rrm.py`. Para não segurar este PR, a web pode extrair "N de M dias úteis" do `sub`, com teste. Isso é extrair, não recalcular. A troca pelo campo fica para depois. Quem decide é o gerente, com o `revisor-codigo`.

## 🟢 Sugestões (podem ir para depois)

1. **Celular, faixa:** sobram ~60 px vazios embaixo dos números (o `min-height:112px` do `.bc3-ks`, que só foi zerado na faixa simples). A faixa tem 213 px nas abas RRM e 245 px nas de painel, porque o filtro desce para uma linha própria e o selo "Desatualizado" fica sozinho à esquerda. O mesmo acontece nos faróis: tratar no CSS comum (T-0033).
2. **ⓘ do "Como ler" no celular:** com `title`, ele também não abre no toque. Na v2, um `<details>` pequeno ou um popover no toque.
3. **Resultado a 1920:** `.rrm` usa `repeat(auto-fill, minmax(340px,1fr))`, e os 3 cartões deixam uma 4ª coluna vazia (~440 px à direita). Com `auto-fit`, os 3 dividem a largura.
4. **Gráfico "Faturamento projetado":** as barras são verde-claras (`#62BB47`). Pela regra da casa, a série é neutra em cinza-verde, e verde significa "ok". Vem da T-0022, fora deste diff: recado ao design-de-marca/T-0033.
5. **Bordas de campo** (`input`, login e senha): a cor `--c-adb5bd` (`#ADB5BD`, cinza azulado) está fora da paleta; a linha da marca é `#D5DAD4`. Vem de antes deste diff. Fica para o design-de-marca.
6. **Ainda abertos do parecer anterior:**
   - o 🟢 1 (Novo usuário começa em "Admin");
   - o 🟢 2 ("Desativar" na própria linha do admin, sem "Cancelar"/Esc);
   - o 🟢 5 ("Mais▾" sem espaço);
   - o 🟢 7 (no celular, os cartões vêm todos abertos).
7. **Simulação da Parcial:** a imagem fictícia do harness mostra "simula��o" (a fonte do PNG de teste não tem "ç"/"ã"). Não é do produto, mas aparece no PNG do po: trocar para "simulacao" ou avisar na legenda.

## 8 PNGs para o po

Confirmo 7 e troco 1. Depois de U8 e U9, regerar as do Painel no novo head (a faixa muda):

1. `sim-t0034/depois2/painel-diretor__pc1366.png`: o diretor abre direto no Painel Executivo (regerar com o DU).
2. **Troca:** `sim-t0034/antes/painel-diretor__pc1366.png` no lugar de `painel-admin__pc1366`. A do admin é igual à do diretor (só muda "Usuários" na lateral) e não mostra nada novo. O "antes" (a grade de quadrados) é o que dá ao po a comparação.
3. `sim-t0034/depois2/painel-diretor-faturamento__pc1366.png`: uma aba de indicador, com caixas lado a lado, sem rolagem e com o filtro de estado na faixa.
4. `sim-t0034/depois2/painel-diretor__cel390.png`: o celular, com "Mais ▾" e a data curta (regerar com o DU).
5. `sim-t0034/depois2/home-prevenda__pc1366.png`: a pré-venda cai no Farol de Pedidos, com a data sem "Dados de".
6. `sim-t0034/depois2/login__pc1366.png`: o login.
7. `sim-t0034/depois2/usuarios-desativar__pc1366.png`: Usuários, com a confirmação do Desativar e "Usuários" ativo na lateral.
8. `sim-t0034/depois2/parcial__pc1366.png`: a Parcial com dados, sem "Voltar ao farol" (ver 🟢 7 sobre a legenda).
