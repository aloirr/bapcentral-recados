# T-0034: parecer de marca (Painel Executivo como página inicial; Login, Trocar senha, Usuários e Parcial no BC3)

- **Revisor:** design-de-marca · 27/11/2026 (Manaus)
- **Vale para o head:** `origin/modulo-web/T-0034-pagina-inicial` @ **`dc81c24`** (`dc81c245aad1be18c009abeea201da3e506a26d6`). Li o código só pelo `git show`, sem trocar de branch e sem alterar nada.
- **Base:** `docs/marca/manual.md` no `main` (aprovado no R-20261126-182227-alexandre) e o R-20261127-010314-alexandre (1 A: selo neutro = #E3E8E4 com #5E6B63; 2 A: sem nível "grave", o grave usa o alerta comum #FDECEA / #B42318).
- **PNGs:** abri as 35 de `sim-t0034/depois3/` (login, senha, usuarios, usuarios-desativar, parcial, painel-diretor, painel-diretor-faturamento, painel-admin, home-prevenda e os 2 faróis a 390, 1366 e 1920; painel-diretor-rolado a 1366 e 1920). Medi a cor com amostragem de pixel e o contraste pela fórmula WCAG 2.1.

## Parecer: **liberado com ajustes** 🟡 (0 🔴 · 5 🟡 · 3 🟢)

Nada fere a marca a ponto de segurar a aprovação do po. O logo, o nome, a placa, a faixa e o `<title>` estão como o manual pede. Os 🟡 são pequenos e quatro deles se corrigem com uma linha de CSS cada. Uma ressalva importante para o po: as PNGs mostram a letra Inter porque a máquina da simulação tem a Inter instalada; no PC da empresa e no celular o site abre hoje em outra letra (MC-0020).

## O que está conforme

| Item pedido | Situação | Evidência |
|---|---|---|
| Placa do logo na barra lateral | **Conforme.** Logo inteiro de 56 px de altura (41 × 56, `contain`, sem esticar) sobre `--preto-bap` #231F20, canto de 10 px. Ao lado, "BAP Central" 15 px/700 e "BAP AUTOPARTS" 10,5 px/600, em branco (16,30:1). Respiro: o círculo tem 28,5 px, ¼ = 7,1 px; a placa dá 8 px em cima e embaixo, 10 px à esquerda e 8 px até o texto | `estilo.css:358-360`; pixel da placa = #231F20 |
| Topo do celular | **Conforme.** A mesma placa com o logo de 48 px (35 × 48); respiro 6 px para 6,1 px pedidos (diferença de 0,1 px, desprezível) | `estilo.css:570` |
| Arquivo do logo | **Conforme.** `web/app/static/logo_bap.png` é **idêntico** byte a byte ao `SISTEMA BAP/recursos/logo_bap.png` (md5 `333aa73a…`). Não foi recolorido nem cortado | — |
| Favicon e ícone do celular | **Conforme** (exceção 11 A). Símbolo "b" no círculo, 32 px e 180 px, verde #59B961/#5AB962 (o #59BA61 depois da redução, sem recolorir). Reconhecível em 16 px | `favicon-32.png`, `apple-touch-icon-180.png` |
| Tokens de cor | **Conforme no que é marca.** O bloco `:root` traz todos os tokens do §4.2 com os hex do manual (`--verde-marca` #59BA61, `--verde-escuro` #2F7D32, `--preto-bap`, `--faixa-*`, `--alerta` = `--erro` #B42318, `--atencao-texto` #8A5A00, neutros). As 55 sobras `--c-<hex>` continuam (já catalogadas, T-0047, ver "Conhecidos") | `estilo.css:3-104` |
| Faixa | **Conforme.** Degradê `--faixa-inicio` #2F7D32 → `--faixa-fim` #1B4D1F; todo o texto em `--faixa-texto` #FFFFFF (pior ponto 5,12:1), inclusive rótulos de 11 px e a data de 12 px. Números de farol na faixa só em ≥ 19 px negrito (o `--faixa-alerta` dá 3,01:1 no pior canto, acima de 3:1 para texto grande) | `estilo.css:375-390`; PNGs do Painel, Usuários, Trocar senha, Parcial |
| `<title>` | **Conforme.** "{tela} · BAP AUTOPARTS" em todas as telas: "Entrar", "Painel Executivo", "Trocar senha", "Usuários", "Parcial · {farol}", "{farol}". Nome pela constante `marca.EMPRESA = "BAP AUTOPARTS"`. Exceção pequena: MC-0025 | `base.html:6` |
| Nome "Painel Executivo" | **Conforme** (12 A). Fecha o MC-0009 nas telas da T-0034 | `painel.html`, `_painel_cab.html` |
| Selos da T-0034 | **Conformes:** "Desatualizado" na faixa (#8A5A00 sobre #FFF4D6, 5,41:1, contorno `--atencao`) e "Troca de senha pendente" (idem). O "Desativado" usa o cinza errado: MC-0024 | `estilo.css:423, 519` |
| Botões e estados | **Conforme.** Botão principal em `--verde-escuro` com branco (5,12:1); "Desativar" em `--erro` #B42318 (6,57:1); aba ativa e item ativo da lateral em `--verde-escuro`; foco #2F7D32 | `estilo.css:404-405, 515-518` |
| **Login, a primeira impressão** | **Conforme no essencial:** placa preto BAP centralizada com o logo inteiro, "BAP Central" e "BAP AUTOPARTS" embaixo (11 px/600, `--suave`, 5,59:1), um só botão verde, sem enfeite. O tamanho e o respiro do logo pedem ajuste fino: MC-0021 | `login.html`, `estilo.css:511-515`; `login__pc1366/1920/cel390.png` |

## Achados

| ID | Onde | Tipo | Fere | Gravidade | Correção | Dono |
|---|---|---|---|---|---|---|
| 🟡 MC-0020 | `web/app/static/estilo.css:93` (`--fonte`) e todas as telas | tipografia | §5 (9 A: "Inter no site", escolhida justamente por **poder ser hospedada** e ficar igual no PC e no celular) | média | Não há `@font-face` nem arquivo de fonte no site: a Inter só aparece onde está instalada. No Windows da empresa o site abre em Segoe UI e no celular em Roboto ou SF; as PNGs (com Inter) não mostram o que o Diretor vai ver. **Correção:** hospedar a Inter (licença OFL, com o `OFL.txt`) em `web/app/static/fontes/` nos pesos 400, 600 e 700 (`.woff2`) e declarar antes do `:root`: `@font-face{font-family:Inter;font-style:normal;font-weight:400;font-display:swap;src:url(/static/fontes/Inter-Regular.woff2) format("woff2")}` (idem 600 SemiBold e 700 Bold). A pilha `--fonte` fica como está. Pronto quando: a tela abre em Inter numa máquina sem a Inter instalada (print). Pode ir nesta T-0034 ou em tarefa própria antes da produção; **não segura a aprovação do po**, mas o po precisa saber da diferença | modulo-web |
| 🟡 MC-0021 | Login: `estilo.css:514` (`.bc3-login-logo`) | logo | §3.3: "Login: logo inteiro de 96 px"; respiro de ¼ do círculo, "nada entra nessa área" | baixa | Hoje o logo sai com 76 × 105 px e o respiro fica em 10 px nas laterais e 11,7 px em cima e embaixo, abaixo dos 13,3 px pedidos (o PNG não tem margem própria: o "bap" ocupa a largura toda e o círculo encosta no topo). **Antes:** `width:96px;height:128px;padding:10px` → **depois:** `width:96px;height:122px;padding:13px`. O logo passa a 70 × 96 px, o respiro a 13 px (o pedido é 12,2 px) e a placa continua com 96 px de largura. Pronto quando: print do login a 1366 e 390 | modulo-web |
| 🟡 MC-0022 | Painel Executivo, barras por estado: `estilo.css:132-134` (`.rc-barras .barra`, `.rot-b`); `_estados.html` | cor (contraste) | §4 (mínimo 4,5:1 no texto, 3:1 no grande) e §4.2 (`--grafico-*` "sempre com o número escrito **ao lado**") | média | O % de atingimento vai **dentro** da barra `--grafico-3` #8FA79A, na cor do farol: verde #2F7D32 dá **1,99:1**, vermelho #B42318 **2,56:1** e âmbar #8A5A00 **2,30:1** (12,8 px, negrito). Vem do `main`, mas agora é a página inicial do Diretor (`painel-diretor__pc1366.png`, "110 %", "9 %", "95 %"). **Correção mínima, sem mudar o desenho:** `.rc-barras .barra .rot-b{background:var(--cartao);border-radius:4px;padding:0 4px;line-height:1.3}`. O número passa a ficar num rótulo branco: 5,12 / 6,57 / 5,93:1. Pronto quando: print do Resultado a 1366 e 390 | modulo-web |
| 🟡 MC-0023 | `estilo.css:122, 126 (2×), 133, 134, 135, 156, 221, 276` | tipografia | §5: "Pesos: só 400, 600 e 700" | baixa | `font-weight:800` → `font-weight:700` nas 9 ocorrências (anel, variações e valores do cartão, rótulos das barras, `.kpi-valor`, `.cob-val`, total da tabela). Sem a Inter hospedada, o 800 nem existe na Segoe UI e o navegador sintetiza | modulo-web |
| 🟡 MC-0024 | Usuários, selo "Desativado": `estilo.css:519` (`.selo-cinza`) | cor | R-20261127-010314-alexandre, 1 A (selo neutro = #E3E8E4 com #5E6B63) | baixa | **Antes:** `.selo-cinza{background:var(--grade);color:var(--suave)}` (#ECEEEB) → **depois:** `.selo-cinza{background:var(--borda);color:var(--suave)}` (#E3E8E4; 4,50:1). Assim o neutro é o mesmo em toda a BAP Central. A fixture das PNGs não tem usuário desativado, então o selo não aparece na simulação | modulo-web |
| 🟢 MC-0025 | `erro.html` | voz (nome na aba) | §7 ("{tela} · BAP AUTOPARTS") | baixa | A página de erro e de acesso negado não define o título e a aba mostra "Início · BAP AUTOPARTS". Acrescentar `{% block titulo %}{{ titulo_erro or "Acesso negado" }}{% endblock %}` | modulo-web |
| 🟢 MC-0026 | Faixa até 1600 px: `estilo.css:97-98` | tipografia | §5 (escala: título 24 px, número 22 px) | baixa | Até 1600 px a faixa usa 21 px no título e 20 px no número; os 24/22 só valem a partir de 1601 px. Foi assim que o BC3 foi visto e aprovado, então **não mexer agora**. Eu levo ao manual (T-0047) a escala por largura, para o Alexandre aprovar | design-de-marca |
| 🟢 MC-0027 | Parcial (`parcial__*.png`) | aplicação | §7 (imagem da parcial) | — | A imagem da simulação é fictícia e não tem a marca. Não dá para conferir o "BAP AUTOPARTS" da parcial real por estas PNGs [não avaliado]. A casca da tela (placa, faixa, botões) está conforme | — |

## Conhecidos, fora do código da T-0034 (não seguram; vão na T-0047)
Aparecem nas PNGs e o po deve saber que **não** são regressão desta branch. Já estão catalogados no `T-0033/marca-tons.md`, §3.
1. **Selo do SLA "grave" cheio** (#B3261E com texto branco, "7", "8" e "9" em `farol-pedidos-uf__*.png`). Isso contraria a decisão 2 A. A cor vem do pacote do PC (`relatorios_nucleo.py`, `CHIP_SLA`, e a fixture `web/tests/farol_fixture.py:89` copia o contrato). Fica na T-0047 (modulo-farois).
2. **Verde antigo #62BB47** nas barras do "Faturamento projetado" (aba Faturamento do Painel) e na barra do "% atendido" do Farol de Pedidos. Vem do `bap_visual.VERDE = "#62BB47"` (`bap_visual.py:64`), que o manual manda passar a #59BA61. Dono: modulo-farois, T-0047. A cor da série é do designer-ux (o 🟢 4 dele pede #8FA79A).
3. **Sobras `--c-<hex>`** no `estilo.css` (55 variáveis), entre elas:
   - o topo dos cartões do Painel #E8F0E4, "quase igual" ao `--verde-claro`. Nele, a variação verde "out +11 %" (#2F7D32) dá **4,39:1** e não passa;
   - o item ativo da lateral #EAF3EA;
   - a borda dos campos #ADB5BD;
   - os fundos de linha #FDF1F0 e #FBDDDA.

   Cada uma vira token do manual ou sai (T-0047, modulo-web). A troca do topo dos cartões muda o tom e vai em simulação.

## Para o po
- **Pode aprovar a T-0034 pela marca:** sem 🔴; o logo e as cores da marca estão como o manual aprovado e o R-20261127-010314-alexandre pedem nas telas da T-0034.
- **Recomendo pedir a correção dos MC-0021 a 0024 antes do merge.** São uma linha de CSS cada, sem mudar o desenho aprovado.
- **O MC-0020 (fonte):** o po decide se entra nesta T-0034 ou numa tarefa própria. Se ficar para depois, a aprovação vale sabendo que o site abre em Segoe UI até a Inter ser hospedada.
- **Na `farol-pedidos-uf`:** os selos do SLA ainda estão no visual antigo. Eles mudam na T-0047, não aqui.

## Reteste
Depois da correção, no novo head: os prints do login (1366 e 390), do Painel · Resultado (1366 e 390) e de Usuários com um usuário desativado, mais a confirmação da Inter numa máquina sem a fonte instalada. Este parecer vale só para o `dc81c24`.

## Fora do meu escopo (encaminhar, não catalogado)
- `farol-visita__pc1920.png`: o botão sai escrito "Parcial **Visitase** Conversão", sem o espaço antes do "e". O `<span class="rot-long"> e Conversão</span>` vira item do `display:flex` do `.bc3-bt` e o espaço do começo some (`_bc3_cab.html`, linha do `rot_parcial`). É texto de interface: vai ao designer-ux e ao modulo-web.
