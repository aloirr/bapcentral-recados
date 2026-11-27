# T-0037 · Farol de Fretes · parecer de UX, redundância e marca da simulação v2

- **Revisor:** designer-ux · 27/11/2026 (Manaus)
- **Head revisado:** `modulo-web/T-0037-fretes` **b2845e6** (0.9.0). Começou em bd057b7; o b2845e6 só muda o rótulo da cidade sem UF na fixture, espelhando o robô 4370d2d.
- **PNGs revisados:** os 14 de `sim-v2/`, na versão refeita às 10:48.
- **Simulação própria:** gerada com a fixture no b2845e6, com `paginas()` do `simular_farol.py` e Playwright, em 1366 px e 390 px. Mede a largura, os alvos de toque, o tamanho do texto e as cores.

**Veredito: não aprovado. 1 🔴, 6 🟡 e 10 🟢.**

## O que está conforme
- **Largura:** nenhuma rolagem para o lado. O `scrollWidth` dá 1366/390 nas 7 telas: Resumo, Notas, UF, Cidade, Transportadora, Editar e Resumo do PA.
- **Alvos de 44 px no celular:**
  - abas: 104/110/71 × 44;
  - "Mais" aberto: Cidade e Transportadora com 146 × 44;
  - busca: 362 × 44; Exportar: 96 × 44;
  - linha da lista: 360 × 44; Editar: 50 × 44; Salvar e Cancelar ≥ 44.
- **Números no formato brasileiro:** R$ 47.750, R$ 2,6 mil, 7,2%, 3,0% do valor e datas dd/mm/aaaa. A exceção é o 🟡 A7.
- **Os totais batem.** As 3 tabelas somam 9 notas, R$ 85.950 e R$ 2.565:
  - UF: 5+3+1;
  - cidade: 3+2+2+1+1;
  - transportadora: 3+2+2+2.
- **Os totais batem com os cartões:** 9, R$ 86 mil, R$ 2,6 mil e 3,0%. Eles também batem com a aba Notas: o frete de 249 a 321 soma 2.565. Em "Entregues 3 · 67% no prazo", as notas 700102 e 700106 estão no prazo e a 700109 atrasou 1 dia.
- **Marca:** a tela-bc3 está igual nas 7 telas, com a placa preta e o logo inteiro, "BAP AUTOPARTS", a faixa `--faixa-inicio`→`--faixa-fim` em texto branco e um só carimbo de hora ("24/11/2026 08:30").
  - O diff de CSS da T-0037 só traz o `white-space:nowrap` em `.ed-marca`, sem hex novo.
  - O único hex fora dos tokens é o do gráfico (🔴 R1).
- **Dados fictícios:**
  - CLIENTE TESTE nn, códigos 9000nn;
  - FILIAL FICTICIA, MOTORISTA FICTICIO n;
  - cidades e transportadoras inventadas, admin.sim.
  - Sem CNPJ, telefone ou e-mail.
- **Edição:** só o admin vê "Editar", com os 5 campos. A nota sem chave mostra "—" com dica no PC e "Não edita na web." no celular.

## 🔴 Bloqueia o merge
### R1 · Resumo, gráfico "Mês a mês": as barras estão em azul, fora da paleta
- **O que se vê:** barras `#2F6FB5` no PC e no celular (01-resumo).
- **De onde vem a cor:**
  - O robô manda `AZUL = "#1F4FD1"` (`relatorios_nucleo.py`, gráfico do Fretes; a mesma constante está no SLA e no "% parcial").
  - O manual (§4.2) diz que esse azul "fica só" no selo NOVO do catálogo.
  - A web aceita qualquer hex da série: `render._cor` só confere o formato `#RRGGBB`.
- **Regra:** manual da marca §4.2 (`--grafico-1/2/3`) e checklist ("cor de série neutra `#8FA79A`").
- **Correção:**
  - **modulo-web:** em `_bloco_barras` e `_bloco_hbarras`, aceitar só hex que esteja em `marca.TOKENS.values()`. Qualquer outro vira `--grafico-3` (`#8FA79A`). Isso protege também os outros faróis que recebem o `AZUL`.
  - **modulo-farois:** em `relatorios_nucleo.py`, trocar o `AZUL` das séries por `#8FA79A`.
  - **Fixture:** usar a mesma cor do robô (hoje `#2F6FB5`, que não é a do robô).
