# T-0045 · Reteste de UX e de marca · tela "Atualizar visitas"

- **Revisor:** designer-ux (UX e marca) · **Data:** 27/11/2026 (Manaus)
- **Head SHA retestado:** `134efc888b6a673ad2e866f526c95bed8af76aa1`. A revisão anterior foi no `8d7368f` (`revisao-ux-marca.md`).
- **PNGs vistos (8):** `sim-t0045/v2/`, telas 1 a 4, cada uma no PC e no celular.
- **Data dos PNGs:**
  - **1 e 3** saíram às 08h34 e batem com o head (campo de data em texto);
  - **2 e 4** saíram às 08h29, do `17e7539`, porque o `2-gerente` ainda mostra o seletor de data (`type=date`).
  - O cabeçalho (tela 4) não mudou entre o `17e7539` e o head, mas o PNG precisa sair do head.

## Resultado

**1 🔴 novo, 2 🟡 novos e os 9 🟡 anteriores fechados.**
- O 🔴 é o campo de data, que passou de seletor para texto. Mudança feita pela web por conta própria.
- **Marca:** sem mudança e conforme (logo, faixa, tokens). O CSS novo (`.vz-cod`, `.vz-diag`) usa só `--suave` e as medidas do manual.
- **Largura:** nada passa de 1366 nem de 390 px.

## Os 9 🟡 da revisão anterior

| # | Achado | Situação no `134efc8` |
|---|---|---|
| 1 | Dois botões principais e botão que não funciona na pausa | ✓ Fechado. Na pausa, "Atualizar visitas" e "Baixar de novo" ficam desabilitados e neutros, com o motivo no `title`. "Retomar" é o único principal. O 409 diz "A atualização está pausada. O admin retoma antes." |
| 2 | Texto da pausa duplicado | ✓ Fechado. A linha da lista diz "Pausou a atualização (motivo acima)." |
| 3 | Código técnico como informação | ✓ Fechado. A faixa mostra "Situação" (Em dia, Parcial, Erro, Pausado). Os selos levam a palavra. O código sai pequeno, como "Código para o suporte: …". O diagnóstico diz "sem problema" |
| 4 | Textos sem ação ou com jargão | ✓ Fechado nos 8 códigos apontados (`NADA_A_FAZER`, `PARCIAL_VENDEDOR`, `MAXIMA_SENHA`, `TELA_MUDOU`, `ERRO_INTERNO`, `SITE_FORA`, `CONFIG_*`). Também fechados o 409, o sucesso ("Pedido enviado.") e o rótulo do recado. O `DESCOMPRESSAO_TETO`, novo, também diz o que fazer |
| 5 | Título repetido no corpo | ✓ Fechado. O cartão agora se chama "Período" |
| 6 | Dois pares De/Até | ✓ Fechado. Há um período só, e "Baixar de novo" é `formaction`, só para o admin, com `title` |
| 7 | Rótulos e horas da faixa | ✓ Fechado. "Agenda diária" e "Acessos à Máxima hoje". A hora tem um formato só, "27/11 06h06". A "Última rodada" saiu da faixa e ficou só na lista |
| 8 | Entrada e 3 toques | ✓ Fechado. O link "Atualizar" aparece só para admin e gerente (`pode_visitas`). A lateral ganhou o item "Atualizar visitas" para admin e gerente: ☰ → Atualizar visitas → botão, 3 toques. Tela 4: o cabeçalho cabe em 390 px |
| 9 | Simulação (aviso sem pacote, data em inglês) | ⚠ Parcial. O aviso "Sem dados ainda" saiu. A data em dd/mm/aaaa veio pela troca do campo, que é o caminho errado (ver 🔴 N1) |

## 🔴 Bloqueia o merge

