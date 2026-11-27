# T-0023 v2 · Revisão de UX e marca (designer-ux)

- **Branch:** `modulo-web/T-0023-web` · **head revisado:** `3cc4fe06cfeff7a9d494fdfa71a74acb83d6730b`.
- **Telas:** os Faróis de Garantias, de Devoluções e de NCC, a Garantia nova e a edição da NCC. São os PNGs 01 a 05 da simulação, em `-pc` e `-cel`. Também conferi o Resumo dos 3 faróis, que é a única tela que o Diretor vê (RN-GER-014) e que ficou fora da simulação.
- **Régua usada:** o contrato `tela-bc3.md` v1 (§N) e o `docs/marca/manual.md` (§4 e §5).
- **Como medi:**
  - abri os 10 PNGs da simulação;
  - montei de novo as 8 telas com a fixture fictícia (`posvenda_fixture.pacote_posvenda`), por um teste local num clone só de leitura;
  - medi no Playwright, a 1366×768 e a 390×844, a largura de cada caixa, a altura da página, a altura de cada alvo de toque, o tamanho da letra e o rótulo que passa da própria caixa.
  - Nenhum dado real foi usado.
- **Resultado:** **🔴 2 · 🟡 7 · 🟢 9.** Não vai ao po como está.

## O que está certo

- **Marca:**
  - "BAP AUTOPARTS" na lateral e no `<title>` ("… · BAP AUTOPARTS");
  - o logo na `.bc3-marca`;
  - a faixa com o degradê `--faixa-inicio` → `--faixa-fim` e o texto branco;
  - os números em farol com `--faixa-alerta`, `--faixa-atencao` e `--faixa-ok`, sempre em número grande e negrito (3,01:1 ou mais no pior ponto, manual §4.3);
  - os selos da grade nos pares `--ok`/`--ok-claro`, `--atencao-texto`/`--atencao-claro` e `--alerta`/`--alerta-claro`;
  - o diff do `estilo.css` só usa `var()`, sem hex novo fora do `:root`.
- **Grade (§6.2):**
  - Garantias com 9 colunas, Devoluções com 10 e NCC com 10, mais o Editar à esquerda;
  - chave sublinhada;
  - nenhuma rolagem lateral nas grades, a 1366 e a 390.
- **Faixa:** 88 px a 1366 em todas as abas (§4.1). As abas de tabela dos 3 faróis cabem em 1366×768, sem rolar a página.
- **Um botão principal por tela (§11):** "Nova garantia" no farol e "Salvar" nos formulários.
- **3 toques no PC:**
  - Garantia nova: lateral → aba Garantias → "Nova garantia";
  - edição da NCC: lateral → Pendentes → "Editar".
- **Dado pessoal:** nas 8 telas, nenhum CNPJ, CPF, e-mail, telefone ou "contato". O formulário avisa nos textos livres. A fixture é toda fictícia.
- **Os números batem entre a faixa, as abas e os cartões:**
  - **Garantias:** 6 em aberto, 3 sem tratativa, 3 atrasadas, 6 com análise pendente, 4 procedentes, 2 improcedentes. A média de SLA das 6 finalizadas é 117 ÷ 6 = 19,5, que aparece como 20 dias. No Resumo, os produtos somam 12.
  - **Devoluções:** 10 notas, R$ 12.250 (aparece como R$ 12,2 mil), 10 clientes, 7 em acompanhamento e 3 sem motivo.
  - **NCC:**
    - saldo de R$ 13.295 (aparece como R$ 13,3 mil), em 11 NCC de 6 clientes;
    - "Compensar já" de R$ 4.935, de 4 clientes;
    - acima de 90 dias, R$ 6.738 em 6 NCC;
    - 10 com SLA atrasado;
    - as barras por estado e por faixa de idade batem com a grade, com até R$ 1 de diferença, que vem dos centavos da fixture.
  - A única exceção é o gráfico do Resumo das Devoluções (🟡 A6).
- **Seletor de data em dd/mm/aaaa: comprovado.** O Chromium completo (`channel: 'chromium'`), com `LANG=pt_BR.UTF-8` e `--lang=pt-BR`, mostra "27/11/2026" e "dd/mm/aaaa". O headless shell, com a mesma configuração, ainda mostra "dd/mm/yyyy". O mm/dd dos PNGs vem só da ferramenta. Ver `ux-data-ptbr-cel.png` e `ux-depois-garantia-nova-pc.png`.

