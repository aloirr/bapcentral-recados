# T-0034 · Conferência final de UX (antes da simulação ao po)

- **Revisor:** designer-ux · **Data:** 27/11/2026 (Manaus)
- **Head revisado:** `modulo-web/T-0034-pagina-inicial` em **`dc81c24`**. Comecei no `9ad9ae9` e o gerente avisou que o head mudou. O `dc81c24` traz `cf93690` (R1: o 4º cartão em diante volta a ter número) e `dc81c24` (com mais de 3 cartões, a área rola por dentro). Tudo o que vale para o `9ad9ae9` foi conferido de novo no `dc81c24`.
- **Desde o parecer anterior (`aae27cc`):** merge da T-0033 (`94b3440`/`ddf6f06`), U8, U9, o bloco único `@media(max-width:700px)` (RD-0066), R1 e o layout com rolagem.
- **Como conferi:**
  - Abri as 36 PNGs de `sim-t0034/depois3`, inclusive as 7 refeitas às 05h21.
  - Medi 46 telas × 3 larguras em cópias do head e do `main` fora do repositório (`git archive`), com a fixture fictícia.
  - Montei uma fixture com 10 cartões no Resultado, como o PC manda.
  - Nada no clone do código foi alterado. A branch não foi trocada.

## Veredito

**Não aprovado ainda: 0 🔴, 3 🟡 (pequenos, no Painel), 6 🟢.**

U8 e U9 estão fechados. A junção dos `@media` não mudou nada no celular (prova abaixo). Os 3 🟡 são:
- o número do 4º cartão em diante sem estilo (U10);
- o DU que some em mês fechado (U11);
- a 3ª linha de cartões quase invisível a 1920 (U12).

## U8 e U9

| # | Situação | Conferido |
|---|---|---|
| U8 | **Fechado** (com a ressalva do U11) | Nas 12 abas do Painel aparece "24/11/2026 08:30 · 13 de 19 DU" a 1366 e a 1920, e "24/11 08:30 · 13 de 19 DU" a 390. Fica numa linha só (17 px), sem corte (`scrollWidth = clientWidth`), com 12 px. O resto da nota continua no `title`. |
| U9 | **Fechado** | A distância da faixa ao que vem depois é de **12 px** em todas as telas e larguras: Painel (abas), Trocar senha (cartão), Usuários (Novo usuário), Parcial, faróis (abas) e farol com estado. O `margin-top` do `.u-novo` saiu. |

## A junção dos `@media(max-width:700px)` (RD-0066): sem regressão

Fiz uma prova de cascata. Remontei o CSS do head com os dois blocos antigos do `aae27cc` nas posições originais. Depois comparei 28 propriedades calculadas de **todos** os elementos, em 46 telas × 390/1366/1920 (138 medições):
- **Única diferença:** o `.bc3-k em` (o detalhe do número na faixa, celular) perdeu `overflow:hidden` e `text-overflow:ellipsis`. Como já era `white-space:normal`, o texto quebra linha em vez de cortar. A altura da página é a mesma em todas as telas. Isso não é regressão.
- O bloco de 600 px, que antes vinha depois do de 700 px, não tem seletor em comum com ele. A ordem nova não muda nada.
- `scrollWidth` = largura em todas as 138 medições. Nada passa de 390 px.

## 🟡 Corrigir antes do merge

