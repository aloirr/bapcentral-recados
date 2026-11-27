# Reteste de tela (designer-ux) · T-0033 · antes dos PRs

- **Heads revisados:** web `modulo-web/T-0033-revisao-geral` **94b3440** · faróis `modulo-farois/T-0033-aderencia-cor` **80daf25**.
- **Pedido:** reteste dos 12 retoques (condição do item 7 do R-20261127-005437-alexandre) e das 2 mudanças novas (selo `alerta` claro; `AVISO_CARTOES`).
- **Régua:** os 12 achados C1–C12 do meu parecer de UX sobre a simulação (`16d2e5a`, reteste aprovado em `3c6419d`), mais o `revisao-ux-geral.md`, o `docs/marca/manual.md` e o contrato `tela-bc3.md`.
- **Como medi:**
  - servidor próprio com o código do 94b3440 exportado por `git archive` para uma pasta descartável, fora do clone (porta 8195), com a fixture fictícia dos 5 faróis;
  - sonda Playwright a 1366 e a 390 (toque real), mais 360 em alguns pontos: `reteste-ux/sonda.mjs`, com o resultado em `reteste-ux/sonda.jsonl`;
  - PNG em `reteste-ux/`. Os de "sugerido" são a mesma tela com a correção aplicada só no navegador. Nenhum código foi alterado.
- **Dados:** só fictícios (CLIENTE/VENDEDOR FICTICIO, admin.sim).

## Veredito

**Os 12 retoques estão feitos. A condição do Alexandre foi cumprida. Nenhum 🔴.**
**Há 2 🟡 nas mudanças novas (N1 e N2), a corrigir antes do merge.** Desde o `3c6419d`, nenhum dos 12 voltou atrás.

## Os 12 retoques no 94b3440

| # | Retoque | Situação | Prova |
|---|---|---|---|
| C1 | "Sem filtro por estado" no Visita | ✅ Aparece uma vez só, como texto na linha da data. Não é selo nem botão e não aparece no corpo. O Visita não desenha o seletor de estado | `_bc3_cab.html:13,20` (`sem_uf`). Sonda: `semUf=1`, `.bc3-uf` ausente em todas as abas, a 1366 e a 390. `vc_visitas_vendedor__pc1366.png` |
| C2 | Faixa da mesma altura; seletor cinza nas abas só da BAP | ✅ PC: 88 px em todas as abas dos 5 faróis. Celular: 245 px (Visita 213). Títulos, Cliente, Cobrar e Solicitação mostram `bc3-uf-off`. Exceção nova: o N2 (com estado escolhido, a faixa encolhe no celular) | `sonda.jsonl` (`faixaH`) |
| C3 | Abas em 2 linhas | ✅ Celular: 3 abas + "Mais▾" numa linha só. O "Mais" abre, e o centro de cada item devolve o próprio link (Visita 5 itens, Inadimplência 1, Metas 4, alvos de 44 px). PC: as 8 abas da Visita e as ações cabem numa linha a 1366 | `mais-visita__cel390.png`; linhas `MAIS` da sonda; `linhasAbas=1`. 🟢 que continua: no celular, a aba ativa "Cliente a cliente · 230" quebra o próprio rótulo em 2 linhas, e o "·" fica solto (`vc_visitas_cliente__cel390.png`) |
| C4 | Rótulos dos números cortados | ✅ Nenhum rótulo ou número com reticências. No celular, os rótulos quebram em 2–3 linhas ("ENTREGAS NO / MÊS", "FATURAMENTO · DESAFIO COMERCIAL") | sonda `cortes` (os únicos casos são os itens do "Mais" fechado, que estão ocultos); `pl_entregas_entregas__cel390.png` |
| C5 | Aderência no celular com o % 2× | ✅ "VENDEDOR FICTICIO 01 · 80%", com o número uma vez só | sonda `lista` (aderência, 390) |
| C6 | Aderência sem cor | ✅ Chip por dia e no acumulado, pelo corte 50/80 do PC (`tom_aderencia`/`faixa_aderencia` em `relatorios_nucleo.py`, 80daf25). Verde `#F0F7EC/#2F7D32`, âmbar `#FFF4D6/#8A5A00`, vermelho `#FDECEA/#B42318` | `vc_visitas_aderencia__pc1366.png` |
| C7 | Ordem da GRADE (NF por último) | ✅ No Entregas, NF é a 1ª coluna. Nas Pendências, a ordem é MÊS · NF · CLIENTE…. 🟢 Nos Títulos, a NF saiu do fim e a chave NOME vem primeiro, mas a ordem é a do `cobranca.ORDEM_TELA` (NOME · SALDO · SITUAÇÃO · NF…), e não a tupla da `GRADE` (`tabelas.py:866`): são duas fontes para a mesma ordem. A tela está boa (o saldo ao lado do nome) | `pl_inadimplencia_titulos__pc1366.png`; `main.py:518`, `cobranca.py:69-76` |
| C8 | Total sem rótulo | ✅ "Total" em Vendedor, Dia a dia, Títulos e Aderência. 🟢 que continua: "TOTAL" em maiúsculas no Supervisor e no Metas (vem do pacote) | `vc_visitas_vendedor__pc1366.png`; sonda `totais` |
| C9 | VENDEDOR cortado no Cliente a cliente | ✅ Nome inteiro em todas as linhas | sonda `vcel`; `vc_visitas_cliente__pc1366.png` |
| C10 | "Ver mais 0" e Total do Metas vazio no celular | ✅ Não há "Ver mais 0". A linha mostra "Total · 40% · R$ 2.400" | `vc_meta_equipe-inteira__cel390.png` |
| C11 | Dica da busca cortada no celular | ✅ A busca ocupa a linha inteira. A dica mais longa tem 207 px num campo de 320 px a 390 (e de 290 px a 360). No PC, a busca é o ícone (§5) | sonda2 (`bc`) |
| C12 | "▶ Filtros" com o marcador do navegador | ✅ "Filtros ▾" (aberto: ▴) a 1366, 390 e 360, sem o marcador nativo | sonda2 (`f`) |
| M1 | Fonte de 10 px na Aderência | ✅ (não está entre os 12) O cabeçalho tem 11–12 px | `vc_visitas_aderencia__pc1366.png` |

