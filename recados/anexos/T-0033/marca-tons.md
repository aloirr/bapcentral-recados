# T-0033: parecer de marca sobre os tons do selo `chip_tom` (PC e site)

- **Revisor:** design-de-marca · 27/11/2026
- **Vale para os head SHAs:**
  - PC: `origin/modulo-farois/T-0033-aderencia-cor` @ `80daf25`;
  - site: `origin/modulo-web/T-0033-revisao-geral` @ `94b3440`.
- **Base:** `docs/marca/manual.md` no `main`, §4.2 a §4.4 (paleta [VALE], 3 A a 8 A, R-20261126-182227-alexandre).
- **Prints:** `sim-t0033-tons/antes` e `/depois` (Entregas e Pedidos PA, 1366 e 390 px). Conferi o Farol de Entregas em 1366 px. Os quatro tons aparecem e se distinguem, e o cinza "8" não se confunde com o vermelho "8".

## Parecer: **liberado com ajustes** 🟡 (nenhum 🔴)

### 1. A paleta está fiel ao manual: sim
| Tom | Fundo → token | Texto → token | Contraste | Manual |
|---|---|---|---|---|
| ok | #F0F7EC `--ok-claro` | #2F7D32 `--ok` / `--verde-escuro` | 4,69:1 | §4.3, listado |
| atenção | #FFF4D6 `--atencao-claro` | #8A5A00 `--atencao-texto` | 5,41:1 | §4.3, listado |
| alerta | #FDECEA `--alerta-claro` | #B42318 `--alerta` | 5,75:1 | §4.3, listado |
| cinza | #E3E8E4 `--borda` | #5E6B63 `--suave` | **4,50:1** (4,503) | par **não listado** (ver item 2) |

