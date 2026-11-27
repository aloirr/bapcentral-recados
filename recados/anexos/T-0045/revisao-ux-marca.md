# T-0045 · Revisão de UX e de marca · tela "Atualizar visitas" (Farol de Visita)

- **Revisor:** designer-ux (UX e marca) · **Data:** 27/11/2026 (Manaus)
- **Branch:** `modulo-web/T-0045-visitas` · **head SHA revisado:** `8d7368f24ce813f2cf1b1847e6a9e476433d75a8`
- **Simulação:** a do modulo-web, gerada nesse SHA com fixture fictícia (`admin.sim`, `gerente.sim`, sem nome de vendedor nem de cliente), a 1366×768 e a 390×844.
- **Referências:** `.coord/contratos/tela-bc3.md` (v1), `docs/marca/manual.md`, decisões R-20261127-005437 (4 A, 6 B, agenda e "Retomar" com o admin).
- **PNGs:** em `ux/`. Os `antes-*` são os 6 da simulação. Os `depois-3-pausa-por-codigo-{pc,cel}` são a correção sugerida, montada numa cópia do template fora do repositório. É só uma maquete: o código é do modulo-web.

## Resultado

**Sem 🔴.** A condição da tela nova (UX e marca sem 🔴) está cumprida, e o po pode aprovar a simulação.
Há **9 🟡** para corrigir antes do merge e 6 🟢.

## O que está certo

- **Largura:** nada cortado e sem rolagem lateral. O `scrollWidth` é 1366 no PC e 390 no celular, e os PNGs saem com 2732 e 780 px a 2×.
- **PC:** a tela cabe em 768 px de altura nos 3 casos.
- **Celular:** os botões e campos de data têm 44 px (`--alvo`). As rodadas viram uma lista de 2 linhas, sem tabela.
- **Perfis:** o gerente vê só o botão e as rodadas (4 A). O admin vê também a agenda, o diagnóstico, o "Baixar de novo" e o "Retomar". O corte é feito no servidor (`PODEM_PEDIR` e `SO_ADMIN` em `main.py`).
- **Sem print da Máxima** (6 B). Nenhum dado pessoal na tela nem nos PNGs.
- **Cor com texto:** todo selo tem palavra, então a cor nunca é a única pista.

## Marca

| Item | Situação |
|---|---|
| **Logo** | ✓ Logo inteiro na placa preto BAP `#231F20`, com "BAP Central" e "BAP AUTOPARTS" (manual §3, L7). No celular, a mesma placa no topo |
| **Nome** | ✓ "BAP AUTOPARTS" escrito certo |
| **Faixa** | ✓ Degradê `--faixa-inicio #2F7D32` → `--faixa-fim #1B4D1F`, com texto branco. Altura de cerca de 87 px a 1366 (`--faixa-alt` = 88) |
| **Cores na faixa** | ✓ `--faixa-ok #A6E3A9`: 3,46:1. ⚠ `--faixa-alerta #FFB4A9`: 3,0:1 no pior ponto, o limite exato. Só passa em texto ≥ 19 px negrito (manual §4), e hoje está aplicado ao código do erro (ver 🟡 3) |
| **Tokens do CSS novo** | ✓ O CSS novo (`.vz-*`) usa só variáveis do `:root`: `--cartao`, `--borda`, `--suave`, `--alerta`, `--alerta-claro`, `--atencao-claro`, `--t-corpo`, `--alvo`. Nenhum hex solto, nenhum azul ou laranja. ⚠ `--c-eef4ec` é um nome que não está no manual (🟢 1) |
| **Selos** | ✓ `selo-erro`: `--alerta` sobre `--alerta-claro`, 5,75:1. ✓ `selo-atencao`: `--atencao-texto #8A5A00` sobre `--atencao-claro`. ⚠ `selo-ok`: `--c-d3f9d8` e `--c-1b5e20`, dívida anterior a este PR (🟢 1) |
| **Botão principal** | ✓ Fundo `--verde-escuro`, texto branco: 5,12:1 |
| **Letra** | ✓ Inter |

## 🟡 Corrigir antes do merge