## 🔴 Bloqueia

### R1 · NCC, celular: o recorte passa da largura e corta "Acima de 90 dias (6)"
- **Tela:** 03-cel (aba Pendentes).
- **Elemento:** `nav.filtros.recortes`.
- **Regra quebrada:** a §8 ("nenhuma rolagem lateral em 390 px, `scrollWidth ≤ clientWidth` em toda caixa"), a §15.1 e "nada cortado".
  - **Medido:** 430 px de conteúdo numa caixa de 362 px.
  - A barra de rolagem está escondida (`scrollbar-width: none`), então nada indica que existe um terceiro recorte.
- **Origem:** `estilo.css:644`, regra do celular que vem da T-0024. Esta é a primeira tela em que os chips não cabem.
- **Correção:** no `@media(max-width:700px)`, trocar `flex-wrap:nowrap;overflow-x:auto` por `flex-wrap:wrap;overflow-x:visible`. Os chips passam para a linha de baixo. Medido depois: 362/362.
- **PNG:** `ux-antes-ncc-recortes-cel.png` → `ux-depois-ncc-recortes-cel.png`.

### R2 · Devoluções, celular: "ABERTAS NO ACOMPANHAMENTO" vaza e encosta no "3" de "Sem motivo"
- **Telas:** 02-cel e o Resumo no celular, que é a tela do Diretor.
- **Elemento:** o rótulo `.bc3-k small` da faixa.
- **Regra quebrada:** "nada cortado" e o rótulo curto da §8. Lido de relance, o cartão vira "ACOMPANHAMENTO3".
  - **Medido:** 118 px de texto numa coluna de 102 px.
- **Correção:** no `@media(max-width:700px)`, `.bc3-k small{hyphens:auto;overflow-wrap:anywhere}`. O `<html lang="pt-BR">` já está lá, então a palavra se divide em "ACOMPANHA-MENTO". Medido depois: nenhum rótulo vaza. Outra saída é um rótulo curto, só na exibição (§13): "Em acompanhamento".
- **PNG:** `ux-antes-devolucoes-faixa-cel.png` → `ux-depois-devolucoes-faixa-cel.png`.

## 🟡 Corrigir antes do merge

### A1 · Garantia nova: a página rola no PC (1.804 px a 1366×768)
- **Tela:** 04-pc.
- **Regra quebrada:** a §1.2 e a §7.4. O formulário só pode rolar no celular, e "uma tela nova que precise rolar volta ao designer-ux". O cartão usa 560 px e deixa 2/3 da tela vazios.
- **Correção:** de 701 px para cima, o `.bc3-corpo .caixa.ed-form` vira uma grade de 4 colunas:
  - os 10 campos curtos em 4 colunas;
  - os 4 textos livres ocupando 2 colunas cada;
  - `max-width:none` no cartão.
  - Medido depois: 768 px, cabe.
- **PNG:** `ux-depois-garantia-nova-pc.png`. O 04-pc é o antes.

### A2 · Alvos de toque abaixo de 44 px no celular
- **Telas:** 04-cel, 05-cel e a linha aberta dos 3 faróis.
- **Regra quebrada:** §8 e §15.7.
- **Medido:**
  - "Salvar": 40 px;
  - "Cancelar": 22 px;
  - campos de 38 a 40 px;
  - "Editar" dentro da linha aberta: **20 px**, no fim do bloco (`ux-antes-ncc-editar-cel.png`).
- **Correção:**
  - no `@media(max-width:700px)`: `.ed-botoes button,.ed-botoes a,.bc3-ed a.bt-ed,.ed-campo input,.ed-campo select{min-height:44px}`;
  - "Cancelar" como botão neutro (contorno `--borda`, texto `--texto`, §11) em vez de link sublinhado.

### A3 · A edição da NCC não diz qual NCC está sendo editada
- **Tela:** 05.
- **O que aparece:** a linha "COMPENSAR JÁ (TÍTULO ABERTO) · NO SLA · 20/11/2026 · 2 · 0-30 DIAS · FILIAL PA".
  - São as 6 primeiras colunas do pacote (`main.py` `form_ctx`, `[:6]`).
  - Repete os 2 campos do próprio formulário (A COMPENSAR e DT. ÚLT. MOV.).
  - Mostra um "2" sem rótulo.
  - Não mostra o número da NCC nem o cliente.