## As 2 mudanças novas

### N1 🟡 O selo `alerta` (de `#B42318` cheio para `#FDECEA` com `#B42318`): numa grade cheia, ele não chama mais a atenção
- **Onde:** coluna SLA do Entregas (`chip_tom`). No site: `tabelas.PALETA_TOM` (`tabelas.py:187-190`). No PC: `bap_visual.py:1309-1313` (80daf25). No contrato: `relatorio.md:688`.
- **O que se vê:** os PNG `sim-t0033-tons/antes|depois/entregas-entregas__pc1366` e `__cel390`, e o meu `pl_entregas_entregas__pc1366.png`.
  - Antes, os 4 selos vermelhos (5 e 8) eram as únicas manchas fortes da grade, e o olho os achava sem ler.
  - Agora os 4 tons (ok, atenção, alerta, cinza) têm o mesmo peso visual: fundo pastel com texto de 700. O alerta só se distingue lendo a cor do algarismo.
  - A legibilidade está certa (5,75:1, AA), mas a hierarquia não: o alerta precisa ser o que mais pesa na tela.
- **Regras quebradas:**
  - **Um estilo por componente.** O mesmo selo de SLA tem dois desenhos entre os faróis. No Pedidos, o `CHIP_SLA` (`relatorios_nucleo.py`, 80daf25) continua com o vermelho cheio `#B42318/#FFFFFF` para "mais de 4 dias", e o pastel `#FDECEA/#B42318` ficou para o degrau de baixo (4 dias). Assim, o vermelho claro diz "no limite" no Pedidos e "atrasado" no Entregas.
  - **Manual §4.2.** O `--alerta-claro` tem o papel de "fundo da linha em alerta", não de selo. O par branco sobre `--erro` (6,57:1) já está no manual como [VALE].
- **Correção proposta:**
  - `chip_tom` `alerta` = `#B42318` de fundo com `#FFFFFF` de texto, nos 3 lugares: `bap_visual.py:1309-1313`, `tabelas.PALETA_TOM` e `relatorio.md:688`. É o mesmo desenho do degrau "mais de 4 dias" do Pedidos.
  - `ok`, `atencao` e `cinza` ficam no tom claro.
  - A Aderência pode ficar no tom claro: lá o chip é um mapa de calor de %, em todas as células, e o cheio pesaria demais. Isso é uma exceção que o design-de-marca precisa registrar no manual.
  - Depois sugerido: `reteste-ux/sugerido-N1-entregas-alerta-cheio__pc1366.png` e `__cel390.png`. Os 5 e 8 voltam a saltar, e o resto continua calmo.
