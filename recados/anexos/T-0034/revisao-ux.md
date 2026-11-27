# T-0034 · Página inicial e telas de conta no BC3: parecer de UX

- **Revisor:** designer-ux · **Data:** 27/11/2026 (Manaus)
- **Head revisado:** `modulo-web/T-0034-pagina-inicial` em `b60cae167bb86d9e4f6add926fd574a725854a74` (diff contra `modulo-web/T-0033-revisao-geral` em `3165af2`).
- **Régua:** contrato `.coord/contratos/tela-bc3.md` v1 (branch `engenheiro-software/T-0033-contrato-bc3`), `docs/marca/manual.md` do `main`, parecer `T-0033/revisao-ux-geral.md` §5 e `T-0033/revisao-redundancias-geral.md` (RD-0038, RD-0043, RD-0059).
- **Telas:** os 24 pares de `sim-t0034/antes` e `/depois` (fixture fictícia), todos abertos. A simulação mostra só a janela visível (`fullPage: false`).
- **Medições extras e PNGs desta revisão** (mesmo servidor da simulação; conferi que `main.py`, `render.py`, `estilo.css`, `usuarios.html`, `_painel_cab.html` e `parcial.html` são iguais aos do head): em `T-0034/ux/`. São a confirmação do Desativar, o Novo usuário aberto, o "Indicadores ▾" e o "Mais ▾" abertos, e três telas de "depois sugerido" (CSS injetado só no navegador, nada no repositório).

## Veredito

**Não aprovado ainda: 0 🔴, 7 🟡, 8 🟢.** Nada estoura a largura (scrollWidth = clientWidth em todas as 24 telas e nas extras), o nome "BAP AUTOPARTS" e as cores estão certos, e a página inicial cai no lugar certo para os 6 perfis. O que segura o merge é redundância (o número da faixa repetido no cartão), a rolagem da página no `/painel` e duas diferenças de padrão da casca.

## O que está certo

- **Redirecionamento (§14):** medido com os 6 perfis. admin, diretor e gerente → `/painel`; pre_venda → `/farol/pv_pedidos`; pos_venda → `/farol/pl_entregas`; vendas → `/farol/vc_visitas`. A grade de quadrados saiu.
- **Casca única (§3):** a lateral aparece em todas as telas logadas. O login fica centralizado, sem lateral, com o logo grande, "BAP Central" e "BAP AUTOPARTS" pequeno; o título não repete o botão. O rodapé com a versão saiu.
- **Faixa (§4.1):** 88 px a 1366 e 96 px a 1920 em todas as abas do Painel, em Usuários, Trocar senha e Parcial (0 px de diferença entre abas).
- **Abas do Painel (§5, §13.3):** nomes curtos numa linha, com "Indicadores ▾" no PC e "Mais ▾" no celular (3 abas + Mais). Alvos de 44 px nas abas, no PC e no celular. "Visitas" no lugar da segunda "Produtividade".
- **Filtro de estado:** segmentado na faixa, à direita. Nas abas só da BAP (Visitas, Preço, Inadimplência), cinza, com o `title` do contrato, e o `AVISO_SO_BAP` saiu do corpo.
- **Cores:** só tokens no CSS novo, sem hex fora do `:root`. Os números da faixa usam `--faixa-ok`, `--faixa-atencao` e `--faixa-alerta`, nos pares do manual §4.3 (3,01:1 a 3,97:1, só em número grande). Barras do RRM em cinza-verde.
- **Um botão principal por tela (§11):** Login "Entrar", Trocar senha "Salvar" e Usuários "Novo usuário". "Trocar senha" é neutro e "Desativar" é perigo, com confirmação ("Desativar o usuário sim.diretor?" + botão "Desativar"). A confirmação cabe a 1366 e a 390 (`ux/usuarios-desativar__*.png`).
- **Perfis por extenso (§13.4)** em Usuários ("Pós-venda", não `pos_venda`) e selos com texto.
- **Regra dos 3 toques:** cumprida.
  - Painel → qualquer aba: 1 toque (2 pelo Indicadores/Mais).
  - Painel → farol: 1 toque no PC, 2 no celular (☰).
  - Desativar um usuário: Usuários → Desativar → confirmar = 3.
  - Parcial → Baixar imagem: 2 a partir do farol.

## 🟡 Corrigir antes do merge