- **Regra quebrada:** a hierarquia (o usuário não sabe o que está editando) e a redundância.
- **Correção:** montar o resumo pela `GRADE` (a chave e o nome da `cel`, mais a UF) e tirar as colunas que já são campos do formulário: "NCC 901 · CLIENTE FICTICIO 01 · PA". A Garantia e as Devoluções já mostram o TICKET e a NF por acaso da ordem; a regra deve valer para as 3.

### A4 · O aviso de dado pessoal aparece 4 vezes na Garantia nova
- **Tela:** 04.
- **O que aparece:** "até 600 caracteres · sem CPF, CNPJ, telefone ou e-mail" embaixo de cada um dos 4 textos livres.
- **Correção:** uma linha só, acima do grupo de textos livres ou no primeiro deles. É o que o `ux-depois-garantia-nova-pc.png` mostra.
- Confirmo no PNG o RD-0143 ("linha nova" repete "Nova garantia") e o RD-0144 ("Sugestão do PC: G-0013" embaixo do campo já preenchido com G-0013), do corretor-redundancias. Não conto os 2 de novo aqui.

### A5 · O PNG 01 mostra valores e cores que o PC não produz
- **Tela:** 01, linhas finalizadas.
- **O que a fixture faz:** põe "FINALIZADA" no PRAZO e o SLA em verde.
- **O que o PC faz:** `garantias.situacao` grava "FECHADA NO PRAZO" ou "FECHADA COM ATRASO" e o tom `cinza` ("o SLA parou de contar").
- **Efeito:** o po aprovaria uma tela em que STATUS e PRAZO repetem "FINALIZADA" em 6 linhas e com um verde que não vai existir.
- **Correção:** em `posvenda_fixture.garantias_registros`, usar o vocabulário e os tons de `garantias.situacao` e gerar o 01 de novo.

### A6 · O Resumo, que é a tela do Diretor, ficou fora da simulação e tem 3 problemas
1. **NCC:** a página rola no PC (827 px a 1366×768, §1.2). Para caber, o "Resumo gerencial" pode ficar ao lado do cartão "Saldo a compensar".
2. **Devoluções:** o gráfico "Devolvido por vendedor (R$)" soma **R$ 16.450**, porque pega 12 meses, OUT e NOV. Ao lado, a faixa diz **R$ 12,2 mil**, só de NOV, e o título não diz o período.
   - O Resumo do PC é outro: "Valor devolvido (R$)" no tempo (`relatorios_nucleo.py:7747`). Esse gráfico é invenção da fixture.
   - O "Resumo gerencial" ("Valor devolvido: R$ 12,2 mil…") repete o número da faixa na mesma tela.
3. **Barras verdes:** a fixture manda `"cores": ["#62BB47"]`. É o verde antigo, que sai da paleta pelo manual §4.2, e verde ali parece "bom". O PC (`painel_farol.ranking`) não manda cor, e a web desenha em `--grafico-3`.
- **Correção:**
  - deixar o painel da fixture igual ao do PC, sem `cores` e com os títulos e o período do PC;
  - fazer o Resumo da NCC caber em 768;
  - tirar a linha do Resumo gerencial que repete a faixa (se a linha vier do PC, recado ao modulo-farois);
  - incluir os 3 Resumos (`-pc` e `-cel`) no pacote para o po.

### A7 · Devoluções: o código do cliente ocupa o espaço do nome
- **Telas:** 02-pc e 02-cel.
- **O que aparece:** a coluna CLIENTE traz "900001 - CLIENTE FICTICI…". O código gasta o corte de 18ch, e no celular sobra "900002 - CLI…".
- **Regra:** a §6.3 (no Entregas, "CLIENTE (só o nome)") e a §6.1.4 (a linha fechada mostra o nome).
- **Correção:** na exibição, a grade e a linha fechada mostram só o nome. O código vai para o popup, no bloco "Nota" ou num bloco "Cliente".

## 🟢 Para depois