- **Quem:** decisão do gerente com o **design-de-marca** (paleta). A execução fica com `modulo-farois`, `modulo-web` e `engenheiro-software` (contrato), no mesmo lote, para o PC e o site não divergirem.

### N2 🟡 `AVISO_CARTOES` no lugar dos números quando há estado ou filtro
- **O que se vê:** em Pedidos e Entregas com `&uf=PA`, a faixa perde os números, e entra a linha "Cartões sem filtro. Com filtro, veja as linhas na tabela." (`main.py:388-394`, `_bc3_cab.html:36-37`). Prints: `pv_pedidos_pedidos_PA__pc1366.png` e `pl_entregas_entregas_PA__cel390.png`.
- **O que está certo:**
  - tirar os números da BAP inteira quando a tela está em PA é mais honesto que mostrá-los com a marca "BAP inteira" (era o W1);
  - o Diretor não perde número: no Pedidos ele só vê o Resumo, e o Resumo com estado traz os números do estado (conferido: `?uf=PA` dá 200, com os números de PA, para o admin e para o diretor);
  - no PC, a faixa fica com 88 px.
- **O que quebra:**
  - **Texto que explica o sistema e fala de algo que não está na tela.** O BC3 não tem "cartões" (os números ficam na faixa). "Cartões sem filtro", escrito com um filtro ligado, se lê ao contrário. A frase não diz onde está o número de PA.
  - **Celular: a faixa muda de altura,** de 245 px para 151 px, com estado escolhido (sonda `faixaH`). No PC, a altura fica.
- **Correção proposta:**
  - no lugar do texto, um link curto e acionável para o número que existe: **"Números de PA no Resumo ›"**, apontando para `/farol/<rid>?uf=PA`. Com filtro sem estado: **"Números sem o filtro no Resumo ›"**;
  - o `AVISO_CARTOES` é texto de contrato (`relatorio.md` §10.7.6 e D5; `tela-bc3.md` §4.2 e §9). A troca é do `engenheiro-software` (contrato), do `modulo-web` (`tabelas.py:198` e `main.py`) e do `testes` (`test_T0017…:947-953`);
  - depois sugerido: `reteste-ux/sugerido-N2-pv_pedidos-PA__pc1366.png` e `sugerido-N2-pl_entregas-PA__cel390.png`;
  - a altura no celular fica como 🟢: o seletor de estado não sai do lugar, e só o conteúdo de baixo sobe.

## 🟢 Para depois (não seguram)
- **Filtros abertos com estado.** Com estado escolhido, os "Filtros" abrem sozinhos (`_tabela.html:18`: `open if not tabela.padrao`, e o `padrao` cai com o estado). No celular, a lista desce para cerca de 1.480 px (`pl_entregas_entregas_PA__cel390.png`). Isso já acontecia antes desta leva. Correção: abrir só quando um filtro de dentro do painel mudou.
- **Fixture do Pedidos com os hex antigos.** A fixture traz os hex antigos no SLA (`#B3261E`, `#FBDDDA`, `#FFF1C7`, `#E5F3DF`), e o PNG do Pedidos não mostra o que o PC novo (80daf25) vai mandar. Atualize o `farol_fixture` antes da próxima simulação.
- **Detalhes de rótulo e alinhamento:**
  - "Mais▾" sem espaço (o "Filtros ▾" tem espaço);
  - o cabeçalho "VENDEDOR" da Aderência está centralizado, e a coluna está à esquerda;
  - sobram ~70 px vazios no pé da faixa do Visita no celular.
- **C7 dos Títulos:** uma fonte só para a ordem (a `GRADE` igual ao `ORDEM_TELA`, ou o inverso). Assunto do corretor-redundancias.

## Para o gerente
- Os 12 retoques fecham a condição do Alexandre.
- Para o merge, ficam N1 e N2. N1 depende da palavra do design-de-marca. Se a decisão for manter o alerta claro, ela vai como decisão registrada (com o print do depois para o Alexandre), e a diferença com o Pedidos precisa ser resolvida do mesmo jeito.