| # | Tela | Elemento | Regra quebrada | Correção proposta |
|---|---|---|---|---|
| U1 | Painel · Resultado / Produtividade / Por DU (1366, 1920, 390) | Cartões RRM | Mesmo número 2× na tela: "R$ 165 mil", "45" e "85", e o MTD/MÊS, ficam na faixa e no cartão. Contrato §14 e parecer T-0033 §5.2: "os cartões perdem o número grande, que já está na faixa" | Tirar `rc-valor` e `rc-leg` do cartão quando o número estiver na faixa. Ficam o título, os anéis, a faixa de variação e as barras. Ver `ux/sugerido-painel-resultado__pc1366.png` |
| U2 | Painel · Resultado (1366) | Página | Rola 2 px (770 × 768). §1.2 e §7.1: a página não rola no PC. O "Como ler de exemplo." ainda ocupa uma linha própria (§14: vira ⓘ com `title`) | "Como ler" vira ⓘ no título da faixa; `.rc` sem `min-height:540px` e com `flex:1`. No sugerido, cabe: 768 × 768 |
| U3 | Painel · abas de painel com tabela (Faturamento 1155 px a 1366 e 1173 px a 1920; Volume e as outras com tabela) | Página | §7.1 e §7.4: a lista de exceções é fechada e o Painel não está nela. Ver a decisão 2 abaixo | Gráfico e tabelas em caixas lado a lado, com a mesma altura e rolagem vertical por dentro (o padrão das "juntas", §6.4), cabendo a 1366×768. No celular, tabelas recolhíveis |
| U4 | Painel, Usuários, Trocar senha, Parcial (PC e celular) | Faixa | Um só estilo por componente. Nos faróis, a faixa é um cartão com margem (16/14 px no PC; 14 px no celular) e cantos arredondados. Nas telas da T-0034, ela encosta no topo e na lateral (top 0, left 200, right 0; no celular, 0/0). A causa: o farol põe a faixa dentro do `main.bc3-corpo` (`_bc3_cab.html`), e as telas novas usam o `{% block faixa %}`, fora dele | Pôr as três faixas (`_painel_cab`, `_faixa_simples` e `_bc3_cab`) no mesmo lugar da casca, com as mesmas margens. Ver `ux/sugerido-senha__pc1366.png` |
| U5 | Usuários, Trocar senha | Item da lateral | §3: item ativo com a marca à esquerda e `aria-current="page"`. Hoje nenhum item fica ativo (medido: `aria-current` nulo) | Em `pagina()`, `ativo` também para `/usuarios` → "usuarios" e `/senha` → "senha", com a chave no `render.menu_lateral` |
| U6 | Painel · faixa (PC e celular) | Linha da data | §1.5 (a tela não explica o sistema) e §8 (no celular, data curta). Hoje: "Dados de 24/11/2026 08:30 · visão absoluta · novembro até 19/11 (13 de 19 dias úteis) · variação × mês fechado". No celular, isso quebra em 2 linhas e leva a faixa a 229 px | "24/11/2026 08:30 · nov até 19/11 · 13 de 19 DU" no PC e "24/11 08:30 · 13 de 19 DU" no celular. "Visão absoluta" e "variação × mês fechado" vão para o `title`. Ver a decisão 1 |
| U7 | Parcial | "Voltar ao farol" | RD-0059 ("o link sai"; o farol já está ativo na lateral). Ele continua, agora como botão, nos dois estados (`parcial.html:10` e `:18`) | Tirar nos dois estados: a lateral "Pedidos", ativa, volta em 1 toque. **E simular a Parcial com dados:** as 3 PNGs mostram só "A parcial ainda não chegou do PC.", e o seletor Acumulado / D-1 / Hoje e o botão principal "Baixar imagem" não foram vistos |

## 🟢 Sugestões (podem ir para depois)

1. **Novo usuário:** o perfil vem marcado como "Admin" (o primeiro da lista). Começar com "Escolha o perfil" (obrigatório), ou com o perfil de menor acesso. Com o formulário aberto, "Criar" é neutro e o principal continua no "Novo usuário" fechado. Melhor: ao abrir, o resumo vira "Cancelar" (neutro) e "Criar" vira o principal.
2. **Desativar:** a própria linha do admin logado oferece "Desativar", e o servidor recusa depois da confirmação ("Você não pode desativar a si mesmo."). Esconder o botão na própria linha. A confirmação também não tem "Cancelar" nem fecha com Esc (§6.2 e §11). E o texto da pergunta poderia ir em `--texto`, ficando o vermelho só no botão.
3. **Usuários a 1366/1920:** o nome fica a ~1.000 px das ações. Limitar a lista a ~960 px ou aproximar as ações. Com todos ativos, o selo "Ativo" em toda linha é ruído: mostrar só o que foge do normal (Desativado, Troca pendente). É decisão do design-de-marca.
4. **Faixa no celular:** sobram ~60 px vazios embaixo (o `min-height` do `.bc3-ks` no celular). Isso também acontece nos faróis (T-0033). Tirar no CSS comum.
5. **"Mais▾"** sem espaço: o contrato escreve "Mais ▾", com o marcador no `::after`, como o "Indicadores ▾".
6. **Filtro desligado:** o contrato §4.2 pede `aria-disabled="true"` no segmentado cinza. Hoje ele só tem `aria-label` e `title`.
7. **Celular, cartões do Painel (§8 e §5.3):** o primeiro aberto e os outros fechados, com as barras por estado deitadas. Hoje os 3 cartões vêm inteiros, com barras em pé (a página do Resultado tem 2.009 px a 390).
8. **Para o corretor-redundancias:**
   - `render.BC3` ficou sem uso, só no `test_T0030_bc3.py` (fim do RD-0044);
   - o filtro de estado está escrito de novo em `_painel_cab.html` (o RD-0044 propõe um macro só);
   - `erro.html` ainda tem `<h1>` no corpo (§4.2).
   - A fixture do Painel não tem `recortes` nas abas RRM: o filtro de estado do Resultado não aparece na simulação e não foi visto. O `testes` deveria incluir um recorte.