- O site está como o manual pede: `web/app/tabelas.py` monta `PALETA_TOM` com `marca.TOKENS[...]`, sem hex solto.
- O alerta de antes (#B3261E cheio com texto branco) tinha duas falhas: o #B3261E é o vermelho "quase igual" que o manual tira (§4.2, `--alerta`), e o fundo cheio de cor de farol não segue o papel do `--alerta-claro`. A troca corrige as duas.
- Fora do meu escopo, para o designer-ux: o selo de alerta perdeu peso visual em relação ao de antes. Se isso pesa na leitura do SLA, quem decide é o designer-ux, não a marca.

### 2. Cinza #E3E8E4 / #5E6B63: lacuna do manual, não uso previsto
- O `--suave` como texto está no papel dele ("texto de apoio").
- O `--borda` tem um papel só no manual: "contorno de cartão e de campo" (§4.2, Neutros). Usar a borda como **fundo de selo** é um papel que o manual não prevê.
- O par #5E6B63 sobre #E3E8E4 não está na tabela de contraste (§4.3). Ele passa, mas raspando: 4,503:1 contra o mínimo de 4,5:1.
- Não há cor nova, e o tom já estava no PC (#E4E7E4 / #69736D, que hoje dá 4,1:1 e não passa). Por isso não seguro a entrega. O papel, porém, precisa do "aprovo" do Alexandre para entrar no manual.

**Pergunta ao Alexandre (pelo po), com o print `depois/entregas-entregas__pc1366.png`:**
> O selo do SLA que parou de contar (entrega fechada) aparece em cinza. Para ele, qual cinza fica?
> - **(a) [recomendo]** O cinza da borda (#E3E8E4) como fundo, com o cinza de apoio (#5E6B63) no número. Não entra cor nova, é o que a tela já mostra, e a leitura fica em 4,5:1, no limite mínimo. O manual ganha o papel "fundo do selo neutro" para o `--borda`.
> - (b) O gelo do fundo (#F3F4F2) com o mesmo cinza de apoio. Lê melhor (5,06:1), mas o selo quase some na linha zebrada (#F6F7F6).
> - (c) Um token próprio de selo neutro (`--neutro-claro`). Só vale se o (a) não agradar no print; exige simulação nova.

Enquanto não houver resposta, o cinza fica como está. Se o Alexandre escolher (a), eu registro em `decisoes.md` e no §4.2 e §4.3 do manual.

## Achados
| ID | Onde | Tipo | Fere | Gravidade | Correção | Dono |
|---|---|---|---|---|---|---|
| MC-0018 | `bap_visual.py:1309-1313` (`chip_tom`) e `relatorios_nucleo.py:314-316` (`_VERM`, `_AMAR`, `_VERD`) | cor | §4: "hex solto no código é proibido, só a constante" | baixa (os valores estão certos; nada muda na tela) | Trocar o hex pela constante: `("#FDECEA", "#B42318")` → `(VERMELHO_CLARO, VERMELHO)`; `#FFF4D6` → `AMARELO_CLARO`; `#E3E8E4` → `CINZA_LINHA`; `#5E6B63` → `SUAVE`; `#2F7D32` → `VERDE_ESCURO`. Criar no `bap_visual.py` as constantes que faltam: `OK_CLARO = "#F0F7EC"` (`--ok-claro`, que hoje só existe em `FUNDOS["ok"]`) e `ATENCAO_TEXTO = "#8A5A00"` (`--atencao-texto`). O `relatorios_nucleo` passa a importar de `bv`. **Pode ir na T-0047**, sem segurar a T-0033 | modulo-farois |
| MC-0019 | selo cinza do `chip_tom` (PC e site) | cor | §4.2 (papel do `--borda`) e §4.3 (par não listado) | baixa | Pergunta ao Alexandre (item 2). Nada a corrigir até a resposta | po → alexandre |

## 3. Selos e faixas por valor ainda fora do manual (para a T-0047)
Fonte: `git grep` em `origin/modulo-farois/T-0033-aderencia-cor` @ `80daf25` e `origin/modulo-web/T-0033-revisao-geral` @ `94b3440`. Correção pelos tokens do §4.2: alerta (#FDECEA, #B42318), atenção (#FFF4D6, #8A5A00), ok (#F0F7EC, #2F7D32); barra e ponto em #B42318 / #B7791F / #2F7D32.

**Já alinhados nesta branch (só falta trocar o hex pela constante, MC-0018):**
- `FAIXA_PCT_META` e `FAIXA_DU_SEM` (`relatorios_nucleo.py:19370-19373`);
- `CORES_SINAL` (`relatorios_nucleo.py:19376`);
- os três primeiros degraus de `CHIP_SLA` (`relatorios_nucleo.py:1769-1772`).

**Fora do manual:**
1. `relatorios_nucleo.py:1773`, último degrau de `CHIP_SLA()`: `(None, "#B42318", "#FFFFFF")`, o vermelho cheio com texto branco para mais de 4 dias. As cores são da paleta, mas o manual só dá o branco sobre `--erro` para o "botão de desativar". Um "selo grave" de farol não existe no manual. Isso vai para o Alexandre na mesma pergunta do item 2: o farol tem um quarto nível, o grave, ou o mais de 4 dias usa o alerta comum?
2. `relatorios_nucleo.py:1776-1778`, `BARRA_ATENDIDO`:
   - `#D9534F` → `--alerta` #B42318;
   - `#E0A526` → `--atencao` #B7791F;
   - `#59BA61` (`--verde-marca`, que não é cor de estado) → `--ok` #2F7D32.
3. `bap_automation.py:7070-7072`, `_FAIXA_ATING_WEB` (alimenta o site): `#FBDDDA/#B3261E`, `#FFF1C7/#8A5A00` e `#E5F3DF/#2F7D32`. Este último é uma combinação proibida (§4.4, 4,44:1). O comentário diz "= FAIXA_PCT_META", mas os valores não batem: a lista deve **importar** `FAIXA_PCT_META` em vez de copiar.
4. `bap_automation.py:6072`, CSS do HTML gerado: `.sobe #B3261E` → #B42318. `.desce #1E6B3A` e `.novo #1D4ED8` ficam fora da paleta: o primeiro vira `--ok` #2F7D32; o segundo vira `--texto`, ou vai ao Alexandre se precisar de cor.
5. `bap_visual.py:2013-2014` (`ATING_FUNDO`), `3705-3706` (`ATING_CORES`) e `3863` (#A3201A):
   - `#FDE0DE/#A3201A` → (#FDECEA, #B42318);
   - `#DDF2DF/#1E6B2A` → (#F0F7EC, #2F7D32).
6. `bap_visual.py:90-93`, `FUNDOS`:
   - `"grave": "#F6C9C4"` e `FUNDO_GRAVE`: cai na pergunta do grave (item 1);
   - `"cinza": "#F1F2F0"`: está fora; vai para `--fundo` #F3F4F2, ou para o que o Alexandre decidir no item 2;
   - `"azul": "#EAF1FB"`: está fora; o azul do manual é só o selo "NOVO" do catálogo.
7. `bap_visual.py:320, 343, 1292`: fundo de seleção `#DCEFD4`, fora da paleta → `--verde-claro` #E5F3DF, sempre com `--texto`.
8. `bap_meta.py`:
   - `3791-3792`: `EXEC_CAB_FUNDO #E5F3DF` com `EXEC_CAB_TEXTO #2F7D32` é uma **combinação proibida** (§4.4). O texto passa a `--texto` #1E2722.
   - `3793-3795`: `EXEC_TRI_*` (#1E7A46, #DDF0E2, #14522F) estão fora; vão para `--verde-escuro`, `--ok-claro` e `--texto`.
   - `306`: o filete `#62BB47` → `VERDE` (#59BA61).
9. Outros vermelhos e cinzas antigos nos programas do PC (selo e texto de estado):
   - `bap_planner.py:150, 154, 4677, 4884`: #69736D, #B3261E, #FFF8E6, #FCEFEE;
   - `bap_oportunidade.py:322`: #62BB47;
   - `cobranca_whatsapp.py:403, 425`: #B3261E;
   - `email_inadimplencia.py:38`: #B3261E;
   - `email_rota.py:276-277, 384, 419`: #62BB47, #69736D, #B3261E, #E3E7E2, #F7F9F6.
10. Site (`94b3440`):
    - o `web/app` está limpo no selo;
    - `web/app/static/estilo.css` tem **55 variáveis `--c-<hex>`**, entre elas `--c-f6c9c4` (o grave). É hex solto com outro nome: cada uma vira token do manual ou sai;
    - os testes `web/tests/farol_fixture.py:89-93`, `painel22_fixture.py:7` e `test_abas.py:486-488, 614-619` ainda conferem as cores antigas e precisam mudar junto com os itens 1 a 3;
    - no `main`, `web/app/tabelas.py:178-179` ainda tem o `PALETA_TOM` antigo. A correção é o PR da `modulo-web/T-0033-revisao-geral`.

**Fora do meu escopo, para o testes:** `smoke_relatorios.py:708-711` e `4209` ainda esperam #E5F3DF, #B3261E e #62BB47. Com esta branch, devem falhar.