- **Antes:** `sim-v2/01-resumo-pc.png`. **Depois:** `revisao-ux-sim-v2/depois-resumo-pc.png` e `-cel.png`.

## 🟡 Corrigir antes do merge
### A1 · Resumo (PC): o gráfico fica estreito. Resposta à pergunta: é 🟡
- **Medição:** com tela de 1366 px, o gráfico tem 157 px de largura.
  - Os rótulos dos meses ficam em pé, com 9,9 px, e só aparece um mês a cada dois.
  - Os valores ficam em pé, com 9,3 px.
  - Sobra uma área vazia de mais de 1.000 px à direita.
- **Regras quebradas:**
  - texto ≥ 12 px no computador;
  - tamanho mínimo de 11 px do manual (§5);
  - "nada de rótulo girado quando dá para evitar".
- **Causa:**
  - `.bc3 .graficos` usa `auto-fit minmax(165px,1fr)` e as tabelas ocupam a linha inteira (`.graf-tab{grid-column:1/-1}`). O gráfico fica sozinho numa trilha de 165 px.
  - O `colspan: 3` que o robô manda é ignorado.
  - O `rotv`/`vert` é decidido pela quantidade de colunas, não pela largura.
- **Correção (modulo-web):**
  - Respeitar o `colspan` do bloco ou pôr `grid-column:1/-1` no gráfico que divide a seção só com tabelas.
  - No gráfico largo, deixar os rótulos e os valores deitados, com ≥ 12 px, e mostrar todos os meses ("DEZ/25 … NOV/26").
  - No celular, usar 3 letras deitadas com 11 px ("DEZ JAN … NOV"). Cabe em 390 px (ver o depois).

### A2 · Resumo: "Sem transportadora" mostra 1 no cartão e 2 na tabela, na mesma tela
- **Por quê:** o cartão (PC, `kpis`: `l[16] and not l[11]`) deixa de fora a nota "(sem acompanhamento)" (700101). A tabela "Por transportadora" agrupa pela transportadora vazia e soma as duas notas.
- **Efeito:** o Diretor vê dois números diferentes com o mesmo nome.
- **Regra:** o mesmo rótulo não pode ter dois números; o número do Diretor tem de ser coerente na tela.
- **Correção (o po decide a regra):**
  - **Recomendada (modulo-farois + modulo-robo):** a tabela "Por transportadora" separa uma linha "Sem acompanhamento" (1 · R$ 8.310 · R$ 249). "Sem transportadora" fica com 1, igual ao cartão. O total não muda (ver o depois).
  - **Alternativa:** o cartão passa a contar as duas notas. Isso muda a regra do cartão no PC.

### A3 · Os rótulos "sem" diferem entre o Resumo e as abas, e a aba Cidade ainda tem a barra solta
- **Conferi no 04-aba-cidade refeito às 10:48.** No PC e no celular, a aba Cidade **ainda mostra "SERRA BONITA /"** e "(sem) / MA". O arquivo é o mesmo de antes (mesmo tamanho em bytes) e eu reproduzi o resultado no b2845e6.
  - A correção do robô 4370d2d só vale para o Resumo (`_rotulo_sem_fretes_web`).
  - A aba vem da tabela do PC: `relatorios_nucleo.py`, l. 8101, `(l[i] or "(sem)") + (f" / {l[7]}" if i == 6 else "")`.
- **As abas UF, Cidade e Transportadora usam "(sem)"; o Resumo usa "Sem UF", "Sem cidade" e "Sem transportadora".** A mesma coisa tem dois nomes.
- **No Resumo:** "SERRA BONITA" logo abaixo de "SERRA BONITA / PA" parece linha repetida.
- **Correção (modulo-farois, na origem, para valer no PC, no Resumo e nas abas):**
  - cidade sem UF: "SERRA BONITA / Sem UF";
  - nota sem cidade: "Sem cidade / MA";
  - nas abas, "Sem UF" e "Sem transportadora".
  - Depois disso, o `_rotulo_sem_fretes_web` do robô fica só como garantia.