## Redundância: RD-0038, RD-0043 e RD-0059

- **RD-0038: fechado.** O título é "Painel Executivo" em todas as abas e no `<title>`, as abas são curtas e sem "Painel ·", e "Visitas" acaba com a duplicidade. Achado novo de redundância no mesmo lugar: o número da faixa repetido no cartão (U1).
- **RD-0043: fechado.** `home.html` saiu, `/` redireciona, o `base.html` tem um layout só e saíram a flag `bc3` e o CSS `.menu`, `.quadro`, `.abas`, `.cab-painel` e `.acoes-farol`. Resta o `render.BC3` morto (🟢 8). A diferença de posição da faixa (U4) é a consequência visual que falta.
- **RD-0059: não fechado.** O título foi para a faixa e os botões são `.bc3-bt`, mas o "Voltar ao farol" ficou (U7).

## Decisões pedidas

1. **"Dados de" na faixa: vale o contrato (§4.1), sem "Dados de".**
   - **Na faixa:** a data sozinha. O `title` leva o texto inteiro ("Dados de 24/11/2026 08:30, horário de Manaus").
   - **Mesmo PR:** a mudança entra em `_painel_cab.html` e também em `_bc3_cab.html` (os faróis), para não nascerem dois padrões. As duas são do modulo-web e trocam uma linha cada.
   - **Se o gerente preferir não mexer nos faróis agora:** mantenha "Dados de" nos dois e registre a pendência na T-0033. O que não pode é o Painel diferente dos faróis.
   - **Não é v2:** a regra já está escrita na v1.
2. **Rolagem vertical do `/painel` nas abas com tabela: não é aceitável pelo contrato v1.**
   - **O que o contrato diz:** a §1.2 e a §7.1 dizem que a página não rola a 1366×768 e 1920×1080. A §7.4 fecha as exceções (a fila do Cobrar e os formulários no celular) e diz "nenhuma outra".
   - **O que está fora:** abrir exceção para o Painel muda a regra de rolagem, e isso é **v2**, com a simulação e o "aprovo" do Alexandre ("não gosto de barra de rolagem", R-20261126-171559).
   - **Caminho recomendado:** U3, a rolagem por dentro das caixas, como nas tabelas de baixo dos faróis.
   - **Se o gerente quiser fazer o merge antes de U3:** o único caminho limpo é pedir ao Alexandre, pelo po, a exceção temporária "abas de painel do Painel Executivo até a T-nnnn", com os PNGs `painel-diretor-faturamento__pc1366/1920` como prova.
   - **No celular:** a página rolar no Painel é o M3 (lista e cartões). Não é achado.

## 8 PNGs para a simulação ao po

Depois das correções 🟡, regerar as mesmas 8 no novo head. Por ora, as melhores do head `b60cae1`:

1. `sim-t0034/antes/painel-diretor__pc1366.png`: o antes (a grade de quadrados).
2. `sim-t0034/depois/painel-diretor__pc1366.png`: o diretor abre direto no Painel Executivo.
3. `T-0034/ux/sugerido-painel-resultado__pc1366.png`: o depois sugerido (sem número repetido, cabe na tela).
4. `sim-t0034/depois/painel-diretor-faturamento__pc1366.png`: uma aba de indicador, com o filtro de estado na faixa.
5. `sim-t0034/depois/painel-diretor__cel390.png`: o celular (M3), com "Mais ▾".
6. `sim-t0034/depois/home-prevenda__pc1366.png`: a pré-venda cai no Farol de Pedidos.
7. `sim-t0034/depois/login__pc1366.png`: o login novo.
8. `T-0034/ux/usuarios-desativar__pc1366.png`: Usuários, com a confirmação do Desativar.