### 1. Dois botões principais e um botão que não funciona (tela 3)
- **Regra:** tela-bc3 §11 e §15.10, "um só por tela".
- **Problema:** na pausa aparecem dois botões verdes, "Retomar" e "Atualizar visitas". O "Atualizar visitas" parece ativo, mas o servidor recusa o pedido (`pedir()` devolve 409, "A nuvem está pausada…"). O usuário toca e recebe erro.
- **Correção:** com `e.pausado` (e também com `v.teto_dia`), o botão fica `disabled`, na classe `bt-neutro`, com o `title` "Pausado: o admin retoma antes". O "Retomar" passa a ser o único principal. O texto do 409 troca "A nuvem está pausada" por "A atualização está pausada. O admin retoma antes."
- **Depois:** `ux/depois-3-*`.

### 2. O texto da pausa aparece duas vezes (pendência já avisada pelo modulo-web)
- **Regra:** tela-bc3 §1.1, "uma informação, um lugar".
- **Problema:** a mesma frase sai na caixa vermelha e na 1ª linha das rodadas, e no PC a linha das rodadas fica em negrito.
- **Correção:** a frase fica só na caixa vermelha. A linha da rodada que pausou leva o selo "Pausou" e o texto "Pausou a atualização (motivo acima)."

### 3. O código técnico fica no lugar da informação (telas 1, 2 e 3)
- **Problema:**
  - a faixa mostra "CÓDIGO" com o valor `MAXIMA_CONFIRMACAO`, que no celular quebra no meio da palavra (`MAXIMA_` / `CONFIRM` / `ACAO`);
  - os selos das rodadas mostram o código em caixa alta com sublinhado (`PARCIAL_VENDEDOR`, `MAXIMA_FORA`);
  - o diagnóstico sai como "ok · OK".
- **Regras:** manual §6 (tom de voz: sem caixa alta para gritar, sem jargão) e tela-bc3 §13 (um código interno não aparece como rótulo).
- **Decisão 6 B:** pede o código **em vez do print**, para o suporte, e não como rótulo principal.
- **Correção:**
  - faixa: o rótulo "Situação" com o valor "Em dia", "Parcial", "Erro" ou "Pausado", na cor de farol;
  - selo das rodadas: a mesma palavra;
  - código: em `--suave`, 12 px, depois do texto ("Código para o suporte: MAXIMA_CONFIRMACAO"), só quando o status não é "ok";
  - diagnóstico: "Último diagnóstico: 25/11 15h46 · sem problema".

### 4. Textos de erro sem ação ou com jargão
- **O que o caller perguntou:** "tem frase que explica?" Tem, nos 6 códigos que aparecem nos PNGs. Mas 8 dos 18 textos de `visitas.CODIGOS` não dizem o que fazer ou usam termos de TI.
- **Regra:** cada texto diz o que aconteceu e o que fazer (quem faz o quê).

| Código | Hoje | Sugestão |
|---|---|---|
| `NADA_A_FAZER` | "" (a linha sai sem texto) | "Já estava em dia. Nada a baixar." |
| `PARCIAL_VENDEDOR` | "2 Excel com erro (25/11)." | "Faltou a visita de 2 vendedores em 25/11. Peça de novo esse dia." |
| `MAXIMA_SENHA` | "…Só o Alexandre troca no painel do Render…" | "A Máxima recusou a senha do site. Avise o Alexandre; depois, o admin clica em Retomar." |
| `TELA_MUDOU` / `ERRO_INTERNO` | "(etapa: maxgestao)" e "Erro inesperado (etapa: …)." | Sem a etapa no texto (ela vai para o código do suporte). "A tela da Máxima mudou. Use o Atualizar visitas do PC por enquanto." / "Algo deu errado. Use o Atualizar visitas do PC e avise o admin." |
| `SITE_FORA` | "O site não foi alcançado pelo serviço de visitas." | "O site não respondeu. Tentamos de novo às HHhMM." (ou o `{t}`) |
| `CONFIG_FALTANDO` / `CONFIG_INSEGURA` | "variáveis… no Render" / "depuração ligada" | "A atualização pelo site está desligada por configuração. Avise o Alexandre." |