### A4 · Resumo gerencial: as frases repetem os números da tabela logo abaixo
- **O que se repete:**
  - "5 das 9 notas" e "(R$ 47.750)" já estão na linha PA e no cartão;
  - "R$ 28.960 em 3 notas" já está na linha TRANSP. GAMA.
- **Regra:** o mesmo número não aparece duas vezes na tela.
- **Correção (modulo-robo, `blocos_resumo_fretes_web`):** a frase fica só com o que é novo, a participação.
  - "PA concentra 56% do valor das notas com frete."
  - "TRANSP. GAMA leva 34% do valor."
  - Ver o depois.

### A5 · Popup da nota: o título sai "Nf 700101"
- **Onde:** `_grade.html`, `data-tit="{{ tab.cols[pc].nome|capitalize }} …"`. O filtro transforma a sigla "NF" em "Nf".
- **Correção (modulo-web):** não usar `capitalize` em sigla, ou não usar em nenhum título. Deve sair "NF 700101".
- **Alcance:** a mesma grade serve os outros faróis, e a correção é de uma linha.

### A6 · Simulação (07-editar): a data aparece "11/10/2026"
- **O que acontece:** o valor salvo é `2026-11-10` (10/11). O campo de data do Chromium sem `--lang` desenha no formato americano. O po e o Alexandre leriam 11 de outubro.
- **Correção (quem gera a simulação):** refazer o 07 com as opções do `web/simular_png.mjs`: `args:['--lang=pt-BR']` e `env LANG=pt_BR.UTF-8`.
- **Teste:** com essas opções, a data sai "10/11/2026" (`revisao-ux-sim-v2/data-editar-antes-depois.png`: em cima, como saiu; embaixo, como deve sair).
- **Alcance:** não é erro do site. No Chrome do usuário em pt-BR, a data já sai certa.

## 🟢 Sugestões (para depois)
1. **TOTAL nas 3 tabelas:** o 9 / R$ 85.950 / R$ 2.565 aparece três vezes, e também nos cartões. Fica, porque espelha o PC e serve de conferência. A opção é deixar o TOTAL só na primeira tabela.
2. **Linhas "Sem …":** ficariam sempre no fim, antes do TOTAL. Hoje "Sem transportadora" cai no meio, porque a ordem é pelo valor.
3. **Cartão "Cidades atendidas":**
   - O PC (`len({l[6] for l in ls})`, já no `main`) conta a cidade vazia como uma cidade.
   - Aqui dá 4 por coincidência; sem a vazia seriam 3 cidades.
   - É uma pergunta de regra para o po, com o modulo-farois. Não muda este PR, porque o número bate com o farol de origem.
4. **Faixa das abas UF, Cidade e Transportadora:**
   - Os 3 cartões dizem "NOTAS" onde o Resumo diz "NOTAS COM FRETE". O mesmo número deveria ter o mesmo nome.
   - No celular sobram ~50 px de verde vazio: `.bc3-ks{min-height:112px}` com uma linha só de cartões.
5. **Celular:** o rótulo "SEM TRANSPORTA-DORA" quebra em 3 linhas. A sugestão é "SEM TRANSP.".
6. **Tela de edição:**
   - A dica "Apague a data para voltar à calculada pelo PC." aparece duas vezes. Na DT. REAL ela não faz sentido, porque a data real não é calculada; fica só na DT. PREVISTA.
   - A linha do topo tem duas datas sem rótulo ("03/11/2026 · 04/11/2026"). A sugestão é "NF 700102 · CLIENTE TESTE 02 · SERRA BONITA/PA".
   - A lista tem fundo cinza e o campo de texto tem fundo branco. Isso vem do componente comum.
7. **Linha atrasada (700104):** só a cor vermelha avisa que está atrasada. A sugestão é um selo "Atrasada" (cor + texto), no padrão comum com o Entregas.
8. **Barra NOV/26:** é mês parcial (até 24/11) e aparece igual aos meses fechados. A sugestão é "NOV/26 (parcial)" ou um tom mais claro.
9. **Resumo no PC:**
   - O cartão "Por UF" sobra ~110 px vazio embaixo, por causa do `min-height:280px` em `.bc3 .graficos .graf`.
   - As tabelas de 4 colunas na largura toda ficam com vãos grandes. A opção é pôr as 3 tabelas lado a lado a partir de 1280 px.