1. **Garantias, celular:** a linha fechada não mostra se a garantia está atrasada. O selo é o STATUS, e o SLA aparece como "57", sem cor e sem "dias". Sugestão: `cel` com o PRAZO no lugar do selo.
2. **Selos longos no celular:** "SLA ATRASADO" e "EM TRATATIVA" deixam só "CLIENTE…" na linha. Sugestão: "ATRASADO" e "TRATATIVA" na exibição.
3. **Recortes que repetem a faixa:** os chips "Em aberto (6)", "Atrasadas (3)", "SLA atrasado (10)" e "Acima de 90 dias (6)" repetem números da faixa (§1.1). No futuro, o próprio número da faixa pode ser o link do recorte, e a linha de chips sai.
4. **Garantias, celular:** o detalhe "abertas depois da DT. FECHAMENTO" ocupa 3 linhas e deixa a faixa com 262 px. Sugestão: "após o prazo".
5. **"Sem filtro por estado":** aparece na faixa do Resumo das Garantias e não aparece na aba Garantias. A faixa deveria ser igual nas abas.
6. **Popup da NCC:** o bloco Cliente mostra "CLIENTE 900001". Sugestão de rótulo: "CÓD.".
7. **Título:** "Farol de Devolução e Reembolsos" (nome do PC, singular) e "Devoluções" na lateral. Se o PC passar a "Devoluções e Reembolsos", a web acompanha.
8. **Celular, editar a NCC:** ☰ → NCC → Pendentes → abrir a linha → Editar dá 5 toques. Com o A2, o "Editar" pode subir para o topo da linha aberta.
9. **Pré-existentes, fora desta PR:**
   - "BAP AUTOPARTS" da lateral em 10,5 px, abaixo do mínimo de 11 px (manual §5);
   - o `select` com fundo cinza, enquanto o `input` é branco;
   - a borda do `textarea` em `--borda`, enquanto a do `input` é `--c-adb5bd`.

## PNGs

- **Anexos desta revisão** (em `recados/anexos/T-0023/`, todos com dados fictícios):
  - `ux-antes-ncc-recortes-cel.png` e `ux-depois-ncc-recortes-cel.png` (R1);
  - `ux-antes-devolucoes-faixa-cel.png` e `ux-depois-devolucoes-faixa-cel.png` (R2);
  - `ux-depois-garantia-nova-pc.png` (A1, A4 e a data em dd/mm/aaaa);
  - `ux-antes-ncc-editar-cel.png` (A2);
  - `ux-data-ptbr-cel.png` (a prova do dd/mm).
  - Nos PNGs "depois", o logo não aparece porque a página foi montada em arquivo local sem o `/static` do logo. Isso não é defeito: nos PNGs da simulação, o logo está lá.
- **O que vai ao po:** nenhum PNG do lote atual. Depois do R1, do R2 e dos 🟡, a simulação deve ser gerada de novo uma vez só:
  - 01 a 05, em `-pc` e `-cel`;
  - mais `06-resumo-garantias`, `07-resumo-devolucoes` e `08-resumo-ncc`, em `-pc` e `-cel` (A6);
  - de preferência no Chromium completo em pt-BR, que já mostra as datas em dd/mm/aaaa.

---

# Reteste no head `928b3ea007b44d95cb13afb76088afb47675b8b2`

- **O que vi:**
  - abri os 16 PNGs da `sim-t0023/v3` (01 a 08, em `-pc` e `-cel`, gerados pelo servidor real);
  - li o diff `3cc4fe0..928b3ea` (`estilo.css`, `editar.html`, `main.py`, `tabelas.py` e `posvenda_fixture.py`);
  - montei de novo as 8 telas com a fixture e medi no Playwright, a 1366×768 e a 390×844.
- **Resultado:** **aprovado.** Os 2 🔴 e os 7 🟡 fecharam. Sobram só 🟢.

## Situação de cada achado