| # | Tela | Elemento | Regra quebrada | Correção proposta |
|---|---|---|---|---|
| U10 | Painel · Resultado, Produtividade e Por DU (PC e celular) | Número e legenda do 4º cartão em diante (`.rc-valor`, `.rc-leg`) | Hierarquia, o número principal primeiro. O `9ad9ae9` apagou as regras `.rc-valor`/`.rc-leg` do CSS como código morto, e o `cf93690` devolveu as classes ao `painel.html`. Resultado: o número sai a **16 px, peso 400**, igual à legenda ("R$ 4.210 / por pedido faturado" em `depois3/painel-diretor__pc1366.png`) e mais fraco que o título do cartão (12,8 px, peso 700) | Voltar as duas regras, sem passar o número da faixa (22 px): `.rc-valor{white-space:nowrap;font-size:1.5rem;font-weight:700;color:var(--texto);line-height:1.15;margin-top:.4rem;font-variant-numeric:tabular-nums}` e `.rc-leg{font-size:.85rem;color:var(--suave);margin-top:.2rem}`. Teste: o CSS tem as duas regras enquanto o template usar as classes. Depois: `conferencia-final-ux/sugerido-resultado__pc1366.png` e `__pc1920.png` |
| U11 | Painel · faixa, mês fechado | Dias úteis | Parte do U8 ficou de fora (o "mês fechado: `19 DU · mês fechado`"). O `render.du_do_painel` só lê "(N de M dias úteis)". Em mês fechado o PC manda "outubro fechado (22 dias úteis)" (`painel_rrm.py`, `base`), e o DU **some** da faixa. Conferido: `du_do_painel(...'outubro fechado (22 dias úteis)'...)` devolve `''`. Isso acontece no 1º dia útil do mês, justamente quando o Diretor olha o fechamento | Uma 2ª expressão: `fechado \((\d+) dias úteis\)` → `"22 DU · mês fechado"`. Teste com o texto do mês fechado, ao lado do `test_dias_uteis_na_faixa_de_todas_as_abas_do_painel` |
| U12 | Painel · Resultado e Produtividade a 1920 | Área dos cartões que rola | Descoberta: com 10 cartões em 4 colunas, a 3ª linha mostra só **18 px**. Os 2 últimos (Cadastros com compra e Inadimplência no PC) parecem não existir. A 1366, por comparação, a 2ª linha mostra 150 px, com título, número e anéis | `grid-auto-rows:minmax(380px,1fr)` no lugar de `420px`. Medido: a 1920 a 3ª linha passa a mostrar 98 px, já com o título e o número. A 1366, 190 px. As barras ficam com 169 px e nenhum cartão corta. Antes e depois: `antes-resultado__pc1920.png` e `sugerido-resultado__pc1920.png` |

## A pergunta do gerente: o Diretor acha a rolagem dentro da área dos cartões?

**Sim, com o U12.** Recomendo **manter a rolagem por dentro** e **não** fazer uma tela por grupo de cartões. Os motivos:

1. **A pista já é forte onde importa.** Medi com a barra de rolagem visível, como no Windows, onde o Chrome e o Edge sempre mostram a barra clássica de 15 px:
   - a 1366, 1440, 1536 (1920 com escala de 125%) e 1600, aparecem de 150 a 280 px da linha seguinte, com o título, o número e os anéis do próximo cartão;
   - um cartão cortado ao meio é a pista mais clara de que há mais;
   - a página não rola, então a roda do mouse sobre os cartões rola a área sem precisar mirar na barra.

   Só a 1920 a pista é fraca, e o U12 resolve isso.
2. **O que é mais importante não fica escondido.** Os 3 números de cabeça estão na faixa e os 3 primeiros cartões aparecem inteiros. A rolagem só leva aos cartões 4 a 10, que são o detalhe.
3. **Uma tela por grupo cria um 4º nível de navegação** (lateral → aba → grupo → cartão) e um componente novo, porque não existe "grupo" nos faróis. Isso quebra o "um só estilo por componente" e a regra dos 3 toques. Também separa cartões que o PC mostra juntos, na mesma grade. O padrão da casa (decisão 2, §6.4) é a caixa rolar por dentro, como as tabelas dos faróis e o gráfico do Faturamento.
4. **No celular** a página rola, como a decisão 2 aceita. Com 10 cartões, o Resultado chega a 5.559 px: ver 🟢 3.

## Conferências

- **Telas que o modulo-web não reabriu:** login, parcial, usuarios-desativar e painel-diretor-faturamento, nas 3 larguras. Estão iguais ao aprovado. A Parcial já mostra "simulação" com acento, o que fecha o meu 🟢 7 anterior. Nas telas de conta e nos 2 faróis havia celular para todas. Não precisei gerar nenhuma.
- **Rolagem da página no PC:** nenhuma tela do T-0034 rola, nem o Resultado com 10 cartões (1366, 1920, 1280×720, 1280×800, 1440, 1536 e 1600). Duas rolam, mas vêm de antes:
  - Usuários com o "Novo usuário" aberto a 1366 (849 px). Já era assim no `aae27cc` (847 px). A diferença de 2 px é o U9.
  - Inadimplência › Cobrar. Também rola no `main`, fora deste diff.