10. **Componentes comuns no celular** (vêm de antes e valem para todos os faróis): os itens do Exportar têm 32 px, as listas dos Filtros 37 px e o botão Filtrar 40 px. Todos ficam abaixo de 44 px.

## Anexos (dados fictícios)
- **Antes:** `recados/anexos/T-0037/sim-v2/*.png` (os 14, versão das 10:48).
- **Depois sugerido:**
  - `recados/anexos/T-0037/revisao-ux-sim-v2/depois-resumo-pc.png` e `depois-resumo-cel.png`: R1, A1, A2 (opção recomendada), A3 (Resumo) e A4. São os mesmos dados da fixture, com CSS e textos aplicados só na simulação.
  - `recados/anexos/T-0037/revisao-ux-sim-v2/data-editar-antes-depois.png`: A6.

## Para quem vai cada item
| Item | Dono |
|---|---|
| R1 | modulo-web (`render.py`) + modulo-farois (`relatorios_nucleo.py`) |
| A1, A5 | modulo-web |
| A2, A3 | modulo-farois (+ modulo-robo no rótulo); o po decide a regra do A2 |
| A4 | modulo-robo |
| A6 | quem gera a simulação |

---

# Reteste · 27/11/2026 (Manaus)
- **O que foi conferido:** os 14 PNGs de `sim-v2/` refeitos às 11:05, a partir da web **7f246ab**, dos faróis **48c6577** e do robô **91e6f8a**.
- **Como:** com uma simulação própria da fixture no 7f246ab, medida no Playwright em 1366, 390 e 360 px.

**Veredito do reteste: ainda não aprovado. São 0 🔴 e 2 🟡, os dois de correção curta no modulo-web.**

## O que foi corrigido
| Item | Situação | Como conferi |
|---|---|---|
| R1 | ✓ | As barras saem `#8FA79A` (`--grafico-3`). `render._cor` só aceita hex de `marca.TOKENS` |
| A1 (PC) | ✓ | O gráfico ocupa a largura toda (1110 px na tela de 1366). Os 12 meses aparecem deitados com 12 px, e os valores com 12 px |
| A2 | ✓ | O cartão "Sem transportadora" mostra 1 e a linha da tabela também. "Sem acompanhamento" (1 · R$ 8.310 · R$ 249) tem linha própria e o TOTAL continua 9 / R$ 85.950 / R$ 2.565 |
| A3 | ✓ | Resumo e abas usam os mesmos rótulos: "Sem UF", "SERRA BONITA / Sem UF", "Sem cidade / MA", "Sem transportadora" e "Sem acompanhamento". Conferi o 04-aba-cidade no PC e no celular |
| A4 | ✓ | As frases são "PA concentra 56% do valor das notas com frete." e "TRANSP. GAMA leva 34% do valor." |
| A5 | ✓ | O título do popup é `data-tit="NF 700101"` |
| A6 | ✓ | O 07-editar mostra 10/11/2026 no PC e no celular |
| 🟢 2 | ✓ | As linhas "Sem …" ficam no fim da tabela, antes do TOTAL |

**Continua conforme:**
- nenhuma rolagem para o lado nas 7 telas (1366 e 390);
- alvos de 44 px no celular;
- totais batendo com os cartões e com a aba Notas;
- só dados fictícios.

## 🟡 Novos
### A7 · Resumo no celular: "NOV" cortado e meses encostados (o aviso do autor se confirma)
- **O que acontece:** a 390 px cada mês tem 24 px de largura, mas o rótulo sai com **12 px**, não com os 11 px pretendidos.
  - "MAR" precisa de 27 px e "NOV" de 26 px.
  - Como `.gb.gb-larga` tem `overflow:hidden`, o "NOV" (o mês corrente) perde o "V" na borda do cartão.
  - "MAR" encosta em "ABR".
  - A 360 px fica pior: "MARABR", "AGOSET" e "NO" cortado.