| Achado | Situação | Prova |
|---|---|---|
| 🔴 R1 · Recortes da NCC no celular | fechado | `flex-wrap:wrap`. Medido: nenhuma caixa rola para o lado a 390. O "Acima de 90 dias (6)" passa inteiro para a linha de baixo (03-cel) |
| 🔴 R2 · Rótulo "ABERTAS NO ACOMPANHAMENTO" | fechado | `hyphens:auto`. Fica "ACOMPANHA-MENTO", e nenhum `.bc3-k` vaza (02-cel e 07-cel) |
| 🟡 A1 · Garantia nova rolava no PC | fechado | Grade de 4 colunas: a página tem 768 px a 1366×768 (04-pc) |
| 🟡 A2 · Alvos abaixo de 44 px | fechado | No celular, Salvar, Cancelar, campos e o "Editar" da linha aberta têm 44 px ou mais. "Cancelar" virou botão neutro |
| 🟡 A3 · A edição não dizia qual NCC | fechado | "NCC 901 · CLIENTE FICTICIO 01 · PA" (05). A linha não repete mais os campos do formulário |
| 🟡 A4 · Aviso de dado pessoal 4 vezes | fechado | Uma linha só: "Textos livres: até 600 caracteres, sem CPF, CNPJ, telefone ou e-mail." Também fecharam o RD-0143 (sai "linha nova") e o RD-0144 (sai "Sugestão do PC" com o mesmo número do campo) |
| 🟡 A5 · O 01 não era fiel ao PC | fechado | PRAZO com "FECHADA NO PRAZO" ou "FECHADA COM ATRASO" e SLA cinza nas fechadas, como em `garantias.situacao`. A CIDADE desceu para o popup (8 colunas) |
| 🟡 A6 · Resumo fora da simulação | fechado | 06, 07 e 08 estão na simulação e cabem em 1366×768. Detalhes abaixo |
| 🟡 A7 · Código do cliente nas Devoluções | fechado | Só o nome na grade e na linha fechada; o código está no popup (02) |

**Detalhes do A6:**
- **NCC:** a página tem 768 px. A barra "Resumo gerencial" com texto de exemplo saiu.
- **Devoluções:**
  - o gráfico agora é "Valor devolvido (R$) · mês a mês", igual ao PC;
  - os valores conferem: OUT dá R$ 4.200 (2.100 + 350 + 700 + 1.050), e NOV dá R$ 12,2 mil, igual à faixa;
  - não há mais a linha que repetia o número da faixa.
- **Barras:** todas em `--grafico-3`.

**Os números continuam batendo** entre a faixa, as abas e os cartões (as contas da primeira revisão valem sem mudança).

**Dado pessoal:** nenhum CNPJ, CPF, e-mail, telefone ou contato nas 8 telas.

## Data em mm/dd nos PNGs

- **Não é 🔴 nem 🟡.** A tela usa o `<input type="date">` nativo, e o navegador mostra a data no formato do idioma dele. Já comprovei que o Chromium completo em pt-BR mostra "27/11/2026" e "dd/mm/aaaa" (`ux-data-ptbr-cel.png`).
- **Basta a legenda.** Texto sugerido: "As datas aparecem em mm/dd só nesta simulação, por limite do navegador automático. No PC e no celular em português, aparecem em dd/mm/aaaa."
- **Opcional:** gerar de novo com `chromium.launch({channel: 'chromium', args: ['--lang=pt-BR'], env: {LANG: 'pt_BR.UTF-8'}})`. Aí o PNG já sai em dd/mm e a legenda não é necessária.

## 🟢 Novos (para depois; não seguram o merge)

1. **Fixture:** o tom "cinza" usa `#EEEEEA`/`#5F6360`, que estão fora da paleta. O PC manda `#E3E8E4`/`#5E6B63` (`bap_visual.py:1313`, `--borda`/`--suave`, contraste de 4,50:1, no limite). Na tela, a diferença é imperceptível. Para a simulação ficar fiel, a fixture deve usar o par do PC. O par do PC fica de olho do design-de-marca, porque está fora da tabela §4.3 do manual.
2. **"Cancelar":** o texto sai verde, porque a regra `.caixa a` ganha da `.ed-cancelar`. O §11 pede `--texto` no botão neutro.
3. **Resumo das Devoluções no PC:** "OUT" e "NOV" ficam no canto esquerdo da coluna, longe da barra, e o "R$ 12,2 mil" quebra em 2 linhas. É o componente de barras no tempo com só 2 meses; no celular está certo.
4. Continuam valendo os 🟢 de 1 a 9 da primeira revisão.

## PNGs que vão ao po

Os 16 PNGs da `sim-t0023/v3`, com a legenda da data acima:
- 01 a 05, em `-pc` e `-cel`: os 3 faróis e os 2 formulários;
- 06 a 08, em `-pc` e `-cel`: os 3 Resumos.