- **Mensagens de ação:**
  - sucesso: troque "A próxima volta do site na Máxima baixa os dias" por "Pedido enviado. As visitas chegam em até N min.";
  - o campo do recado no Retomar do `DADO_PESSOAL`: troque o placeholder `R-AAAAMMDD-HHMMSS-alexandre` pelo rótulo visível "Número do recado do Alexandre".

### 5. Título repetido no corpo
- **Regra:** tela-bc3 §4.2, "Proibido: título repetido no corpo".
- **Problema:** "Atualizar visitas" aparece 3 vezes: no título da faixa, no h2 do 1º cartão e no botão.
- **Correção:** o h2 passa a "Período", e o botão fica como está.

### 6. Dois pares de datas De/Até na tela do admin
- **Problema:** o "Baixar de novo" tem um período próprio, com padrão de hoje a hoje, e o admin não sabe qual data vale para qual botão. A diferença entre "Atualizar" e "Baixar de novo" também não está escrita.
- **Correção:** um período só. O "Baixar de novo" vira um `bt-neutro` no mesmo formulário (`formaction="/visitas/refazer"`), só para o admin, com o `title` "Baixa de novo os dias que já vieram". O cartão Admin fica com a agenda e o diagnóstico.

### 7. Rótulos e horas na faixa
- **"ENTRADAS HOJE":** não diz nada a quem não é técnico. Troque por "Acessos à Máxima hoje".
- **"AGENDA 06H00":** o `text-transform` deixa o "H" maiúsculo. Troque por "Agenda diária", com a hora no `title`.
- **A mesma hora em 3 formatos:** "08h36 · 27/11", "27/11/2026 06:06" e "27/11 06h06". Use um só, "27/11 06h06", na faixa, na caixa da pausa e nas rodadas.

### 8. A entrada na tela e a regra dos 3 toques
- **Para quem aparece:** o link "Atualizar" do cabeçalho do Farol de Visita (`_bc3_cab.html`) sai para todos os perfis do farol. O vendedor que toca nele cai numa tela sem nenhuma ação. Mostre o link só para admin e gerente.
- **Toques:**
  - PC: Visita → Atualizar → Atualizar visitas, 3 cliques ✓;
  - celular: ☰ → Visita → Atualizar → botão, 4 toques ✗.
- **Correção:** para admin e gerente, um item "Atualizar visitas" na lateral, abaixo de Visita. Fica ☰ → Atualizar visitas → botão.
- **Simulação:** faltam os PNGs do cabeçalho do Farol de Visita com o link, a 1366 e a 390, para conferir se a barra cabe.

### 9. A simulação que vai ao po
- **Problema 1:** o aviso "Sem dados ainda. A primeira atualização chega às 06h30" (de `base.html`, quando não há pacote) contradiz a "Última rodada 08h36" e o "Sem dados hoje" da lateral. É efeito da fixture sem pacote.
- **Problema 2:** os campos de data saem em mm/dd/aaaa, porque o Chromium está em inglês.
- **Correção:** refaça os PNGs com um pacote fictício e o navegador em pt-BR (`--lang=pt-BR`) antes de o po aprovar.
- **Nota da maquete:** no `depois`, o aviso foi tirado de propósito. A opção `locale` do Playwright não mudou o formato do campo de data.

## 🟢 Sugestões para depois

1. **Tokens com nome de hex:** `--c-eef4ec`, `--c-d3f9d8` e `--c-1b5e20` não estão no manual. Troque por `--ok-claro` e `--ok`. É dívida anterior a este PR (MC-0006).
2. **Largura no PC:** o `.vz` tem `max-width: 980px`, e os cartões ficam mais estreitos que a faixa. Alinhe as larguras.
3. **10 rodadas na tela:** com `RODADAS_NA_TELA = 10`, a página passa de 768 px no PC (tela-bc3 §1.2). Mostre 5 e "ver mais", ou role a lista por dentro.
4. **Lateral:** o item "Visita" não fica marcado como ativo nesta tela.
5. **Títulos dos cartões:** os h2 `.vz-cx` estão no estilo de rótulo, em maiúsculas. O manual pede 16 px e peso 600 para título de bloco. Siga o que os outros cartões do BC3 já usam.
6. **Confirmação do Retomar:** peça confirmação antes ("Retomar a atualização pelo site?"), porque a ação volta a entrar na Máxima.