- **Abas no celular:** a regra única `abas_no_celular` dá o mesmo resultado do template antigo em todas as abas medidas. A única diferença está na aba desconhecida: agora aparecem 3 abas em vez de 2, o que fica melhor.
- **Marca e cores:**
  - só tokens no CSS novo;
  - nada de azul-marinho nem de laranja;
  - "BAP AUTOPARTS" na lateral, no login e no `<title>`;
  - o aviso dos cartões da T-0033 ("Cartões sem filtro…") aparece na faixa, uma vez só.

## 🟢 Sugestões (podem ir para depois)

1. **1280 px de largura:** com a barra de rolagem (15 px), a grade dos cartões cai de 3 para 2 colunas. Faturamento e Positivação ficam juntos, e Pedidos vai para a linha de baixo (`antes-resultado__pc1280x720.png`). Faltam ~8 px. Uma saída é `minmax(330px,1fr)` na `.rrm` do PC, conferindo a 1920 que não vira 5 colunas. A 5 colunas, "R$ 149 mil" quebra a linha. Vale só se houver notebook de 1280 na empresa.
2. **Simulação ao po:** na fixture de 10 cartões do modulo-web, o 1º cartão (Faturamento líquido) traz os anéis da Positivação (40 % / 112 e 93 % / 163), e a faixa sai em âmbar. O po pode ler isso como erro. Para os PNGs dele, use os anéis da fixture original (11 % / 1,03 mi e 100 % / 1,50 mi) e só acrescente os cartões 4 a 10.
3. **Celular, Resultado com 10 cartões:** a página tem 5.559 px. Fica mais forte o meu 🟢 7 anterior: no celular, do 4º cartão em diante, abrir só a cabeça (título, número e anéis) e deixar as barras num toque.
4. **Filtros do farol no celular:** o botão "Filtrar" tem 40 px de alto (abaixo dos 44 px) e fica desalinhado do "Limpar". O `main` é igual: vem da T-0033, recado ao dono.
5. **Mês fechado na faixa do Painel**, depois do U11: conferir com o pacote real do 1º dia útil de dezembro.
6. **Ainda abertos dos pareceres anteriores:**
   - o 1 (Novo usuário começa em "Admin");
   - o 2 ("Desativar" na própria linha do admin, sem "Cancelar"/Esc);
   - o 4 (barras verdes do "Faturamento projetado", que deveriam ser cinza-verde `#8FA79A`);
   - o 5 (bordas `#ADB5BD` fora da paleta);
   - o "Mais▾" sem espaço.

## 8 PNGs para o po

Confirmo as 8. Duas precisam ser refeitas depois de U10 e U12, e todas as do Painel devem sair com a fixture coerente (🟢 2):

1. `sim-t0034/depois3/painel-diretor__pc1366.png`: o Diretor cai direto no Painel, com "13 de 19 DU" na faixa e a 2ª linha de cartões aparecendo. **Refazer** com o U10.
2. `sim-t0034/antes/painel-diretor__pc1366.png`: o "antes" (a grade de quadrados), para a comparação.
3. `sim-t0034/depois3/painel-diretor-faturamento__pc1366.png`: aba de indicador, com caixas lado a lado, sem rolagem e com o filtro de estado na faixa. OK.
4. `sim-t0034/depois3/painel-diretor__cel390.png`: celular, com "Mais ▾" e "24/11 08:30 · 13 de 19 DU". OK (refazer só se a fixture mudar).
5. `sim-t0034/depois3/home-prevenda__pc1366.png`: a pré-venda cai no Farol de Pedidos. OK.
6. `sim-t0034/depois3/login__pc1366.png`: o login. OK.
7. `sim-t0034/depois3/usuarios-desativar__pc1366.png`: Usuários, com a confirmação do Desativar e 12 px sob a faixa. OK.
8. `sim-t0034/depois3/parcial__pc1366.png`: a Parcial com dados e "simulação" com acento. OK.

**Anexo extra recomendado** (o layout é novo e o po precisa vê-lo): `painel-diretor-rolado__pc1366.png`, refeito com o U10. Mostra o fim da área rolada.

## Anexos deste parecer

`recados/anexos/T-0034/conferencia-final-ux/` (fixture fictícia, sem dado pessoal):
- `antes-resultado__pc1920.png`: `dc81c24` com 10 cartões. A 3ª linha mostra 18 px e o número do cartão sai sem estilo.
- `sugerido-resultado__pc1920.png` e `sugerido-resultado__pc1366.png`: U10 + U12.
- `antes-resultado__pc1280x720.png`: 🟢 1 (2 colunas).