### N1. O campo de data passou de seletor (`type=date`) para texto dd/mm/aaaa
- **Onde:** `editar.html`, a edição da T-0021 em Pedidos e Entregas, tela já aprovada, e `visitas.html`.
- **Resposta à pergunta:** sim, a troca piora a UX, sobretudo no celular.
  1. **No celular, a tarefa pode ficar impossível.** O campo usa `inputmode="numeric"`, que abre o teclado só de números: no iPhone não há "/", e no teclado numérico do Android também não. O `pattern="\d{2}/\d{2}/\d{4}"` exige as barras, e não há máscara em JS. Quem apaga a data (a tela da T-0021 manda "Apague a data para voltar à calculada pelo PC") e digita outra não consegue enviar o formulário.
  2. **Some o calendário.** No celular, o seletor nativo é o jeito mais rápido e sem erro de escolher a data. Com texto, são 10 toques ou mais e o erro de digitação aparece.
  3. **Somem os limites na tela.** O `min` e o `max` da T-0021 (a janela de datas permitidas) saíram do campo. Agora a pessoa só descobre a faixa permitida depois de enviar ("data fora das permitidas (de … a …)").
  4. **A tela de outra tarefa mudou sem simulação.** A T-0021 mudou sem simulação antes (regra 10) e fora do escopo da T-0045.
- **A causa não era o campo.** O mm/dd/aaaa vinha só do Chromium da simulação, que estava em inglês. Num navegador em português, o `type=date` já mostra dd/mm/aaaa:
  - prova 1: o próprio `v2/2-gerente-*.png`, tirado no `17e7539` com o seletor, mostra "21/11/2026";
  - prova 2: `ux/reteste-campo-data-ptbr-vs-texto-cel.png` mostra o `type=date` com "27/11/2026" (Chromium completo, `--lang=pt-BR` e `LANG=pt_BR.UTF-8`) ao lado do campo de texto.
- **Correção:**
  - volte ao `type=date` nas duas telas, com `min` e `max` (a janela da T-0021 e o `max` = hoje das visitas);
  - mantenha a validação no servidor e o `ymd_do_form`, que já aceita aaaa-mm-dd;
  - gere a simulação com o navegador em pt-BR: `chromium.launch({ channel: 'chromium', args: ['--lang=pt-BR'], env: { ...process.env, LANG: 'pt_BR.UTF-8', LANGUAGE: 'pt_BR:pt' } })` e `newContext({ locale: 'pt-BR' })`.

## 🟡 Novos (corrigir antes do merge)

### N2. Detalhe do diagnóstico aberto, empurrando as rodadas
- **Onde:** telas 1 e 3, admin.
- **Problema:**
  - O cartão Admin ganhou 9 métricas abertas: Duração, Memória (pico), Login, maxGestão, Filtros, Por vendedor, Colunas retiradas, Células limpas, Achados. São termos técnicos e são o detalhe menos usado da tela.
  - A 1366, elas empurram "Últimas rodadas" para uma caixa com rolagem interna (`calc(100vh - 620px)`). Ficam visíveis só 3 linhas, e na tela 1 a 4ª aparece cortada na borda, sem sinal de que a lista rola.
- **Regra:** hierarquia (o principal primeiro, o detalhe por último).
- **Correção:**
  - um `<details>` fechado, "Detalhes do diagnóstico", com as métricas dentro;
  - com isso, a lista volta a caber sem rolagem interna (5 linhas a 768 px);
  - a régua do `.vz-adm .vz-lista` fica só para quando o detalhe estiver aberto.

### N3. "Baixando agora" mostra a etapa crua
- **Onde:** `visitas.html`, faixa `e.rodada_ativa`. Não foi simulado.
- **Problema:** aparece "Etapa: maxgestao" (ou `espelho`, `grade`, `filtro`…), o mesmo jargão que saiu dos textos de erro.
- **Correção:** mostre só o andamento ("Baixando agora · 2 de 5 dias") ou troque a etapa por 3 palavras: "Entrando na Máxima" (login, inicio, maxgestao, menu), "Baixando" (filtros, grade, espelho, filtro, salvar) e "Enviando" (envio).

## 🟢 Para depois

1. **Rótulo do link:** a 1366 e a 390, o link do cabeçalho do Farol de Visita mostra só "Atualizar", porque o `rot-long` fica escondido. Ao lado do farol, parece "atualizar o farol". Agora que a lateral tem o item, mude o rótulo para "Atualizar visitas" ou tire o botão do cabeçalho.
2. **Largura dos botões no celular:** "Ligar a agenda" e "Rodar diagnóstico" não ocupam a largura toda, e "Baixar de novo" ocupa. Use a mesma largura nos três (`.vz-linha form button{width:100%}` a ≤ 700 px).
3. **`PARCIAL_TEMPO`:** "o resto vem na próxima volta" ainda usa jargão. Proposta: "o resto vem na próxima atualização".
4. **Os 6 🟢 da revisão anterior** continuam valendo: tokens `--c-*`, largura do `.vz`, lateral, títulos dos cartões e confirmação do Retomar. O item da lateral já foi resolvido.