- **Causa:** a regra do celular `.gb-larga .gb-rot{font-size:11px}` perde para `.bc3 .graf .gb.gb-larga .gb-rot{font-size:12px}`, que é mais específica. Além disso, o cartão do gráfico no celular tem só 6 px de padding.
- **Correção (modulo-web, `estilo.css`, no `@media` do celular):**
  - `.bc3 .graf .gb.gb-larga .gb-rot{font-size:11px}`, com a mesma especificidade;
  - `.bc3 .graf .gb.gb-larga{overflow:visible}`;
  - `.bc3 .graficos .graf{padding:0 12px}`;
  - a partir do último mês, um rótulo sim e um não (`.gb-col:nth-last-child(even) .gb-rot{visibility:hidden}`): ficam NOV, SET, JUL, MAI, MAR e JAN. O mês corrente sempre aparece e nenhum rótulo encosta no outro, nem a 360 px.
  - Medido: o "NOV" termina em 365 px, dentro do cartão (376 px menos 12 px de padding).
- **Antes:** `revisao-ux-sim-v2/reteste-grafico-cel-390-antes.png` e `-360-antes.png`. **Depois:** `…-390-depois.png` e `…-360-depois.png`.

### A8 · Efeito do R1 em outros faróis: a barra amarela de "atenção" vira cinza-verde
- **O que acontece:** o filtro novo do `_cor` manda para `--grafico-3` tudo o que não é token. O `AMARELO #C98A00` do PC não é token.
  - Testei `render._bloco_hbarras` com `cores=[#59BA61, #C98A00, #B42318]`: sai `[#59BA61, #8FA79A, #B42318]`.
- **Faróis atingidos:**
  - atingimento por trimestre do Painel e de Metas (`relatorios_nucleo.py` ~4507, `{"ok": VERDE, "atencao": AMARELO, "alerta": VERMELHO}`);
  - ocupação, dia e sábado da rota (~5307 a 5340);
  - situação dos clientes, nos CHURN 60/90.
- **Efeito:** a barra em atenção fica igual a uma barra neutra e o estado se perde.
- **Por que antes não acontecia:** o mapeamento em CSS (`estilo.css` l. 320, `i[style*="C98A00"] → --grafico-2`) virou código morto, porque a cor já chega trocada.
- **Regra quebrada:** "cor só com significado: âmbar = atenção". Não é 🔴, porque nenhuma cor fora da marca aparece.
- **Correção (modulo-web, `render._cor`):** antes do filtro, traduzir as cores antigas do PC para o token do mesmo papel. Depois disso, a regra da l. 320 pode sair.
  - `#C98A00` → `--grafico-2` (o que o CSS fazia e o Alexandre já viu);
  - `#62BB47` → `--verde-marca`;
  - `#B3261E` → `--alerta`;
  - `#A7B0AA` e `AZUL` → `--grafico-3`.
- **Teste:** um caso de `hbarras` com ok, atenção e alerta.

## 🟢 Novo e o que segue aberto
- **Novo:**
  - A etapa e o filtro ETAPA da aba Notas ainda dizem "(sem acompanhamento)", entre parênteses e em minúsculas. A linha da tabela diz "Sem acompanhamento". Vale alinhar no PC.
  - O gráfico do próprio PC (Tkinter/PDF) do Fretes ainda usa o `AZUL #1F4FD1` (`relatorios_nucleo.py` l. 8116). A web já neutraliza; no PC fica para a limpeza da marca (MC-0006).
- **Seguem abertos os 🟢 1 e 3 a 10 do parecer acima.** Nenhum bloqueia.

## Anexos do reteste
- `recados/anexos/T-0037/revisao-ux-sim-v2/reteste-grafico-cel-390-antes.png`
- `recados/anexos/T-0037/revisao-ux-sim-v2/reteste-grafico-cel-390-depois.png`
- `recados/anexos/T-0037/revisao-ux-sim-v2/reteste-grafico-cel-360-antes.png`
- `recados/anexos/T-0037/revisao-ux-sim-v2/reteste-grafico-cel-360-depois.png`
- Todos com dados da fixture. O "depois" é só CSS aplicado na simulação.

---

# Reteste 2 · 27/11/2026 (Manaus)
- **O que foi conferido:** web **2274cb2** e os PNGs novos de `sim-v2/` (11:15): `01-resumo-cel.png` (390), `01-resumo-cel-360.png` e `08-rota-barras-de-estado-cel.png`.
- **Simulação própria:** a fixture no 2274cb2, medida a 390 e a 360 px.
- **Testes:** `test_T0037_fretes.py` dá 20 passed (com `PYTHONPATH=..`, porque a fixture importa o `relatorios_nucleo` da raiz).