## Os 8 PNGs que vão ao po

Depois do N1 e do N2, gere os 8 no head da correção, com o navegador em pt-BR:

1. `1-admin-agenda-desligada-pc.png` e `1-admin-agenda-desligada-cel.png`
2. `2-gerente-pc.png` e `2-gerente-cel.png`
3. `3-pausa-por-codigo-pc.png` e `3-pausa-por-codigo-cel.png`
4. `4-cabecalho-farol-visita-pc.png` e `4-cabecalho-farol-visita-cel.png`

Nenhum dos 8 PNGs do `v2/` vai ao po como está:
- os PNGs 1 e 3 têm o campo de texto e o diagnóstico aberto;
- os PNGs 2 e 4 não saíram do head.

A tela de edição da T-0021 não precisa de PNG ao po se voltar ao `type=date` como era. Se a web quiser manter o campo de texto, aí precisa de simulação própria e do "aprovo" do Alexandre.

---

## Reteste final · head `d1e0034f2d7d86875575f2dcd9264aa9497a40e4` (27/11/2026)

- **PNGs vistos (8):** `sim-t0045/v3/`, telas 1 a 4, no PC e no celular. Foram gerados com o Playwright em pt-BR e no fuso de Manaus.
- **Os `2-gerente-*` do v3 são idênticos byte a byte aos do v2.** Isso é coerente: a tela do gerente no `d1e0034` é a mesma do `17e7539` (seletor de data, mesmos textos). O render é determinístico com a mesma fixture.

**Resultado: aprovado. Sem 🔴 e sem 🟡 em aberto, na UX e na marca.**

| Achado | Situação |
|---|---|
| 🔴 N1: data em texto | ✓ Fechado. `type=date` de volta nas visitas (`max` = hoje) e na edição da T-0021, com `min`/`max` e `atual_iso`. A linha do `editar.html` é igual à do `main` de antes. Os PNGs mostram "21/11/2026" com o calendário, no PC e no celular. O servidor aceita aaaa-mm-dd e dd/mm/aaaa (`ymd_do_form`) |
| 🟡 N2: diagnóstico aberto | ✓ Fechado. O diagnóstico fica num `<details>` fechado, "Detalhes do diagnóstico". As 5 rodadas cabem a 1366×768, sem rolagem interna, que agora só vale com o detalhe aberto (`:has(.vz-det[open])`) |
| 🟡 N3: etapa crua | ✓ Fechado. `_andamento` mostra "Entrando na Máxima", "Baixando o dia dd/mm" ou "Enviando", com "(n de N)". A etapa técnica fica só no código do suporte |
| 🟢 1: rótulo do link | ✓ Feito. O link diz "Atualizar visitas" a 1366 e a 390 e cabe ao lado de "Parcial Visitas" |
| 🟢 2: largura dos botões | ✓ Feito. "Ligar a agenda" e "Rodar diagnóstico" ocupam a largura toda no celular |
| 🟢 3: `PARCIAL_TEMPO` | ✓ Feito. O texto agora diz "próxima atualização" |

**Marca:**
- conforme: placa do logo, faixa `--faixa-inicio` → `--faixa-fim`, texto branco e só tokens do manual;
- nenhuma largura passa de 1366 nem de 390 px;
- um botão principal por tela: "Retomar" na pausa e "Atualizar visitas" fora dela.

**🟢 Restantes, para depois:**
- o `summary` "Detalhes do diagnóstico" tem cerca de 20 px de altura no celular; o alvo pede 44 px (`min-height: var(--alvo)` a ≤ 700 px);
- os 🟢 de tokens `--c-*`, largura do `.vz`, título dos cartões e confirmação do Retomar seguem da revisão anterior.

**Vão ao po os 8 PNGs do `v3/`:**
- `1-admin-agenda-desligada-{pc,cel}`
- `2-gerente-{pc,cel}`
- `3-pausa-por-codigo-{pc,cel}`
- `4-cabecalho-farol-visita-{pc,cel}`

A edição da T-0021 voltou exatamente ao que era e não precisa de PNG.