**Veredito: APROVADO. Não há 🔴 nem 🟡 em aberto.**

## O que foi corrigido
| Item | Situação | Como conferi |
|---|---|---|
| A7 | ✓ | **A 390 px:** os rótulos têm 11 px e aparece um mês sim, um não, contando do último: JAN, MAR, MAI, JUL, SET e NOV. O "NOV" sai inteiro e nenhum rótulo encosta no outro. **A 360 px:** o "NOV" também fica inteiro, dentro do padding de 12 px do cartão. O `scrollWidth` é 390/360 |
| A8 | ✓ | `marca.COR_PC` traduz a cor antiga antes do filtro. **Atingimento do Painel:** chamei `_bloco_hbarras` com as cores que o PC manda (`{"ok": VERDE, "atencao": AMARELO, "alerta": VERMELHO, "neutro": CINZA}`) e saiu `#59BA61`, `#D8B56E`, `#B42318` e `#8FA79A`, quatro estados distintos. **Rota (08):** no "Visitas no sábado", o âmbar volta como `--grafico-2` e o vermelho (acima do teto) continua vermelho. O teste `test_UX_A8_…` cobre ok, atenção, alerta e neutro. **CHURN:** não há fixture de barras por situação. O caminho é o mesmo `_cor` dos cartões acima (CHURN 60/90 = AMARELO → `--grafico-2`) |

## Tabelas do Resumo a 360 px: é 🟢, não 🟡
- **O que se vê:**
  - o cabeçalho quebra no meio da palavra ("NOTA S");
  - os valores quebram em duas linhas ("R$" / "85.950" no TOTAL e "R$" / "29.580");
  - "SERRA BONITA / Sem UF" ocupa duas linhas, o que é aceitável.
- **O que não acontece:** nada passa da largura (`scrollWidth` 360) e nenhum número some.
- **Por que 🟢:**
  - A largura de referência do celular é 390 px, e lá as tabelas estão certas.
  - A regra que quebra é a `estilo.css` l. 607 (`.graf-tab .tab-dados th, td {white-space:normal; overflow-wrap:anywhere}`). Ela já está no `main` e vale para todas as tabelas de Resumo dos faróis; não nasceu neste PR.
- **Correção (modulo-web, pode entrar já, ou numa tarefa curta).** Testada a 360 px: as 3 tabelas cabem (304/304 px), os números e o cabeçalho ficam numa linha só, e só o nome da cidade quebra.
  ```css
  @media(max-width:700px){
    .graf-tab .tab-dados th,.graf-tab .tab-dados td{overflow-wrap:normal;word-break:normal}
    .graf-tab .tab-dados th,.graf-tab .tab-dados td.num{white-space:nowrap}
  }
  ```
- **Antes:** `revisao-ux-sim-v2/reteste2-tabela-cel-360-antes.png`. **Depois:** `…-360-depois.png`.

## 🟢 Novo
- **O "um rótulo sim, um não" vale para qualquer gráfico `gb-larga`, não só para meses.** Hoje só fica largo o gráfico que é o único da tela (`render.py` ~630), então o efeito é raro. Mas um farol livre com um só gráfico de categorias (ex.: AM, AP, MA, MT, PA, RR) perderia metade dos nomes no celular.
- **Sugestão:** aplicar o esconde-alterna só quando os rótulos são meses (o `rot_c` difere do `rot`) e há mais de 8 colunas. Por exemplo, uma classe `gb-meses` posta pelo `render`.
- **Seguem abertos e não bloqueiam:** os 🟢 1 e 3–10 do parecer e os dois 🟢 do reteste 1 ("(sem acompanhamento)" na ETAPA; AZUL no gráfico do PC).

## Anexos do reteste 2
- `recados/anexos/T-0037/revisao-ux-sim-v2/reteste2-tabela-cel-360-antes.png`
- `recados/anexos/T-0037/revisao-ux-sim-v2/reteste2-tabela-cel-360-depois.png`
- Os dois com dados da fixture. O "depois" é só CSS aplicado na simulação.
